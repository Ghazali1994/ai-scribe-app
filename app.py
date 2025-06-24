from audiorecorder import audiorecorder
import os
import uuid

# Existing imports...
from whisper_transcribe import transcribe_audio
from local_soap_generator import generate_soap_note_ollama

st.title("🩺 AI Scribe: Voice to SOAP Note")

# 🎤 Step 1: Record or Upload Audio
st.subheader("🎙️ Record Doctor's Voice")

audio = audiorecorder("Click to record", "Recording... Speak now...")

uploaded_file = st.file_uploader("Or upload an audio file (.mp3/.wav)", type=["mp3", "wav"])

# Handle microphone recording
if audio and len(audio) > 0:
    audio_filename = f"{uuid.uuid4()}.wav"
    with open(audio_filename, "wb") as f:
        f.write(audio.tobytes())
    audio_path = audio_filename
    st.audio(audio_path)
    source = "microphone"
elif uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name
    st.audio(audio_path)
    source = "uploaded"
else:
    audio_path = None

# 🎯 Step 2: Transcribe and Generate SOAP Note
if audio_path:
    st.info("🔊 Transcribing...")
    raw_text = transcribe_audio(audio_path)
    st.success("📝 Transcription Complete")
    st.text_area("📄 Transcribed Text", raw_text, height=150)

    if st.button("✍️ Generate SOAP Note"):
        st.info("🧠 Generating with Ollama...")
        soap_note = generate_soap_note_ollama(raw_text)
        st.success("✅ SOAP Note Ready")
        st.text_area("🗒️ SOAP Note", soap_note, height=250)
        st.download_button("📥 Download SOAP", soap_note, file_name="soap_note.txt")
