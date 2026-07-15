from mios_controller.portability import (
    EmbodimentManifest,
    ResourceMeasurement,
    check_transfer,
)


def test_uno_q_transfer_requires_contracts_and_target_budgets() -> None:
    manifest = EmbodimentManifest(
        "uno-q",
        "1.0.0",
        frozenset(
            {
                "append",
                "promote",
                "retract",
                "search",
                "authorize",
                "protective_stop",
                "checkpoint",
                "resume",
            }
        ),
        128,
    )
    measurement = ResourceMeasurement("uno-q", 96, 40, 128, 100)
    assert check_transfer(manifest, measurement)
    assert not check_transfer(manifest, ResourceMeasurement("uno-q", 160, 40, 128, 100))
