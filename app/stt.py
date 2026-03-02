from transformers import pipeline

asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base"
)

def transcribe(audio_path: str) -> str:
    result = asr(audio_path)
    return result["text"]