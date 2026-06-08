print("Hello World")
import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="house Price Prediction", description="To Predict Price of Housee")

model = joblib.load("house_price_modelV1.joblib")

predictions = {}
prediction_id = 1


class HouseDetails(BaseModel):
    Area: int
    Bedrooms: int
    Bathrooms: int
    Floors: int
    YearBuilt: int
    Location: str
    Condition: str
    Garage: str


@app.get("/")
def home():
    return {"message": "House Price Prediction API"}


@app.post("/predict")
def predict_house_price(house: HouseDetails):
    global prediction_id

    house_data = pd.DataFrame([house.dict()])

    predicted_price = model.predict(house_data)[0]

    result = {
        "id": prediction_id,
        "input": house.dict(),
        "predicted_price": round(predicted_price, 2)
    }

    predictions[prediction_id] = result
    prediction_id += 1

    return result


@app.get("/predictions")
def get_all_predictions():
    return predictions


@app.get("/predictions/{id}")
def get_prediction(id: int):
    return predictions[id]


@app.put("/predictions/{id}")
def update_prediction(id: int, house: HouseDetails):
    house_data = pd.DataFrame([house.dict()])

    predicted_price = model.predict(house_data)[0]

    result = {
        "id": id,
        "input": house.dict(),
        "predicted_price": round(predicted_price, 2)
    }

    predictions[id] = result

    return result


@app.delete("/predictions/{id}")
def delete_prediction(id: int):
    deleted_prediction = predictions[id]
    del predictions[id]

    return {
        "message": "Prediction deleted successfully",
        "deleted_prediction": deleted_prediction
    }