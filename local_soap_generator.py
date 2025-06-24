import subprocess

def generate_soap_note_ollama(raw_text, model_name="mistral"):
    prompt = f"""
You are a medical scribe. Convert the following into a SOAP note:

{raw_text}

Format as:
Subjective:
Objective:
Assessment:
Plan:
"""
    result = subprocess.run(
        ["C:\Users\LPTP13\AppData\Local\Programs\Ollama\ollama.exe", "run", model_name],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return result.stdout.decode("utf-8").strip()
