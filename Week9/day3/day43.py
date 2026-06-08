print("Hello wqorld")
from typing import Dict

import requests
from fastapi import FastAPI, HTTPException, Query

"""

app = FastAPI()
@app.get("/home")
def read_root():
    return{"Message : Hekko FastApi!"}

"""
app = FastAPI()

students = {
    1: {"name": "Santhosh", "age": 22},
    2: {"name": "Kumar", "age": 23}
}


@app.get("/")
def home():
    return {"message": "Welcome to Student API"}


@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):
    return students[student_id]


@app.post("/students")
def add_student(student_id: int, name: str, age: int):
    students[student_id] = {"name": name, "age": age}
    return {"message": "Student added successfully", "student": students[student_id]}


@app.put("/students/{student_id}")
def update_student(student_id: int, name: str, age: int):
    students[student_id] = {"name": name, "age": age}
    return {"message": "Student updated successfully", "student": students[student_id]}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    deleted_student = students[student_id]
    del students[student_id]
    return {"message": "Student deleted successfully", "student": deleted_student}