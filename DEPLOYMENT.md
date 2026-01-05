# 🚀 AgriAI Deployment Guide

This guide covers how to run AgriAI locally for development and how to deploy it to the cloud (Render.com).

## 💻 1. Local Development (Windows)

### Prerequisites
-   **Python 3.9+** installed.
-   **Git** installed.
-   **Docker Desktop** (Optional, for Full Stack).

### Option A: Frontend Only (Fastest)
Use this if you just want to work on the UI.
1.  Open Terminal in the project folder:
    ```powershell
    cd C:\Users\moham\OneDrive\Desktop\Folderzz\AgriAI
    ```
2.  Install dependencies:
    ```powershell
    pip install -r requirements.txt
    ```
3.  Run the App:
    ```powershell
    streamlit run frontend_streamlit/app.py
    ```
4.  Open http://localhost:8501

### Option B: Full Stack (Docker)
Use this to run the Frontend, Backend API, and Database together.
1.  Ensure Docker Desktop is running.
2.  Run the command:
    ```powershell
    docker-compose up --build
    ```
3.  Access Points:
    -   **App**: http://localhost:8501
    -   **API**: http://localhost:8000/docs

---

## ☁️ 2. Cloud Deployment (Render.com)

We recommend **Render** as it offers a free tier for Web Services and Docker.

### Step 1: Push Code to GitHub
Ensure your code is pushed to a GitHub repository.

### Step 2: Deploy Backend API
1.  Create a **New Web Service** on Render.
2.  Connect your GitHub repo.
3.  **Root Directory**: leave blank (Default)
4.  **Runtime**: Python 3
5.  **Build Command**: `pip install -r requirements.txt`
6.  **Start Command**: `uvicorn backend_api.main:app --host 0.0.0.0 --port 10000`
7.  Click **Create Web Service**. Copy the URL (e.g., `https://agri-backend.onrender.com`).

### Step 3: Deploy Frontend Dashboard
1.  Create another **New Web Service**.
2.  Connect the same repo.
3.  **Root Directory**: `.` (Root)
6.  **Environment Variables**:
    -   Key: `BACKEND_URL`
    -   Value: `https://agri-backend.onrender.com` (The URL from Step 2)
    -   (Optional, for Email):
        -   `EMAIL_USER`: `mdharoon21@gmail.com`
        -   `EMAIL_PASSWORD`: `your-16-char-app-password`
7.  Click **Create Web Service**.

### Step 4: Verification
Visit your Frontend URL. It should load the dashboard and communicate with your deployed API!

---

## 🛠️ Troubleshooting

-   **Black Screen?**: We have forced Light Mode in `.streamlit/config.toml`. If issues persist, clear browser cache.
-   **API Error?**: Ensure `BACKEND_URL` is set correctly in the Frontend environment variables.
