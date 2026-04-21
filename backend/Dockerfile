FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for audio and building packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything into the container
COPY . .

# Pre-download the model into the image layers during build
# This makes subsequent starts/warmups nearly instant
RUN python download_model.py

# Hugging Face Spaces run on port 7860 by default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
