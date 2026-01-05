# 🌾 AgriAI: Smart Farming Assistant (Smart Agri)

![AgriAI Banner](banner.png)

**Live Demo:** 👉 [**Smart Agri Enterprise Link**](https://agriai-frontend-57v0.onrender.com)

**AgriAI** is a state-of-the-art AI assistant designed specifically for the farmers of Tamil Nadu. It bridges the gap between complex technology and the hands that feed us, following a **"Data-Light, Voice-First"** approach.

## 🚀 Key Features via "MNC Architecture"

We have upgraded the platform to meet **Enterprise Standards** while keeping it practically useful for a 2G network village environment.

### 1. 🔍 Digital Maruthuvar (Docs & Scanner)
*   **Offline-First Scanner**: Identify crop diseases (Leaf Blight, Rot) instantly.
*   **Zero-Cost Compression**: Uses custom `PIL` algorithms to compress 10MB sensor images to 200KB *before* upload, saving data costs.
*   **Async "Notify Me"**: Don't wait in the sun. Click "Notify Me via SMS" and pocket your phone while the AI processes.

### 2. 🎙️ Digital Thinnai (Voice Community)
*   **Voice-First Interface**: Farmers can ask queries in Tamil audio.
*   **Intent Parsing**: Our `VoiceEngine` prepares speech for LLM processing (Action: `Get Price`, Location: `Thanjavur`).

### 3. 📉 Data-Light & Twilight Mode
*   **2G Optimized**: Toggle "Data-Light Mode" to strip heavy assets for instant loading in remote fields.
*   **Twilight Mode**: Automatic Sepia/Dark theme for eye comfort during early morning (4 AM) or late evening usage.

### 4. 💰 Pasumai Sandhai (Marketplace)
*   **Real-Time Prices**: Aggregates data from local Mandis.
*   **Crowdsourced Pricing**: Farmers can report the *actual* selling price, creating a "Waze for Agriculture".

## 🛠️ Tech Stack (Zero-Cost Architecture)

Built to run indefinitely on free-tier infrastructure without compromising performance.

*   **Frontend**: Streamlit (Python) with Custom CSS Components.
*   **AI Engine**: TensorFlow Lite (Quantized Models for CPU).
*   **Database**: PostgreSQL (Supabase) - *Schema Prepared*.
*   **Storage**: Cloudinary / Local Optimized.

## 💻 Installation

To run this locally:

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/haroon2109/AgriAI.git
    cd AgriAI
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**:
    ```bash
    streamlit run frontend_streamlit/app.py
    ```

## 📄 License
Open Source & Free for Indian Farmers.
