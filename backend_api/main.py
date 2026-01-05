from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="AgriAI Backend API", version="1.0")

# --- DATA MODELS ---
class DistrictRequest(BaseModel):
    district_name: str
    crop: str

class YieldResponse(BaseModel):
    district: str
    predicted_yield_kg_per_acre: float
    confidence_score: float
    advisory: str

# --- MOCK ML LOGIC (To be replaced with PyTorch model) ---
def mock_yield_prediction(district, crop):
    # Baseline data (Tamil Nadu Context)
    base_yields = {
        "Paddy": 2400,
        "Tomato": 15000, 
        "Maize": 3000
    }
    base = base_yields.get(crop, 2000)
    
    # Add random variation simulating "model inference"
    variation = random.uniform(0.9, 1.1) 
    return round(base * variation, 2)

# --- ENDPOINTS ---
@app.get("/")
def read_root():
    return {"message": "AgriAI API is running. Use /predict_yield for inference."}

@app.post("/predict_yield", response_model=YieldResponse)
def predict_yield(request: DistrictRequest):
    """
    Predicts crop yield based on district historical baseline.
    """
    try:
        # 1. Fetch District Geometry (Mock Step: Real app would query PostGIS)
        # 2. Fetch Sentinel-2 Index (Mock Step: Real app would hit STAC API)
        
        # 3. Predict
        yield_val = mock_yield_prediction(request.district_name, request.crop)
        
        return YieldResponse(
            district=request.district_name,
            predicted_yield_kg_per_acre=yield_val,
            confidence_score=0.85,
            advisory=f"Good conditions for {request.crop} in {request.district_name}. Monitor irrigation."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class DiseaseRequest(BaseModel):
    crop: str
    symptoms: str
    humidity_level: float

@app.post("/disease_risk")
def predict_disease_risk(request: DiseaseRequest):
    """
    Assesses disease risk based on weather and symptoms.
    Uses TNAU Expert System Logic (Rule-based).
    """
    risk = "Low"
    score = 0.1
    
    # Simple Rule Engine (TNAU Logic Mock)
    if request.humidity_level > 80:
        score += 0.4
        if "spot" in request.symptoms.lower():
            risk = "High"
            score += 0.4
        elif "yellow" in request.symptoms.lower():
            risk = "Medium"
            score += 0.2
            
    return {
        "crop": request.crop,
        "risk_level": risk,
        "risk_score": round(score, 2),
        "alert": f"High humidity ({request.humidity_level}%) increases fungal risk." if score > 0.5 else "Conditions are stable."
    }
