import streamlit as st
import time

def show_advisor():
    st.title("🤖 Velaan-Thozhan (Agri-Friend)")
    st.caption("Your Arivu Ayya (Wise Assistant)")

    # Mascot & Welcome
    # Mascot & Welcome
    c1, c2 = st.columns([1, 4])
    with c1:
        if not st.session_state.get('low_data_mode', False):
            st.image("advisor_mascot.png", width=150)
        else:
            st.markdown("🤖 **Advisor**")
    with c2:
        st.info("வணக்கம்! இன்று உங்கள் விவசாயம் செழிக்க நான் என்ன செய்யட்டும்? (Greetings! How can I help your farm flourish today?)")

    # Quick Reply Buttons
    st.markdown("##### Quick Actions (விரைவான உதவி)")
    col1, col2, col3, col4 = st.columns(4)
    query = None
    
    with col1:
        if st.button("🍂 Crop Disease"): query = "என் பயிரில் பூச்சி தாக்குதல் உள்ளது (I have pest attack)"
    with col2:
        if st.button("💰 Market Price"): query = "இன்றைய சந்தை விலை என்ன? (Today's price?)"
    with col3:
        if st.button("🏛️ Govt Aid"): query = "எனக்கு அரசு மானியம் வேண்டும் (I need govt subsidy)"
    with col4:
        if st.button("🌧️ Weather"): query = "மழை வருமா? (Will it rain?)"

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- VOICE FIRST INPUT ---
    from streamlit_mic_recorder import mic_recorder
    
    c_voice, c_text = st.columns([1, 4])
    with c_voice:
        st.write("Speaking? (பேசவா?)")
        audio = mic_recorder(start_prompt="🎤 Start", stop_prompt="⏹️ Stop", key='recorder')
    
    # Check for Voice Input first
    if audio:
        st.audio(audio['bytes'])
        query = "Voice input received (Mock: 'What is the price of tomato?')" # Mock translation since no backend STT yet
        
    # Handle Input (Button or Text or Voice)
    if query:
        # User Message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        # Assistant Response (Mock)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            thinking_msg = "கொஞ்சம் பொறுங்கள், விவரங்களைச் சரிபார்க்கிறேன்... (Checking details...)"
            message_placeholder.markdown(f"*{thinking_msg}*")
            time.sleep(1.5)
            
            if "pest" in query or "Disease" in query:
                full_response = "படம் எடுத்து 'Digital Maruthuvar' பகுதியில் பதிவேற்றவும். (Please upload a photo in the Disease Scanner section.)"
            elif "price" in query or "Price" in query or "tomato" in query.lower():
                full_response = "Madurai Mandi: Tomato is ₹45/kg today."
            elif "subsidy" in query or "Aid" in query:
                full_response = "Check 'Arasu Thittam' tab for eligibility."
            elif "rain" in query or "Weather" in query:
                full_response = "No rain expected for 3 days."
            else:
                full_response = "I heard you. I am just a demo for now, but soon I will speak back!"
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Manual Input (Fallback)
    prompt = st.chat_input("Type to Arivu Ayya...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown("Received. Let me think...")
            st.session_state.messages.append({"role": "assistant", "content": "Received. Let me think..."})
