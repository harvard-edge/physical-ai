# MiOS Evolution Controller

This package is the durable control plane for MiOS experiments. It is separate
from the robot runtime and owns no physical authority.

Phase 1A proves one deterministic, offline cycle from a synthetic observation to
`LOCAL_CANDIDATE_READY`. It uses a disposable fixture repository, a local forge,
content-addressed artifacts, a hash-chained ledger, and an approved workflow
substrate. It cannot call a model, publish to GitHub, reach a robot, or use child
data.

The controller is designed to be supervised continuously, not to spin forever.
When idle it backs off. Budgets, repeated failures, policy violations, integrity
errors, signals, or the persistent kill switch pause it. Restarting does not
resume effects without a dedicated resume command and matching campaign,
policy, and approval-artifact digests. The shared provider-neutral service
contract is documented in
[`governance/operating-loop.md`](../governance/operating-loop.md).

## Commands

After installing the package in a virtual environment:

```text
mios-controller init --root .mios
mios-controller ingest evolution/fixtures/synthetic-observation.json
mios-controller resume --root .mios
mios-controller run --root .mios
mios-controller resume --root .mios
mios-controller supervise --root .mios --max-cycles 20 --resume
mios-controller pause --root .mios
mios-controller status --root .mios
mios-controller verify --root .mios
```

`supervise` is bounded unless the operator explicitly supplies `--continuous`.
Even in continuous mode the persistent kill switch, budgets, and circuit breaker
remain active.

The `--resume` flag on `supervise` confirms that the process was started for an
already authorized controller. It does not clear `STOP` or grant authority. Only
the separate `resume` command can do that.
