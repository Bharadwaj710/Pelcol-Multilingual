from functools import lru_cache
from pathlib import Path
from threading import Lock

from faster_whisper import WhisperModel

from app.config import settings

_transcribe_lock = Lock()
_SHORT_HALLUCINATIONS = {
    "thank you",
    "thanks for watching",
    "subscribe",
    "follow",
    "follow follow follow",
    "i'll hold you",
}


@lru_cache(maxsize=1)
def get_model() -> WhisperModel:
    return WhisperModel(
        settings.model_size,
        device=settings.device,
        compute_type=settings.compute_type,
    )


def warmup_model() -> dict:
    get_model()
    return {
        "status": "ready",
        "model_size": settings.model_size,
        "device": settings.device,
        "compute_type": settings.compute_type,
    }


def transcribe_audio_file(audio_path: Path, language: str | None = None) -> dict:
    with _transcribe_lock:
        segments, info = get_model().transcribe(
            str(audio_path),
            language=language or None,
            task="transcribe",
            vad_filter=True,
            vad_parameters={
                "min_silence_duration_ms": 700,
                "speech_pad_ms": 300,
            },
            beam_size=1,
            condition_on_previous_text=False,
        )

        segment_list = list(segments)
        text = " ".join(segment.text.strip() for segment in segment_list if segment.text.strip())
        normalized = " ".join(text.lower().replace(".", "").replace(",", "").split())
        no_speech_values = [
            getattr(segment, "no_speech_prob", 0)
            for segment in segment_list
            if getattr(segment, "no_speech_prob", None) is not None
        ]
        avg_no_speech_prob = (
            sum(no_speech_values) / len(no_speech_values)
            if no_speech_values
            else 0
        )
        skipped = None

        if not text:
            skipped = "no speech detected"
        elif normalized in _SHORT_HALLUCINATIONS and avg_no_speech_prob > 0.35:
            text = ""
            skipped = "likely silence hallucination"

        return {
            "text": text,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "no_speech_probability": avg_no_speech_prob,
            "skipped": skipped,
        }
