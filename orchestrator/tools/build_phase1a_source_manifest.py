"""Freeze the exact source scope used to generate Phase 1A evidence."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tools.evidence_common import MANIFEST_PATH, build_source_manifest, canonical
except ModuleNotFoundError:
    from evidence_common import MANIFEST_PATH, build_source_manifest, canonical


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()
    output = args.output or repository / MANIFEST_PATH
    manifest = build_source_manifest(repository)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical(manifest) + b"\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
