import streamlit as st
from audiorecorder import audiorecorder
import tempfile
import uuid
import os

from whisper_transcribe import transcribe_audio
from local_soap_generator import generate_soap_note_ollama

st.set_page_config(page_title="AI Scribe", page_icon="🩺")
st.title("🩺 AI Scribe: Doctor Voice to SOAP Note")

st.subheader("🎙️ Record Doctor's Voice or Upload Audio")

# --- 🎙️ Record from microphone ---
audio = audiorecorder("🔴 Start Recording", "⏹️ Stop Recording")

# --- 📁 Optional file upload ---
uploaded_file = st.file_uploader("Or upload a .wav or .mp3 file", type=["wav", "mp3"])

audio_path = None

if audio and len(audio) > 0:
    # Save mic recording to temp file
    audio_filename = f"{uuid.uuid4()}.wav"
    with open(audio_filename, "wb") as f:
        f.write(audio.tobytes())
    audio_path = audio_filename
    st.audio(audio_path, format="audio/wav")
    st.success("🎧 Voice recorded successfully")

elif uploaded_file:
    # Save uploaded file to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name
    st.audio(audio_path)
    st.success("📁 Audio uploaded")

# --- 🔄 Process audio if available ---
if audio_path:
    st.divider()
    st.subheader("📝 Transcribe & Generate SOAP Note")

    if st.button("🔍 Transcribe & Summarize"):
        st.info("Transcribing with Whisper...")
        raw_text = transcribe_audio(audio_path)
        st.success("📝 Transcription Complete")
        st.text_area("Transcript", raw_text, height=150)

        st.info("Generating SOAP Note with Ollama...")
        soap_note = generate_soap_note_ollama(raw_text)
        st.success("📋 SOAP Note Ready")
        st.text_area("SOAP Note", soap_note, height=250)
        st.download_button("📥 Download SOAP", soap_note, file_name="soap_note.txt")

        # Optionally remove temporary file
        if audio and len(audio) > 0:
            os.remove(audio_path)
