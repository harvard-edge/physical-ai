# UNO Q transfer readiness

MiOS transfer to UNO Q means the cognitive contracts remain unchanged while
embodiment adapters and resource profiles are target-specific. This checklist
does not claim transfer until it is executed on a physical UNO Q.

## Contract gate

- [ ] Install the versioned portable-core manifest without modifying its memory,
      safety, or cognition operations.
- [ ] Run conformance tests for `append`, `promote`, `retract`, `search`,
      `authorize`, `protective_stop`, `checkpoint`, and `resume`.
- [ ] Confirm physical authority remains local to the UNO Q adapter.
- [ ] Confirm the release manifest and rollback target are content-addressed.

## Resource evidence

Record a target-device artifact containing:

| Measurement | Required record |
| --- | --- |
| Peak memory | MB, sampling method, runtime version |
| p95 latency | milliseconds for the portable-core operation set |
| CPU and thermal behavior | duration, load, temperature, throttling |
| Storage and restart | database size, restore time, retained memory count |
| Safety response | protective-stop latency and unsafe-command count |

The target profile must pass the declared memory and latency budgets. A contract
pass without measurements is only a portability check, not a transfer result.

## Reproducibility

Run the same synthetic Maya protocol and portable-core conformance suite on the
UNO Q image. Record failures and inconclusive runs, not only successful runs.
Keep the result labeled target-hardware evidence and do not merge it with
Reachy-specific physical measurements.
