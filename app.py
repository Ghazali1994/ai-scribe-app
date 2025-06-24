import streamlit as st
from whisper_transcribe import transcribe_audio
from local_soap_generator import generate_soap_note_ollama
import tempfile

st.title("🩺 AI Scribe: Voice to SOAP Note")

audio_file = st.file_uploader("Upload doctor's voice note (.mp3/.wav)", type=["mp3", "wav"])

if audio_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    st.info("🔊 Transcribing audio...")
    raw_text = transcribe_audio(tmp_path)
    st.success("✅ Transcription Complete")
    st.text_area("📝 Transcribed Text", raw_text, height=150)

    if st.button("✍️ Generate SOAP Note"):
        st.info("🧠 Generating SOAP Note (via Ollama)...")
        soap_note = generate_soap_note_ollama(raw_text)
        st.success("📋 SOAP Note Ready")
        st.text_area("📄 SOAP Note", soap_note, height=250)
        st.download_button("📥 Download Note", soap_note, file_name="soap_note.txt")
