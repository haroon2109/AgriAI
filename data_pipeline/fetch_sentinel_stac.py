import pystac_client
import stackstac
import planetary_computer
import xarray as xr
import numpy as np
import json
import os

# Config
STAC_API_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
COLLECTION = "sentinel-2-l2a"

# Thanjavur, Tamil Nadu (Approximate Bounding Box)
# Min Lon, Min Lat, Max Lon, Max Lat
THANJAVUR_BBOX = [78.8, 10.5, 79.5, 11.0]

def fetch_sentinel_stac(bbox=THANJAVUR_BBOX, date_range="2023-11-01/2023-11-30", max_cloud_cover=20):
    print(f"[INFO] Connecting to STAC API: {STAC_API_URL}")
    catalog = pystac_client.Client.open(STAC_API_URL, modifier=planetary_computer.sign_inplace)
    
    print(f"[INFO] Searching for items in {COLLECTION}...")
    search = catalog.search(
        collections=[COLLECTION],
        bbox=bbox,
        datetime=date_range,
        query={"eo:cloud_cover": {"lt": max_cloud_cover}}
    )
    
    items = search.item_collection()
    print(f"[INFO] Found {len(items)} items.")
    
    if len(items) == 0:
        return None
    
    # Select the least cloudy item
    least_cloudy_item = min(items, key=lambda item: item.properties["eo:cloud_cover"])
    print(f"[INFO] Selected Item: {least_cloudy_item.id} (Cloud Cover: {least_cloudy_item.properties['eo:cloud_cover']}%)")
    
    # Load data lazily with stackstac
    # Fetching Bands: B04 (Red), B08 (NIR) for NDVI
    data = stackstac.stack(
        [least_cloudy_item],
        assets=["B04", "B08"],
        resolution=20 # 20m resolution to save bandwidth
    )
    
    return data

def calculate_ndvi(xr_data):
    """Calculate NDVI from Xarray DataArray (STAC output)."""
    # Create NDVI DataArray
    nir = xr_data.sel(asset="B08").astype("float32")
    red = xr_data.sel(asset="B04").astype("float32")
    
    ndvi = (nir - red) / (nir + red)
    
    # Compute mean NDVI
    mean_ndvi = ndvi.mean().item()
    print(f"[RESULT] Mean NDVI for selected region: {mean_ndvi:.4f}")
    return ndvi

if __name__ == "__main__":
    try:
        data = fetch_sentinel_stac()
        if data is not None:
            # We need to compute() to actually fetch pixels if we want values
            # Using a small slice or just metadata for demo speed
            print("[INFO] Data structure loaded (Lazy Xarray):")
            print(data)
            
            # Uncomment to actually download and compute (might take time/bandwidth)
            # ndvi = calculate_ndvi(data.compute())
            
            print("[SUCCESS] Pipeline verification complete.")
        else:
            print("[WARN] No data found for the specified criteria.")
            
    except Exception as e:
        print(f"[ERROR] STAC Fetch failed: {e}")
        print("[TIP] Ensure 'pystac-client' and 'stackstac' are installed.")
