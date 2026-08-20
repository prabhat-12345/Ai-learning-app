import os
import streamlit as st
import google.generativeai as genai

# 1. API Key Setup
gemini_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=gemini_key)

# Page Configuration for Kids (Bada text aur attractive rang)
st.set_page_config(page_title="Balwadi AI Teacher", page_icon="👶")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎒 Balwadi AI Teacher 🧸</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'><b>Baccho! Mic daba kar bolo (Cat, Dog, A for Apple, 1 2 3)</b></p>", unsafe_allow_html=True)

# 2. Input Box with BIG font for kids
user_word = st.text_input("", placeholder="🗣️ Yahan bolein ya likhein...", key="kid_input")

if user_word:
    # Super Prompt for Toddlers
    prompt = f"""
    You are a playful, loving, and energetic nursery school teacher talking to a 3-year-old toddler. 
    The child said: '{user_word}'.
    Respond in a fun, exciting way using simple Hindi (mixed with common English words) in exactly 1 short sentence (max 5-6 words).
    Rules:
    - Animals: Make sound + Hindi name (e.g., "Woof Woof! Dog yani Kutta!")
    - Alphabets: Praise + next letter (e.g., "Wow! B for Ball!")
    - Numbers: Next numbers (e.g., "Yeey! 4, 5, 6!")
    - Generic words: Hindi meaning with energy (e.g., "Water yani Paani!")
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    with st.spinner("🎈 AI Didi soch rahi hain..."):
        response = model.generate_content(prompt)
        ai_reply = response.text.strip()
    
    # Big text display for kids to see
    st.markdown(f"<div style='background-color: #F0F2F6; padding: 20px; border-radius: 10px; text-align: center;'><h2 style='color: #1E88E5;'>👩‍🏫 {ai_reply}</h2></div>", unsafe_allow_html=True)
    
    # 3. Text-to-Speech Voice Jadu (Thoda slow aur sweet voice baccho ke liye)
    tts_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{ai_reply}");
        msg.lang = "hi-IN"; 
        msg.rate = 0.9; // Baccho ke liye thoda slow bolega taaki samajh aaye
        msg.pitch = 1.2; // Voice ko thoda sweet aur cheerful banayega
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(tts_code, height=0)
