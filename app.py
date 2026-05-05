from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()


# ------------------ MODELS ------------------

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0, lt=120)
    gender: Optional[Literal['male', 'female', 'other']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)


class Patient(BaseModel):
    patient_id: str
    name: str
    city: str
    age: Annotated[int, Field(gt=0, lt=120)]
    gender: Literal['male', 'female', 'other']
    height: Annotated[float, Field(gt=0)]
    weight: Annotated[float, Field(gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 25:
            return "normal"
        elif self.bmi < 30:
            return "overweight"
        else:
            return "obese"


# ------------------ FILE HANDLING ------------------

def load_data():
    try:
        with open("patient.json", "r") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)


# ------------------ ROUTES ------------------

@app.get("/")
def hello():
    return {"message": "hello This is patient data records"}


@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    record = load_data()
    if patient_id in record:
        return record[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")


@app.get("/view")
def patient_records():
    return load_data()


@app.get("/sort")
def sort_patient(
    sort_by: str = Query(...),
    order: str = Query("asc")
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(400, f"Choose from {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(400, "Order must be asc or desc")

    record = load_data()

    patients = [Patient(**p) for p in record.values()]

    sorted_data = sorted(
        patients,
        key=lambda x: getattr(x, sort_by),
        reverse=(order == "desc")
    )

    return [p.model_dump() for p in sorted_data]


@app.post("/create")
def create_patient(patient: Patient):
    record = load_data()

    if patient.patient_id in record:
        raise HTTPException(400, "patient already exists")

    record[patient.patient_id] = patient.model_dump()

    save_data(record)

    return JSONResponse(status_code=201, content={"message": "patient created"})


@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, updates: PatientUpdate):
    record = load_data()

    if patient_id not in record:
        raise HTTPException(404, "Patient not found")

    existing = record[patient_id]

    update_data = updates.model_dump(exclude_unset=True)

    existing.update(update_data)

    existing.pop("patient_id", None)
    updated_patient = Patient(patient_id=patient_id, **existing)

    record[patient_id] = updated_patient.model_dump()

    save_data(record)

    return {"message": "patient updated"}


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    record = load_data()

    if patient_id not in record:
        raise HTTPException(404, "Patient not found")

    del record[patient_id]

    save_data(record)

    return {"message": "patient deleted"}