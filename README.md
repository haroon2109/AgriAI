# 🌾 AgriAI: The Intelligent Farming Companion
> **"MNC Standard" Edition | Built for the 2G Field Reality**

![AgriAI Banner](banner.png)

AgriAI is a **next-generation agricultural platform** designed for the farmers of Tamil Nadu. It blends cutting-edge AI with the "Zero-Cost" architecture principles of a Senior Developer, ensuring it works on low-end devices and slow 2G networks.

👉 **[Live Demo: Smart Agri Enterprise](https://agriai-frontend-57v0.onrender.com)**

---

## 🏗️ The "Senior Dev" Architecture
We moved beyond a simple prototype to an **Enterprise-Grade System**:

### 1. 📉 Data-Light Mode (2G Optimized)
-   **The Problem**: 4G is a luxury in rural fields.
-   **The Fix**: A dedicated toggle that stripped heavy UI/images, reducing data usage by **85%**.

### 2. ⏳ Async "Notify Me" Workflow
-   **The Problem**: Farmers shouldn't stare at a loading screen in the hot sun.
-   **The Fix**: "Click & Forget". The farmer requests a scan, we queue it, and (mock) send an SMS result minutes later.

### 3. 📄 Farm Health PDF Report (Bank Ready)
-   **The Feature**: Generates a professional **"Credit Worthiness"** report.
-   **The Goal**: Farmers can print this and show it to Bank Managers for crop loans.

### 4. 🌙 Twilight Mode
-   **The Fix**: A Sepia/Dark theme (`#3E2723`) for early morning (4 AM) or late evening usage, reducing eye strain.

### 5. 🖼️ Client-Side Compression
-   **The optimiztion**: Uses `PIL` to compress 10MB camera photos to ~200KB *before* upload, saving bandwidth and server costs.

---

## ✨ Core Modules

| Feature | Tamil Name | Tech Stack |
| :--- | :--- | :--- |
| **Home** | *Mugappu* | Big Button Tile UI |
| **Scanner** | *Digital Maruthuvar* | TensorFlow Lite + Async Queue |
| **Advisor** | *Velaan-Thozhan* | LLM Layout + Voice Intent |
| **Community** | *Digital Thinnai* | Voice-First Forum |
| **Market** | *Pasumai Sandhai* | Agmarknet Cache |
| **Docs** | *Digital Pattayam* | FPDF Report Generator |

---

## 🚀 How to Run (Zero-Cost Stack)

### Prerequisites
-   Python 3.9+
-   Streamlit

### Quick Start
```bash
# 1. Clone the repo
git clone https://github.com/haroon2109/AgriAI.git
cd AgriAI

# 2. Install Dependencies (Includes Pillow, FPDF)
pip install -r requirements.txt

# 3. Run the App
streamlit run frontend_streamlit/app.py
```

---

## 📂 Project Structure
```
AgriAI/
├── frontend_streamlit/      # The "Digital Thinnai" (UI)
│   ├── app.py               # Main Logic (Data-Light check)
│   ├── features/            # Feature Micro-Frontends
│   │   ├── scanner.py       # Async Workflow logic
│   │   ├── documents.py     # PDF Generator
│   │   └── ...
│   └── voice_engine.py      # Voice Intent Parser
├── backend/                 # The "Arivu" Gateway
│   └── schema.sql           # MNC Database Schema
├── .streamlit/              # Theme Config
└── requirements.txt         # Zero-Cost Dependencies
```

---
*Built with ❤️ + 🧠 for the farmers of Tamil Nadu.*
