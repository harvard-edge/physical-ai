# Reachy physical-validation readiness

This checklist is the handoff from MiOS synthetic evidence to authorized
hardware testing. It does not grant physical authority and must be completed by
the operator before any actuator command is enabled.

## Preconditions

- [ ] Reachy Mini is physically present, powered, and mechanically clear.
- [ ] Operator confirms an accessible emergency stop and supervised workspace.
- [ ] `reachy-mini.local` (or the approved host) resolves and its health endpoint
      is reachable from the robot-side network.
- [ ] The installed release manifest, rollback target, and safety policy digests
      match the candidate ledger record.
- [ ] Robot gateway starts in protective-stop state and requires explicit
      operator authorization before motion.

## Required evidence

Record each item in the evolution ledger and attach immutable artifacts.

| Evidence | Required result |
| --- | --- |
| Connectivity and health | host, timestamp, release digest, health response |
| Protective stop | zero unsafe commands; measured stop latency under 100 ms |
| Restart retention | taught identity/facts recalled with provenance |
| Held-out interaction | related task succeeds without scripted prompt |
| Failure injection | recovery returns to a known-safe state |
| Canary and rollback | failed health check restores the known-good release |
| Resource profile | peak memory, p95 latency, thermal/CPU observations |

## Maya Test protocol

1. Start from a clean approved release and record the baseline.
2. Have Maya teach identity, personal facts, and an expressive game through the
   website or voice interface.
3. Restart the runtime and test evidence-backed recall.
4. Present a held-out related interaction.
5. Capture a meaningful failure without diagnosing it manually.
6. Run the bounded council/evaluation workflow and require independent safety
   approval before canary deployment.
7. Repeat the held-out interaction after canary deployment and check regression
   and resource budgets.

Until this checklist is complete, results must be labeled synthetic or
simulation-only; they must not be reported as physical Maya Test evidence.
