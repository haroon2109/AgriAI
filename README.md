# 🌾 SmartKisan: AI-Powered Mobile Assistant

SmartKisan is an end-to-end AI system designed to assist farmers with **Crop Recommendations**, **Disease Detection**, **Market Price Forecasting**, and **Government Schemes**.

## 🚀 Quick Start (Recommended)

The easiest way to run the full stack (Database, API, Frontend) is using Docker.

### Prerequisites
- Docker & Docker Compose installed.

### Steps
1.  **Build and Start**:
    Open your terminal in this folder and run:
    ```bash
    docker-compose up --build
    ```
2.  **Access the App**:
    - **Frontend (Mobile Simulator)**: Open [http://localhost:8501](http://localhost:8501)
    - **API Docs**: Open [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠️ Manual Setup (Local Python)

If you don't use Docker, follow these steps to run everything manually.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Data & Train Models
Before running the app, you need to create the synthetic data and train the AI models.
```bash
# 1. Fetch/Generate Data
python data_pipeline/fetch_yield.py         # Generates yield_data.csv
python data_pipeline/synthetic_data_generator.py # Generates disease images

# 2. Train Models
python models/train_yield_xgb.py   # Trains Crop Model
python models/train_price.py       # Trains Market Price Model
python models/train_disease_resnet.py # Trains Disease CNN (Optional, takes time)
```

### 3. Start the Backend API
Open a new terminal:
```bash
uvicorn api.app.main:app --reload --host 0.0.0.0 --port 8000
```
*Wait until you see "Application startup complete".*

### 4. Start the Frontend App
Open a **second** terminal:
```bash
streamlit run frontend_streamlit/app.py
```

---

## 📁 Project Structure
- `api/`: FastAPI backend handling AI inference.
- `frontend_streamlit/`: Mobile-app simulator.
- `models/`: Training scripts and saved artifacts (`.pkl`, `.json`, `.pth`).
- `data_pipeline/`: Scripts to fetch satellite/weather data.

## 🔑 Features to Demo
1.  **Crop Planner**: Select "Thanjavur" + "Rice" to see yield estimates.
2.  **Disease Cam**: Upload a leaf image (or use webcam) to detect "Stressed" vs "Healthy".
3.  **Market**: Select "Tomato" to see price forecasts.
4.  **Schemes**: Type "loan" or "insurance" to find government schemes.
