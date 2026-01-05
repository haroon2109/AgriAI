import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Paths
DATA_PATH = "data_pipeline/yield_data.csv"
MODEL_DIR = "models/artifacts"
MODEL_PATH = os.path.join(MODEL_DIR, "yield_xgb.json") # XGBoost prefers JSON/UBJSON

def train_yield_xgb():
    print("[INFO] Starting XGBoost Yield Model Training...")
    
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] Data file {DATA_PATH} not found. Run fetch_yield.py first.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # Preprocessing
    # Factorize categoricals
    df['District_Code'], district_uniques = pd.factorize(df['District'])
    df['Season_Code'], season_uniques = pd.factorize(df['Season'])
    df['Crop_Code'], crop_uniques = pd.factorize(df['Crop'])
    
    mappings = {
        "District": {name: i for i, name in enumerate(district_uniques)},
        "Season": {name: i for i, name in enumerate(season_uniques)},
        "Crop": {name: i for i, name in enumerate(crop_uniques)}
    }
    
    features = ['District_Code', 'Season_Code', 'Crop_Code', 'Year']
    target = 'Yield_Tonnes_Hectare'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train XGBoost
    reg = xgb.XGBRegressor(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=5, 
        random_state=42,
        objective='reg:squarederror'
    )
    reg.fit(X_train, y_train)
    
    # Evaluate
    preds = reg.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    
    print("-" * 30)
    print("XGBoost Model Performance:")
    print(f"MAE: {mae:.2f}")
    print(f"R² : {r2:.2f}")
    print("-" * 30)
    
    # Save Model
    os.makedirs(MODEL_DIR, exist_ok=True)
    reg.save_model(MODEL_PATH)
    
    # Save mappings separately (using joblib/pickle)
    mapping_path = os.path.join(MODEL_DIR, "xgb_mappings.pkl")
    joblib.dump(mappings, mapping_path)
    
    print(f"[INFO] Model saved to {MODEL_PATH}")
    print(f"[INFO] Mappings saved to {mapping_path}")

if __name__ == "__main__":
    train_yield_xgb()
