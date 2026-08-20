# Craft: The Proposal and Permission Privilege Split

- Chapter: `book/chapters/01-boundary/01-boundary.qmd`
- Section: `## The Proposal and Permission Privilege Split`
- Status: AWAITING_APPROVAL
- Cycle: 1
- Last board: 2026-08-20

## Inventory

- Monolithic fallacy intro
- fig-anatomy
- Two-brain prose + CBF QP display
- callout-contract (lease, chunk, CBF, STO)
- tbl-processor-comparison
- Silicon-level privilege isolation subsection

## Board cycle 1

- **Explained well:** why monolithic pixels→PWM fails; MPU vs MCU roles; anatomy figure.
- **Named only:** CBF QP, FOC, lease fields, chunk `H`—sound taught.
- **Missing:** UNO Q who-may-write-PWM; heartbeat/lease expiry as mechanism with ms budget.
- **Embedded:** firewall/SRAM claims need bench-observable sentence.

## Bullet outline

Status: AWAITING_APPROVAL

### B1. Keep monolithic-fallacy motivation
- **Owns:** Why end-to-end to PWM violates fault containment
- **Transfer:** argue against pixels→PWM on privilege grounds (not taste)
- **Ladder:** intuition → mechanism
- **Depends on:** autopsy
- **Assets:** existing opening + Saltzer/Brooks cites
- **Notes:** KEEP
- **Expand to:** polish only
- **State:** PROPOSED

### B2. Keep two-brain split + anatomy figure
- **Owns:** Untrusted proposal vs trusted permission substrates
- **Transfer:** assign VLM/ACT to MPU and PWM/gate-enable to MCU
- **Ladder:** mechanism
- **Depends on:** B1
- **Assets:** fig-anatomy; tbl-processor-comparison
- **Notes:** KEEP rates as instances, not eternal law (Ch3 deepens)
- **Expand to:** KEEP
- **State:** PROPOSED

### B3. Fence CBF QP and FOC as named previews
- **Owns:** Honesty about what is taught vs pointed
- **Transfer:** know `h(x)≥0` / QP / FOC will be built in Ch8; here only “MCU projects/refuses”
- **Ladder:** mechanism (fence)
- **Depends on:** B2
- **Assets:** soften display math or caption with “preview; Ch8”
- **Notes:** Do not delete the idea—fence it
- **Expand to:** 1–2 sentences
- **State:** PROPOSED

### B4. Teach lease/heartbeat revocation as a mechanism
- **Owns:** How permission dies when proposal dies
- **Transfer:** state a concrete rule: if heartbeat/lease age `> τ` ms, MCU cuts PWM / Cat-1 brake (pick one SI budget, e.g. 10–20 ms class) 
- **Ladder:** mechanism + SI rigor
- **Depends on:** B2
- **Assets:** new short paragraph; contract row stays
- **Notes:** Abstention depth → Ch6; here only timeout→revoke
- **Expand to:** 1–2 paragraphs
- **State:** PROPOSED

### B5. Add UNO Q privilege map (bench-observable)
- **Owns:** Kit instantiation of the split
- **Transfer:** say which core proposes, which alone drives timers, what mailbox the student can observe
- **Ladder:** mechanism
- **Depends on:** B2
- **Assets:** 1 paragraph; optional pointer to appendix UNO Q ref
- **Notes:** No vendor brochure—contract language
- **Expand to:** 1 paragraph
- **State:** PROPOSED

### B6. Keep contract callout; strip `<br>` if any remain
- **Owns:** Proposal–permission table
- **Transfer:** read MPU/MCU/escalation rows as the chapter contract
- **Ladder:** mechanism
- **Depends on:** B3–B5
- **Assets:** callout-contract
- **Notes:** CMOS table cells single-line
- **Expand to:** table cleanup if needed
- **State:** PROPOSED
