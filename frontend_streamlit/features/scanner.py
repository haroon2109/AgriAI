import streamlit as st
import time

import time

@st.cache_resource
def load_diagnostic_model():
    # Simulate heavy model loading (MobileNetV2 / YOLO)
    time.sleep(1) # Fake delay
    return "Model_Loaded_v1.0"

def show_scanner():
    model = load_diagnostic_model()
    st.markdown("""
    <style>
        /* Camera Button Styling */
        .camera-btn {
            display: flex; justify-content: center; align-items: center;
            width: 80px; height: 80px;
            background-color: #2E7D32; /* Deep Paddy Green */
            border-radius: 50%;
            border: 4px solid #FFC107; /* Turmeric Gold */
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
            margin: 0 auto;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .camera-btn:hover { transform: scale(1.1); }
        
        /* Scanning Animation - Golden Thread */
        @keyframes scan {
            0% { top: 0%; opacity: 0; }
            50% { opacity: 1; box-shadow: 0 0 15px #FFC107; }
            100% { top: 100%; opacity: 0; }
        }
        .scan-line {
            position: absolute; width: 100%; height: 4px;
            background: #FFC107; /* Turmeric Gold */
            animation: scan 2s infinite linear;
            z-index: 10;
        }
        .scan-container {
            position: relative; overflow: hidden;
            border: 2px dashed #2E7D32;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.get('low_data_mode', False):
        st.image("scanner_tech.png", use_column_width=True)
    st.markdown("## 🌿 Digital Maruthuvar (பயிர் மருத்துவர்)")
    st.caption("உங்கள் பயிருக்கான நவீன மருத்துவர் (Your Digital Crop Doctor)")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📸 Capture (படம் பிடி)")
        st.info("💡 **Tip:** இலையின் பாதிக்கப்பட்ட பகுதியைத் தெளிவாகக் காட்டவும்.")
        
        # --- CAMERA INPUT ---
        st.write("Click 'Take Photo' below (கீழே உள்ள கேமராவை அழுத்தவும்)")
        cam_file = st.camera_input("Scanner Active")
        
        # Fallback Uploader
        st.markdown("---")
        st.caption("Or upload from gallery (அல்லது கேலரியில் இருந்து பதிவேற்றவும்)")
        uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'], label_visibility="collapsed")
        
        final_file = cam_file if cam_file else uploaded_file

        if not final_file:
            st.markdown("""
            <div style="text-align:center; padding:20px; border:2px dashed #ddd; border-radius:10px;">
                <h3 style="color:#aaa;">Waiting for Leaf...</h3>
                <p style="color:#888;">பயிரைப் படம் பிடிக்கவும்</p>
            </div>
            """, unsafe_allow_html=True)
        else:
             # Compress before processing (Senior Dev Optimization)
            compressed_bytes = compress_image(final_file)
            st.success(f"✅ Image Compressed: {len(final_file.getvalue())/1024:.1f}KB -> {len(compressed_bytes)/1024:.1f}KB")
            
            st.image(final_file, caption="Analyzing...", use_column_width=True)
            
            # Scanning Animation
            with st.spinner("🕵️ ஆராய்ந்து கொண்டிருக்கிறோம்... (Scanning...)"):
                st.markdown('<div class="scan-container"><div class="scan-line"></div><p>Er-Arivan is analyzing...</p></div>', unsafe_allow_html=True)
                time.sleep(3) # Mock processing
                
            # --- Diagnosis Report ---
            st.success("✅ Analysis Complete! (ஆய்வு முடிந்தது)")
            
            # --- Results Section ---
            st.markdown("---")
            st.header("📋 Diagnosis Report (கண்டறிதல் அறிக்கை)")
            
            # 1. THE WHAT (Diagnosis)
            st.subheader("1. What is it? (என்ன பிரச்சனை?)")
            st.error("🔴 **Diagnosis:** இலைக்கருகல் நோய் (Early Blight)")
            st.markdown("**Confidence (உறுதித்தன்மை):** 96%")

            # 2. THE WHY (Cause)
            st.subheader("2. Why did it happen? (காரணம்)")
            st.write("பூஞ்சை தாக்குதலால் ஏற்படுகிறது (Caused by fungal infection named *Alternaria solani*). High humidity favors this.")
            
            # 3. THE HOW (Remedy)
            st.subheader("3. Solution (தீர்வு)")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 🍃 இயற்கை முறை (Organic)")
                st.info("Spray **Neem Oil (வேப்ப எண்ணெய்)** mixed with water every 3 days.")
            with c2:
                st.markdown("#### 🧪 நவீன முறை (Chemical)")
                st.warning("Apply **Mancozeb** fungicide (2g/liter) if infection is severe.")
            
            # --- Expert Consult ---
            st.markdown("---")
            st.markdown("#### Still in doubt? (இன்னும் சந்தேகம் உள்ளதா?)")
            if st.button("📞 Talk to an Expert (நிபுணரிடம் பேசுங்கள்)"):
                st.info("Connecting to dedicated Agri-Officer... (Mock Call Initiated)")
            
            st.text_area("🎤 Voice Note (உங்கள் கேள்வியைப் பதிவு செய்யுங்கள்)", placeholder="Type or speak here...")
