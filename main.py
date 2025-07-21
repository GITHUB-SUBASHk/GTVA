from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from app.tts import speak_text

app = FastAPI()

# Allow cross-origin requests (needed for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directory for audio output
BASE_DIR = os.path.dirname(__file__)
STATIC_AUDIO_PATH = os.path.join(BASE_DIR, "static", "audio")
os.makedirs(STATIC_AUDIO_PATH, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("frontend/index.html")

@app.post("/speak")
async def speak(request: Request):
    try:
        data = await request.json()
        gesture = data.get("gesture", "")
        file_path = speak_text(gesture, audio_dir=STATIC_AUDIO_PATH)
        if file_path:
            return {
                "audio_url": f"/static/audio/{os.path.basename(file_path)}",
                "gesture": gesture
            }
        return JSONResponse({"error": "Invalid gesture"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
