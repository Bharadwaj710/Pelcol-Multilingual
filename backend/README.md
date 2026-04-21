# Backend

FastAPI service that accepts short audio chunks and transcribes them with `faster-whisper`.

## Run Locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

## Configuration

```bash
set WHISPER_MODEL_SIZE=base
set WHISPER_DEVICE=cpu
set WHISPER_COMPUTE_TYPE=int8
set CORS_ORIGINS=http://localhost:5173
set HF_TOKEN=your_huggingface_token_optional
```

The first transcription downloads the model from Hugging Face. `HF_TOKEN` is optional for public models, but it avoids unauthenticated rate limits and can make downloads more reliable.

Use `base` for the default demo. Use `tiny` only for very low-resource machines. Use `small` or `medium` for better Hindi-English accuracy.
