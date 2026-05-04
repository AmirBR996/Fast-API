from fastapi import FastAPI
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


@app.get("/view")
def patient_records():
    record = data()
    return record




