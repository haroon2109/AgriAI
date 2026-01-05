import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import json

# Paths
DATA_PATH = "data_pipeline/yield_data.csv"
MODEL_DIR = "models/artifacts"
MODEL_PATH = os.path.join(MODEL_DIR, "yield_model.pkl")

def get_data_from_db():
    """
    Placeholder: In production, this would connect to the PostgreSQL 
    database using sqlalchemy to fetch the training set.
    """
    print("[INFO] DB Connection not active. Loading from local CSV cache.")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Run fetch_yield.py first.")
    return pd.read_csv(DATA_PATH)

def train_yield_model():
    print("[INFO] Starting Yield Model Training (Phase 1)...")
    
    try:
        df = get_data_from_db()
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    # Preprocessing
    # Encoding categorical variables: District, Season, Crop
    # We save these mappings to ensure consistency during inference (API)
    
    df['District_Code'], district_uniques = pd.factorize(df['District'])
    df['Season_Code'], season_uniques = pd.factorize(df['Season'])
    df['Crop_Code'], crop_uniques = pd.factorize(df['Crop'])
    
    mappings = {
        "District": {name: i for i, name in enumerate(district_uniques)},
        "Season": {name: i for i, name in enumerate(season_uniques)},
        "Crop": {name: i for i, name in enumerate(crop_uniques)}
    }
    
    # Feature Selection
    # In a real scenario, we'd include rainfall/soil data which would be joined in `fetch_yield.py`
    features = ['District_Code', 'Season_Code', 'Crop_Code', 'Year']
    target = 'Yield_Tonnes_Hectare'
    
    X = df[features]
    y = df[target]
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model Training
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluation
    preds = rf.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print("-" * 30)
    print(f"Model Performance (Random Forest):")
    print(f"MAE: {mae:.2f} tonnes/hectare")
    print(f"R² : {r2:.2f}")
    print("-" * 30)
    
    # Save Artifacts
    os.makedirs(MODEL_DIR, exist_ok=True)
    artifact = {
        "model": rf,
        "mappings": mappings,
        "features": features
    }
    joblib.dump(artifact, MODEL_PATH)
    print(f"[INFO] Model and mappings saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_yield_model()
