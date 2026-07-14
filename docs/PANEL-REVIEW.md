# Expert Panel Review: Would This Space Agree, and What Do We Uniquely Own?

**Status:** working synthesis for review. Round 1 (8 experts) complete. Round 2
(3 ecosystem incumbents: Pollen Robotics, Hugging Face LeRobot, Nvidia Physical
AI) is running and will be appended.

## Bottom Line

Verdict distribution across the 8-person panel:

- **Endorse-with-reservations:** 7 (embodied-AI researcher, CPS professor, ML-systems/benchmarking, TinyML educator, learning scientist, industry practitioner, K-12/parent)
- **Skeptical:** 1 (maker-community leader)
- **Reject:** 0

Read that honestly. Nobody dismissed it, which means the core is real and not a
rename dressed up. But the endorsements are *conditional*, and the conditions are
strikingly consistent across eight very different vantages. Two framings we lead
with are overclaimed (the "distinct discipline" claim and the "MLPerf for physical
AI" claim), the kit economics are currently incoherent, and the safety story can
teach false confidence. All fixable. None fatal. The unique thing is real, but it
is narrower and more defensible than the current framing.

## The Unique Thing We Actually Own (Panel-Convergent)

This is the answer to "we have to have our own unique thing," and it is not the one
the docs currently lead with. Three independent reviewers (embodied-AI, ML-systems,
industry) arrived at the same place unprompted:

> **The whole field measures the MODEL or the TASK. Nobody measures the LOOP.**
> MLPerf measures a model's accuracy on a frozen dataset. Every robot benchmark
> (RoboSuite, FurnitureBench, RobotArena, LIBERO) measures task success, did it
> grasp the cube. Nobody measures the deployment properties of the *running loop*,
> tail latency, joules per decision, bytes off the device per hour, time-to-safe-
> state, belief drift, and nobody teaches you to defend *where each capability runs*
> with those numbers.

That measurement-and-placement layer, made physically visible on the propose/dispose
boundary and honest enough to ship into a child's bedroom, is the thing we own. It is
the **engineering** layer that sits *above* LeRobot's "learning" and *beneath* Nvidia's
"physical AI." Four components the panel certified as genuinely ours, not borrowed:

1. **Measuring the loop's systems-properties** as a defended, per-property protocol (the axis nobody occupies).
2. **"Placement defended by a number"** as the recurring pedagogical verb (vs "get it working" / "train a policy," which every competitor teaches).
3. **The invisible-to-visible instrumentation move** (LED on missed deadline, MCU refusing a command, byte counter). The maker reviewer: "the most maker-native robotics-teaching hook I've seen in years."
4. **MCU/MPU = propose/dispose = placement-by-chip** as a physically enforced, *measurable* privilege boundary (a great teaching instrument, even though the architecture itself is old).

The moat, exactly as with TinyML, is the **released instrument** (a runnable "measure
the loop" protocol people cite), not the noun. Every reviewer who reached the "next
TinyML" question said the same thing: TinyML became a movement because MLPerf Tiny
*existed*. Ship the protocol as software or this stays a very good book, not a
movement.

## What We Must Stop Claiming (and the Prior Art That Owns It)

The panel was unanimous and specific here. Each overclaim has a 25-year lineage we
currently do not cite, and a reviewer who will make the whole review about it.

| **We claim** | **Who actually owns it** | **The fix** |
| --- | --- | --- |
| "Distinct discipline" | It's a *synthesis*, not a new field | Reframe to "the missing engineering layer," cite the lineage |
| Propose/dispose as our signature | **Simplex architecture** (Sha 1998); **Neural Simplex** (2020); runtime assurance, control barrier functions, shielding | Name it, state our delta: we make the boundary *observable and measurable* at kit scale |
| Nine properties + budget identity | The **"-ilities"** / ISO 25010 / non-functional requirements | Keep as a teaching device, sell it as one, not as discovery |
| "Open world" as our novelty | **ISO 21448 SOTIF** (automotive's whole answer to "the world exceeds the design") | Cite it, reframe as "the SOTIF problem, taught" |
| Placement | HW/SW co-design partitioning + edge/cloud offloading + System 1/2 | Established, credit it |
| "MLPerf for physical AI" | Overreaches: a closed loop in an open world can't freeze the stimulus, the thing that made MLPerf reproducible | Split into two tiers (below) |

The two-tier fix for the benchmark claim (ML-systems reviewer, the sharpest single
contribution of the panel):

- **Benchmark tier** = the *replay slice*. Push a fixed sensor log through the stack, measure latency/energy/memory/egress deterministically with error bars. *This* is genuinely "MLPerf one level up." Call only this a benchmark.
- **Characterization tier** = the closed-loop-in-open-world numbers. Report with variance and stop calling them a benchmark.
- Add a **task-efficacy floor** to every property, or a do-nothing null system wins every one of the nine (it is maximally timely, safe, private, and energy-cheap). MLPerf gates cost behind an accuracy threshold for exactly this reason.

## The Positioning Collision (Two Incumbents Already Own the Ground)

Multiple reviewers independently flagged this, and it is the strategic crux:

- **Nvidia owns the term.** In 2026 "Physical AI" = GR00T, Cosmos, Jetson Thor, *building and training the learned controller*. Our scope is the exact opposite (the model is a black-box component). A reader sees "Physical AI Engineering," expects to build a VLA, and gets a course that measures one.
- **Hugging Face / LeRobot owns the hardware-and-hands story.** The free LeRobot Robot Learning Course teaches imitation/RL/VLA on $100-300 arms, and **our hero robot, Reachy Mini, is theirs** (Pollen Robotics, now HF). We are launching a paid kit-course into a niche where a $4T company owns the word and the incumbent free course owns the hardware.

TinyML worked because *nobody owned the word* and Vijay's group got to define it. Here
the word is taken and the adjacent course is free. The fix the panel points to: own
**"physical AI *engineering*"** as a distinct, explicit layer, the deployment/assurance/
measurement discipline, explicitly *not* GR00T/Cosmos model-building and explicitly
*not* the LeRobot policy-training course. Say this by name in Chapter 1. Silence reads
as either bait-and-switch or naivety. (Round 2 is probing exactly whether these
incumbents see us as complementary or redundant.)

## The Must-Fix List (Grouped)

**A. The instrument (this is the movement-maker).**
- Promote the measurement protocol from Appendix A to a front-and-center, released, versioned, runnable spec + reference harness. It is the single most defensible asset and currently the least concrete. If it stays prose, cut the MLPerf analogy, experts will call the bluff.

**B. Kit economics + first-hour win (this is the movement-killer if unfixed).**
- The kit story is incoherent in our own words: UNO Q is now $59-79 (rose from $44); the "hero" Reachy Mini is $399-499 *and runs a Raspberry Pi CM4, not the UNO Q we teach*. So the flagship demo is not reproducible on the taught board, and the taught board has no flagship demo.
- UNO Q is a Linux SBC, which breaks TinyML's determinism and zero-sysadmin on-ramp (30 boards = 30 failure modes). Ship a frozen, offline, one-click re-flashable image and treat break-proofness as a first-class deliverable.
- **Firewall the hero from the required path**: state in writing that all six outcomes are assessable on the bare $59-79 UNO Q; Reachy is aspirational, never a lab dependency.
- **Lead with the wow, not the measurement.** "The robot saw me and talked back" recruits the novice; "measure the invisible property" is the convert's payoff. Sell the magic first, then puncture it with the measurement twist in the same session.
- **The $79 "MCU physically vetoes the AI" demo is the hook.** It needs only the board plus a servo, it is the one place thesis and silicon align perfectly, and "watch the safety chip refuse the AI's dumb command" is this kit's "it heard me say yes." Lead the book and the marketing with it.

**C. Safety honesty (non-negotiable with a child in frame).**
- Teaching "MCU disposes, therefore safe" without forward-invariance, a proven backup controller, and a *bounded, measured* dispose-path latency manufactures false assurance, "the single most dangerous thing a real-time-safety course can do." Real dispose channels are certified, independent, redundant (ISO 13482, SIL/PL target). Teach that the kit *models* an enforcer but is not a safety-rated one.
- Teach where sim/replay/shadow confidence is *worth zero*: replay is invalid the instant the policy would diverge from the log; sim lies hardest on contact, sensor timing, and actuator delay, the safety-relevant cases.

**D. Learning design (specific, from the learning scientist).**
- The capstone is ~90% O4 (placement). It does not gate O2, O5, O6, so the profile's six co-equal outcomes are "marketing, not assessment." Make the ship/no-ship gate (O5), the runtime design-defense (O2), and the teach/approve/forget flow (O6) first-class capstone deliverables with their own pass bars.
- The design/synthesis muscle the book says is central is under-practiced: the student only thickens the handed-down runtime, never architects a greenfield one. Add one greenfield synthesis lab on an unfamiliar embodiment.
- Unpack the compound outcomes (O3/O5/O6 each bundle 5-6 sub-skills). Give diagnosis a taught method (hypothesis to bisect to confirm) plus one graded checkpoint before the capstone.
- **"Three altitudes" is kidding itself.** It is one concept curriculum (engineer) + a difficulty-variant (maker) + a use-case not on the ladder (the 6-year-old). Maya is not a rung; she is the *context* that keeps the engineering honest. Reframe to "one system, three relationships to it."

**E. Child ethics (from the K-12/parent reviewer, load-bearing not decorative).**
- The reference build sends a child's words to the cloud (Claude), the exact surface of the FTC/Amazon Echo Dot Kids COPPA case. The book names the gate; the hero walks a child through it. Make Maya's own words the worked egress example in Ch12/13, with the FTC case as the war story.
- Teach the robot's mortality. A years-long child companion that can be switched off from a datacenter (Moxie, Jibo, kids cried) must teach graceful offline degradation, data portability, and an honest attachment/exit conversation.
- Build one real kid-facing artifact or drop the three-altitudes claim; do not let the warmest claim be the unbuilt one.

## Per-Panelist Verdicts

| **Persona** | **Verdict** | **Sharpest single objection** |
| --- | --- | --- |
| Embodied-AI researcher | Endorse-w/-reservations | Name + scope collide, both already owned (Nvidia term, LeRobot course + hardware) |
| CPS / real-time professor | Endorse-w/-reservations | Propose/dispose is Simplex/RTA, uncited; box-clamp is a filter, not a safety guarantee |
| ML-systems / benchmarking | Endorse-w/-reservations | Closed loop can't freeze the stimulus (kills comparability); null system wins every property |
| TinyML educator | Endorse-w/-reservations | Linux SBC breaks determinism + zero-sysadmin on-ramp; grad-level prereqs; audience undecided |
| Learning scientist | Endorse-w/-reservations | Capstone samples 1 of 6 outcomes; synthesis muscle it declares central is under-built |
| Maker-community leader | **Skeptical** | $400-600 across two mismatched platforms; hero doesn't run the board you teach |
| Industry practitioner | Endorse-w/-reservations | Teaches the safety *pattern*, not the safety *case*; no industrial nouns (ROS2/tf2/BT) |
| K-12 educator / parent | Endorse-w/-reservations | Kid altitude asserted not built; cloud brain walks a child through the very gate the book preaches |

## Recurring Sources the Panel Cited

- **Safety lineage:** Sha, Simplex (IEEE Software 2001); Neural Simplex (NFM 2020); Black-Box Simplex; Cofer et al., Run-Time Assurance (NFM 2020); control barrier functions; shielding (Alshiekh AAAI 2018); ISO 21448 SOTIF; ISO 26262 FTTI; ISO 13482.
- **Competing kits/courses:** HF LeRobot + Robot Learning Course; SO-101/SO-ARM101 ($100-240); Nvidia JetBot / DLI robotics teaching kit; Hiwonder Jetson rigs; Petoi; original TinyML (Nano 33 BLE Sense).
- **Benchmark prior art:** MLPerf Inference/Tiny/Mobile; RoboSuite; FurnitureBench; SceneReplica; RobotArena; the embodied-eval reproducibility crisis.
- **Term owner:** Nvidia Physical AI (GR00T, Cosmos, Jetson Thor).
- **Child ethics:** FTC/DOJ v. Amazon (Alexa/COPPA, 2023); Moxie/Jibo shutdown coverage; child-robot interaction ethics reviews.
- **Hardware ground truth:** Arduino UNO Q ($59/$79, price rose from $44/$59; Debian; hub+cable not in box); Reachy Mini ($399 Lite / $499 Wireless; Raspberry Pi CM4; HF/Pollen).

## Round 2: Ecosystem Incumbents (Complete)

The three players who own the adjacent turf, asked bluntly: do we have our own
unique thing, or are we reinventing yours? **All three independently ceded the axis
to us** — the strongest possible validation — while drawing a precise boundary
around what is actually defensible and issuing one shared warning.

**Verdicts:**
- **Pollen Robotics / Reachy (now HF):** Complementary-but-skeptical. Would collaborate on the measurement protocol specifically (a "loop-property card" as an HF Hub artifact). Keeps the paid Arduino kit at arm's length (open/free identity clash).
- **HF LeRobot lead:** Complementary-but-we're-closing-it. The loop-measurement gap is real today, but v0.6.0 ("Closing the Loop") walked them into the deployment/eval half, and they could add a `lerobot-profile` subcommand in one release cycle.
- **Nvidia Physical AI / DLI:** Complementary-but-brand-will-drown-it. Structurally cede the axis (it points customers *off* their silicon), but "Physical AI" is their headline noun and "engineering" is a weak modifier on it.

**What all three agree we uniquely own** (and none will build):

> A released, runnable protocol that puts a defended number on the deployment
> properties of the whole running loop (tail latency, joules/decision, egress
> bytes/hour, time-to-safe-state, drift) and uses those numbers to place each
> capability (loop/box/chip), plus the egress/privacy/safety-to-a-child's-home
> governance layer. In LeRobot's words: "the part of physical AI engineering that
> neither Nvidia's GR00T nor my LeRobot wants to own."

**The one warning all three issue: the window is closing.** The moat is the shipped
instrument, not the book. LeRobot, most bluntly: "If their measurement protocol
stays prose in Appendix A, I can add a `lerobot-profile` subcommand that emits
tail-latency / joules / bytes on a replay slice in one release cycle, and I vacuum
up the systems-metrics gap before their Chapter 1 ships." Ship the instrument,
versioned and cited, or lose the axis to a free incumbent with the distribution to
make it the default the day it lands.

**The precise defensible boundary** (concede these, plant the flag there):
- CONCEDE latency-by-placement. LeRobot owns it (Real-Time Chunking; async-inference degradation factor across Jetson/edge/cloud).
- CONCEDE the safety *case*. Nvidia Halos for Robotics (certified to IEC 61508 / ISO 13849) owns it. Propose/dispose is a *teaching instrument*, not a safety claim.
- CONCEDE model internals + task-success eval. LeRobot's whole reason to exist.
- CLAIM the model-as-black-box "measure the deployed loop" instrument + the COPPA-shaped, child-in-the-home governance layer. Defensible for years because it is orthogonal to how both incumbents make money.

**The name decision** (Nvidia, blunt): "Physical AI" is owned. Either hard-fork the
noun (lead with the axis — the Loop / Deployment / Placement — or coin a term) or
relegate "physical AI" to a single Chapter-1 sentence that names Nvidia and says "we
measure and place the loop; we do not build the brain."

**The positioning** (both HF voices agree): build ON the stack, not beside it. Frame
as the deploy-and-govern layer *downstream* of the LeRobot course and they co-brand
and cross-link. Make the instrument **vendor-neutral across the whole spectrum**
($59 UNO Q → $249 Orin Nano → $3,499 Thor). Nvidia: "runs only on the cheap board →
reads as a toy; spans $59→$3,499 → reads as a discipline," and they would point DLI
educators at it.

**The strategic fork this forces (yours to decide):** the incumbents' advice (build
on SmolVLA / lerobot-rollout / Reachy, downstream of the LeRobot course) pulls partly
against the Arduino/Qualcomm commission (the UNO Q and its MCU/MPU coupling are the
point). These reconcile cleanly *if* the UNO Q stays the coupling-teaching rig and
the propose/dispose hook demo while the common measurement method remains
vendor-neutral and spans everything. But how tightly to couple to the HF ecosystem
versus stay Arduino-native is a real decision only you can make.

**Reachy-as-hero, resolved** (Pollen): Reachy Mini has *no* propose/dispose boundary
(one CM4 brain; the peripheral MCUs in the servos and audio DSP are smart peripherals,
not an independent enforcer), so the "$79 MCU vetoes the AI" demo cannot run on it.
Their reframe is stronger than hiding it: make Reachy the **"no-enforcer" case study**
that teaches the *cost* of not having the boundary (single brain, learned controller,
no independent dispose, shipping into a kid's room), and frame single-brain as
placement at a lower risk scale, not the naive thing before you learn better.

**Two factual corrections from Pollen** (they made a point of it, since we preach
measurement): Reachy Mini runs a **CM4** (this vindicates our original Appendix C; the
maker reviewer's "Pi 5" was wrong), and it is **$399 Lite / $499 Wireless**. Corrected
above.

> **Caveat on the specifics:** the incumbent product claims (LeRobot v0.6.0, a
> `lerobot-profile` subcommand, a LeRobot CVE, Nvidia Halos dates, GR00T rankings,
> exact prices) come from the personas' web searches and one agent corrected
> another's fact. Treat them as leads to verify before anything public. The strategic
> conclusions are robust regardless of whether every cited product detail is precise.

---

## Round 3: The Sharpened Thesis Under Expert Fire (6 reviewers)

Six focused reviewers on the closed-loop / freshness-bound thesis: an information
theorist, a control theorist, an embodied-AI researcher, an ML-systems/benchmarking
expert, a learning scientist, and a science-writer skeptic. Center of gravity: is the
freshness bound thermodynamics or cybernetics?

**Verdict: as worded, cybernetics. Rescuable to thermodynamics, and the panel handed
over the exact, cited path.** Nobody rejected the direction, all agreed the shift from
"new field" to "engineering discipline defined by a constraint" is right and stronger.
But "the Carnot limit of the field," as stated, does not survive contact with the
people who own the relevant theorems.

### The freshness bound is three known theorems in one slogan (unanimous)

All three technical reviewers decomposed it and named the prior art the book does not
yet cite:

- **T1, estimation:** MMSE of the current state given a sample of age Δ is a known monotone function of age; for an Ornstein-Uhlenbeck source, MMSE(Δ) = σ²(1−e^{−2θΔ}). This makes "the world's timescale" precise and measurable, it is the source's decorrelation time 1/θ.
- **T2, information:** the data-processing inequality. No downstream computation restores information the delay destroyed. *This* is the real "Shannon" claim; name it as such.
- **T3, control:** the dead-time / delay-margin bandwidth limit (Bode, Nyquist). Loop delay τ caps achievable bandwidth; past it no controller can track. Undergraduate sampled-data control, currently missing as a first-class statement.
- **The formal metric already exists and is uncited: Age of Information** (Kaul, Yates, Gruteser 2012). A decade-old field owns the book's load-bearing concept. Not citing it is "a bridging-clause failure on the book's own load-bearing concept."

### Two clauses are wrong or overclaimed (unanimous)

- **"Carnot limit of the field" overclaims.** Carnot is a closed-form inviolable frontier; this is a monotone truism plus known theorems. The honest, still-strong, demonstrable-on-a-$59-board version is already in the outline: "you cannot be both fully informed and fully current."
- **"Past the wall, more intelligence buys nothing" is FALSE** (two reviewers killed it independently). In the predictable regime a world model acts on a *prediction*, so error collapses to the *innovation* (entropy the world generates over the delay), not the raw age. Intelligence buys back the predictable part. And empirically the async-inference frontier (Real-Time Chunking, VLASH) routes around a single wall by running multi-rate, plan slow, act fast. The book's own Ch7 two-speed brain half-implements this and quietly contradicts Ch2. The fix makes the World Model chapter *the buy-back machine* and Ch7 the *resolution* of Ch2.
- **Raw age is the retired metric.** The field moved to Age of *Incorrect* Information and Value-of-Information, which is *non-monotone* in age and set by the plant's dynamics. Demote raw age to a source-agnostic surrogate; the real object is the measured value-decay curve.

### Where to plant the flag (what is genuinely new)

- **The setting, not the bound.** Classical dead-time theory assumes a cheap fixed controller. Here the controller is a large learned model whose inference latency *grows with capability*, so capability-vs-freshness is a monotone, self-defeating trade no classical control faced. Claim that.
- **The dimensionless number (the thermodynamics move):** put **η_loop = loop_latency / world_timescale** on the card. A system reporting "η_loop = 0.3" reports against a bound the way an engine reports against Carnot. None of the five current card metrics *is* the fundamental; they are hygiene. η_loop is the entropy-analog.
- **The crux as a law:** "freshness is comparable only within a frozen world-dynamics regime; unfreeze the world and you have characterization, not measurement." The replay tier is its operational embodiment.

### The fundamental is TWO (or three), not one

- **Embodied-AI:** time is the *secondary* axis for learned policies. The dominant real-robot failure is the *distribution* axis, action becomes next input, error compounds, policy drives itself OOD (Ross-Bagnell: O(T²ε) closed-loop vs O(Tε) open-loop), often at *quasi-static* tasks where the world isn't moving. The book black-boxes the axis that dominates.
- **Information theorist:** split perishability (estimation/info) from irreversibility (control). Two prices, two theorems.
- **Learning scientist:** three faces, time / irreversibility / persistence-and-exposure. Governance chapters (Ch6, 9, 12, 13) do NOT descend from "time"; forcing them teaches students privacy is a latency problem.
- **Consensus:** don't crown time alone. Name the distribution axis honestly, scope it out, signpost where it's taught (LeRobot). Broaden the spine to its real faces so governance chapters are children, not hostages.

### Measurement Before the Book (Insight Retained, Product Rejected)

The reviewers were right that the measurement method must precede strong claims,
but the later product decision rejects a separately named instrument. It would add
another product before repeated labs have demonstrated a stable common substrate.
The retained requirements are narrower and more useful:

- **Define the number before the chapter uses it.** Every lab needs an operational definition before it can make a property visible.
- **Only the replay tier is a benchmark.** A frozen sensor log carries ground truth and supports a task-efficacy floor so a do-nothing system cannot win.
- **Treat live closed-loop results as characterization.** Compare A versus B on a fixed rig rather than publishing absolute cross-lab claims.
- **Measure externally when instrumentation perturbs the hot path.** Use GPIO timing, an external power rail, or another independent reference when self-measurement would distort the result.
- **Embed the reusable harness in the reference runtime.** Each lab emits the same evidence record, while a standalone tool remains deferred until real repetition earns it.

### Structure and tightening (partly contested)

- **Promote Measurement Protocol to an early chapter: UNANIMOUS yes.**
- **Split the overloaded Ch2: UNANIMOUS.** Name the nine properties once as a one-page map; introduce each just-in-time where it binds; move the budget identity to Ch10.
- **Merge Perception + World Model: LEAN NO.** The world model is a *state estimator/observer* (Kalman); don't conflate measurement with estimate. Ch5 is where real systems die. If merged, one chapter, two scaffolded halves, two labs, estimation content as the spine. Alternative: merge Meaning + Cognition instead (both the slow semantic path).
- **Dissolve Memory: CONTESTED.** Three say OK (persistence is a different axis); learning scientist says NO, false economy that buries forgetting-as-first-class (the warm COPPA-defensible idea) into an overloaded Ch13. Compromise: keep forgetting prominent, don't just dump it.
- **Ch0 quickstart: only as a swap,** compress Ch1 simultaneously.
- **Labs:** visible-property law is excellent design, but *visible is not measured*. Every lab needs a mandatory rung, visible signal → the number → the placement it justifies. Signature demos (Lab 3, Lab 8) currently stop at the perceptual.
- **Diagnosis still has no taught method.** Add a short reusable procedure (hypothesis → bisect → confirm) early, plus one graded checkpoint before the capstone.
- **Capstone:** distribute the summative load; add the greenfield synthesis task (the design muscle is still never truly exercised).

### The dichotomy, the name, and Maya

- **Open/closed is a great teaching device, a leaky field-name.** Closed loop dates to Maxwell 1868; HFT is closed-loop AI with no robot; a TinyML wake-word gating an actuator closes a loop. Rigorous cut: "does the policy change its own future input distribution?" Keep it to orient beginners; don't plant a field-flag on it.
- **Own the substrate-independence.** The bound is a control/estimation limit, not a uniquely physical one; physical AI is where it bites hardest and where irreversibility is literal. Stating it (with the HFT counterexample) pre-empts "cybernetics with a robot on the cover."
- **Maya:** make her load-bearing (her actual words as the Ch12 egress example) or make her the dedication. "Warmth is fine. Warmth doing argumentative work is the tell."

> **Caveat:** the technical results cited (Age of Information, Bode sensitivity
> integral, the data-rate theorem Σlog|λ|, MMSE-OU, DAgger O(T²ε), RTC/VLASH) are
> real established results, but came via the reviewers' web searches. Verify the exact
> statements and citations before they go in the book.

---

## Round 4: External Cross-Check — Gemini 3.1 Pro + Codex (gpt-5.6, xhigh)

Two frontier models outside the Claude family reviewed the full outline cold. The
value is where they *independently converge* with the three Claude panels (that
collapses uncertainty into a decision) and the one place they open a genuine fork.

### Now unanimous across every source — decisions, not opinions

- **Cut the Memory chapter.** Nothing in it is uniquely closed-loop. Forgetting → Human Loop; state/estimator history → World Model or Runtime; retention/egress → Safety. (Gemini, Codex, and 4 Claude reviewers.)
- **Merge Meaning + Cognition** into one "Reasoner / slow semantic path" chapter. (Gemini, Codex, Claude embodied.)
- **Quickstart is unnumbered front matter,** not a chapter. (Both externals + Claude learning scientist.)
- **Two axes, not one spine.** Codex names them: the **feedback constraint** (freshness, uncertainty, delay, stability, placement, recovery) and the **delegation constraint** (authority, safety, privacy, consent, inspectability, reversibility-of-deployment). Governance does not descend from "the loop prices time." **Four independent voices** now (Codex, Gemini's "two books stapled," Claude science-writer's "two spines," Claude learning scientist). The most-converged structural finding in the whole review.
- **Drop "the Carnot limit," scope η_loop.** Keep it, but report per-loop and per-regime with a specified latency percentile and a precisely defined task timescale; a single scalar hides the binding failure mode. (Codex sharp; Claude control + info + science-writer.)
- **Reconcile the two docs** (OUTLINE.md 14 ch / measurement in Appendix A vs CHAPTER-OUTLINES.md 15 ch / measurement in Ch4). They currently disagree on the architecture.

### Sequence: measurement even earlier

Codex: Measurement should come **immediately after Ch2, before the Runtime**, because prescribing a service architecture before teaching how requirements are measured "makes the runtime look like the author's preferred framework rather than something derived from constraints." So: definition → limit → **measurement** → runtime → loop components → placement → validation & governance.

### The genuine fork: the triad's composition

Both externals independently say the beloved triad's first two parts overlap, and both name a *missing* fundamental, but different ones:

- **#1 "perishable" and #2 "partial and stale" are largely one claim** (freshness, sensor-end vs estimator-end). Codex adds neither #2 nor #3 is *uniquely* closed-loop: partial observability exists open-loop too, and many actions are reversible. "Action is irreversible" is literally false as a universal; the rigorous claim is path-dependence.
- **Codex's missing fundamental: ENDOGENEITY.** The action changes the distribution its next decision depends on, the uniquely-closed-loop property, and the book black-boxes it out. Its effects (policy-induced distribution shift, compounding error, recovery frequency, envelope departure) are measurable *without* teaching model internals. Backed by the Claude embodied + control reviewers, so three voices.
- **Gemini's missing fundamental: ENERGY.** For a *physical* AI book from the TinyML lineage, Joules is the brutal constraint; without it "this is just a book on control theory." Make the triad Time / Energy / Consequence, and the Placement Map a true 3-D problem.
- **Reconciliation (my read):** by Codex's own uniqueness test, energy is not the closed-loop differentiator (open-loop TinyML is all about energy), so **endogeneity is the better fundamental** (the closed-loop signature the book currently hides), while **energy is a first-class measured property and the "physical" framing**, prominent in the manifesto and placement, but not a fourth "price." Keep the beautiful triad as the *experiential* framing, and have Ch2 separate it into a **claims hierarchy** (theorem-backed / heuristic / metaphor). Poetry up top, rigor underneath.

### Biggest risk, sharpened: metrology, not just shipping

Codex raises the measurement bar above "ship it." A discipline needs operational
definitions, calibration, uncertainty intervals, repeatability, reference tasks,
comparison rules, negative controls, and *evidence the measurements predict
engineering outcomes*. The reference implementation and labs must show that a
placement chosen from their numbers beats plausible alternatives under controlled
perturbation, reproducibly across ≥3 systems with different dynamics. Otherwise
η_loop is "vocabulary from a compelling book, not an engineering standard." If the
method does not validate, narrow the "new discipline" claim before publishing.
