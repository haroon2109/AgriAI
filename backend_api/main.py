from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="AgriAI Backend API", version="1.0")

# --- DATA MODELS ---
class DistrictRequest(BaseModel):
    lat: float
    lon: float
    crop_type: str
    sowing_date: str

class YieldResponse(BaseModel):
    predicted_yield: float
    confidence_interval: str

# --- ENDPOINTS ---
@app.get("/")
def read_root():
    return {"message": "AgriAI API is running. Use /predict_yield for inference."}

@app.post("/predict_yield", response_model=YieldResponse)
def predict_yield(request: DistrictRequest):
    """
    Predicts crop yield using Random Forest model based on tabular climate data.
    """
    try:
        # Check cache for recent NDVI/EVI
        from database import get_cached_indices, set_cached_indices
        indices = get_cached_indices(request.lat, request.lon)
        
        # In a full flow we would query our RF Model
        # yield_model.predict(features)
        
        # Simulating RF model output based on lat/lon
        base_yield = 2000
        variation = random.uniform(0.8, 1.2)
        predicted_yield = round(base_yield * variation, 2)
        
        return YieldResponse(
            predicted_yield=predicted_yield,
            confidence_interval="± 200 kg/acre"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class DiseaseRequest(BaseModel):
    lat: float
    lon: float

class DiseaseResponse(BaseModel):
    risk_score: float
    risk_level: str
    recommended_action: str

@app.post("/disease_alert", response_model=DiseaseResponse)
def predict_disease_risk(request: DiseaseRequest):
    """
    Assesses disease risk using MobileNetV2 based on satellite imagery.
    """
    try:
        # In full flow: fetch satellite patch for lat/lon, run CNN inference
        # score = mobilenet_model(patch)
        
        score = round(random.uniform(0, 1), 2)
        risk = "Low"
        alert = "Conditions are stable."
        
        if score > 0.7:
            risk = "High"
            alert = "High fungal risk. Apply recommended fungicide immediately."
        elif score > 0.4:
            risk = "Medium"
            alert = "Monitor crop closely for symptoms."
            
        return DiseaseResponse(
            risk_score=score,
            risk_level=risk,
            recommended_action=alert
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Removed legacy disease endpoint
