from gtts import gTTS
import os

def synthesize(text: str, output_path: str):
    tts = gTTS(text=text, lang="en")
    tts.save(output_path)