import pandas as pd
import numpy as np
import os

DATA_DIR = "data_pipeline"
OUTPUT_FILE = os.path.join(DATA_DIR, "synthetic_tabular_data.csv")
DISTRICTS = ['Thanjavur', 'Madurai', 'Coimbatore', 'Tiruchirappalli', 'Salem']
CROPS = ['Paddy', 'Sugarcane', 'Cotton', 'Maize', 'Groundnut']
YEARS = [2020, 2021, 2022, 2023]
SEASONS = ['Kharif', 'Rabi']

def generate_tabular_data():
    """Generates synthetic historical tabular data blending yield, climate, and soil features."""
    print(f"[INFO] Generating tabular data for {len(DISTRICTS)} districts...")
    
    records = []
    
    for dist in DISTRICTS:
        for year in YEARS:
            for season in SEASONS:
                for crop in CROPS:
                    # Base Yields mapping
                    base_yield = 2000
                    if crop == 'Paddy': base_yield = 2500
                    elif crop == 'Sugarcane': base_yield = 40000
                    elif crop == 'Cotton': base_yield = 800
                    elif crop == 'Maize': base_yield = 3000
                    elif crop == 'Groundnut': base_yield = 1500
                    
                    # Generate weather/soil features
                    rainfall = np.random.normal(500, 100) if season == 'Kharif' else np.random.normal(200, 50)
                    temp_min = np.random.normal(22, 2)
                    temp_max = np.random.normal(32, 2)
                    humidity = np.random.normal(70, 10)
                    ph_level = np.random.normal(6.5, 0.5)
                    nitrogen = np.random.normal(100, 20)
                    phosphorus = np.random.normal(40, 10)
                    potassium = np.random.normal(60, 15)
                    
                    # Target variable modification based on features
                    yield_modifier = 1.0
                    if rainfall < 300 and season == 'Kharif': yield_modifier *= 0.8
                    if ph_level < 5.5 or ph_level > 7.5: yield_modifier *= 0.9
                    
                    final_yield = base_yield * yield_modifier * np.random.uniform(0.9, 1.1)
                    
                    records.append({
                        'District': dist,
                        'Year': year,
                        'Season': season,
                        'Crop': crop,
                        'Rainfall_mm': round(rainfall, 2),
                        'Temp_Min_C': round(temp_min, 2),
                        'Temp_Max_C': round(temp_max, 2),
                        'Humidity_Pct': round(humidity, 2),
                        'pH_Level': round(ph_level, 2),
                        'Nitrogen_kgha': round(nitrogen, 2),
                        'Phosphorus_kgha': round(phosphorus, 2),
                        'Potassium_kgha': round(potassium, 2),
                        'Yield_Tonnes_Hectare': round(final_yield / 1000, 2) # Convert kg to tonnes roughly
                    })
                    
    df = pd.DataFrame(records)
    
    # Save the synthetic robust dataset
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"[SUCCESS] Synthetic tabular data saved to {OUTPUT_FILE} with {len(df)} records.")

if __name__ == "__main__":
    generate_tabular_data()
