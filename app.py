from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from model.predict import predict_output
from schema.user_input import UserInput
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/health")
def health():
    return {
        "status": "OK",
        "version": "1.0.0",
        "model_loaded": "True"
    }


@app.post("/predict")
def predict_premium(data: UserInput):
    input_dict = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }
    try:
        prediction = predict_output(input_dict)
        return JSONResponse(status_code=200, content=prediction)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})




