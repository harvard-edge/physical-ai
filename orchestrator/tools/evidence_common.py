"""Shared source-identity helpers for Phase 1A evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


MANIFEST_PATH = Path("evaluation/manifests/phase1a-source.json")
SOURCE_ROOTS = (
    Path("code"),
    Path("governance"),
    Path("protocol"),
    Path("evolution/approvals"),
    Path("evolution/decisions"),
    Path("evolution/fixtures"),
    Path("orchestrator/mios_controller"),
    Path("orchestrator/tests"),
    Path("orchestrator/tools"),
)
SOURCE_FILES = (
    Path("docs/MIOS-DESIGN-REVIEW.md"),
    Path("docs/MIOS-EMBODIED-BOOTSTRAP-GOAL.md"),
    Path("evaluation/manifests/phase0-baseline.yml"),
    Path("evolution/reports/PHASE-1A-SUBSTRATE-BAKEOFF.md"),
    Path("orchestrator/README.md"),
    Path("orchestrator/pyproject.toml"),
    Path("orchestrator/uv.lock"),
)
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", ".ruff_cache"}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_entries(repository: Path) -> list[dict[str, Any]]:
    repository = repository.resolve()
    paths: set[Path] = set()
    for relative_root in SOURCE_ROOTS:
        root = repository / relative_root
        if not root.is_dir() or root.is_symlink():
            raise RuntimeError(f"source root is missing or unsafe: {relative_root}")
        for path in root.rglob("*"):
            relative = path.relative_to(repository)
            if any(part in EXCLUDED_PARTS for part in relative.parts):
                continue
            if "assets" in relative.parts and "cache" in relative.parts:
                continue
            if path.is_symlink():
                raise RuntimeError(f"source manifest rejects symlink: {relative}")
            if path.is_file() and path.suffix != ".pyc":
                paths.add(relative)
    for relative in SOURCE_FILES:
        path = repository / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"source file is missing or unsafe: {relative}")
        paths.add(relative)

    entries = []
    for relative in sorted(paths, key=lambda item: item.as_posix()):
        data = (repository / relative).read_bytes()
        entries.append(
            {
                "path": relative.as_posix(),
                "sha256": sha256(data),
                "size": len(data),
            }
        )
    return entries


def build_source_manifest(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    ).stdout.strip()
    entries = source_entries(repository)
    return {
        "schema_version": "1.0.0",
        "evidence_kind": "phase1a_source_manifest",
        "base_commit": head,
        "source_tree_digest": sha256(canonical(entries)),
        "file_count": len(entries),
        "files": entries,
    }


def source_reference(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    path = repository / MANIFEST_PATH
    raw = path.read_bytes()
    manifest = json.loads(raw)
    current_entries = source_entries(repository)
    if manifest.get("files") != current_entries:
        raise RuntimeError(
            "Phase 1A source changed after the source manifest was frozen"
        )
    current_tree_digest = sha256(canonical(current_entries))
    if manifest.get("source_tree_digest") != current_tree_digest:
        raise RuntimeError("Phase 1A source-tree digest is invalid")
    if manifest.get("file_count") != len(current_entries):
        raise RuntimeError("Phase 1A source-manifest file count is invalid")
    return {
        "manifest_path": MANIFEST_PATH.as_posix(),
        "manifest_sha256": sha256(raw),
        "source_tree_digest": current_tree_digest,
        "base_commit": manifest["base_commit"],
    }
