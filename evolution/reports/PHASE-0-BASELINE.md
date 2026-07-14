# MiOS Phase 0 Baseline

**Observed:** July 14, 2026
**Implementation cutoff:** `7a7f27ffb2e588abfbfb2481a52137b991e6b724`
**Gate status:** Not approved for continuous evolution or physical deployment

## Current Implementation

The pre-autonomy implementation is the `mayas-reachy` 0.1.0 Python package in
`code/`. It hosts a FastAPI interface, transcribes through Groq Whisper, asks a
Groq-hosted language model for structured interpretation, stores episodic and
semantic memory in SQLite, synthesizes speech through Piper, and directly calls
the Reachy Mini SDK for movement.

The runtime has useful seams for reasoning and action policies, but its current
physical boundary is not an independent deterministic safety supervisor.
`MayasReachyApp` still owns direct SDK calls, application queues, memory, cloud
requests, voice, and the web interface.

## Measured Local Baseline

| **Measure** | **Observed result** | **Evidence boundary** |
| --- | --- | --- |
| Behavioral tests | 19 passed in 0.60 seconds | macOS, global Python environment |
| Test process memory | Approximately 75 MiB maximum RSS | Independent audit run |
| Local fake stop route | 1.07 ms p95, 13.93 ms maximum over 200 requests | FastAPI TestClient, not robot |
| Wheel size | 144 KiB | Fresh local build |
| Repeated wheel hash | `4b9bec4630528873c5d96ec5c7d87d801160659bf95c62d46cd7a15ca9e260bc` | Two builds with fixed epoch |
| Application source | 2,138 lines across Python and web files | Excludes generated caches |
| SQLite at 100 claims | 147,456 bytes | Temporary local database |
| Retrieval at 100 claims | Approximately 0.43 ms for eight results | Temporary local database |

The 19 behavioral tests pass, but an independent `unittest` run reported
unclosed SQLite connection warnings. A clean `uv` test environment also failed
while resolving the Linux Reachy dependency through PyGObject and PyCairo on
macOS. The wheel itself built reproducibly, but dependency installation is not
locked or reproducible across target platforms.

## External State

- The repository has one worktree on `dev` and no configured Git remote.
- Substantial unrelated book and documentation work is uncommitted and must not
  be touched by autonomous engineering jobs.
- Approved engineering-provider profiles have not been activated. No paid model
  calls were made during Phase 0 preparation.
- `reachy-mini.local` did not resolve. The installed robot release, Raspberry Pi
  resource use, physical stop latency, and recovery behavior are unverified.
- No GitHub workflows, protected environments, controller, durable evolution
  ledger, signed release, or automated rollback mechanism exists.

## Assurance Gaps

The current LAN interface has no demonstrated authentication or role separation.
Memory inspection and reset are exposed through application routes. Raw audio is
transient, but transcripts, recent conversation, and retrieved personal memory
can be sent to Groq. Guardian consent, provider allowlisting, retention,
redaction, verified deletion, and child-data incident procedures are not yet
implemented.

Microphone Stop is interaction cancellation, not a protective or hardware
emergency stop. It ends recording but does not prove
preemption of queued reasoning, speech, or motion. Hardcoded bounded poses are
not a centralized authorization envelope. Recovery failures are logged rather
than enforced through a separate watchdog.

SQLite backup creation exists, but restoration, corruption recovery, schema
migration, consent-aware rollback, WAL deletion, and backup expiry are not
verified. The in-memory event journal is bounded and contains verbatim text. It
is not the privacy-filtered, append-only evolution ledger.

## Protected-Check Coverage

| **Required check** | **Baseline state** |
| --- | --- |
| Unit tests | Partial, 19 passing |
| Formatting, lint, types, dependency policy | Missing |
| Provider contracts and degraded-service integration | Partial |
| Memory migration, restore, corruption, and privacy | Missing or partial |
| Deterministic action envelope, protective stop, and watchdog | Missing |
| Recorded replay and held-out cognitive evaluation | Missing |
| Target edge resource measurement | Missing |
| Simulation and shadow attestation | Missing |
| Independent decisive reviews | Missing |
| Pinned build, SBOM, signature, and provenance | Missing or partial |
| Persistent-state rollback rehearsal | Missing |

## Phase 0 Gate

Local policy drafting and deterministic synthetic-controller work may proceed
after approval of the requested pilot budget. External GitHub publication, paid
model calls, child-data egress, automatic merge, new physical capabilities, and
physical deployment remain disabled.

Phase 0 cannot close until the revised charter and governance artifacts are
approved, an independent protected-evaluation custodian is assigned, privacy
decisions are made, and the known-good local baseline is pinned. Reproducible
target dependency installation, target-hardware assurance, and rollback
rehearsal are Phase 2 gates and cannot be used as circular prerequisites for
building the offline controller that will record them.
