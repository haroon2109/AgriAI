# 🚀 AgriAI Deployment Guide (Updated)

This guide covers the modern, microservices-based deployment of AgriAI using React, Node.js, FastAPI, and Supabase.

## 🏗️ 1. Architecture Overview
- **Frontend (Face)**: [React + Tailwind](file:///c:/Users/moham/OneDrive/Desktop/Folderzz/AgriAI/frontend_react) (Hosted on Vercel)
- **Core API (Heart)**: [Node.js + Express](file:///c:/Users/moham/OneDrive/Desktop/Folderzz/AgriAI/backend_node) (Hosted on Render)
- **ML Backend (Brain)**: [FastAPI](file:///c:/Users/moham/OneDrive/Desktop/Folderzz/AgriAI/backend_api) (Hosted on Render)
- **Database**: PostgreSQL (Hosted on Supabase)

---

## 💻 2. Local Development (Docker)

1.  **Ensure Docker Desktop** is running.
2.  **Environment Setup**:
    -   Create `.env` files in `backend_node` and `backend_api` based on the `.env.example` templates.
3.  **Run the Stack**:
    ```powershell
    docker-compose up --build
    ```
4.  **Access Points**:
    -   **Frontend**: http://localhost:3000
    -   **Core API**: http://localhost:5000/api
    -   **ML Docs**: http://localhost:8000/docs

---

## ☁️ 3. Production Deployment

### Step 1: Database (Supabase)
- Create a new project on Supabase.
- Copy the **Connection String** (PostgreSQL) and save it for the Core API.

### Step 2: ML Backend (Render)
1.  Create a **New Web Service** on Render.
2.  Connect your repo, set Root Directory to `backend_api`.
3.  Render will auto-detect the `Dockerfile`.
4.  Once live, copy the URL (e.g., `https://agri-ml.onrender.com`).

### Step 3: Core API (Render)
1.  Create a **New Web Service**, set Root Directory to `backend_node`.
2.  Add Environment Variables:
    -   `DATABASE_URL`: Your Supabase link.
    -   `JWT_SECRET`: A secure random string.
    -   `FASTAPI_URL`: The URL from Step 2.
3.  Once live, copy the URL (e.g., `https://agri-core.onrender.com`).

### Step 4: Frontend (Vercel)
1.  Import your repo to Vercel, set Root Directory to `frontend_react`.
2.  Add Environment Variable:
    -   `VITE_API_URL`: The URL from Step 3 (add `/api` at the end).
3.  Deploy!

---

## 🏺 4. Legacy Streamlit Flow
The original Streamlit dashboard is preserved in [legacy_archive/frontend_streamlit](file:///c:/Users/moham/OneDrive/Desktop/Folderzz/AgriAI/legacy_archive/frontend_streamlit) for internal testing.
To run it:
```powershell
pip install -r backend_api/requirements.txt
streamlit run legacy_archive/frontend_streamlit/app.py
```
