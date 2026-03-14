from pydantic import BaseModel
from typing import List, Optional

class YieldInput(BaseModel):
    district: str
    crop: str
    season: str
    year: int

class YieldOutput(BaseModel):
    state: str = "Tamil Nadu"
    district: str
    crop: str
    predicted_yield_tonnes_hectare: float
    confidence_interval: List[float] # [low, high]

class DiseaseRiskResponse(BaseModel):
    filename: str
    risk_level: str # 'Healthy', 'Stressed'
    confidence: float
    advisory: str
