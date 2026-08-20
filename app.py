import os
import streamlit as st
from google import genai

# 1. API Key Validation
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets me GEMINI_API_KEY nahi mili!")

# Page Styling for Toddlers
st.set_page_config(page_title="Balwadi AI Teacher", page_icon="👶")
st.markdown("<h1 style='text-align: center; color: #FF4B4B; font-size: 38px;'>🎒 Balwadi AI Teacher 🧸</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 22px; color: #4A4A4A;'><b>Niche bade Mic 🎙️ button ko dabakar bolein!</b></p>", unsafe_allow_html=True)

# Session state to hold speech text
if "speech_output" not in st.session_state:
    st.session_state.speech_output = ""

# 2. JAVASCRIPT JADU: Browser Microphone and Voice Input Button
# Isse browser ka microphone trigger hoga aur text automatic form me submit ho jayega
voice_button_html = """
<div style="text-align: center; margin-top: 10px;">
    <button id="start-record-btn" style="background-color: #FF4B4B; color: white; border: none; padding: 20px 40px; font-size: 24px; font-weight: bold; border-radius: 50px; cursor: pointer; box-shadow: 0px 4px 10px rgba(0,0,0,0.2); transition: 0.3s;">
        🎙️ BOLNA SHURU KAREIN
    </button>
    <p id="status-text" style="color: gray; font-size: 16px; margin-top: 10px;">Button dabayein aur bolein...</p>
</div>

<script>
    const recordBtn = document.getElementById('start-record-btn');
    const statusText = document.getElementById('status-text');

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.lang = 'en-US'; // Baccha English words bolega (Cat, Dog, A for Apple)
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recordBtn.onclick = function() {
            recognition.start();
            recordBtn.style.backgroundColor = '#4CAF50';
            recordBtn.innerText = '🛑 MAI SUN RAHI HOON...';
            statusText.innerText = 'Bolein, AI Didi sun rahi hain...';
        };

        recognition.onresult = function(event) {
            const resultText = event.results[0][0].transcript;
            statusText.innerText = 'Aapne bola: ' + resultText;
            
            // Streamlit ke data transfer layer ko text bhejkar auto-submit karna
            const streamlitInput = window.parent.document.querySelector('input[aria-label="hidden_input"]');
            if (streamlitInput) {
                streamlitInput.value = resultText;
                streamlitInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
        };

        recognition.onspeechend = function() {
            recognition.stop();
            resetButton();
        };

        recognition.onerror = function(event) {
            statusText.innerText = 'Error aaya: ' + event.error;
            resetButton();
        };

        function resetButton() {
            recordBtn.style.backgroundColor = '#FF4B4B';
            recordBtn.innerText = '🎙️ BOLNA SHURU KAREIN';
        }
    } else {
        statusText.innerText = 'Aapka browser voice support nahi karta. Google Chrome use karein!';
    }
</script>
"""

# Invisible hidden text input trick to sync JavaScript with Python
hidden_word = st.text_input("hidden_input", label_visibility="collapsed", key="voice_input_trigger")

# Render the interactive Voice Button
st.components.v1.html(voice_button_html, height=150)

# 3. AI Core Processing Logic (Gemini 3.7 Flash)
if hidden_word:
    st.markdown(f"<p style='text-align: center; font-size: 18px;'>👶 Bacche ne bola: <b>{hidden_word}</b></p>", unsafe_allow_html=True)
    
    prompt = f"""
    You are a playful, loving, and energetic nursery school teacher talking to a 3-year-old toddler. 
    The child said: '{hidden_word}'.
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
                model='gemini-3.7-flash',  # Ultra-fast flagship version
                contents=prompt,
            )
            ai_reply = response.text.strip()
        
        # Display response beautifully
        st.markdown(f"<div style='background-color: #F0F2F6; padding: 25px; border-radius: 20px; text-align: center; border: 2px dashed #FF4B4B;'><h2 style='color: #1E88E5; font-size: 28px;'>👩‍🏫 {ai_reply}</h2></div>", unsafe_allow_html=True)
        
        # 4. Automatic Audio Response (Text-to-Speech)
        tts_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{ai_reply}");
            msg.lang = "hi-IN"; 
            msg.rate = 0.85; // Bacchon ke liye sahi dhireshiki speed
            msg.pitch = 1.25; // Sweet child-friendly voice pitch
            window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(tts_code, height=0)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        
