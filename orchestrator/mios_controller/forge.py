"""Offline forge manifests. No GitHub adapter is present in Phase 1A."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .canonical import atomic_write, canonical_bytes


class LocalForge:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, experiment_id: str, name: str, manifest: dict[str, Any]) -> Path:
        if "/" in name or ".." in name:
            raise ValueError("manifest name must be a basename")
        destination = self.root / experiment_id / f"{name}.json"
        atomic_write(destination, canonical_bytes(manifest) + b"\n", mode=0o600)
        return destination
