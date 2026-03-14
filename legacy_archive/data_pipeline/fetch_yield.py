import pandas as pd
import numpy as np
import os

def generate_mock_yield_data(output_path="data_pipeline/yield_data.csv"):
    """
    Generates synthetic yield data mimicking Data.gov.in structure.
    Columns: District, Year, Season, Crop, Area (Hectare), Production (Tonnes), Yield (Tonnes/Hectare)
    """
    districts = ["Thanjavur", "Madurai", "Coimbatore", "Tiruchirappalli", "Salem", "Erode"]
    years = range(2015, 2024)
    seasons = ["Kharif", "Rabi"]
    crops = ["Rice", "Sugarcane"]
    
    data = []
    
    for d in districts:
        for y in years:
            for s in seasons:
                for c in crops:
                    # Synthetic logic for variance
                    base_yield = 3.5 if c == "Rice" else 100.0 # Sugarcane has much higher tonnage/acre raw
                    
                    # Random variation +/- 20%
                    variation = np.random.uniform(0.8, 1.2)
                    yld = base_yield * variation
                    
                    area = np.random.uniform(5000, 20000)
                    production = area * yld
                    
                    data.append({
                        "State": "Tamil Nadu",
                        "District": d,
                        "Year": y,
                        "Season": s,
                        "Crop": c,
                        "Area_Hectare": round(area, 2),
                        "Production_Tonnes": round(production, 2),
                        "Yield_Tonnes_Hectare": round(yld, 2)
                    })
                    
    df = pd.DataFrame(data)
    
    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[INFO] Generated mock yield data at {output_path}")
    return df

def fetch_real_data_gov_in():
    """
    Placeholder for actual API call to OGD Platform (Data.gov.in).
    Requires API Key.
    """
    print("[WARN] Data.gov.in API key not configured. Using synthetic data.")
    return generate_mock_yield_data()

if __name__ == "__main__":
    fetch_real_data_gov_in()
