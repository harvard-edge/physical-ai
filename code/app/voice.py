"""Offline Piper speech for the robot-native app."""
from __future__ import annotations

import os
import tempfile
import threading
import wave
from pathlib import Path
from typing import Any


class VoiceUnavailable(RuntimeError):
    """Raised when the local Piper voice cannot synthesize speech."""


class PiperVoiceSynthesizer:
    """Load one Piper model lazily and turn short replies into WAV files."""

    def __init__(self, model_path: Path | str | None = None) -> None:
        configured_path = os.environ.get("MAYAS_REACHY_PIPER_MODEL")
        self.model_path = Path(
            model_path
            or configured_path
            or (
                Path.home()
                / ".local"
                / "share"
                / "mayas-reachy"
                / "voices"
                / "en_US-lessac-low.onnx"
            )
        ).expanduser()
        self._voice: Any | None = None
        self._lock = threading.Lock()

    @property
    def configured(self) -> bool:
        return self.model_path.is_file() and Path(
            f"{self.model_path}.json"
        ).is_file()

    def synthesize(self, text: str) -> Path:
        """Synthesize one reply locally and return its temporary WAV path."""
        if not self.configured:
            raise VoiceUnavailable(f"Piper voice is missing at {self.model_path}")

        with self._lock:
            self._load_voice()

            handle = tempfile.NamedTemporaryFile(
                prefix="mayas-reachy-", suffix=".wav", delete=False
            )
            output_path = Path(handle.name)
            handle.close()
            try:
                with wave.open(str(output_path), "wb") as wav_file:
                    self._voice.synthesize_wav(text[:300], wav_file)
            except Exception as exc:
                output_path.unlink(missing_ok=True)
                raise VoiceUnavailable(f"Piper could not synthesize speech: {exc}") from exc
            return output_path

    def warm_up(self) -> None:
        """Load the model early so the first child does not pay that delay."""
        if not self.configured:
            return
        with self._lock:
            self._load_voice()

    def _load_voice(self) -> None:
        if self._voice is not None:
            return
        try:
            from piper import PiperVoice

            self._voice = PiperVoice.load(str(self.model_path))
        except Exception as exc:
            raise VoiceUnavailable(f"Could not load Piper voice: {exc}") from exc
