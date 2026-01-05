import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta

# Config
MODEL_DIR = "models/artifacts"
MODEL_PATH = os.path.join(MODEL_DIR, "market_price_model.pkl")

def generate_market_data():
    """Generate synthetic daily market prices for last 2 years."""
    dates = pd.date_range(end=datetime.today(), periods=730)
    crops = ["Rice", "Sugarcane", "Tomato", "Onion"]
    mandis = ["Thanjavur", "Madurai", "Coimbatore"]
    
    data = []
    for c in crops:
        base_price = 2000 if c == "Rice" else 3000 # Base price per quintal
        if c == "Tomato": base_price = 1500
        
        for m in mandis:
            # Simulate trends with sine wave + noise
            trend = np.sin(np.arange(730) * 0.1) * 200
            noise = np.random.normal(0, 50, 730)
            prices = base_price + trend + noise
            
            for d, p in zip(dates, prices):
                data.append({
                    "Date": d,
                    "Crop": c,
                    "Mandi": m,
                    "Price_Quintal": round(p, 2)
                })
    return pd.DataFrame(data)

def train_price_model():
    print("[INFO] Training Market Price Model...")
    df = generate_market_data()
    
    # Feature Engineering
    df['DayOfYear'] = df['Date'].dt.dayofyear
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    
    # Factorize
    df['Crop_Code'], crop_uniques = pd.factorize(df['Crop'])
    df['Mandi_Code'], mandi_uniques = pd.factorize(df['Mandi'])
    
    mappings = {
        "Crop": {name: i for i, name in enumerate(crop_uniques)},
        "Mandi": {name: i for i, name in enumerate(mandi_uniques)}
    }
    
    X = df[['Crop_Code', 'Mandi_Code', 'DayOfYear', 'Month', 'Year']]
    y = df['Price_Quintal']
    
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    
    # Save
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({"model": model, "mappings": mappings}, MODEL_PATH)
    print(f"[INFO] Market Price Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_price_model()
