# MiOS Embodied Bootstrap Goal

**Working name:** MiOS, Maya's Intelligence Operating System
**Experiment:** The MiOS Embodied Bootstrap Challenge
**Status:** Phase 0 execution charter, revision 0.2
**Primary embodiment:** Reachy Mini
**Transfer embodiment:** Arduino UNO Q

## Goal Command Input

The following text is the concise goal to give a long-running agent. The agent
must read this entire file before acting.

> Build and operate the MiOS Embodied Bootstrap experiment described in
> `docs/MIOS-EMBODIED-BOOTSTRAP-GOAL.md`. Begin from the existing Maya's Reachy
> prototype and evolve it into an inspectable, portable machine-intelligence
> runtime. Organize a bounded team of specialist agents, reuse suitable existing
> frameworks, maintain an append-only evolution ledger, and improve the system
> through measured GitHub issues, experiments, pull requests, reviews, and
> canary deployments. Optimize for demonstrated embodied capability, safety,
> reproducibility, edge efficiency, and understandable design rather than code
> volume or agent activity. Do not weaken safety, privacy, evaluation, budget,
> or deployment controls. Continue until the success criteria in this file are
> met or a stop condition requires Professor Vijay Janapa Reddi's decision.

The command grants autonomy to conduct local research, create branches, write
code and tests, run simulations, maintain experiment records, and prepare pull
requests. It does not grant authority to publish externally, spend beyond the
declared budget, expose private data, weaken protected controls, or deploy new
physical capabilities without the approval policy defined below.

## North Star

Starting with the existing prototype, physical hardware documentation, and a
constitutional safety specification, an autonomous agent organization will
design and implement an embodied-intelligence runtime, deploy it, learn through
interactions with Maya, identify deficiencies in its own design, and measurably
improve itself through an auditable sequence of experiments and pull requests.
Humans will not write implementation code for the experiment.

The autonomy claim begins at the pre-autonomy baseline commit recorded in the
evaluation manifest. Earlier prototype code remains part of the starting
condition. Human approvals, hardware setup, protected-test authorship, and
safety interventions are recorded separately from implementation contributions.
The experiment must never describe inherited code or human-authored evaluation
criteria as agent-generated work.

The final demonstration is the **Maya Test**:

1. Maya teaches the robot a new identity, personal facts, and a physical or
   expressive game that was not encoded as a scripted demonstration.
2. The robot retains the knowledge across restarts and can show the evidence
   supporting what it believes.
3. The robot uses the knowledge in a related interaction it has not seen before.
4. A meaningful failure is observed and captured without a human diagnosing it.
5. The MiOS agent organization forms competing hypotheses, implements an
   experiment, reviews the result, and produces a pull request.
6. The candidate passes independent evaluation and the physical-safety gate.
7. After authorized canary deployment, the robot succeeds on a held-out variant
   without regressing its safety or resource budgets.
8. The same runtime contracts are transferred to UNO Q without a human redesign
   of the cognitive architecture.

The project succeeds only when the result can be reproduced from the repository
and evolution ledger. A fluent demonstration without traceable evidence does
not pass.

### Autonomy Levels

The experiment reports autonomy as an observed level rather than the binary
phrase “human in or out of the loop.”

| **Level** | **Agent authority demonstrated** | **Required human role** |
| --- | --- | --- |
| A0 | Executes an explicitly specified implementation task | Directs the task |
| A1 | Decomposes and implements a bounded issue | Approves the issue and result |
| A2 | Selects work from measured observations | Approves consequential release |
| A3 | Forms and tests competing improvement hypotheses | Owns protected evaluation and safety authority |
| A4 | Completes a reflective observation-to-improvement cycle | Approves physical canary |
| A5 | Transfers the architecture to a new embodiment | Supplies hardware and constitutional bounds |

MiOS must report the highest level supported by complete evidence and the number
and type of human interventions required. It may not infer a higher level from
the amount of generated code.

## Research Claim

MiOS investigates whether an agentic development system can continually improve
the architecture of an embodied machine-intelligence runtime through evidence
from physical interaction while preserving safety, reproducibility, resource
efficiency, and an inspectable account of its decisions.

The experiment does not claim to replace Linux or autonomously train a general
foundation model. Linux remains the operating substrate. MiOS is the operating
layer for perception, memory, reasoning, skills, safety, and reflective
improvement.

The research claim is falsifiable. MiOS does not support the claim if repeated
experiments show no advantage over a fixed single-agent workflow at matched
model, tool, token, time, and evaluation budgets, or if improvement disappears
on protected cases, target hardware, or a second embodiment.

Each consequential study compares at least these conditions when feasible:

1. a fixed single-agent baseline;
2. a fixed specialist team with no organizational adaptation; and
3. the adaptive MiOS agent organization.

Model versions stay fixed within a comparison. Tasks are randomized or paired,
failed and inconclusive runs remain in the denominator, and the analysis reports
effect sizes and uncertainty rather than only pass rates. Model upgrades begin
a new comparison block so improvements in the underlying model are not
misattributed to MiOS.

## Precedents and Design Lessons

The experiment adopts the strongest parts of two recent long-horizon agent
demonstrations without treating either one as a complete template.

[Anthropic's C compiler experiment](https://www.anthropic.com/engineering/building-c-compiler)
used parallel Claude agents, a shared repository, explicit task claiming, and a
strong external oracle. Its central lesson for MiOS is that autonomy depends on
the surrounding harness, decomposition, tests, and feedback quality as much as
on model capability.

[Google's Antigravity demonstration](https://research.google/blog/a-new-era-of-innovation-google-research-at-io-2026/)
used a prompt-refinement and approval step followed by an orchestrator that
spawned specialized agents for long-running implementation, testing, and
debugging. Its central lesson for MiOS is to approve a precise charter first,
then delegate through a durable orchestrator rather than repeatedly steering
individual coding sessions.

MiOS adds three requirements that are less prominent in those demonstrations.
The specification is partly discovered through open-ended interaction, progress
is judged through independent physical outcomes, and accepted improvements must
remain safe under edge-device constraints. The experiment therefore needs an
assurance plane and evolution ledger in addition to an agent team and test
harness.

The rationale for revision 0.2 and its infrastructure choices is recorded in
[`MIOS-DESIGN-REVIEW.md`](MIOS-DESIGN-REVIEW.md).

## Success Measures

Progress is measured against externally defined outcomes. Agent activity,
tokens consumed, pull requests opened, and lines of code are costs rather than
evidence of success.

| **Dimension** | **Primary measure** | **Initial success threshold** |
| --- | --- | --- |
| Learning | Held-out recall after correction and restart | At least 90% |
| Grounding | Answers supported by retrieved evidence | At least 95% |
| Generalization | Success on unseen variants of taught skills | At least 75% |
| Responsiveness | Interaction-cancel UI acknowledgment | Under 100 ms |
| Physical control | Unsafe actuator commands executed | Zero |
| Recovery | Return to known state after injected failures | 100% of hazard-derived required scenarios |
| Edge operation | Core runtime remains within declared device budgets | No budget violation |
| Evolution | Cumulative preregistered utility versus the fixed-agent baseline | Positive effect with uncertainty reported |
| Experiment integrity | Registered experiments with complete outcomes | 100%, including failures and rollbacks |
| Regression | Critical protected regressions admitted to release | Zero |
| Autonomy | Human implementation contributions | Zero |
| Intervention | Human interventions by type and autonomy level | Reported for every experiment |
| Transfer | Versioned cognitive contracts passing unchanged conformance tests on UNO Q | Core contracts all pass |
| Reproducibility | Clean reconstruction from release and ledger | Two successful rebuilds |

Thresholds may be tightened through a governance pull request. An agent may not
lower a threshold to make its own candidate pass.

Safety is reported jointly with required-task completion and calibrated
abstention. A system that refuses every task does not satisfy the physical-control
criterion. “No regression” means a critical regression blocks release; lower
severity findings remain visible with an owner and resolution deadline.

## System Boundaries

MiOS consists of three cooperating systems with separate authority.

```text
Maya and the physical world
            │ observations and outcomes
            ▼
┌──────────────────────────────────────────────────────┐
│ MiOS Runtime                                         │
│ perception · memory · reasoning · skills · safety    │
└───────────────────────┬──────────────────────────────┘
                        │ telemetry and evidence
                        ▼
┌──────────────────────────────────────────────────────┐
│ MiOS Evolution Controller                            │
│ observe · hypothesize · delegate · experiment · PR   │
└───────────────────────┬──────────────────────────────┘
                        │ candidate release
                        ▼
┌──────────────────────────────────────────────────────┐
│ Independent Assurance Plane                          │
│ sealed evals · safety checks · budgets · deployment  │
└───────────────────────┬──────────────────────────────┘
                        │ authorized capability bundle
                        ▼
                   physical robot
```

The Runtime may learn knowledge and bounded skills during operation. The
Evolution Controller may change ordinary implementation code through reviewed
pull requests. The Assurance Plane owns protected tests, safety invariants,
credentials, budgets, and release authority. Ordinary agents cannot modify or
bypass it.

## The Continuous Evolution Controller

The controller is a restartable service, not a permanent model conversation. It
stores state in ordinary durable systems and invokes models as replaceable
workers. A crash, context reset, or model upgrade must not erase the experiment.

Its state machine is:

```text
OBSERVED → TRIAGED → PREREGISTERED → DESIGNED → IMPLEMENTING
                                                    │
                                                    ▼
LEARNED ← MONITORING ← ACCEPTED ← CANARY ← SHADOW ← REVIEWING ← EVALUATING
                                ▲
                                │ explicit authorization
                    LOCAL_CANDIDATE_READY

Any nonterminal state → PAUSED | REJECTED | INCIDENT
Any deployed state    → ROLLED_BACK
```

Each transition requires a versioned artifact. The controller may resume only
from the last completed transition. It must never infer completion from an
agent's prose when a machine-verifiable result is expected. Revision never
rewrites a preregistration. It creates a linked child experiment with a new
hypothesis, budget, and evaluation record.

The Runtime and Evolution Controller maintain separate records. Runtime memory
contains consented knowledge used during interaction. The evolution ledger
contains privacy-filtered engineering evidence. An interaction does not become
training, evaluation, or public engineering data merely because the runtime
observed it.

### Controller Services

The first controller implementation should reuse the smallest dependable pieces:

1. **Durable workflow substrate.** Run a bounded bakeoff before building a
   scheduler. DBOS is the leading local candidate because its Python workflows
   checkpoint to SQLite and resume completed steps. Temporal is the scale-up
   candidate when multi-host operation or long human waits justify its service.
   A custom state machine is accepted only if the bakeoff documents a required
   capability that neither provides within the edge and governance constraints.
2. **Experiment registry.** A MiOS-owned SQLite database records hypotheses,
   observations, budgets, artifacts, model calls, approvals, and outcomes. The
   workflow substrate owns execution checkpoints; the registry owns research
   truth. Stable identifiers correlate them without treating either as a copy
   of the other.
3. **GitHub adapter.** Git branches, issues, pull requests, checks, releases, and
   protected environments form the engineering control plane.
4. **Agent runner.** Every worker receives a clean task packet, bounded tools,
   time and token budgets, an isolated worktree, and an explicit output schema.
5. **Evaluation runner.** Inspect AI is the preferred agent-evaluation harness
   because it supports datasets, scorers, limits, sandboxed tools, and external
   Claude, Codex, and Gemini agents. Deterministic tests, simulation, replay,
   sealed behavioral cases, and hardware measurements remain separate scorers
   rather than model-written verdicts.
6. **Deployment controller.** Releases progress through simulation, shadow,
   supervised canary, and ordinary operation. Failed gates trigger rollback.
7. **Ledger writer.** Every cycle is appended to the evolution ledger with
   provenance links. Existing records are never rewritten to improve a result.
8. **Monitor.** Health checks detect stalled leases, repeated failures, budget
   exhaustion, regressions, unsafe proposals, and drift in deployed behavior.
9. **Telemetry.** OpenTelemetry carries correlated traces, metrics, and
   privacy-filtered events across the controller, evaluators, and runtime. The
   evolution ledger references immutable evidence but does not replace
   operational telemetry.

Prefect remains an operations-oriented alternative when scheduling and dashboard
needs dominate. LangGraph may run inside a reasoning worker when a task truly
requires branching model state. Neither becomes the release authority or the
source of research truth.

## Evolution Ledger

Every proposed improvement receives a stable experiment identifier. The ledger
must link the physical observation to the engineering outcome.

```yaml
experiment_id: MIOS-EXP-0001
parent_experiment_id: null
campaign_id: MIOS-CAMPAIGN-001
autonomy_level_claimed: A1
trigger:
  observation_ids: []
  detected_by: runtime-monitor
  privacy_class: derived-nonverbatim
hypothesis:
  statement: ""
  expected_mechanism: ""
baseline:
  release: ""
  comparison_condition: fixed_single_agent
  metrics: {}
preregistration:
  artifact_hash: ""
  frozen_at: ""
  primary_metric: ""
  minimum_effect: ""
  sample_size: 0
alternatives: []
selected_design:
  decision_record: ""
risks: []
budgets:
  money_usd: 0
  model_tokens: 0
  wall_clock_hours: 0
  device_memory_mb: 0
evaluation:
  public_suite: ""
  sealed_suite_attestation: ""
  simulation_result: ""
  evaluator_version: ""
  complete_failure_inventory: []
change:
  issue: ""
  branch: ""
  pull_request: ""
  commits: []
review:
  architecture: ""
  safety: ""
  verification: ""
deployment:
  release: ""
  canary_window: ""
  rollback_release: ""
outcome:
  decision: inconclusive
  measured_delta: {}
  human_interventions: []
  autonomy_level_supported: A0
lesson:
  supported_claims: []
  rejected_claims: []
  next_questions: []
```

The implementation should use a validated schema rather than parsing arbitrary
Markdown. Human-readable reports may be rendered from the structured record.
Every record includes a previous-record hash, actor identity, resolved model and
prompt hash when applicable, input and output artifact hashes, privacy class,
budget actuals, and state transition. A correction appends a record that names
the superseded assertion.

## Seed Agent Organization

The coordinator begins with the following roles. Each role receives only the
tools and repository context required for its task.

| **Agent** | **Responsibility** | **May change code** | **May approve itself** |
| --- | --- | ---: | ---: |
| Governor | Applies the constitution, budgets, and escalation rules | No | No |
| Systems Architect | Owns interfaces, decomposition, and decision records | Design documents | No |
| Framework Scout | Finds and compares maintained reusable systems | No | No |
| Embodiment Engineer | Understands Reachy, UNO Q, timing, and hardware constraints | Adapters and tests | No |
| Memory Researcher | Develops episodic, semantic, and procedural memory | Experimental branches | No |
| Learning Researcher | Designs reflection, consolidation, and adaptation | Experimental branches | No |
| Edge Systems Engineer | Enforces latency, memory, energy, and thermal budgets | Optimization branches | No |
| Implementation Engineer | Implements one accepted design | Yes | No |
| Verification Engineer | Creates tests and reproduces claims from a clean context | Tests, not candidate code | No |
| Safety Reviewer | Reviews action authority and failure containment | Protected proposals only | No |
| Research Skeptic | Challenges novelty, causality, metrics, and simpler alternatives | No | No |
| Education Translator | Maps MiOS mechanisms to child interactions and UNO Q labs | Interface and lab proposals | No |
| Release Manager | Advances artifacts through approved environments | Release metadata | No |

The coordinator may propose a new agent only when recurring work cannot be
owned cleanly by an existing role. The proposal must define its authority,
inputs, outputs, evaluation, cost, and retirement condition. Creating more
agents is not itself progress.

No agent may both implement a candidate and provide its decisive review. The
coordinator may synthesize evidence but cannot override a failing protected
check.

Independence has three recorded dimensions. **Context independence** means the
reviewer receives a clean task packet rather than the implementer's conversation.
**Model independence** means a different provider or model family is used.
**Authority independence** means the reviewer cannot change the candidate,
evaluation source, threshold, or release decision. Consequential architecture
requires context and model independence. Physical safety requires authority
independence and deterministic evidence; an AI review alone is never decisive.

## Model Portfolio and Routing

MiOS should use multiple model families to reduce correlated mistakes and to
match cost to difficulty. Model identifiers belong in deployment configuration,
not architectural contracts.

The preferred initial portfolio uses an approved Claude Opus model for sustained
architecture and critical review, an approved Gemini Pro model for independent
research and alternative designs, and the strongest approved Codex GPT model
for repository-native implementation and verification. These are capability
aliases, not promises that a particular preview or numbered release exists. At
execution time the controller discovers the exact available model behind each
alias and records the provider, model identifier, configuration, prompt version,
tools, input and output tokens, cache use, latency, and actual or imputed cost.

Routing follows task evidence rather than brand loyalty:

- Use at least two independent model families for consequential architecture or
  safety analysis.
- Use a strong coding agent for implementation, repository navigation, and test
  repair.
- Use a different model or clean-context agent for decisive review.
- Use smaller, cheaper models for classification, summarization, and routine
  monitoring after their parity is measured.
- Escalate only when a task fails, uncertainty remains high, or expected impact
  justifies the cost.
- Never silently substitute a weaker model for a protected review role.
- Keep model versions fixed inside a controlled comparison and start a new block
  when the provider changes the resolved model.
- Send only synthetic or policy-approved redacted evidence to engineering
  models. Provider access does not imply child-data access.

Model disagreement is preserved as evidence. The coordinator must state why it
selected one proposal and what observation could prove that decision wrong.
Repeated model samples are treated as stochastic measurements. Exact replay is
required for stored artifacts and tool traces, not falsely claimed for remote
model generation.

## Agent Task Packet

Every delegated task must contain the following fields:

```yaml
task_id: ""
experiment_id: ""
role: ""
objective: ""
context_files: []
allowed_tools: []
write_scope: []
prohibited_actions: []
acceptance_tests: []
budgets:
  wall_clock_minutes: 0
  tokens: 0
  money_usd: 0
required_outputs: []
escalation_conditions: []
```

Agents must inspect existing work before implementing. They should reuse a
maintained framework when it satisfies the contracts and target-device budget,
wrap it when its API should remain replaceable, borrow a proven pattern when the
runtime is too heavy, and build only the smallest uncovered component.

## GitHub Development Protocol

GitHub records the system's engineering evolution. It is not the scheduler for
unsafe physical actions.

### Issues

An automatically created issue must cite one or more observations, quantify the
current behavior, identify affected requirements, and distinguish a defect from
an open research question. Duplicate and low-evidence observations are grouped
rather than converted into issue noise.

### Experimental Branches

Each implementation runs in an isolated worktree and branch associated with one
experiment. The worktree starts from the experiment's pinned baseline commit,
not a dirty integration checkout. Agents may not share a writable worktree.
Generated artifacts and private interaction data remain outside public commits.

### Pull Requests

Every pull request contains:

- the preregistered hypothesis and causal mechanism;
- baseline measurements and acceptance thresholds;
- alternatives considered, including doing nothing;
- code, schema, dependency, privacy, and physical risks;
- public evaluation results and links to protected-check attestations;
- target-device resource measurements;
- deployment, monitoring, and rollback instructions;
- known limitations and unresolved disagreement;
- the exact human assistance received.

The agent that wrote the implementation may respond to review but cannot dismiss
the decisive reviewer or modify protected tests.

### Required Checks

The initial protected checks are:

1. formatting, static analysis, dependency policy, and unit tests;
2. contract and integration tests with fake hardware;
3. memory migration, backup, restoration, and privacy tests;
4. deterministic action-envelope, protective-stop, watchdog, and required
   hardware-stop tests;
5. recorded interaction replay and held-out cognitive evaluations;
6. resource measurements on representative edge hardware;
7. simulation or shadow execution for changed physical behavior;
8. independent architecture, verification, and safety reviews;
9. reproducible build with pinned provenance;
10. rollback rehearsal for releases that alter persistent state.

Inspect AI should host agent and cognitive evaluations where its dataset,
sandbox, limit, and scorer abstractions fit. Conventional unit, property,
integration, hardware, and safety tests remain ordinary test programs. A model
grader may supply advisory evidence, but cannot grade deterministic safety or
authorize physical release.

### Merge and Deployment

Ordinary low-risk code may be configured for automatic merge after all checks
and independent reviews pass. Changes affecting physical capabilities, safety,
privacy, credentials, protected evaluations, budgets, or governance require
human approval.

Deployment progresses through four environments:

```text
replay and unit tests → simulation → shadow mode → supervised physical canary
```

Only a signed release artifact may reach the robot. The deployment controller
must retain the last known-good release and restore it automatically when a
canary violates its preregistered bounds.

Candidate code runs on GitHub-hosted or clean ephemeral workers with no robot or
household credentials. A persistent self-hosted runner must never execute
untrusted candidate code. Hardware evaluation uses a separate pull-based worker
that accepts only an already attested artifact and a bounded test manifest. A
least-privilege GitHub App is preferred over a personal access token. GitHub
artifact attestations, an SBOM, and a digest-pinned dependency manifest provide
build provenance once a remote exists; local development uses hashed manifests
until then.

## Runtime Learning Policy

MiOS separates learning by consequence and timescale.

1. **Interaction learning** updates knowledge, identity, preferences, and
   conversational context immediately through validated memory operations.
2. **Consolidation learning** runs during bounded idle windows to resolve
   aliases, identify contradictions, decay unsupported beliefs, and propose
   concepts. It is reversible and evidence preserving.
3. **Policy learning** compares retrieval, reasoning, and skill-selection
   strategies against recorded and held-out episodes.
4. **Skill learning** creates capability implementations inside declared action
   envelopes. New actuator authority requires approval. A skill can select only
   capabilities already admitted by the deterministic supervisor.
5. **Architectural learning** proceeds only through experiment branches and
   pull requests.
6. **Safety changes** never occur autonomously. Agents may identify weaknesses
   and propose stronger controls, but humans govern the protected boundary.

Model fine-tuning is optional and arrives only after memory, retrieval, policy,
and tool improvements have been evaluated. A changed model must pass the same
promotion ladder as changed code.

The interaction Stop control is a cancellation mechanism, not a safety-rated
emergency stop. The safety plan separately defines a protective software stop,
watchdog behavior, and, where the hazard analysis requires it, an independent
power-removal or hardware emergency-stop path. Documentation and tests must not
use these terms interchangeably.

## Monitoring and Reflection Cadence

Continuous evolution does not mean continuous code churn. The controller runs
several bounded cadences:

| **Cadence** | **Activity** | **Output** |
| --- | --- | --- |
| Per interaction | Record state transitions, outcomes, and anomalies | Privacy-filtered episode |
| Every few minutes | Health, queue, latency, error, and safety monitoring | Operational alert or no-op |
| Daily idle window | Memory consolidation and observation clustering | Proposed memory changes and issue candidates |
| Weekly | Select high-evidence improvement hypotheses | Experiment portfolio |
| Per pull request | Independent evaluation and adversarial review | Check attestations |
| Per release | Shadow and canary comparison against baseline | Keep or rollback decision |
| Monthly | Architecture, agent organization, cost, and intervention review | Evolution report |
| Per milestone | Reproduction from a clean environment | Reproducibility attestation |

The weekly portfolio limits work in progress. The controller should prefer one
well-measured improvement over many speculative branches. Anomaly clustering,
minimum evidence, deduplication, and rate limits prevent telemetry from becoming
an automatic issue-spam generator. Monitoring detects and proposes; it does not
silently redefine objectives or thresholds.

## Human Authority

Professor Vijay Janapa Reddi serves as principal investigator and constitutional
authority. Routine engineering should proceed without intervention, but the
system must escalate when it encounters:

- a proposed weakening of safety, privacy, evaluation, or rollback controls;
- a new physical capability or expanded actuator envelope;
- access to new private data, credentials, paid services, or external systems;
- publication, external communication, or changes visible outside the project;
- budget exhaustion or a requested budget increase;
- unresolved disagreement among decisive reviewers;
- repeated inability to reproduce an improvement;
- evidence that the objective or metric is producing harmful incentives;
- an event involving injury, property damage, privacy loss, or loss of control.

Guardian consent does not replace a child's age-appropriate assent. A child can
stop an interaction, decline memory, or ask the robot to forget without needing
to understand the engineering system. Research-data admission remains a
separate adult-controlled decision from ordinary product memory.

Human feedback and intervention are recorded in the ledger. The experiment
should measure where human judgment remains necessary rather than conceal it.

## Constitutional Invariants

The following rules remain protected throughout the experiment:

1. A probabilistic model may propose physical action but cannot directly command
   an actuator.
2. Deterministic local code owns limits, authorization, timeout, interaction
   cancellation, protective stopping, and neutral recovery. An independent
   hardware stop is used when required by the hazard analysis.
3. The robot must remain safe when cloud models, networks, agents, and the
   Evolution Controller are late, unavailable, or wrong.
4. Private interactions and raw media are minimized, access controlled, and
   excluded from public repositories and model prompts unless explicitly
   authorized.
5. Every durable belief retains provenance and can be corrected, forgotten, or
   reset according to policy.
6. Every release is reproducible, attributable to an experiment, observable in
   operation, and reversible.
7. Proposing, implementing, independently evaluating, and authorizing a
   consequential change remain separate authorities.
8. Protected evaluations and thresholds cannot be changed by a candidate to
   make itself pass.
9. The controller operates within explicit compute, cost, time, storage, and
   work-in-progress budgets.
10. The system stops safely rather than improvising when authority or evidence
    is insufficient.
11. Product memory, research data, operational telemetry, and the engineering
    ledger remain distinct stores with explicit admission and deletion rules.
12. No model-generated review may authorize physical safety. Deterministic
    checks and the designated human authority own that decision.

## Execution Phases

### Phase 0. Freeze the Experimental Contract

Inventory the current prototype, establish the baseline, write the protected
constitution, define budgets, and create a sealed-evaluation manifest under an
independent custodian. This phase also records which existing code was written
before autonomous operation. Protected cases remain outside candidate-accessible
storage and may be disclosed after the campaign for reproducibility.

**Exit evidence:** Committed charter, pinned pre-autonomy commit, threat model,
authority map, approved budget, evaluation manifest and custodian attestation,
local baseline build hashes, and an explicit list of hardware evidence deferred
to Phase 2.

### Phase 1. Build the Evolution Substrate

Run a time-bounded bakeoff of DBOS, Temporal, and the minimum custom alternative
against crash recovery, cancellation, idempotent effects, offline operation,
inspection, versioning, ARM support, maintenance burden, and policy enforcement.
Adopt the smallest substrate that passes. Implement structured task packets,
isolated agent worktrees, model adapters, the registry, ledger schema, artifact
store, and `LocalForge`. Use deterministic fixtures before granting model or
repository authority.

**Exit evidence:** The selected substrate survives crash injection at every
transition, resumes without duplicate effects, completes a synthetic
observation-to-local-candidate cycle, detects tampering, enforces budgets and
roles, and reproduces the cycle from a clean directory without network access.

### Phase 2. Establish Independent Assurance

Separate candidate tests from protected evaluations. Add fake hardware,
recorded replay, deterministic action checks, dependency scanning, edge resource
measurement, signed artifacts, and rollback rehearsal. Build the local
capability supervisor, protective stop, watchdog, and privacy-filtered runtime
telemetry boundary before any autonomous physical release.

**Exit evidence:** Deliberately flawed candidates are rejected for functional,
safety, resource, and metric-gaming failures.

### Phase 3. Run Bounded Autonomous Maintenance

Allow the organization to improve tests, observability, reliability, and
internal structure under automatic merge rules. No new physical authority is
introduced.

**Exit evidence:** At least three registered maintenance experiments, including
all failed and inconclusive outcomes, with correct provenance, no critical
protected regression admitted to release, successful rollback, and autonomy
levels supported by intervention records. Accepted changes must improve
preregistered utility after complexity and resource costs.

### Phase 4. Run the First Reflective Improvement

Expose privacy-filtered interaction outcomes. Require MiOS to find a repeated
cognitive or interaction failure, form hypotheses, perform the experiment, and
produce a candidate without a human diagnosis.

**Exit evidence:** One independently verified improvement on a held-out measure
and a complete evolution record from observation through canary outcome. The
same task is compared with fixed single-agent and fixed-team controls at matched
budgets before attributing the improvement to adaptive organization.

### Phase 5. Pass the Maya Test

Run the complete teach, remember, generalize, fail, diagnose, improve, and
retest sequence. Maya's teaching content and held-out variants are not revealed
to the engineering agents in advance.

**Exit evidence:** All Maya Test steps pass, the result survives restart, and a
fresh evaluator reproduces the evidence.

### Phase 6. Transfer to UNO Q

Give the organization the UNO Q documentation, hardware adapter boundary, and
resource constraints. It must reuse or adapt MiOS contracts and explain every
necessary divergence.

**Exit evidence:** Every contract labeled `portable-core` in the frozen contract
manifest passes the same conformance suite unchanged. Platform adapters are
allowed to differ. Core labs run within the UNO Q budget, and final actuator
authorization remains local to the microcontroller boundary.

### Phase 7. Reproduce MiOS From Its Lineage

Provision a clean target using only the repository, signed releases, declared
dependencies, and evolution ledger. Ask a clean-context agent organization to
explain the architecture and reproduce the demonstration.

**Exit evidence:** Two successful independent reconstructions and an explicit
account of discrepancies. Publishable claims are generated only from the frozen
campaign dataset, including negative results and human interventions.

### Campaign 1 Completion Boundary

The first research campaign is bounded so “continuous” does not mean endless.
It ends after all phase gates pass and the system has recorded at least twelve
registered experiments, including three triggered from runtime observations,
one complete reflective improvement, the Maya Test, the UNO Q transfer, and two
clean reconstructions. The campaign may also end at the approved time or cost
limit. In that case it produces a negative or partial result rather than moving
the goalposts.

An experiment counts toward the twelve only if its admission record was frozen
before results and identifies a nonduplicate hypothesis, primary metric,
minimum meaningful effect, comparison condition, budget, and terminal outcome.
Synthetic controller fixtures validate infrastructure but do not count as
embodied-improvement experiments.

## Stop Conditions

The controller must pause safely and request a decision when:

- a protective stop, required hardware stop, or deterministic safety supervisor
  fails a protected test;
- a release causes an unsafe or privacy-impacting physical event;
- rollback cannot restore the last known-good state;
- the monthly budget is exhausted;
- three consecutive experiments fail for the same unresolved infrastructure
  reason;
- protected metrics show sustained regression;
- the controller cannot establish which code, model, data, or prompt produced a
  result;
- agents attempt to alter protected controls outside the governance path;
- the work no longer tests the research claim and has become unbounded feature
  development.

Failure to improve is a valid experimental result. It must not be hidden through
metric changes, selective reporting, or continued spending without a revised
hypothesis.

## Initial Repository Artifacts

The first autonomous milestone should create or formalize this structure while
preserving the working application:

```text
governance/
  constitution.md
  authority-policy.yml
  budgets.yml
  protected-paths.yml
evolution/
  schema/
  experiments/
  reports/
  decisions/
orchestrator/
  workflow/                 # selected durable substrate adapter
  registry/                 # experiment and budget truth
  agents/
  providers/
  github/
  deployment/
evaluation/
  public/
  replay/
  simulation/
  manifests/                 # hashes and metadata only
observability/
  semantic-conventions/
  dashboards/
mios/
  runtime/
  memory/
  reasoning/
  skills/
  safety/
  embodiment/
apps/
  reachy/
  uno_q/
```

Protected test source, consent evidence, credentials, and signing keys live
outside candidate-accessible checkouts. Their in-repository manifests contain
opaque identifiers and hashes, not secret cases or personal data.

This is a target separation of concerns, not permission for an immediate mass
rename. The first architecture agent must map existing modules to these
boundaries and propose incremental migrations that keep Maya's Reachy usable.

## First Autonomous Assignment

After the goal is created, the coordinating agent should perform only the
following first assignment:

1. Read this charter and the current architecture and roadmap.
2. Inventory code, tests, dependencies, deployment paths, hardware access, and
   uncommitted work without modifying unrelated files.
3. Produce a baseline report with measured tests and resource gaps.
4. Draft the constitutional invariants as machine-checkable policies.
5. Propose the minimum Evolution Controller that can complete one synthetic
   observation-to-local-candidate cycle.
6. Obtain clean-context advisory critiques without external spending. Record the
   cross-family Claude, Gemini, and Codex critique as a Phase 1B requirement when
   approved provider profiles become available.
7. Reconcile disagreements and record the reasons for the selected design.
8. Present the Phase 0 artifacts and requested budgets for approval before
   enabling continuous operation or physical deployment.

This first gate is deliberate. The system receives broad freedom to engineer,
but it must prove that it can preserve state, evaluate claims, and stop safely
before it receives persistent external, publication, or physical authority.

## Completion Standard

The goal is complete when the Campaign 1 boundary, Maya Test, UNO Q transfer,
and clean-lineage reproduction have passed; the constitutional invariants
remain intact; the reported metrics and comparison conditions are reproducible;
and the evolution ledger provides a continuous explanation from initial
prototype through final release. Completion refers to the bounded campaign, not
the claim that MiOS can never improve further.

If MiOS cannot meet those conditions within its approved budget, the final
artifact should be a rigorous negative result describing what failed, why the
agent organization could not overcome it, where human intervention remained
essential, and which claims the evidence does and does not support.
