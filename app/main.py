from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid

from app.stt import transcribe
from app.llm import generate_response
from app.tts import synthesize
from app.database import save_conversation

# --------------------------------------------------
# Create App
# --------------------------------------------------

app = FastAPI(title="Voice AI Assistant")

# --------------------------------------------------
# CORS (restrict in production)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://voice-ai-frontend-chi.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# Audio directory setup
# --------------------------------------------------

AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
def health():
    return {"status": "Backend running"}

@app.post("/voice")
async def voice_chat(file: UploadFile = File(...)):
    unique_id = str(uuid.uuid4())

    input_path = os.path.join(AUDIO_DIR, f"{unique_id}_input.wav")
    output_path = os.path.join(AUDIO_DIR, f"{unique_id}_response.mp3")

    # Save file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("STEP 1: File saved")

    # STT
    print("STEP 2: STT starting")
    user_text = transcribe(input_path)
    print("STT RESULT:", user_text)

    # LLM
    print("STEP 3: LLM starting")
    ai_response = generate_response(user_text)
    print("LLM RESULT:", ai_response)

    # TTS
    print("STEP 4: TTS starting")
    synthesize(ai_response, output_path)
    print("TTS DONE")

    # DB
    print("STEP 5: DB saving")
    save_conversation(user_text, ai_response)
    print("DB DONE")

    return {
        "transcript": user_text,
        "response": ai_response,
        "audio_url": f"/audio/{unique_id}_response.mp3"

    }
