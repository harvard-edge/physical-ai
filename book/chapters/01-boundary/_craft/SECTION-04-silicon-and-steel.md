# Craft: Physical Constraints in Silicon and Steel

- Chapter: `book/chapters/01-boundary/01-boundary.qmd`
- Section: `## Physical Constraints in Silicon and Steel`
- Status: AWAITING_APPROVAL
- Cycle: 1
- Last board: 2026-08-20

## Inventory

- Sim vs bench intro + tbl-software-vs-physics
- Momentum / `E_k` subsection
- Joule heating subsection
- Inductive rise subsection
- Backlash / jerk subsection

## Board cycle 1

- **Explained well:** why each phenomenon breaks sim assumptions; comparison table.
- **Named only / thin:** formulas without a worked kit-scale number (blocks Obj. 2).
- **Safety/Student:** need one SI drill OR narrow objectives.

## Bullet outline

Status: AWAITING_APPROVAL

### B1. Keep four-phenomenon structure + comparison table
- **Owns:** Momentum, heat, inductance, backlash/jerk as systems impacts
- **Transfer:** map each row of tbl-software-vs-physics to a failure mode
- **Ladder:** intuition → mechanism
- **Depends on:** Crossing the Threshold
- **Assets:** tbl-software-vs-physics
- **Notes:** KEEP skeleton
- **Expand to:** light bridges only
- **State:** PROPOSED

### B2. Add one worked SI example (momentum or travel-under-latch)
- **Owns:** Transfer for “Quantify” objective
- **Transfer:** compute `p` or `E_k` for stated `m`,`v` OR distance traveled during a stated latch window (`v·Δt`) and interpret
- **Ladder:** SI rigor
- **Depends on:** B1
- **Assets:** new short worked example (desk-kit or autopsy numbers)
- **Notes:** Prefer autopsy-aligned: e.g. 1.2 m/s × 50 ms latch → 60 mm—enough to crush a fixture. Pick ONE drill, not four.
- **Expand to:** 1–2 paragraphs
- **State:** PROPOSED

### B3. Keep `I²R` as bound language; defer continuous-rating derivation
- **Owns:** Heat as irreversible budget preview
- **Transfer:** state why continuous stall current is a release constraint, not a peak-torque brag
- **Ladder:** mechanism
- **Depends on:** B1
- **Assets:** existing ODE/integral (preview)
- **Notes:** Full `I_cont` derivation → Ch2 thermal column
- **Expand to:** 1 fence sentence
- **State:** PROPOSED

### B4. Keep `τ_e = L/R` as why torque is not instantaneous
- **Owns:** Electrical delay before magnetic force
- **Transfer:** explain why zero software latency still leaves actuation lag
- **Ladder:** mechanism
- **Depends on:** B1
- **Assets:** existing V=RI+L dI/dt equation
- **Notes:** KEEP; no deep FOC
- **Expand to:** KEEP
- **State:** PROPOSED

### B5. Keep backlash/jerk as gearbox protection preview
- **Owns:** Discontinuous commands damage mechanisms
- **Transfer:** name jerk/torque-rate as invariants the MCU will later clamp
- **Ladder:** intuition
- **Depends on:** B1
- **Assets:** existing prose
- **Notes:** clamps owned in loop charter / Ch8
- **Expand to:** KEEP
- **State:** PROPOSED
