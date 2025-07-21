from gtts import gTTS
import os
from datetime import datetime

def speak_text(text: str, audio_dir: str = None) -> str | None:
    """
    Convert text to speech and save as an MP3 file.
    Returns the file path if successful, else None.
    """
    if not text:
        return None
    try:
        if audio_dir is None:
            audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "audio")
        os.makedirs(audio_dir, exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d%H%M%S%f") + ".mp3"
        file_path = os.path.join(audio_dir, filename)
        tts = gTTS(text)
        tts.save(file_path)
        return file_path
    except Exception as e:
        import logging
        logging.exception("Error in speak_text")
        return None
