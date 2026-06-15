import joblib
import json
import pandas as pd
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator


app = FastAPI(
    title="House Price Prediction - Serving ML Models",
    description="To Predict Price of House"
)


try:
    model = joblib.load("HousePredv1.joblib")
    with open("monitoring_report.json", "r") as f:
        training_metrics = json.load(f)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")



predictions = {}
prediction_id = 1


monitoring_data = {
    "total_predictions": 0,
    "successful_predictions": 0,
    "failed_predictions": 0,
    "last_prediction_time": None,
    "model_status": "running",

    "training_metrics": training_metrics
}


class HouseDetails(BaseModel):
    Area: int = Field(..., gt=0, description="Area must be greater than 0")
    Bedrooms: int = Field(..., ge=1, le=4, description="Bedroom range is only from 1-4")
    Bathrooms: int = Field(..., ge=1, le=5, description="Please enter range from 1-5")
    Floors: int = Field(..., ge=1, le=10, description="Maximum floors are 10")
    YearBuilt: int = Field(..., ge=1800, le=2026)
    Location: str = Field(..., min_length=2, description="Minimum length should be 2")
    Condition: str = Field(..., min_length=2)
    Garage: str = Field(..., min_length=2, description="Garage must be Yes or No")

    @field_validator("Location", "Condition", "Garage")
    @classmethod
    def validate_text_fields(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty. Please fill the field")
        return value.strip()


@app.get("/")
def home():
    return {"message": "House Price Prediction API"}



@app.get("/health")
def health_check():
    return {
        "status": "API is running",
        "model_status": monitoring_data["model_status"]
    }


@app.get("/monitor")
def monitor_model():
    return monitoring_data


@app.post("/predict")
def predict_house_price(house: HouseDetails):
    global prediction_id

    monitoring_data["total_predictions"] += 1
    if house.Area == 999:
        monitoring_data["failed_predictions"] += 1
        raise HTTPException(status_code=500, detail="unsuccessful prediction")

    try:
        house_data = pd.DataFrame([house.model_dump()])
        predicted_price = model.predict(house_data)[0]

        result = {
            "id": prediction_id,
            "input": house.model_dump(),
            "predicted_price": round(float(predicted_price), 2)
        }

        predictions[prediction_id] = result
        prediction_id += 1

        monitoring_data["successful_predictions"] += 1
        monitoring_data["last_prediction_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return result

    except Exception as e:
        monitoring_data["failed_predictions"] += 1
        monitoring_data["model_status"] = "error"

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed Due to Internal Server Error: {e}"
        )


@app.get("/predictions")
def get_all_predictions():
    return predictions


@app.get("/predictions/{id}")
def get_prediction(id: int):
    if id not in predictions:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found. Please Enter A Valid ID."
        )

    return predictions[id]


@app.put("/predictions/{id}")
def update_prediction(id: int, house: HouseDetails):
    if id not in predictions:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found. Please Enter The Correct ID."
        )

    try:
        house_data = pd.DataFrame([house.model_dump()])
        predicted_price = model.predict(house_data)[0]

        result = {
            "id": id,
            "input": house.model_dump(),
            "predicted_price": round(float(predicted_price), 2)
        }

        predictions[id] = result

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Update prediction failed Due To Internal Server Error: {e}"
        )


@app.delete("/predictions/{id}")
def delete_prediction(id: int):
    if id not in predictions:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found. Please Enter a Valid ID to Delete the Record."
        )

    deleted_prediction = predictions[id]
    del predictions[id]

    return {
        "message": "Prediction deleted successfully",
        "deleted_prediction": deleted_prediction
    }