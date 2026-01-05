import ee
import datetime
import argparse
import sys

def initialize_gee(use_mock=False):
    """Initialize Earth Engine API or mock if credentials missing."""
    if use_mock:
        print("[INFO] Running in MOCK mode. No GEE authentication required.")
        return False
    
    try:
        ee.Initialize()
        print("[INFO] Google Earth Engine initialized successfully.")
        return True
    except Exception as e:
        print(f"[WARN] GEE Initialization failed: {e}")
        print("[INFO] Falling back to MOCK mode.")
        return False

def get_tamil_nadu_roi():
    """Define Region of Interest: Tamil Nadu."""
    # Simplified polygon for Tamil Nadu (Example bounds)
    return ee.Geometry.Rectangle([76.2, 8.0, 80.3, 13.5])

def add_indices(image):
    """Compute NDVI and EVI."""
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    
    # EVI formula: 2.5 * ((NIR - Red) / (NIR + 6 * Red - 7.5 * Blue + 1))
    evi = image.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
            'BLUE': image.select('B2')
        }).rename('EVI')
        
    return image.addBands([ndvi, evi])

def fetch_sentinel_data(start_date, end_date, real_mode=False):
    """Fetch Sentinel-2 collection and compute stats."""
    if not real_mode:
        # Mock data return
        return {
            "status": "success",
            "mode": "mock",
            "data": [
                {"date": "2023-10-01", "district": "Thanjavur", "ndvi_mean": 0.65, "evi_mean": 0.45},
                {"date": "2023-10-15", "district": "Thanjavur", "ndvi_mean": 0.72, "evi_mean": 0.51},
                {"date": "2023-10-01", "district": "Madurai", "ndvi_mean": 0.45, "evi_mean": 0.30},
            ]
        }
    
    roi = get_tamil_nadu_roi()
    
    s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterDate(start_date, end_date) \
        .filterBounds(roi) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(add_indices)
        
    # In a real pipeline, we would reduce regions by district vectors here.
    # For this script, we'll just print image count.
    count = s2.size().getInfo()
    print(f"[INFO] Found {count} Sentinel-2 images.")
    
    return {"status": "success", "image_count": count}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Sentinel-2 Data for AgriAI")
    parser.add_argument("--start", type=str, default="2023-01-01", help="Start Date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2023-01-31", help="End Date (YYYY-MM-DD)")
    parser.add_argument("--mock", action="store_true", help="Force mock mode")
    
    args = parser.parse_args()
    
    is_real = initialize_gee(args.mock)
    data = fetch_sentinel_data(args.start, args.end, is_real)
    
    print("Output Data Sample:")
    print(data)
