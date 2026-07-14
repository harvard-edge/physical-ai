from __future__ import annotations

import yaml

from mios_controller.supply_chain import evaluate_dependency_licenses


def policy() -> dict:
    return yaml.safe_load(
        """
spdx_allowlist: [MIT, Apache-2.0, BSD-3-Clause, LGPL-3.0-only]
declared_aliases:
  MIT: [MIT]
classifier_aliases:
  "OSI Approved :: Apache Software License": [Apache-2.0]
  "OSI Approved :: BSD License": [BSD-3-Clause]
obligations:
  LGPL-3.0-only: [review before distribution]
"""
    )


def distribution(**overrides: object) -> dict:
    value = {
        "name": "fixture",
        "version": "1.0.0",
        "license_expression": None,
        "license_declared": None,
        "license_classifiers": [],
    }
    value.update(overrides)
    return value


def test_license_policy_allows_expressions_aliases_and_obligations() -> None:
    result = evaluate_dependency_licenses(
        [
            distribution(license_expression="MIT AND Apache-2.0"),
            distribution(name="alias", license_declared="MIT"),
            distribution(
                name="dual",
                license_declared="Dual License",
                license_classifiers=[
                    "OSI Approved :: Apache Software License",
                    "OSI Approved :: BSD License",
                ],
            ),
            distribution(name="copyleft", license_expression="LGPL-3.0-only"),
        ],
        policy(),
    )

    assert result["status"] == "passed"
    assert result["violations"] == []
    assert result["active_distribution_obligations"] == {
        "LGPL-3.0-only": ["review before distribution"]
    }


def test_license_policy_fails_closed_for_unknown_or_denied_metadata() -> None:
    result = evaluate_dependency_licenses(
        [
            distribution(name="unknown"),
            distribution(name="denied", license_expression="AGPL-3.0-only"),
            distribution(
                name="classifier",
                license_classifiers=["Other/Proprietary License"],
            ),
        ],
        policy(),
    )

    assert result["status"] == "failed"
    assert result["violations"] == [
        {"name": "unknown", "reason": "unknown_metadata"},
        {"name": "denied", "reason": "not_allowlisted:AGPL-3.0-only"},
        {"name": "classifier", "reason": "unrecognized_classifier"},
    ]
