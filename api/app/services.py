import os
import joblib
import json
import xgboost as xgb
import torch
import numpy as np
import pandas as pd
from torchvision import transforms, models
from PIL import Image
import io
from datetime import datetime

# Model Paths
MODEL_DIR = "models/artifacts"
XGB_PATH = os.path.join(MODEL_DIR, "yield_xgb.json")
MAPPING_PATH = os.path.join(MODEL_DIR, "xgb_mappings.pkl")
RESNET_PATH = os.path.join(MODEL_DIR, "disease_resnet18.pth")
PRICE_MODEL_PATH = os.path.join(MODEL_DIR, "market_price_model.pkl")

class ModelService:
    def __init__(self):
        self.xgb_model = None
        self.xgb_mappings = None
        self.resnet_model = None
        self.price_model = None
        self.price_mappings = None
        self.device = torch.device("cpu")

    def load_models(self):
        print("[INFO] Loading SmartKisan models...")
        
        # 1. XGBoost Yield
        if os.path.exists(XGB_PATH):
            self.xgb_model = xgb.XGBRegressor()
            self.xgb_model.load_model(XGB_PATH)
            self.xgb_mappings = joblib.load(MAPPING_PATH)
        
        # 2. ResNet Disease
        if os.path.exists(RESNET_PATH):
            model = models.resnet18(pretrained=False)
            num_ftrs = model.fc.in_features
            model.fc = torch.nn.Linear(num_ftrs, 2)
            model.load_state_dict(torch.load(RESNET_PATH, map_location=self.device))
            model.eval()
            self.resnet_model = model

        # 3. Market Price
        if os.path.exists(PRICE_MODEL_PATH):
            data = joblib.load(PRICE_MODEL_PATH)
            self.price_model = data["model"]
            self.price_mappings = data["mappings"]
            print("[INFO] Market Price Model loaded.")

    def predict_yield(self, district, crop, season, year):
        # ... (Existing Logic) ...
        # Simplified for brevity/robustness
        if not self.xgb_model: return 0.0, [0.0, 0.0]
        try:
             d = self.xgb_mappings['District'].get(district, 0)
             s = self.xgb_mappings['Season'].get(season, 0)
             c = self.xgb_mappings['Crop'].get(crop, 0)
             
             input_data = pd.DataFrame([{ 'District_Code': d, 'Season_Code': s, 'Crop_Code': c, 'Year': year }])
             pred = float(self.xgb_model.predict(input_data)[0])
             return pred, [pred*0.9, pred*1.1]
        except Exception as e:
            print(f"Yield Pred Error: {e}")
            return 0.0, [0.0, 0.0]

    def predict_disease(self, image_bytes):
        # ... (Existing Logic) ...
        if not self.resnet_model: return "Unknown", 0.0
        CLASSES = ['Healthy', 'Stressed']
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            image = transform(image).unsqueeze(0)
            with torch.no_grad():
                out = self.resnet_model(image)
                probs = torch.nn.functional.softmax(out, dim=1)
                conf, idx = torch.max(probs, 1)
            return CLASSES[idx.item()], float(conf.item())
        except Exception as e:
            print(f"Disease Pred Error: {e}")
            return "Error", 0.0

    def predict_price(self, crop, mandi):
        """Forecast price for next 7 days."""
        if not self.price_model:
            return 0.0, "Model Not Loaded"

        try:
            c_code = self.price_mappings['Crop'].get(crop, 0)
            m_code = self.price_mappings['Mandi'].get(mandi, 0)
            
            # Predict for tomorrow
            tomorrow = datetime.now()
            X = pd.DataFrame([{
                'Crop_Code': c_code,
                'Mandi_Code': m_code,
                'DayOfYear': tomorrow.timetuple().tm_yday + 1,
                'Month': tomorrow.month,
                'Year': tomorrow.year
            }])
            
            price = float(self.price_model.predict(X)[0])
            return price, "Stable" # Logic for trend could be added
        except Exception as e:
            print(f"Price Pred Error: {e}")
            return 0.0, "Error"

model_service = ModelService()
