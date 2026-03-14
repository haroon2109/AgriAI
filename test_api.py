import requests
import time
import subprocess
import os

print("Starting FastAPI...")
# Start using shell on windows
backend_process = subprocess.Popen("uvicorn backend_api.main:app --host 127.0.0.1 --port 8000", shell=True)

time.sleep(5)

try:
    print("Testing /predict_yield...")
    res1 = requests.post(
        "http://127.0.0.1:8000/predict_yield", 
        json={"lat": 10.78, "lon": 79.13, "crop_type": "Paddy", "sowing_date": "2023-10-01"}
    )
    print("Yield Response:", res1.json())

    print("\nTesting /disease_alert...")
    res2 = requests.post(
        "http://127.0.0.1:8000/disease_alert", 
        json={"lat": 10.78, "lon": 79.13}
    )
    print("Disease Response:", res2.json())
finally:
    print("Done testing.")
    backend_process.terminate()
