from fastapi import FastAPI, Query, HTTPException
import json
app = FastAPI()

def data():
    with open("patient.json" , "r") as f:
        data = json.load(f)
        return data

@app.get("/")
def hello():
    return {"message" : "hello This is patient data records"}

@app.get("/about")
def about():
    return {"message" : "Here is data of many patient "}

@app.get("/patient/{patient_id}")
def get_patient(patient_id : str):
    record = data()
    if patient_id in record :
        return record[patient_id]
    return {"message" : "patient not found!"}

@app.get("/view")
def patient_records():
    record = data()
    return record

@app.get("/sort")
def sort_patient(
    sort_by: str = Query(..., description="Sort on the basis of height, weight and bmi"),
    order: str = Query("asc", description="Sorting order: asc or desc")
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Order must be 'asc' or 'desc'"
        )

    record = data()
    sorted_order = True if order == "desc" else False
    sorted_data = sorted(record.values() , key = lambda x : x.get(sort_by , 0) , reverse = sorted_order)
    return sorted_data
# Example:
# http://127.0.0.1:8000/sort?sort_by=weight&order=desc
