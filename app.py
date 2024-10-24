import streamlit as st
import speech_recognition as sr
from textblob import TextBlob
import os


# Function to transcribe audio to text
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text


# Function to extract features from text
def analyze_emotion(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    # Classify sentiment into emotions
    if sentiment > 0:
        return "happy"
    elif sentiment < 0:
        return "angry"
    else:
        return "neutral"


# Streamlit web interface
st.title("VocalVibes: Audio Emotion Analyzer")
st.write("Upload a WAV audio file to transcribe and analyze its emotional content.")

# File upload section for WAV file
uploaded_file = st.file_uploader("Choose a WAV file", type="wav")

if uploaded_file is not None:
    # Save the file to a temporary location
    temp_file_path = os.path.join("temp", uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Transcribe the uploaded audio file
    st.write("Transcribing the audio...")
    try:
        transcription = transcribe_audio(temp_file_path)
        st.subheader("Transcribed Text")
        st.write(transcription)
        
        # Analyze emotion from the transcription
        st.write("Analyzing emotion...")
        emotion = analyze_emotion(transcription)
        
        # Display emotion analysis
        st.subheader("Detected Emotion")
        st.write(f"The emotion in the conversation is: **{emotion.capitalize()}**")

    except Exception as e:
        st.error(f"An error occurred during transcription or analysis: {str(e)}")

# Footer
st.write("---")
st.write("Made with ❤️ using Streamlit")
