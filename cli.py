#!/usr/bin/env python3
"""Root entrypoint for Physical AI CLI (psyai / pai)."""
import sys
from pathlib import Path

# Add repo root to sys.path
repo_root = Path(__file__).resolve().parent
sys.path.insert(0, str(repo_root))

from cli.main import main

if __name__ == "__main__":
    main()
