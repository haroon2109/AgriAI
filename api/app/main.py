from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .services import model_service
from .voice_agent import voice_agent

app = FastAPI(title="SmartKisan API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    model_service.load_models()

# --- Schemas ---
class YieldInput(BaseModel):
    district: str
    crop: str
    season: str
    year: int

class PriceInput(BaseModel):
    crop: str
    mandi: str

class SchemeInput(BaseModel):
    query: str

# --- Endpoints ---

@app.get("/")
def home():
    return {"message": "SmartKisan AI Assistant Online"}

@app.post("/recommend_crop")
def recommend_crop(data: YieldInput):
    pred, interval = model_service.predict_yield(
        data.district, data.crop, data.season, data.year
    )
    return {"crop": data.crop, "estimated_yield": pred, "range": interval}

@app.post("/detect_disease")
async def detect_disease(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Invalid image")
    data = await file.read()
    label, conf = model_service.predict_disease(data)
    
    treatment = "Apply organic neem oil." if label == "Stressed" else "Continue monitoring."
    return {"disease": label, "confidence": conf, "treatment": treatment}

@app.post("/market_price")
def market_price(data: PriceInput):
    price, trend = model_service.predict_price(data.crop, data.mandi)
    return {
        "crop": data.crop,
        "mandi": data.mandi,
        "forecast_price": price,
        "trend": trend,
        "advice": "Sell Now" if price > 2000 else "Hold"
    }

@app.post("/gov_scheme")
def gov_scheme(data: SchemeInput):
    schemes = voice_agent.find_schemes(data.query)
    return {"schemes": schemes}
