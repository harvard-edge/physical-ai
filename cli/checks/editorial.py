"""Editorial standards, Michael Alley scientific writing rules, and banned terminology checks."""

from __future__ import annotations

import re

from .base import BaseCheck, CheckRegistry
from ..context import BookContext
from ..report import LintIssue, LintReport


@CheckRegistry.register
class BannedTerminologyCheck(BaseCheck):
    name = "banned_terminology"
    description = "Enforces global book policy against course/syllabus/dossier terms in body copy"
    category = "editorial"

    BANNED = [
        (re.compile(r"\b(14-week|fourteen-week)\b", re.IGNORECASE), "Course syllabus duration term ('14-week')"),
        (re.compile(r"\b(dossier checkpoint|engineering dossier)\b", re.IGNORECASE), "Course dossier term (use 'engineering notebook' or omit)"),
        (re.compile(r"\b(grading milestone|grading rubric)\b", re.IGNORECASE), "Class grading term"),
        (re.compile(r"\b(Milestone \d+)\b", re.IGNORECASE), "Course milestone marker"),
        (re.compile(r"\b(LOOP-01|OBS-01|STATE-01|INTENT-01|PLAN-01|ENFORCE-01|PLACE-01|GOV-01|QUAL-01|RELEASE-01)\b"), "Legacy course rubric tag"),
    ]

    def run(self, ctx: BookContext, report: LintReport):
        for file_path in ctx.qmd_files:
            rel_path = str(file_path.relative_to(ctx.repo_root))
            lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            in_code_block = False

            for idx, line in enumerate(lines, start=1):
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue

                for pattern, desc in self.BANNED:
                    if pattern.search(line):
                        report.add_issue(LintIssue(
                            category="editorial",
                            severity="ERROR",
                            file=rel_path,
                            line=idx,
                            page=None,
                            message=f"Banned course/syllabus terminology: {desc}",
                            context=line.strip()
                        ))
