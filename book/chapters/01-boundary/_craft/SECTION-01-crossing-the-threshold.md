# Craft: Crossing the Threshold

- Chapter: `book/chapters/01-boundary/01-boundary.qmd`
- Section: `## Crossing the Threshold`
- Status: AWAITING_APPROVAL
- Cycle: 1
- Last board: 2026-08-20

## Inventory

- Bridge sentence to preface — ownership fence
- Transduction chain (float → PWM → MOSFET → flux → mass) — intuition/mechanism
- Digital vs physical display math — mechanism
- Momentum / `I²R` footnotes — SI preview
- Crash ≠ de-energize coils — mechanism
- Forward pointer — glue

## Board cycle 1

- **Explained well:** copper/PWM path; latch foreshadow; no undo.
- **Named only:** articulated `E_k` and thermal integral (OK as preview if SI section owns the drill).
- **Missing:** optional one-sentence “what you will compute next” without stealing Ch2.

## Bullet outline

Status: AWAITING_APPROVAL

### B1. Keep visceral transduction chain
- **Owns:** Bits become gate drive become mass in motion
- **Transfer:** describe the hardware path from neural float to moving mass
- **Ladder:** intuition → mechanism
- **Depends on:** none
- **Assets:** existing prose (KEEP / light tighten)
- **Notes:** strongest hook in the chapter—do not dilute
- **Expand to:** 1–2 paragraphs (polish only)
- **State:** PROPOSED

### B2. Keep digital-vs-physical display equation
- **Owns:** `W_t` unchanged vs `W_t → W_{t+1} → O_{t+1}`
- **Transfer:** classify a failure as digital-retryable vs physically permanent
- **Ladder:** mechanism
- **Depends on:** B1
- **Assets:** existing display math
- **Notes:** none
- **Expand to:** keep + 1 bridging sentence
- **State:** PROPOSED

### B3. Fence momentum/`I²R` footnotes as previews
- **Owns:** Formulas appear; computation lives in Silicon-and-Steel
- **Transfer:** reader knows these are real limits, not metaphors, and where the drill is
- **Ladder:** mechanism
- **Depends on:** SECTION-04
- **Assets:** one fence sentence
- **Notes:** avoid teaching the integral here
- **Expand to:** 1 sentence
- **State:** PROPOSED

### B4. Keep crash-does-not-zero-PWM claim
- **Owns:** Independent timer clock tree; software death ≠ safe electrical state
- **Transfer:** explain why process crash is not a safety mechanism
- **Ladder:** mechanism
- **Depends on:** B1
- **Assets:** existing paragraph; autopsy will deepen
- **Notes:** autopsy section owns the full six-field case
- **Expand to:** 1 paragraph (KEEP)
- **State:** PROPOSED
