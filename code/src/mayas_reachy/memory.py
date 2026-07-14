"""Small, inspectable, on-robot memory for the first teaching loop."""
from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any


def default_memory_path() -> Path:
    """Choose persistent app data outside the installed Python package."""
    override = os.environ.get("MAYAS_REACHY_MEMORY_FILE")
    if override:
        return Path(override).expanduser()
    data_home = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return data_home / "mayas-reachy" / "memory.json"


class MemoryStore:
    """Thread-safe JSON memory that can be opened and explained to a child."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_memory_path()
        self._lock = threading.Lock()

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return self._read_unlocked()

    def robot_name(self) -> str | None:
        robot = self.snapshot().get("robot", {})
        name = robot.get("name") if isinstance(robot, dict) else None
        return name if isinstance(name, str) and name else None

    def remember_robot_name(self, name: str) -> dict[str, Any]:
        """Persist a newly taught robot name with minimal provenance."""
        with self._lock:
            data = self._read_unlocked()
            data["robot"] = {
                "name": name,
                "learned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source": "family web chat",
            }
            self._write_unlocked(data)
            return data

    def _read_unlocked(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"version": 1, "robot": {}}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"version": 1, "robot": {}}
        return data if isinstance(data, dict) else {"version": 1, "robot": {}}

    def _write_unlocked(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, self.path)
