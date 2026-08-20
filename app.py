import os
import streamlit as st
from google import genai
# Streamlit ka official audio tool import ho raha hai
from streamlit_mic_recorder import speech_to_text

# API Key Validation
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets me GEMINI_API_KEY nahi mili!")

st.set_page_config(page_title="Balwadi AI Teacher", page_icon="👶")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎒 Balwadi AI Teacher 🧸</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'><b>Niche Mic daba kar bolein:</b></p>", unsafe_allow_html=True)

# 1. Streamlit Official Speech to Text Component
# Isse browser background me Google Speech Service ka use karke direct text return karega
text_input = speech_to_text(
    start_prompt="🎙️ BOLNA SHURU KAREIN",
    stop_prompt="🛑 BAS KAREIN",
    language='en', # Baccha 'Cat', 'Dog' jise English words bolega
    use_container_width=True,
    key='speech'
)

# 2. AI Core Processing Logic (Gemini 3.7 Flash)
if text_input:
    st.markdown(f"<p style='text-align: center; font-size: 18px;'>👶 Aapne bola: <b>{text_input}</b></p>", unsafe_allow_html=True)
    
    prompt = f"""
    You are a playful, loving, and energetic nursery school teacher talking to a 3-year-old toddler. 
    The child said: '{text_input}'.
    Respond in a fun, exciting way using simple Hindi (mixed with common English words) in exactly 1 short sentence (max 5-6 words).
    Rules:
    - Animals: Make sound + Hindi name (e.g., "Woof Woof! Dog yani Kutta!")
    - Alphabets: Praise + next letter (e.g., "Wow! B for Ball!")
    - Numbers: Next numbers (e.g., "Yeey! 4, 5, 6!")
    - Generic words: Hindi meaning with energy (e.g., "Water yani Paani!")
    """
    
    try:
        with st.spinner("🎈 AI Didi soch rahi hain..."):
            response = client.models.generate_content(
                model='gemini-3.7-flash',
                contents=prompt,
            )
            ai_reply = response.text.strip()
        
        # Jawab ko bade aur sundar box me display karna
        st.markdown(f"<div style='background-color: #F0F2F6; padding: 25px; border-radius: 20px; text-align: center; border: 2px dashed #FF4B4B;'><h2 style='color: #1E88E5; font-size: 28px;'>👩‍🏫 {ai_reply}</h2></div>", unsafe_allow_html=True)
        
        # Audio response generator
        tts_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{ai_reply}");
            msg.lang = "hi-IN"; 
            msg.rate = 0.85; 
            msg.pitch = 1.25; 
            window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(tts_code, height=0)
        
    except Exception as e:
        st.error(f"Error aaya: {str(e)}")
        
