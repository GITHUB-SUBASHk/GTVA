
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.tts import speak_text
import os

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files for audio
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")
AUDIO_DIR = os.path.join(STATIC_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve frontend (index.html, style.css, script.js)
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.post("/speak")
async def speak(request: Request):
    try:
        data = await request.json()
        gesture = data.get("gesture", "")
        file_path = speak_text(gesture, audio_dir=AUDIO_DIR)
        if file_path:
            return JSONResponse({
                "audio_url": f"/static/audio/{os.path.basename(file_path)}",
                "gesture": gesture
            })
        return JSONResponse({"error": "Invalid gesture"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
