# Chapter 1 Representation Packet

**Status:** composition briefs accepted; assets not yet built  
**Chapter packet:** `CTX-CH01-001`  
**Visual grammar:** two world states, proposal distinct from action, named
authority, visible physical consequence, and a cumulative dossier strip

## Shared Composition Rules

- Use warm paper as the explicit background.
- Use IBM Plex Sans for labels and IBM Plex Mono for \(W_t\), \(o_t\),
  \(p_t\), \(u_t\), identifiers, and field names.
- Keep text at or above a 9-point print equivalent.
- Use structural navy and neutral gray as the base.
- Use amber only for learned proposals.
- Use teal only for observations and allowed action paths.
- Use violet only for accountable authority.
- Use coral only for physical consequence or a terminated path.
- Pair every color with line style, shape, label, or position.
- Keep comparison and contract tables as native Quarto tables.
- Build conceptual figures as SVG with prefixed title, description, marker, and
  clipping identifiers.
- Inspect every artifact at full width, manuscript width, thumbnail size, and in
  grayscale.
- Use no model, robot, board, or partner branding.

These rules retain the useful figure discipline learned from strong technical
books without borrowing another project's visual ontology or page templates.

## `REP-CH01-FIG-001` — Matched Deployments

### Claim

The learned component does not determine whether the system belongs inside the
book's scope. The causal and authority path after inference does.

### Reader Inference

The same observation and learned output may remain advisory in one deployment
and enter a consequential physical loop in another. A proposal becomes system
action only after an authority path permits it.

### Format and Layout

- Authored SVG.
- Full manuscript width.
- Two stacked horizontal panels.
- Identical x-coordinates for `World W_t`, `Observation o_t`, learned component,
  authority decision, physical action, and `World W_{t+1}`.
- Suggested path `book/assets/diagrams/ch01-matched-deployments.svg`.

A neutral bracket above both model boxes reads:

`same observation · same learned component · same proposal`

Only the path after the learned output changes.

### Advisory Deployment

1. Open world field `Tabletop W_t` with the object in its source position and a
   nearby collaborator named.
2. Solid teal information arrow labeled `observed as o_t`.
3. Structural component `Learned object selector` with secondary label
   `suggests object + destination`.
4. Dashed amber arrow labeled `suggestion`.
5. Violet diamond outside the engineered action boundary labeled
   `Person decides`.
6. Human path labeled `human chooses and acts`.
7. Open world field `Tabletop W_{t+1}`.
8. Boundary note `physical authority remains with person`.

Do not label this panel open loop. Advice may influence a person and later
events. The engineered system has not received delegated physical authority.

### Delegated Deployment

1. Reuse the same initial world, observation, and learned component.
2. Dashed amber arrow labeled `proposal p_t`.
3. Violet-outlined diamond labeled `Permission check` with secondary label
   `task and limits approved`.
4. Violet authority lane labeled `workspace owner defines allowed tasks and
   limits`.
5. Solid teal arrow labeled `allowed action u_t`.
6. Physical component labeled `Move or divert`.
7. Solid teal arrow labeled `changes`.
8. Open world field `Tabletop W_{t+1}` with the object in the destination zone.
9. Small coral outline on the changed object.

The engineered boundary encloses observation, learned component, permission
path, and physical action.

### Bottom Labels

- Advisory panel: `learned output remains advisory`.
- Delegated panel: `learned proposal may produce system action`.

Do not place scope verdicts in this first figure. The scope table supplies the
classification after the rule has been taught.

### Omit

- completed belief \(b_t\);
- runtime services;
- detailed enforcement, safe sets, or fallback;
- latency, clocks, measurement, or evidence;
- device, cloud, accelerator, or board placement;
- a generic robot icon; and
- a return arrow to an unchanged world.

### Caption

**The model does not determine the boundary.** With the same observation and
learned selector, the advisory deployment leaves physical action authority with
the person, while the delegated deployment permits the system to issue an
action that produces the next world state.

### Alt Text

Two aligned deployments use the same tabletop observation and learned object
selector. In the advisory deployment, the selector sends a suggestion to a
person, who retains the physical decision. In the delegated deployment, the
selector sends a dashed proposal to a separate permission check, which issues a
solid allowed action that moves the object and produces a changed tabletop
state.

### Rendering Risks

- Keep the person outside the engineered boundary so human action does not look
  like system action.
- Preserve the suggestion-to-person arrow so the advisory panel does not appear
  causally disconnected.
- Align common objects exactly so the comparison remains matched.
- Show the permission check as separate from the learned proposal generator.
  Defer its implementation to Chapter 8.
- Use stacked panels before reducing label size.

## `REP-CH01-TBL-001` — Scope Test

### Claim

This book's working scope requires learned influence, consequential physical
feedback, and delegated system authority. No superficial feature substitutes
for the three checks.

### Format

- Native Quarto table.
- Full manuscript width.
- Rows ordered by the classification argument rather than alphabetically.
- Use `Yes`, `No`, or `Depends`; never color-only marks.

| Deployment | Learned influence | Physical feedback | System authority | Working verdict |
| --- | --- | --- | --- | --- |
| Image-description model | Yes | No | No | Outside |
| Digital recommender | Yes | No under the declared physical boundary | No | Outside |
| Fixed thermostat | No | Yes | Yes | Outside |
| Advisory inspection system | Yes | No system action | No | Outside |
| Teleoperated robot with learned assistance | Yes | Yes | Depends on retained autonomy | Boundary-dependent |
| Learned HVAC controller | Yes | Yes | Yes | Inside |
| Automated rejector | Yes | Yes | Yes | Inside |
| Learned shared-workspace handler | Yes | Yes | Yes | Inside |

Add one note below the table.

> A different boundary can change a verdict. Human action influenced by advice
> is not automatically delegated system action, and a teleoperated robot may
> contain autonomous functions that need their own loop charter.

Outside is a scope classification, not a failure. Do not encode it in coral.
The caption and prose must say that this is the book's working scope rather than
a universal definition of Physical AI.

### Caption

**Three checks prevent classification by appearance.** A learned component,
consequential physical feedback, and delegated system authority are all required
under this book's working scope, and the declared boundary can change the
result.

## `REP-CH01-SCHEMA-001` — Loop Charter

### Claim

A classification becomes auditable only when its causal path, authority path,
affected people, boundary, and assumptions are recorded.

### Format

- Native semantic field tables, not an SVG or rasterized form.
- Full manuscript width.
- Four stacked field groups under `LOOP-001`.
- Three columns throughout: `Field`, `What to record`, and
  `CASE-SWH-001 v0.1`.
- A two-page PDF span is acceptable. Do not shrink type to force one page.

### Group A — Identity and Scope

Include loop identifier, version, status, deployment, task, owner, date, learned
component, learned premise, physical-feedback result, delegated-authority
result, scope verdict, and rationale.

### Group B — Causal Path

Include \(W_t\), \(o_t\), optional \(b_t\), \(p_t\), the permission
result, \(u_t\), \(d_t\), physical consequence, \(W_{t+1}\),
\(o_{t+1}\), and the causal explanation.

### Group C — Authority and People

Include authority granted, authority retained, affected roles, affected
interests, and permission assumptions.

### Group D — Boundary and Assumptions

Include components and processes inside the analysis, deliberate exclusions,
alternative boundary, verdict assumptions, known ambiguity, and unresolved
obligations.

Use mono for field names, neutral fill for prompts, and warm paper for completed
example values. Use teal text only for accepted values and amber with an
explicit `Ambiguous` label where uncertainty remains.

Do not add timing requirements, evidence statistics, runtime services, safety
envelopes, placement fields, or release claims.

### Caption

**A boundary claim becomes auditable only when its causal and authority paths
are recorded.** The completed handler entry exposes what the system may change,
who may permit it, who is affected, and which assumptions could reverse the
verdict.

## `REP-CH01-TBL-002` — Intellectual Lineage

### Claim

The component ideas have established intellectual homes. The book's
contribution lies in systems integration, progressive pedagogy, and the
cumulative engineering dossier.

### Format

Use a native Quarto table with four columns.

| Discipline | Established contribution | Use in this book | Deliberate boundary |
| --- | --- | --- | --- |
| Machine learning systems | Model, data, service, deployment, and evaluation lifecycle | Treat learned capability as a measurable component in a physical loop | No training, compression, compiler, or model-architecture curriculum |
| Control | Feedback, dynamics, delay, stability, and disturbance response | Reason about physical consequence from delayed or imperfect proposals | No full controller-synthesis or stability-theory curriculum |
| Robotics | Sensing, embodiment, planning, manipulation, and physical interaction | Ground observations, proposals, and actions in a body and workspace | No mechanics, kinematics, or motion-planning curriculum |
| Embedded and real-time systems | Timing, resources, execution, and fault handling | Connect implementation behavior to world-derived deadlines and recovery | No hardware-specific programming or RTOS internals course |
| Cyber-physical systems | Coupled computation and physical processes | Define computational and physical behavior as one engineered system | No comprehensive hybrid-systems or formal-verification treatment |
| Systems engineering | Requirements, interfaces, lifecycle, traceability, and assurance cases | Accumulate contracts, evidence, decisions, and assumptions | No complete requirements-management or certification method |
| Human factors and HCI | Automation allocation, legibility, intervention, and human capability | Make affected people and authority part of the architecture | No full interaction-design or human-factors methodology |
| Safety engineering | Hazards, controls, recovery, risk, and assurance | Connect consequence to action limits and release evidence | No domain certification or complete hazard-analysis curriculum |
| Security engineering | Trust, identity, integrity, command authenticity, and attack surfaces | Trace authority across commands, data, updates, and boundaries | No cryptography or secure-systems curriculum |

Add a note stating that the disciplines overlap and the rows show primary
lineage and depth, not exclusive ownership.

Use no icons or per-discipline colors. If four columns become unreadable in PDF,
combine established contribution and use before reducing type.

### Caption

**The synthesis is new to the book, not the component ideas.** Each neighboring
discipline contributes established methods that this book uses to engineer the
complete learned physical system while preserving depth boundaries.

## `REP-CH01-PLATE-001` — Cumulative System Plate 0.1

### Claim

Chapter 1 fixes the causal and authority boundary around a learned proposal that
may become an allowed action and produce the next physical world state.

### Format and Grid

- Authored SVG.
- Full manuscript width.
- Suggested path
  `book/assets/diagrams/system-build/ch01-loop-charter.svg`.
- Stable viewBox `0 0 1200 520`.
- Top lane for authority.
- Main lane for the world-to-world transition.
- Boundary lane for the chosen engineering and causal context.
- Bottom ledger for `LOOP-001`.

Reserve the coordinate system for later observe, estimate, propose, enforce, and
act stages even when Chapter 1 leaves some internal detail unresolved.

### Authority Lane

Use a violet role tag `workspace owner / accountable operator`. A violet line
descends to `Permission check` and is labeled `defines allowed tasks and
limits`. Do not use an unlabeled person icon.

### Main Path

1. Open field `World W_t` with secondary label `object + person positions`.
2. Solid teal arrow `observed as o_t`.
3. Structural component `Learned object selector` with amber output edge.
4. Dashed amber arrow `proposal p_t`.
5. Violet diamond `Permission check` with secondary label `details later`.
6. Solid teal arrow `allowed action u_t`.
7. Physical component `Move or divert`.
8. Solid teal arrow `changes`.
9. Open field `World W_{t+1}` with secondary label
   `object moved · next view differs`.
10. Small coral outline on the changed object.
11. Neutral disturbance arrow `d_t · external change` entering the final world.

A small neutral note below the early path reads `state and belief resolved
later`. It foreshadows \(b_t\) without drawing a completed estimator.

### Boundary Lanes

- Primary navy bracket from observation through physical action labeled
  `engineered boundary chosen in LOOP-001`.
- Lighter bracket spanning both world states and affected people labeled
  `causal analysis includes consequence and affected people`.

### Dossier Strip

Use a sharp structural rectangle labeled
`LOOP-001 · LOOP CHARTER · v0.1`. Include five compact fields:

- task;
- scope verdict;
- causal path;
- authority and people; and
- assumptions.

This is a contract strip, not a takeaway banner.

### Caption

**Chapter 1 fixes the causal and authority boundary.** A learned output remains
a dashed proposal until permission produces an allowed action, and the physical
consequence creates the next world state recorded in `LOOP-001`.

## Cross-Artifact Consistency Check

All five representations must preserve these semantics.

- \(p_t\) is a dashed amber learned proposal.
- The permission check is violet and separate from the learned proposal
  generator. Its implementation is not yet shown.
- \(u_t\) is a solid teal allowed action.
- \(W_t\) and \(W_{t+1}\) are distinct physical world states.
- Advisory human action remains outside delegated system authority.
- The three classification checks appear in the same order.
- `LOOP-001` contains causal path, authority, affected people, boundary, and
  assumptions.
- “Inside” means inside this book's working scope, not a universal field
  definition.
- No artifact suggests that hardware or model family determines the verdict.

Provisional asset production is authorized from these accepted compositions and
may proceed alongside the opening-cluster prose pilot. Final assets must be
reconciled with accepted wording and pass HTML, PDF, manuscript-width,
grayscale, and alt-text review.
