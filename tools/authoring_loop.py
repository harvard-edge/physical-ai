#!/usr/bin/env python3
"""Build a safe, provider-neutral task graph for Physical AI authoring.

This first implementation is intentionally read-only with respect to the book.
It discovers the current chapter shells, creates a chapter-by-chapter and
section-by-section work graph, and materializes agent request packets for a dry
run. A later execution adapter can consume those requests after the repository
has an accepted baseline.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


SCHEMA_VERSION = 1

ROLE_PURPOSE = {
    "domain_scout": (
        "Find indispensable concepts, counterexamples, failure modes, and "
        "primary sources. Return research notes, not manuscript prose."
    ),
    "pedagogy_auditor": (
        "Work backward from the objective and transfer task. Identify hidden "
        "prerequisites, misconceptions, and the smallest effective teaching order."
    ),
    "representation_planner": (
        "Decide whether the section needs a figure, table, equation, algorithm, "
        "trace, worked example, or prose alone. Name the reader inference."
    ),
    "chapter_steward": (
        "Own the chapter argument and voice. Draft or revise exactly one named "
        "section in a call. Do not write adjacent sections independently."
    ),
    "book_architect": (
        "Integrate accepted evidence, protect concept ownership, and decide what "
        "enters the versioned context for the next call."
    ),
    "figure_builder": (
        "Draft only an approved figure or diagram, including claim, composition, "
        "caption, alt text, source, and rendering risks."
    ),
    "table_builder": (
        "Draft only an approved table or schema with exact rows and columns and "
        "the comparison or lookup it enables."
    ),
    "algorithm_builder": (
        "Draft only an approved algorithm or state machine with inputs, state, "
        "outputs, timing assumptions, failure conditions, and fallback."
    ),
    "quantitative_builder": (
        "Draft only an approved equation, plot, or worked calculation with terms, "
        "units, assumptions, source or data, and the decision it changes."
    ),
    "technical_reviewer": (
        "Check definitions, equations, units, claims, source locations, and "
        "qualifications. Diagnose exact defects without rewriting the prose."
    ),
    "progression_reviewer": (
        "Read as a capable newcomer. Find undefined terms, hidden prerequisites, "
        "premature solutions, repeated teaching, and unnecessary jargon."
    ),
    "continuity_reviewer": (
        "Check transitions, terminology, notation, worked-example state, and "
        "dependencies. Route a problem to the earliest section that owns it."
    ),
    "practitioner_reviewer": (
        "Test whether the section supports a real engineering decision on an "
        "unfamiliar system and states assumptions and failure behavior."
    ),
    "representation_reviewer": (
        "Check that every visual, table, equation, and algorithm supports a named "
        "inference and remains legible, sourced, and consistent."
    ),
    "lab_mapper": (
        "Map complete teaching into analytical, hosted, and physical forms with "
        "the same prediction, controlled change, evidence, failure, and decision."
    ),
    "novice_book_reviewer": (
        "Audit the full book for prerequisite order, first-use definitions, plain "
        "language, and cumulative cognitive load."
    ),
    "transfer_book_reviewer": (
        "Test whether the complete method transfers to unfamiliar models, bodies, "
        "environments, and computing platforms."
    ),
    "citation_book_reviewer": (
        "Audit technical claims, equations, source locations, and the distinction "
        "between established results and this book's synthesis."
    ),
    "systems_book_reviewer": (
        "Audit the evolving system, interfaces, notation, requirements, evidence, "
        "authority, and deployment decision across all chapters."
    ),
    "lab_book_reviewer": (
        "Check that every lab assesses concepts already taught and reaches the "
        "same decision in analytical, hosted, and physical forms."
    ),
    "visual_book_reviewer": (
        "Audit figures, tables, algorithms, accessibility, HTML, PDF, grayscale, "
        "captions, and alt text."
    ),
    "voice_book_reviewer": (
        "Find formulaic structure, repeated setup, vague abstractions, inflated "
        "claims, and writing that makes the reader decode the prose first."
    ),
}


class PlanError(RuntimeError):
    pass


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def discover_chapter_paths(repo: Path, config: dict[str, Any]) -> list[Path]:
    quarto = repo / config["book"]["quarto_config"]
    pattern = re.compile(r"^\s*-\s+(chapters/(\d\d)-[^\s]+\.qmd)\s*$")
    chapters: list[Path] = []
    for line in quarto.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match and 1 <= int(match.group(2)) <= 13:
            chapters.append(repo / "book" / match.group(1))
    if len(chapters) != 13:
        raise PlanError(
            f"expected 13 numbered chapters in {quarto}, found {len(chapters)}"
        )
    return chapters


def parse_chapter(path: Path, repo: Path) -> dict[str, Any]:
    title = ""
    headings: list[str] = []
    active_callout: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not title and stripped.startswith("# "):
            title = stripped[2:].strip()
            continue
        callout = re.match(r"^::: \{\.callout-([a-z-]+)\}$", stripped)
        if callout:
            active_callout = callout.group(1)
            continue
        if stripped == ":::" and active_callout:
            active_callout = None
            continue
        if stripped.startswith("## ") and active_callout is None:
            headings.append(stripped[3:].strip())
    number_match = re.match(r"(\d\d)-", path.name)
    if not title or not number_match:
        raise PlanError(f"could not parse {path}")
    chapter_id = f"CH{number_match.group(1)}"
    sections = [
        {
            "section_id": f"{chapter_id}-OPENING",
            "title": "Opening",
            "kind": "opening",
        }
    ]
    sections.extend(
        {
            "section_id": f"{chapter_id}-SEC{index:02d}",
            "title": heading,
            "kind": "teaching",
        }
        for index, heading in enumerate(headings, start=1)
    )
    return {
        "chapter_id": chapter_id,
        "number": int(number_match.group(1)),
        "title": title,
        "path": str(path.relative_to(repo)),
        "steward_id": f"steward-{chapter_id.lower()}",
        "sections": sections,
    }


class GraphBuilder:
    def __init__(self, repo: Path, config: dict[str, Any], chapters: list[dict[str, Any]]):
        self.repo = repo
        self.config = config
        self.chapters = chapters
        self.tasks: list[dict[str, Any]] = []
        self.counter = 0

    def add_task(
        self,
        phase: str,
        role: str,
        chapter: dict[str, Any] | None,
        section: dict[str, Any] | None,
        depends_on: list[str],
        *,
        parallel_group: str | None = None,
        condition: str = "always",
        loop: dict[str, Any] | None = None,
        optional: bool = False,
        writes_prose: bool = False,
    ) -> str:
        self.counter += 1
        chapter_id = chapter["chapter_id"] if chapter else "BOOK"
        section_id = section["section_id"] if section else "ALL"
        task_id = (
            f"T{self.counter:05d}-"
            f"{slug(chapter_id)}-{slug(section_id)}-{slug(phase)}-{slug(role)}"
        )
        task = {
            "task_id": task_id,
            "phase": phase,
            "role": role,
            "role_purpose": ROLE_PURPOSE[role],
            "chapter_id": chapter_id,
            "chapter_title": chapter["title"] if chapter else None,
            "section_id": section_id,
            "section_title": section["title"] if section else None,
            "steward_id": chapter["steward_id"] if chapter else None,
            "depends_on": depends_on,
            "parallel_group": parallel_group,
            "condition": condition,
            "loop": loop,
            "optional": optional,
            "writes_prose": writes_prose,
            "write_scope": "candidate output only",
        }
        self.tasks.append(task)
        return task_id

    def parallel(
        self,
        phase: str,
        roles: list[str],
        chapter: dict[str, Any] | None,
        section: dict[str, Any] | None,
        depends_on: list[str],
        *,
        condition: str = "always",
        optional: bool = False,
    ) -> list[str]:
        group = f"PG-{len(self.tasks) + 1:05d}-{slug(phase)}"
        return [
            self.add_task(
                phase,
                role,
                chapter,
                section,
                depends_on,
                parallel_group=group,
                condition=condition,
                optional=optional,
            )
            for role in roles
        ]

    def build(self) -> dict[str, Any]:
        previous_chapter_acceptance: list[str] = []
        for chapter in self.chapters:
            research = self.parallel(
                "chapter_research",
                self.config["roles"]["chapter_research"],
                chapter,
                None,
                previous_chapter_acceptance,
            )
            architecture = self.add_task(
                "chapter_architecture",
                "chapter_steward",
                chapter,
                None,
                research,
            )
            architecture_reviews = self.parallel(
                "chapter_architecture_review",
                self.config["roles"]["chapter_review"],
                chapter,
                None,
                [architecture],
            )
            architecture_approval = self.add_task(
                "chapter_architecture_approval",
                "book_architect",
                chapter,
                None,
                architecture_reviews,
                condition="all architecture reviews pass",
                loop={
                    "on_failure": "chapter_architecture",
                    "maximum_revision_rounds": self.config["execution"][
                        "max_chapter_revision_rounds"
                    ],
                    "human_approval": True,
                },
            )
            previous_section_acceptance = [architecture_approval]
            for section in chapter["sections"]:
                support = self.parallel(
                    "section_support",
                    self.config["roles"]["section_support"],
                    chapter,
                    section,
                    previous_section_acceptance,
                )
                brief = self.add_task(
                    "section_brief",
                    "book_architect",
                    chapter,
                    section,
                    support,
                )
                draft = self.add_task(
                    "section_draft",
                    "chapter_steward",
                    chapter,
                    section,
                    [brief],
                    writes_prose=True,
                )
                artifacts = self.parallel(
                    "section_artifact",
                    [
                        "figure_builder",
                        "table_builder",
                        "algorithm_builder",
                        "quantitative_builder",
                    ],
                    chapter,
                    section,
                    [brief, draft],
                    condition="artifact type approved by section brief",
                    optional=True,
                )
                reviews = self.parallel(
                    "section_review",
                    self.config["roles"]["section_review"],
                    chapter,
                    section,
                    [draft, *artifacts],
                )
                revision = self.add_task(
                    "section_revision",
                    "chapter_steward",
                    chapter,
                    section,
                    reviews,
                    condition="any review requests revision",
                    loop={
                        "return_to": "section_review",
                        "maximum_revision_rounds": self.config["execution"][
                            "max_section_revision_rounds"
                        ],
                        "revision_scope": "this section only",
                    },
                    writes_prose=True,
                )
                acceptance = self.add_task(
                    "section_acceptance",
                    "book_architect",
                    chapter,
                    section,
                    [*reviews, revision],
                    condition="all required reviews pass",
                )
                previous_section_acceptance = [acceptance]

            integration = self.add_task(
                "chapter_integration",
                "chapter_steward",
                chapter,
                None,
                previous_section_acceptance,
                writes_prose=True,
            )
            chapter_feedback = self.parallel(
                "chapter_feedback",
                self.config["roles"]["chapter_feedback"],
                chapter,
                None,
                [integration],
            )
            revision_router = self.add_task(
                "chapter_revision_router",
                "book_architect",
                chapter,
                None,
                chapter_feedback,
                condition="route findings to earliest owning section",
                loop={
                    "revision_order": "one section at a time",
                    "return_to": "chapter_feedback",
                    "maximum_revision_rounds": self.config["execution"][
                        "max_chapter_revision_rounds"
                    ],
                },
            )
            lab = self.add_task(
                "lab_mapping",
                "lab_mapper",
                chapter,
                None,
                [revision_router],
                condition="chapter teaching passes review",
            )
            chapter_acceptance = self.add_task(
                "chapter_acceptance",
                "book_architect",
                chapter,
                None,
                [lab],
                condition="chapter, sources, representations, transfer, and lab agree",
                loop={"human_approval": True},
            )
            previous_chapter_acceptance = [chapter_acceptance]

        book_feedback = self.parallel(
            "book_feedback",
            self.config["roles"]["book_feedback"],
            None,
            None,
            previous_chapter_acceptance,
        )
        book_revision_router = self.add_task(
            "book_revision_router",
            "book_architect",
            None,
            None,
            book_feedback,
            condition="route each finding to concept owner and first-use section",
            loop={
                "revision_order": "earliest chapter and section first",
                "prose_lock": "one affected section at a time",
                "return_to": "book_feedback",
                "maximum_revision_rounds": self.config["execution"][
                    "max_book_revision_rounds"
                ],
            },
        )
        final_acceptance = self.add_task(
            "book_acceptance",
            "book_architect",
            None,
            None,
            [book_revision_router],
            condition="no blocking findings and all renders pass",
            loop={"human_approval": True},
        )
        return {
            "schema_version": SCHEMA_VERSION,
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "invariants": {
                "active_chapters": 1,
                "chapter_stewards": 1,
                "prose_sections_per_generation_call": 1,
                "parallel_specialists": self.config["execution"]["max_parallel_agents"],
                "raw_agent_output_is_context": False,
                "labs_follow_complete_teaching": True,
                "canonical_book_writes": False,
            },
            "chapters": self.chapters,
            "tasks": self.tasks,
            "final_task": final_acceptance,
        }


def context_contract(
    repo: Path,
    config: dict[str, Any],
    task: dict[str, Any],
    chapter: dict[str, Any] | None,
) -> dict[str, Any]:
    static_paths = [
        config["book"]["book_goal"],
        config["book"]["authoring_system"],
        config["book"]["voice_rules"],
    ]
    static = []
    for relative in static_paths:
        path = repo / relative
        content = path.read_text(encoding="utf-8")
        static.append({"path": relative, "sha256": sha256_text(content)})
    packets = []
    if chapter:
        packets = config["book"].get("chapter_packets", {}).get(
            chapter["chapter_id"], []
        )
    return {
        "static_book_context": static,
        "chapter_context": {
            "chapter_id": task["chapter_id"],
            "chapter_title": task["chapter_title"],
            "chapter_outline": config["book"]["chapter_outline"],
            "chapter_packets": packets,
            "steward_id": task["steward_id"],
        },
        "accepted_dynamic_context": {
            "immediately_previous_section": "full accepted text at execution time",
            "older_sections": "accepted summaries and context changes only",
            "accepted_claims_and_sources": "relevant registry slice",
            "accepted_terms_and_notation": "relevant registry slice",
            "canonical_example_state": "current accepted version",
            "unresolved_questions": "accepted open questions only",
        },
        "current_section": {
            "section_id": task["section_id"],
            "section_title": task["section_title"],
            "later_sections": "titles and dependency sentences only, never prose",
        },
        "forbidden_context": [
            "rejected drafts",
            "raw reviewer transcripts",
            "unaccepted suggestions",
            "future section prose",
            "lab outcomes before the conceptual chapter passes",
        ],
    }


def task_prompt(task: dict[str, Any]) -> str:
    role = task["role"]
    return (
        "# Physical AI Authoring Request\n\n"
        f"Task ID: {task['task_id']}\n\n"
        f"Role: {role}\n\n"
        f"Chapter: {task['chapter_id']} — {task['chapter_title'] or 'Whole book'}\n\n"
        f"Section: {task['section_id']} — {task['section_title'] or 'All sections'}\n\n"
        f"Purpose: {ROLE_PURPOSE[role]}\n\n"
        "## Working Rules\n\n"
        "- Work on the named chapter and section only.\n"
        "- Only the persistent chapter steward may write reader-facing prose.\n"
        "- A prose task writes or revises exactly one section.\n"
        "- Use accepted context only. Later sections appear as dependencies, not prose.\n"
        "- State the plain idea before specialized terminology.\n"
        "- Do not invent sources, measurements, quotations, or results.\n"
        "- A figure, table, equation, or algorithm must support one named inference.\n"
        "- Reviewers diagnose and route defects. They do not replace the manuscript.\n"
        "- Return structured findings with the smallest repair and an acceptance test.\n\n"
        "## Output Contract\n\n"
        "Return JSON with a factual summary, proposed artifacts, context changes, "
        "and findings. A prose task also returns one manuscript section. A review "
        "returns pass or revise. An optional representation task may return "
        "not_needed. Follow authoring/result.schema.json.\n"
    )


def validate_output_path(repo: Path, output: Path) -> None:
    """Keep generated agent traffic out of the manuscript and public docs."""
    try:
        relative = output.resolve().relative_to(repo.resolve())
    except ValueError:
        return
    if not relative.parts or relative.parts[0] != ".authoring-runs":
        raise PlanError(
            "an output inside the repository must be under .authoring-runs/"
        )


def materialize(
    repo: Path,
    config: dict[str, Any],
    graph: dict[str, Any],
    output: Path,
) -> None:
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "plan.json", graph)
    chapters = {chapter["chapter_id"]: chapter for chapter in graph["chapters"]}
    for task in graph["tasks"]:
        task_dir = output / "tasks" / task["task_id"]
        task_dir.mkdir(parents=True, exist_ok=True)
        chapter = chapters.get(task["chapter_id"])
        request = {
            "protocol_version": SCHEMA_VERSION,
            "task": task,
            "context": context_contract(repo, config, task, chapter),
            "adapter_contract": {
                "input": "this request.json and prompt.md",
                "output": "result.json",
                "write_scope": "task output directory only",
                "canonical_book_write": False,
            },
        }
        write_json(task_dir / "request.json", request)
        (task_dir / "prompt.md").write_text(task_prompt(task), encoding="utf-8")


def summary(graph: dict[str, Any]) -> dict[str, Any]:
    groups = {}
    for task in graph["tasks"]:
        groups[task["phase"]] = groups.get(task["phase"], 0) + 1
    return {
        "chapters": len(graph["chapters"]),
        "sections_including_openings": sum(
            len(chapter["sections"]) for chapter in graph["chapters"]
        ),
        "tasks": len(graph["tasks"]),
        "optional_tasks": sum(task["optional"] for task in graph["tasks"]),
        "conditional_tasks": sum(
            task["condition"] != "always" for task in graph["tasks"]
        ),
        "tasks_by_phase": groups,
        "final_task": graph["final_task"],
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Plan the Physical AI multi-agent authoring loop."
    )
    result.add_argument(
        "--repo-root",
        help="repository root; defaults to the parent of this script",
    )
    result.add_argument(
        "--config",
        default="authoring/loop-config.json",
        help="configuration path relative to the repository",
    )
    sub = result.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="print the discovered authoring plan")
    plan.add_argument("--json", action="store_true")
    dry = sub.add_parser("dry-run", help="materialize request packets safely")
    dry.add_argument("--output", required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    repo = (
        Path(args.repo_root).expanduser().resolve()
        if args.repo_root
        else Path(__file__).resolve().parent.parent
    )
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = repo / config_path
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        chapters = [
            parse_chapter(path, repo)
            for path in discover_chapter_paths(repo, config)
        ]
        graph = GraphBuilder(repo, config, chapters).build()
        if args.command == "plan":
            if args.json:
                print(json.dumps(graph, indent=2))
            else:
                info = summary(graph)
                print("Physical AI authoring loop")
                print(f"Chapters: {info['chapters']}")
                print(f"Sections including openings: {info['sections_including_openings']}")
                print(f"Planned tasks: {info['tasks']}")
                print()
                for chapter in chapters:
                    print(f"{chapter['chapter_id']}  {chapter['title']}")
                    for section in chapter["sections"]:
                        print(f"  {section['section_id']:16} {section['title']}")
            return 0
        output = Path(args.output).expanduser()
        if not output.is_absolute():
            output = repo / output
        output = output.resolve()
        validate_output_path(repo, output)
        materialize(repo, config, graph, output)
        print(json.dumps(summary(graph), indent=2))
        print(f"Dry-run requests written to {output}")
        return 0
    except (OSError, json.JSONDecodeError, PlanError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
