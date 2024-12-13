from dotenv import load_dotenv
import streamlit as st
from elevenlabs.client import ElevenLabs
import os
from typing import List
import datetime 

# Load environment variables from .env file
load_dotenv()

class ElevenLabsTTS:
    def __init__(self, api_key: str, model: str = "eleven_multilingual_v2"):
        """Initialize ElevenLabs TTS provider."""
        self.client = ElevenLabs(api_key=api_key)
        self.model = model
        
    def generate_audio(self, text: str, voice: str) -> bytes:
        """Generate audio using ElevenLabs API."""
        audio = self.client.generate(
            text=text,
            voice=voice,
            model=self.model
        )
        return b''.join(chunk for chunk in audio if chunk)
    
    def get_voices(self) -> dict:
        """Get available voices."""
        try:
            voices_response = self.client.voices.get_all()
            return {voice.name: voice.voice_id for voice in voices_response.voices}
        except Exception as e:
            st.error(f"Error fetching voices: {str(e)}")
            return {"Bella": "bella"}  # Fallback voice

# Initialize TTS engine
tts = ElevenLabsTTS(api_key=os.getenv("ELEVEN_API_KEY"))

# Page config
st.set_page_config(page_title="ElevenLabs TTS Demo", page_icon="🎙️")

# Header
st.image(
    "https://user-images.githubusercontent.com/12028621/262629275-4f85c9cf-85b6-435e-ab50-5b8c7c4e9dd2.png", 
    use_container_width=True
)

# Description
st.markdown("""
A demo of the world's most advanced TTS systems, made by [ElevenLabs](https://elevenlabs.io). 
Eleven Multilingual V2 is a single foundational model supporting 28 languages including: 
English, Chinese, Spanish, Hindi, Portuguese, French, German, Japanese, Arabic, Korean, 
Indonesian, Italian, Dutch, Turkish, Polish, Swedish, Filipino, Malay, Romanian, Ukrainian, 
Greek, Czech, Danish, Finnish, Bulgarian, Croatian, Slovak, and Tamil.
""")

# Get available voices
voices = tts.get_voices()

# Input fields
text_input = st.text_area(
    "Input Text",
    value="",
)

voice_name = st.selectbox("Voice", list(voices.keys()))

# Generate button
if st.button("Generate Voice"):
    try:
        with st.spinner("Generating audio..."):
            # Get the voice ID for the selected voice name
            voice_id = voices[voice_name]
            
            # Generate audio
            audio_data = tts.generate_audio(
                text=text_input,
                voice=voice_id
            )
            
            # Create columns for audio player and download button
            col1, col2 = st.columns([3, 1])
            
            # Play the audio
            with col1:
                st.audio(audio_data, format="audio/mp3")
            
            # Download button with timestamp for sequential naming
            with col2:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="Download Audio",
                    data=audio_data,
                    file_name=f"{timestamp}_elevenlabs_tts_{voice_name}.mp3",
                    mime="audio/mp3"
                )
                
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
