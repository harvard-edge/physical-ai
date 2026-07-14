"""Fail-closed dependency-license admission for evidence collection."""

from __future__ import annotations

import re
from typing import Any


_SPDX_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9.+-]*")
_SPDX_OPERATORS = {"AND", "OR", "WITH"}


def _expression_ids(expression: str) -> list[str] | None:
    """Return license identifiers from a small, strict SPDX expression subset."""
    scrubbed = expression
    for token in _SPDX_TOKEN.findall(expression):
        if token not in _SPDX_OPERATORS:
            continue
        scrubbed = scrubbed.replace(token, " ")
    scrubbed = scrubbed.replace("(", " ").replace(")", " ")
    identifiers = _SPDX_TOKEN.findall(scrubbed)
    residue = _SPDX_TOKEN.sub(" ", scrubbed)
    if residue.strip() or not identifiers:
        return None
    return sorted(set(identifiers))


def _metadata_license_ids(
    distribution: dict[str, Any], policy: dict[str, Any]
) -> tuple[list[str] | None, str]:
    expression = distribution.get("license_expression")
    if expression:
        return _expression_ids(str(expression)), "license_expression"

    declared = distribution.get("license_declared")
    aliases = policy.get("declared_aliases", {})
    if declared and declared in aliases:
        return sorted(set(aliases[declared])), "declared_alias"

    classifiers = distribution.get("license_classifiers", [])
    classifier_aliases = policy.get("classifier_aliases", {})
    resolved: list[str] = []
    for classifier in classifiers:
        if classifier not in classifier_aliases:
            return None, "unrecognized_classifier"
        resolved.extend(classifier_aliases[classifier])
    if resolved:
        return sorted(set(resolved)), "classifier_alias"
    return None, "unknown_metadata"


def evaluate_dependency_licenses(
    inventory: list[dict[str, Any]], policy: dict[str, Any]
) -> dict[str, Any]:
    """Evaluate an installed dependency inventory against repository policy."""
    allowed = set(policy.get("spdx_allowlist", []))
    obligations = policy.get("obligations", {})
    decisions: list[dict[str, Any]] = []
    violations: list[dict[str, str]] = []
    active_obligations: dict[str, list[str]] = {}

    for distribution in inventory:
        name = str(distribution["name"])
        identifiers, source = _metadata_license_ids(distribution, policy)
        if identifiers is None:
            decisions.append(
                {
                    "name": name,
                    "version": distribution["version"],
                    "status": "denied",
                    "evidence_source": source,
                    "license_ids": [],
                }
            )
            violations.append({"name": name, "reason": source})
            continue

        denied = sorted(set(identifiers) - allowed)
        status = "denied" if denied else "allowed"
        decisions.append(
            {
                "name": name,
                "version": distribution["version"],
                "status": status,
                "evidence_source": source,
                "license_ids": identifiers,
            }
        )
        for identifier in identifiers:
            if identifier in obligations:
                active_obligations[identifier] = obligations[identifier]
        if denied:
            violations.append(
                {"name": name, "reason": f"not_allowlisted:{','.join(denied)}"}
            )

    return {
        "status": "passed" if not violations else "failed",
        "evaluated_distribution_count": len(inventory),
        "decisions": decisions,
        "violations": violations,
        "active_distribution_obligations": active_obligations,
        "scope_note": (
            "Dependency admission for local Phase 1A research only; this is not "
            "project-license selection or public-distribution clearance."
        ),
    }
