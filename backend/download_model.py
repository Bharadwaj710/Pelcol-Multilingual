import os
from faster_whisper import WhisperModel

# Pre-download both models to the cache so they are part of the Docker image
model_size = os.getenv("WHISPER_MODEL_SIZE", "base")
print(f"Pre-downloading Whisper model: {model_size}...")
WhisperModel(model_size, device="cpu", compute_type="int8")
print("Download complete!")
