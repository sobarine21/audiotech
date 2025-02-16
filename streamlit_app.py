import streamlit as st
import requests
import random
from transformers import pipeline

# Set up Hugging Face API details
API_URLS = [
    "https://api-inference.huggingface.co/models/openai/whisper-small",
    "https://api-inference.huggingface.co/models/facebook/seamless-m4t-v2-large",
    "https://api-inference.huggingface.co/models/openai/whisper-large-v2",
    "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
]

# Retrieve Hugging Face API token from Streamlit secrets
API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Function to send the audio file to a random API
def transcribe_audio(file):
    try:
        # Select a random API URL from the list
        api_url = random.choice(API_URLS)
        
        # Read the file as binary
        data = file.read()
        response = requests.post(api_url, headers=HEADERS, data=data)
        if response.status_code == 200:
            return response.json()  # Return transcription
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
st.title("🎙️ Audio Transcription Web App")
st.write("Upload an audio file, and this app will transcribe it using various models via Hugging Face API.")

# File uploader
uploaded_file = st.file_uploader("Upload your audio file (e.g., .wav, .flac, .mp3)", type=["wav", "flac", "mp3"])

if uploaded_file is not None:
    # Display uploaded audio
    st.audio(uploaded_file, format="audio/mp3", start_time=0)
    st.info("Transcribing audio... Please wait.")
    
    # Transcribe the uploaded audio file
    result = transcribe_audio(uploaded_file)
    
    # Display the result
    if "text" in result:
        st.success("Transcription Complete:")
        st.write(result["text"])
        
        # Add download button
        transcription_text = result["text"]
        st.download_button(
            label="Download Transcription",
            data=transcription_text,
            file_name="transcription.txt",
            mime="text/plain"
        )
    elif "error" in result:
        st.error(f"Error: {result['error']}")
    else:
        st.warning("Unexpected response from the API.")

# Use a pipeline as a high-level helper
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large")
``` ▋
