"""Content-addressed local artifact storage."""

from __future__ import annotations

import mimetypes
import os
import stat
from pathlib import Path
from typing import Any

from .canonical import atomic_write, canonical_bytes, sha256_bytes
from .domain import ArtifactReference, IntegrityViolation


class ArtifactStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, digest: str) -> Path:
        if len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        ):
            raise ValueError("invalid SHA-256 digest")
        return self.root / digest[:2] / digest[2:]

    @staticmethod
    def _read_regular(path: Path) -> bytes:
        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(path, flags)
        except OSError as error:
            raise IntegrityViolation(
                f"artifact is missing or unsafe: {path.name}"
            ) from error
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise IntegrityViolation(
                    f"artifact must be a single-linked regular file: {path.name}"
                )
            chunks = []
            while chunk := os.read(descriptor, 1024 * 1024):
                chunks.append(chunk)
            return b"".join(chunks)
        finally:
            os.close(descriptor)

    def put_bytes(
        self, logical_name: str, data: bytes, media_type: str
    ) -> ArtifactReference:
        digest = sha256_bytes(data)
        destination = self.path_for(digest)
        if destination.exists():
            if self._read_regular(destination) != data:
                raise IntegrityViolation(
                    f"digest collision or corrupted artifact: {digest}"
                )
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.parent.is_symlink() or not destination.parent.is_dir():
                raise IntegrityViolation("artifact digest prefix is unsafe")
            atomic_write(destination, data, mode=0o400)
        return ArtifactReference(
            sha256=digest,
            size=len(data),
            media_type=media_type,
            logical_name=logical_name,
        )

    def put_json(self, logical_name: str, value: Any) -> ArtifactReference:
        return self.put_bytes(
            logical_name, canonical_bytes(value) + b"\n", "application/json"
        )

    def put_file(
        self, logical_name: str, source: Path, media_type: str | None = None
    ) -> ArtifactReference:
        inferred = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
        return self.put_bytes(
            logical_name, self._read_regular(source), media_type or inferred
        )

    def read_verified(self, digest: str) -> bytes:
        path = self.path_for(digest)
        data = self._read_regular(path)
        if sha256_bytes(data) != digest:
            raise IntegrityViolation(f"artifact digest mismatch: {digest}")
        return data

    def verify_all(self) -> list[str]:
        verified: list[str] = []
        for prefix in sorted(self.root.iterdir()):
            if prefix.is_symlink() or not prefix.is_dir() or len(prefix.name) != 2:
                raise IntegrityViolation(f"unexpected artifact entry: {prefix}")
            for path in sorted(prefix.iterdir()):
                digest = prefix.name + path.name
                self.read_verified(digest)
                verified.append(digest)
        return verified
