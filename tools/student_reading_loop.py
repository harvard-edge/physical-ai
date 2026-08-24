#!/usr/bin/env python3
"""Student Reading & Section-by-Section Improvement Loop for Physical AI.

This module indexes every chapter in `book/chapters/` into its exact H2 sections,
calculating precise line number ranges (StartLine to EndLine) and formatting
targeted inspection prompts for student reader personas (Maya, Carlos, Alex).
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class SectionSpec:
    chapter_num: int
    chapter_dir: str
    chapter_file: str
    section_index: int
    section_title: str
    start_line: int
    end_line: int
    line_count: int


def discover_all_sections(book_root: Path) -> List[SectionSpec]:
    """Scan all chapter qmd files and extract H2 sections with line boundaries."""
    chapter_files = sorted(glob.glob(str(book_root / "chapters" / "*" / "*.qmd")))
    all_sections: List[SectionSpec] = []

    for fpath in chapter_files:
        p = Path(fpath)
        dir_name = p.parent.name
        # Match chapter number prefix e.g. '01-boundary' -> 1
        m = re.match(r"^(\d+)-", dir_name)
        if not m:
            continue
        ch_num = int(m.group(1))

        with open(p, "r", encoding="utf-8") as fp:
            lines = fp.readlines()

        h2_indices = []
        for idx, line in enumerate(lines):
            if line.startswith("## "):
                title = line.strip()[3:].strip()
                h2_indices.append((idx + 1, title))

        for s_idx, (start_l, title) in enumerate(h2_indices):
            if s_idx + 1 < len(h2_indices):
                end_l = h2_indices[s_idx + 1][0] - 1
            else:
                end_l = len(lines)

            # Trim trailing blank lines from section
            while end_l > start_l and not lines[end_l - 1].strip():
                end_l -= 1

            all_sections.append(
                SectionSpec(
                    chapter_num=ch_num,
                    chapter_dir=dir_name,
                    chapter_file=str(p.resolve()),
                    section_index=s_idx + 1,
                    section_title=title,
                    start_line=start_l,
                    end_line=end_l,
                    line_count=(end_l - start_l + 1),
                )
            )

    return all_sections


def format_student_reader_prompt(section: SectionSpec) -> str:
    """Generate the structured student reader evaluation prompt for a specific section."""
    return f"""================================================================================
STUDENT READER AUDIT PROMPT: Chapter {section.chapter_num} (Section {section.section_index})
================================================================================

TARGET SECTION TO READ:
- File: {section.chapter_file}
- Section Title: "{section.section_title}"
- Line Range: Lines {section.start_line} to {section.end_line} ({section.line_count} lines)
- Scope Rule: Focus your primary evaluation on lines {section.start_line} to {section.end_line}.
  You are explicitly encouraged to view preceding lines or earlier chapters for context/continuity.

EVALUATION CRITERIA (The Student Lens):
1. **Flow & Narrative Continuity:** Does this section connect naturally to the preceding sections?
   Does the introduction/transition avoid abrupt jumps?
2. **First-Principles Understanding:**
   - Are physical laws (mass, momentum, friction, thermal heat, energy) grounded intuitively?
   - Are systems mechanisms (SRAM, DMA, AXI QoS, timing cadences, zero heap) physically motivated?
   - Is mathematical derivation bloat avoided in favor of clear systems contracts?
3. **Cross-Archetype Generalizability:**
   - Does the section make sense across all 3 archetypes:
     • Archetype 1: Mobility & Locomotion (Free-space momentum $mv$, stopping distance $d_{{stop}}$)
     • Archetype 2: Contact Manipulation (Stiff contact, joint dynamics $M(q)$, jerk limits $\\dddot{{q}}$)
     • Archetype 3: Cybernetic Energy & Processes (State flows, Joule heat $I^2Rt$, switching $di/dt$)
4. **Persona-Specific Accessibility Checks:**
   - **Maya (CS/ML):** Do the ML representations make clear physical sense?
   - **Carlos (ECE/Embedded):** Are silicon registers, cache boundaries, and WCET limits realistic?
   - **Alex (Robotics/MechE):** Are dynamics, gear protection, and barrier invariants rigorous?

DELIVERABLE:
- Read Scorecard (Clarity: /10, First-Principles: /10, Generalizability: /10)
- Specific Friction Points or Stumbling Blocks (if any)
- Concrete Recommended Line Edits (if improvements are needed)
================================================================================
"""


def main():
    parser = argparse.ArgumentParser(description="Physical AI Student Reading Loop Orchestrator")
    parser.add_argument("--chapter", type=int, default=None, help="Filter by specific chapter number (1-13)")
    parser.add_argument("--section", type=int, default=None, help="Filter by specific section index")
    parser.add_argument("--json", action="store_true", help="Output section index as JSON")
    parser.add_argument("--prompts", action="store_true", help="Print student reader prompts")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    book_root = repo_root / "book"

    sections = discover_all_sections(book_root)

    if args.chapter is not None:
        sections = [s for s in sections if s.chapter_num == args.chapter]
    if args.section is not None:
        sections = [s for s in sections if s.section_index == args.section]

    if args.json:
        print(json.dumps([asdict(s) for s in sections], indent=2))
        return

    print(f"Discovered {len(sections)} H2 sections across chapters.")
    print("-" * 80)

    for s in sections:
        if args.prompts:
            print(format_student_reader_prompt(s))
        else:
            print(f"Ch {s.chapter_num:02d} | Sec {s.section_index:02d} | Lines {s.start_line:3d}-{s.end_line:3d} ({s.line_count:3d} lines) | {s.section_title}")


if __name__ == "__main__":
    main()
