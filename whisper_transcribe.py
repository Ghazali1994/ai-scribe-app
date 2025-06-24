from faster_whisper import WhisperModel
from pydub import AudioSegment
import tempfile
import os

model = WhisperModel("base", compute_type="int8")

def transcribe_audio(file_path):
    # Convert to WAV with pydub (optional: helps with format issues)
    audio = AudioSegment.from_file(file_path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        audio.export(tmp_wav.name, format="wav")
        clean_path = tmp_wav.name

    segments, _ = model.transcribe(clean_path)
    text = " ".join(segment.text for segment in segments)

    os.unlink(clean_path)  # Clean up
    return text.strip()
