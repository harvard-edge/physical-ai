"""The LLM-driven teach-and-talk policy between interface and memory."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from .cloud import CloudUnavailable, GroqCloud
from .memory import MemoryStore


@dataclass(frozen=True)
class ResponsePlan:
    text: str
    mood: str
    source: str
    learned: dict[str, str] | None = None


class Conversation:
    """Let the LLM understand language, then validate what may be persisted."""

    def __init__(self, memory: MemoryStore, cloud: GroqCloud) -> None:
        self.memory = memory
        self.cloud = cloud
        self.history: list[dict[str, str]] = []

    def respond(self, user_text: str) -> ResponsePlan:
        text = user_text.strip()
        robot_name = self.memory.robot_name()
        if not self.cloud.configured:
            response = self._offline_response(robot_name, configured=False)
            self._remember_turn(text, response)
            return ResponsePlan(response, "warm", "offline-fallback")

        try:
            result = self.cloud.analyze_turn(
                text,
                robot_name=robot_name,
                history=self.history,
            )
        except CloudUnavailable as exc:
            logging.getLogger(__name__).warning("Cloud turn unavailable: %s", exc)
            response = self._offline_response(robot_name, configured=True)
            self._remember_turn(text, response)
            return ResponsePlan(response, "warm", "offline-fallback")

        learned = None
        if result.get("intent") == "teach_robot_name":
            taught_name = self._valid_robot_name(result.get("robot_name"))
            if taught_name is not None:
                self.memory.remember_robot_name(taught_name)
                learned = {"robot_name": taught_name}

        response = result["reply"]
        self._remember_turn(text, response)
        return ResponsePlan(
            response,
            result["mood"],
            "groq-cloud",
            learned=learned,
        )

    def _remember_turn(self, user_text: str, response: str) -> None:
        # Conversation context stays in RAM. Only explicitly taught facts are persisted.
        self.history.extend(
            [
                {"role": "user", "content": user_text[:500]},
                {"role": "assistant", "content": response[:200]},
            ]
        )
        self.history = self.history[-12:]

    @staticmethod
    def _offline_response(robot_name: str | None, *, configured: bool) -> str:
        if configured:
            return "My cloud brain had trouble answering just now. Please try again."
        if robot_name:
            return f"I heard you! I'm {robot_name}, and my cloud brain is resting right now."
        return "My cloud brain needs its Groq key before I can understand what you teach me."

    @staticmethod
    def _valid_robot_name(value: object) -> str | None:
        """Validate the LLM's extracted value without interpreting the sentence."""
        if not isinstance(value, str):
            return None
        name = value.strip()
        if not 1 <= len(name) <= 24:
            return None
        if not name[0].isalpha():
            return None
        if any(not (char.isalnum() or char in "-' ") for char in name):
            return None
        return name[0].upper() + name[1:]
