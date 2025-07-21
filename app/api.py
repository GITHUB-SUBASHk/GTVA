from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.tts import speak_text
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Get absolute path for static/audio
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")
AUDIO_DIR = os.path.join(STATIC_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Mount static files for serving audio
# Serve audio
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve CSS and JS
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.post("/speak", response_model=dict)
async def speak(request: Request):
    """Convert gesture text to speech and return audio file URL."""
    import logging
    try:
        data = await request.json()
        gesture = data.get("gesture", "")
        # Pass absolute audio dir to speak_text
        file_path = speak_text(gesture, audio_dir=AUDIO_DIR)
        if file_path:
            return JSONResponse({
                "audio_url": f"/static/audio/{os.path.basename(file_path)}",
                "gesture": gesture
            })
        return JSONResponse({"error": "Invalid gesture"}, status_code=400)
    except Exception as e:
        logging.exception("Error in /speak endpoint")
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/", include_in_schema=False)
def read_index():
    return FileResponse("frontend/index.html")
