# 🌾 AgriAI: The Intelligent Farming Companion

**"Mannum Marabum" (Soil & Tradition) Edition**

AgriAI is a next-generation agricultural platform designed for Tamil Nadu. It blends cutting-edge AI (Satellite monitoring, Disease Detection) with deep cultural wisdom (Crop Calendars, Traditional Knowledge).

![AgriAI Banner](https://via.placeholder.com/1000x300?text=AgriAI+-+Technology+Meeting+Tradition)

## 🏗️ Architecture: Full-Stack

The platform uses a modern containerized microservices architecture:

1.  **Frontend**: Streamlit (Python) for the interactive dashboard.
2.  **Backend Brain**: FastAPI (Python) for AI inference (`/predict_yield`, `/disease_risk`).
3.  **Database**: PostgreSQL + PostGIS for spatial data (Districts, Farms).
4.  **AI Models**:
    -   **Vision**: CNN for Disease Detection (PlantVillage).
    -   **Tabular**: Random Forest for Yield Prediction (Kaggle TN Dataset).

## 🚀 How to Run

### Option 1: Quick Start (Standalone Frontend)
If you only want to see the UI without the backend API:
```bash
pip install -r requirements.txt
streamlit run frontend_streamlit/app.py
```

### Option 2: Full-Stack (Recommended)
To run the App, API, and Database together using Docker:
```bash
docker-compose up --build
```
-   **Frontend**: http://localhost:8501
-   **Backend API**: http://localhost:8000/docs (Swagger UI)

## ✨ Key Features
-   **🤖 Velaan-Thozhan**: AI Chatbot with Voice support.
-   **🌿 Digital Maruthuvar**: Plant Disease Scanner.
-   **🗺️ Sat-Map**: Satellite-based Yield Prediction Map.
-   **💰 Pasumai Sandhai**: Real-time Marketplace with Agmarknet data.
-   **☀️ Sunlight Mode**: High-Contrast UI for field use.

## � Project Structure
-   `frontend_streamlit/`: Main UI Application.
-   `backend_api/`: FastAPI logic and ML Pipelines.
-   `database/`: SQL scripts for PostGIS schema.
-   `docker-compose.yml`: Container Orchestration.

---
*Built with ❤️ for the farmers of Tamil Nadu.*
