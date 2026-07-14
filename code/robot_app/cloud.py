"""Optional Groq free-tier language-understanding adapter."""
from __future__ import annotations

import json
import os
import secrets
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
_ENV_API_KEY = object()


def configured_api_key() -> str | None:
    """Load the key from the process environment or a private app config file."""
    value = os.environ.get("GROQ_API_KEY", "").strip()
    if value:
        return value
    configured_path = os.environ.get("GROQ_API_KEY_FILE")
    path = (
        Path(configured_path).expanduser()
        if configured_path
        else Path.home() / ".config" / "mayas-reachy" / "groq_api_key"
    )
    try:
        return path.read_text(encoding="utf-8").strip() or None
    except (FileNotFoundError, PermissionError, OSError):
        return None


class CloudUnavailable(RuntimeError):
    """Raised when optional cloud intelligence cannot answer."""


class GroqCloud:
    """Minimal HTTPS client so the robot app needs no extra cloud SDK."""

    def __init__(self, api_key: str | None | object = _ENV_API_KEY) -> None:
        self.api_key = configured_api_key() if api_key is _ENV_API_KEY else api_key
        self.chat_model = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")
        self.transcription_model = os.environ.get(
            "GROQ_TRANSCRIPTION_MODEL", "whisper-large-v3-turbo"
        )

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def analyze_turn(
        self,
        user_text: str,
        *,
        robot_name: str | None,
        history: list[dict[str, str]],
        memory_context: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Use one LLM turn to understand, extract memory, and write the reply."""
        name_context = (
            f"Maya and Alexander taught you that your name is {robot_name}."
            if robot_name
            else "You do not have a name yet."
        )
        system = (
            "You are the language-understanding layer for a small Reachy Mini robot "
            "that children Maya and Alexander teach. Analyze the child's natural language, "
            "extract explicitly taught knowledge, and write the robot's reply. "
            f"{name_context} Set intent to teach_robot_name only when the child clearly "
            "assigns the robot a name. Never infer a name from a greeting, a person's name, "
            "or an example. Otherwise set robot_name to null. Extract only claims directly "
            "stated by the child; do not turn guesses into facts. Use only the allowed "
            "predicates. Do not duplicate the robot-name assignment in claims. Resolve "
            "pronouns conservatively. Be warm, playful, truthful, "
            "and brief. The reply must use at most two short sentences and 45 words. "
            "Never ask for private information or invent a memory."
        )
        if memory_context:
            system += " Relevant validated memories: " + json.dumps(memory_context[:8])
        messages: list[dict[str, str]] = [{"role": "system", "content": system}]
        messages.extend(history[-6:])
        messages.append({"role": "user", "content": user_text[:500]})
        schema = {
            "type": "object",
            "properties": {
                "intent": {
                    "type": "string",
                    "enum": [
                        "teach_robot_name",
                        "ask_robot_name",
                        "greeting",
                        "conversation",
                    ],
                },
                "robot_name": {"type": ["string", "null"]},
                "reply": {"type": "string"},
                "mood": {
                    "type": "string",
                    "enum": ["curious", "excited", "friendly", "warm"],
                },
                "entities": {
                    "type": "array",
                    "maxItems": 8,
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "kind": {"type": "string", "enum": ["person", "robot", "animal", "place", "object", "concept"]},
                        },
                        "required": ["id", "name", "kind"],
                        "additionalProperties": False,
                    },
                },
                "claims": {
                    "type": "array",
                    "maxItems": 8,
                    "items": {
                        "type": "object",
                        "properties": {
                            "subject": {"type": "string"},
                            "predicate": {"type": "string", "enum": [
                                "is_a", "part_of", "has_property", "likes", "dislikes",
                                "knows", "named", "located_in", "created_by", "related_to",
                                "can_do", "interested_in"
                            ]},
                            "object": {"type": "string"},
                            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        },
                        "required": ["subject", "predicate", "object", "confidence"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["intent", "robot_name", "reply", "mood", "entities", "claims"],
            "additionalProperties": False,
        }
        data = self._request_json(
            "/chat/completions",
            {
                "model": self.chat_model,
                "messages": messages,
                "temperature": 0.4,
                "max_completion_tokens": 768,
                "reasoning_effort": "low",
                "reasoning_format": "hidden",
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "mayas_reachy_turn",
                        "strict": True,
                        "schema": schema,
                    },
                },
            },
        )
        try:
            content = data["choices"][0]["message"]["content"]
            result = json.loads(content)
        except (KeyError, IndexError, TypeError, AttributeError) as exc:
            raise CloudUnavailable("Groq returned an unexpected chat response") from exc
        except json.JSONDecodeError as exc:
            raise CloudUnavailable("Groq returned invalid structured output") from exc

        if not isinstance(result, dict):
            raise CloudUnavailable("Groq returned an unexpected structured output")
        required = {"intent", "robot_name", "reply", "mood", "entities", "claims"}
        if set(result) != required or not isinstance(result.get("reply"), str):
            raise CloudUnavailable("Groq output did not match the turn schema")
        result["reply"] = result["reply"].strip()[:200]
        return result

    def transcribe(self, audio: bytes, *, filename: str = "speech.wav") -> str:
        """Transcribe one short audio clip with Groq Whisper."""
        if not audio:
            raise CloudUnavailable("No microphone audio was captured")
        if len(audio) > 10 * 1024 * 1024:
            raise CloudUnavailable("The microphone recording is too large")

        boundary = f"mayas-reachy-{secrets.token_hex(12)}"
        fields = {
            "model": self.transcription_model,
            "response_format": "json",
            "language": "en",
        }
        body = bytearray()
        for name, value in fields.items():
            body.extend(f"--{boundary}\r\n".encode())
            body.extend(
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
            )
            body.extend(value.encode())
            body.extend(b"\r\n")
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            (
                f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
                "Content-Type: audio/wav\r\n\r\n"
            ).encode()
        )
        body.extend(audio)
        body.extend(f"\r\n--{boundary}--\r\n".encode())

        raw = self._request_raw(
            "/audio/transcriptions",
            bytes(body),
            content_type=f"multipart/form-data; boundary={boundary}",
        )
        try:
            parsed = json.loads(raw)
            text = parsed["text"].strip()
        except (json.JSONDecodeError, KeyError, TypeError, AttributeError) as exc:
            raise CloudUnavailable("Groq returned an invalid transcription") from exc
        if not text:
            raise CloudUnavailable("I could not hear any words")
        return text[:500]

    def _request_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        raw = self._request_bytes(path, payload)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise CloudUnavailable("Groq returned invalid JSON") from exc
        if not isinstance(parsed, dict):
            raise CloudUnavailable("Groq returned an unexpected response")
        return parsed

    def _request_bytes(self, path: str, payload: dict[str, Any]) -> bytes:
        return self._request_raw(
            path,
            json.dumps(payload).encode("utf-8"),
            content_type="application/json",
        )

    def _request_raw(self, path: str, data: bytes, *, content_type: str) -> bytes:
        if not self.api_key:
            raise CloudUnavailable("GROQ_API_KEY is not configured")
        request = urllib.request.Request(
            GROQ_BASE_URL + path,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": content_type,
                "User-Agent": "mayas-reachy/0.1",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read(300).decode("utf-8", errors="replace")
            raise CloudUnavailable(f"Groq request failed ({exc.code}): {detail}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise CloudUnavailable(f"Groq is unreachable: {exc}") from exc
