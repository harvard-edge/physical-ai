"""
book/tools/figures/ch01.py
Figures for Chapter 1: The Boundary Between Bits and Physics.
"""

from .common import (
    NAVY, BLUE, PETROL, TEAL, BRONZE, AMBER, CRIMSON, CORAL, PURPLE,
    SLATE, MUTED, INK, BG_LIGHT, BG_WHITE, BORDER, BORDER_DARK,
    COMMON_STYLE, COMMON_DEFS, save_svg_and_pdf
)

def gen_fig00_master_roadmap():
    W = 920
    H = 460
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="30" class="title">PHYSICAL AI: WHOLE-CURRICULUM ARCHITECTURE ROADMAP</text>')
    svg.append(f'<text x="{W/2}" y="46" class="subtitle">A Principled Journey from Physical Constraints to Frontier Dual-Brain Embodied Systems</text>')

    parts = [
        ("PART I: FOUNDATIONS", "Physics, Silicon & Hierarchy", NAVY, [
            ("Ch 1: The Boundary", "The physical AI imperative · Causal loop · 3 Tribes"),
            ("Ch 2: Constraints", "5 Physical Columns · Latency fresh wall · d_stop"),
            ("Ch 3: Cognition", "5 Cognitive Stages · The Great Systems Tension"),
            ("Ch 4: Hierarchy", "Multi-rate asynchronous topology · 3 Cadences")
        ]),
        ("PART II: THE 5 ORGANS", "Sensory-Motor Execution Pipeline", BLUE, [
            ("Ch 5: Perception", "Sensory transduction · Spatial tokenization · UMA bus"),
            ("Ch 6: Memory", "SE(3) World models · Dynamic frame trees · Covariance"),
            ("Ch 7: Reasoning", "VLM Grounding · Expiring intent leases · Reachability"),
            ("Ch 8: Planning", "Action chunking · C² jerk continuity · Ensembling"),
            ("Ch 9: Reflexes", "Real-time MCU enforcer · CBF projection · ISO stops")
        ]),
        ("PART III: INTEGRATION", "Hardware, Governance & Release", PURPLE, [
            ("Ch 10: Placement", "4-Tier heterogeneous placement · Thermal budgets"),
            ("Ch 11: Governance", "Authority arbitration · C² bumpless takeover · DAgger"),
            ("Ch 12: Assurance", "CAE safety cases · 4-Rung qualification ladder"),
            ("Ch 13: Capstone", "Dual-brain physical kit · Oral defense dossier")
        ])
    ]

    card_w = 270
    gap = 20
    start_x = (W - (3 * card_w + 2 * gap)) / 2

    for i, (part_hdr, part_sub, col, chapters) in enumerate(parts):
        x = start_x + i * (card_w + gap)
        y = 70
        h = 360

        svg.append(f'<rect x="{x}" y="{y}" width="{card_w}" height="{h}" rx="8" fill="{BG_WHITE}" stroke="{col}" stroke-width="1.3" filter="url(#shadow)"/>')
        svg.append(f'<rect x="{x}" y="{y}" width="{card_w}" height="28" rx="8" fill="{col}" fill-opacity="0.12"/>')
        svg.append(f'<text x="{x+card_w/2}" y="{y+18}" font-size="10" font-weight="700" fill="{col}" text-anchor="middle">{part_hdr}</text>')
        svg.append(f'<text x="{x+card_w/2}" y="{y+44}" font-size="11.5" font-weight="700" fill="{INK}" text-anchor="middle">{part_sub}</text>')

        cur_cy = y + 60
        for ch_t, ch_d in chapters:
            svg.append(f'<rect x="{x+10}" y="{cur_cy}" width="{card_w-20}" height="58" rx="5" fill="{BG_LIGHT}" stroke="{BORDER}" stroke-width="1"/>')
            svg.append(f'<text x="{x+18}" y="{cur_cy+18}" font-size="9.5" font-weight="700" fill="{col}">{ch_t}</text>')
            svg.append(f'<text x="{x+18}" y="{cur_cy+36}" font-size="8.5" fill="{SLATE}">{ch_d.split("·")[0].strip()}</text>')
            svg.append(f'<text x="{x+18}" y="{cur_cy+48}" font-size="8.5" fill="{MUTED}">· {ch_d.split("·")[1].strip() if len(ch_d.split("·"))>1 else ""}</text>')
            cur_cy += 68

        if i < 2:
            ax1 = x + card_w + 2
            ax2 = ax1 + gap - 4
            ay = y + h/2
            svg.append(f'<line x1="{ax1}" y1="{ay}" x2="{ax2}" y2="{ay}" stroke="{col}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/01-boundary/figures/fig00_master_roadmap.svg", "\n".join(svg))

def gen_fig01_pipeline_intro():
    W = 900
    H = 460
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">THE COMPLETE PHYSICAL AI SENSORY-MOTOR PIPELINE</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Asynchronous Multi-Rate Flow: From Physical Transduction to Real-Time Safety-Filtered Actuation</text>')

    stages = [
        ("STAGE 1: TRANSDUCTION", "Sensory Ingestion", "MIPI CSI-2 Vision · IMU · Encoders\nDMA zero-copy ring buffers (malloc=0)\nHardware PTP nanosecond timestamping", NAVY, 24, 70),
        ("STAGE 2: PERCEPTION", "Spatial Tokenization", "Metric depth &amp; 3D bounding primitives\nPatch embeddings → Spatial affordances\nZero-copy tensor views into shared SRAM", BLUE, 320, 70),
        ("STAGE 3: MEMORY", "World Model &amp; Frame Tree", "Dynamic SE(3) kinematic coordinate tree\nProprioceptive innovation updates\nLatent JEPA physics state prediction", BLUE, 616, 70),
        ("STAGE 4: REASONING", "Semantic Intent Leases", "Edge VLM deliberate task grounding\nEmits coarse 3D target + expiring lease\nt_expire lease bounds execution window", BRONZE, 616, 230),
        ("STAGE 5: PLANNING", "Action Chunking (H=16)", "Diffusion / ACT action trajectory chunks\nC² continuous quintic spline fitting\nTemporal ensembling over overlapping plans", BRONZE, 320, 230),
        ("STAGE 6: REFLEX", "Real-Time MCU Enforcer", "1000 Hz zero-allocation QP solver\nControl Barrier Function: h(x) ≥ 0\nDynamic stopping clearance check", PETROL, 24, 230)
    ]

    bw = 260
    bh = 135
    for tag, title, desc, col, x, y in stages:
        svg.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{BG_WHITE}" stroke="{col}" stroke-width="1.2" filter="url(#shadow)"/>')
        svg.append(f'<rect x="{x}" y="{y}" width="{bw}" height="22" rx="6" fill="{col}" fill-opacity="0.12"/>')
        svg.append(f'<text x="{x+10}" y="{y+15}" font-size="8.5" font-weight="700" fill="{col}">{tag}</text>')
        svg.append(f'<text x="{x+10}" y="{y+38}" font-size="11" font-weight="700" fill="{INK}">{title}</text>')
        for idx, l in enumerate(desc.split("\n")):
            svg.append(f'<text x="{x+10}" y="{y+56+idx*16}" font-size="8.5" fill="{SLATE}">• {l}</text>')

    # Connectors
    svg.append(f'<line x1="284" y1="137" x2="320" y2="137" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arr-navy)"/>')
    svg.append(f'<line x1="580" y1="137" x2="616" y2="137" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#arr-blue)"/>')
    svg.append(f'<line x1="746" y1="205" x2="746" y2="230" stroke="{BRONZE}" stroke-width="1.5" marker-end="url(#arr-bronze)"/>')
    svg.append(f'<line x1="616" y1="297" x2="580" y2="297" stroke="{BRONZE}" stroke-width="1.5" marker-end="url(#arr-bronze)"/>')
    svg.append(f'<line x1="320" y1="297" x2="284" y2="297" stroke="{PETROL}" stroke-width="1.5" marker-end="url(#arr-petrol)"/>')

    # Bottom Physical World Strip
    wy = 390
    svg.append(f'<rect x="24" y="{wy}" width="{W-48}" height="50" rx="6" fill="{CRIMSON}" fill-opacity="0.06" stroke="{CRIMSON}" stroke-width="1.2"/>')
    svg.append(f'<text x="{W/2}" y="{wy+18}" font-size="11" font-weight="700" fill="{CRIMSON}" text-anchor="middle">THE PHYSICAL WORLD &amp; ACTUATION DYNAMICS (W_t ⟶ W_t+1)</text>')
    svg.append(f'<text x="{W/2}" y="{wy+36}" font-size="9" fill="{SLATE}" text-anchor="middle">Kinetic Momentum · Friction Limits · Thermal Constraints · Motor Torque Saturation · No Software Undo</text>')

    svg.append(f'<line x1="154" y1="365" x2="154" y2="{wy}" stroke="{PETROL}" stroke-width="1.5" marker-end="url(#arr-petrol)"/>')
    svg.append(f'<line x1="110" y1="{wy}" x2="110" y2="205" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arr-navy)"/>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/01-boundary/figures/fig01_pipeline_intro.svg", "\n".join(svg))

def gen_fig01_agent_anatomy():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">ANATOMY OF AN EMBODIED PHYSICAL AI AGENT</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">The Closed Causal Interaction Loop: Perception, Latent Modeling, Action, and Physical Law</text>')

    # 4 Quadrants
    quads = [
        ("1. TRANSDUCTION &amp; SENSING", "Physical Photons/Forces → Digital Bits", "Camera CMOS pixel wells · Shunt current sense\nIMU Coriolis force gyroscopes · Encoder ticks", NAVY, 40, 70),
        ("2. COGNITIVE SYNTHESIS", "Spatial World Model &amp; Reasoning", "3D SE(3) Frame Tree · Latent state belief\nDiffusion action chunks · Expiring intent lease", BLUE, 480, 70),
        ("3. REAL-TIME SAFETY ENFORCER", "Proposal Veto &amp; Invariant Projection", "Active-Set QP solver: h(x) ≥ 0\nDynamic stopping clearance: d_stop ≤ d_gap\nDeterministic 1 kHz FreeRTOS execution", PETROL, 480, 240),
        ("4. PHYSICAL PLANT &amp; DYNAMICS", "Silicon Commands → Continuous Physics", "BLDC motor inverter bridges · Contact mechanics\nKinetic energy E_k = 1/2 m v² · Thermal heating", CRIMSON, 40, 240)
    ]

    qw = 360
    qh = 140
    for tag, title, desc, col, x, y in quads:
        svg.append(f'<rect x="{x}" y="{y}" width="{qw}" height="{qh}" rx="8" fill="{BG_WHITE}" stroke="{col}" stroke-width="1.2" filter="url(#shadow)"/>')
        svg.append(f'<rect x="{x}" y="{y}" width="{qw}" height="24" rx="8" fill="{col}" fill-opacity="0.12"/>')
        svg.append(f'<text x="{x+12}" y="{y+16}" font-size="9" font-weight="700" fill="{col}">{tag}</text>')
        svg.append(f'<text x="{x+12}" y="{y+42}" font-size="11" font-weight="700" fill="{INK}">{title}</text>')
        for idx, line in enumerate(desc.split("\n")):
            svg.append(f'<text x="{x+12}" y="{y+62+idx*16}" font-size="8.5" fill="{SLATE}">• {line}</text>')

    # Causal Loop Arrows
    svg.append(f'<line x1="400" y1="140" x2="480" y2="140" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')
    svg.append(f'<text x="440" y="132" font-size="8" font-weight="600" fill="{BLUE}" text-anchor="middle">z_t (Bits)</text>')

    svg.append(f'<line x1="660" y1="210" x2="660" y2="240" stroke="{BRONZE}" stroke-width="1.8" marker-end="url(#arr-bronze)"/>')
    svg.append(f'<text x="670" y="228" font-size="8" font-weight="600" fill="{BRONZE}">p_t (Proposal)</text>')

    svg.append(f'<line x1="480" y1="310" x2="400" y2="310" stroke="{PETROL}" stroke-width="1.8" marker-end="url(#arr-petrol)"/>')
    svg.append(f'<text x="440" y="302" font-size="8" font-weight="600" fill="{PETROL}" text-anchor="middle">u_t (Permission)</text>')

    svg.append(f'<line x1="220" y1="240" x2="220" y2="210" stroke="{CRIMSON}" stroke-width="1.8" marker-end="url(#arr-crimson)"/>')
    svg.append(f'<text x="210" y="228" font-size="8" font-weight="600" fill="{CRIMSON}" text-anchor="end">W_t (Continuous State)</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/01-boundary/figures/fig01_agent_anatomy.svg", "\n".join(svg))

def gen_fig01_codesign_matrix():
    W = 880
    H = 460
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">THE 5×5 PHYSICAL AGENT CO-DESIGN MATRIX</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">The Master Systems Synthesis: Balancing Physics, Silicon, Memory, Models, and Authority</text>')

    cols = ["1. Physical Column", "2. Silicon Substrate", "3. Algorithmic Organ", "4. Failure Mode", "5. Systems Invariant"]
    rows = [
        ("TIME", "Cortex MPU ⟷ RT MCU", "1 kHz QP Barrier Solver", "Tail latency overrun", "P99.9 Wall Latency < Budget", NAVY),
        ("INERTIA", "Static SRAM (Zero Malloc)", "Action Chunking (H=16)", "Kinetic collision", "d_stop(t) ≤ d_clearance", BLUE),
        ("ACTUATION", "Gate Drivers / Inverters", "C² Quintic Trajectory", "Gearbox jerk shock", "Jerk Continuity j ≤ j_max", BRONZE),
        ("ENERGY", "Dynamic Voltage Scaling", "Multi-Rate Observers", "Thermal throttling", "Junction Temp T_j ≤ 85°C", AMBER),
        ("SILICON", "Lock-Free DMA TCM", "Expiring Intent Leases", "Uncontained crash", "Watchdog Lease τ ≤ 50 ms", PURPLE)
    ]

    col_widths = [110, 170, 180, 170, 190]
    start_x = 30
    cur_y = 70

    # Header Row
    cur_x = start_x
    for i, (c_name, c_w) in enumerate(zip(cols, col_widths)):
        svg.append(f'<rect x="{cur_x}" y="{cur_y}" width="{c_w}" height="26" fill="{NAVY}" rx="3"/>')
        svg.append(f'<text x="{cur_x+c_w/2}" y="{cur_y+17}" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">{c_name}</text>')
        cur_x += c_w + 6

    cur_y += 32
    for r_title, r_sil, r_alg, r_fail, r_inv, col in rows:
        cur_x = start_x
        row_items = [r_title, r_sil, r_alg, r_fail, r_inv]
        for idx, (val, c_w) in enumerate(zip(row_items, col_widths)):
            bg = f"{col}12" if idx == 0 else BG_LIGHT
            f_col = col if idx == 0 else (CORAL if idx == 3 else (TEAL if idx == 4 else INK))
            weight = "700" if idx in [0, 3, 4] else "500"
            svg.append(f'<rect x="{cur_x}" y="{cur_y}" width="{c_w}" height="56" rx="4" fill="{bg}" stroke="{BORDER}" stroke-width="1"/>')
            svg.append(f'<text x="{cur_x+c_w/2}" y="{cur_y+32}" font-size="9" font-weight="{weight}" fill="{f_col}" text-anchor="middle">{val}</text>')
            cur_x += c_w + 6
        cur_y += 62

    # Bottom Callout
    svg.append(f'<rect x="30" y="390" width="820" height="42" rx="6" fill="{BG_LIGHT}" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="408" font-size="9.5" font-weight="700" fill="{NAVY}" text-anchor="middle">THE CO-DESIGN AXIOM</text>')
    svg.append(f'<text x="{W/2}" y="422" font-size="8.5" fill="{SLATE}" text-anchor="middle">Optimizing any single row in isolation without satisfying all 5 columns guarantees physical failure in closed-loop operation.</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/01-boundary/figures/fig01_codesign_matrix.svg", "\n".join(svg))

def gen_fig01_three_tribes():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">THE THREE TRIBES OF EMBODIED INTELLIGENCE</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Bridging the Disciplinary Divides Between Computer Science, Embedded Systems, and Mechanical Robotics</text>')

    tribes = [
        ("DISCIPLINE 1: COMPUTER SCIENCE / AI", "Machine Learning Perspective", "Loss functions · Transformers · Latent world models\nPython abstractions · Generative policies · Tokenization", BLUE, 40, 70),
        ("DISCIPLINE 2: EMBEDDED SYSTEMS / ECE", "Silicon & Firmware Perspective", "Microsecond jitter · DMA memory buses · Interrupt service routines\nStatic SRAM (malloc=0) · Watchdogs · AXI QoS priorities", BRONZE, 480, 70),
        ("DISCIPLINE 3: ROBOTICS &amp; MECHANICS", "Kinematics & Dynamics Perspective", "Kinetic momentum · Friction cones · Contact compliance\nStopping distance d_stop · Gearbox backlash · Dynamic stability", CRIMSON, 260, 255)
    ]

    tw = 360
    th = 135
    for tag, sub, desc, col, x, y in tribes:
        svg.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="8" fill="{BG_WHITE}" stroke="{col}" stroke-width="1.3" filter="url(#shadow)"/>')
        svg.append(f'<rect x="{x}" y="{y}" width="{tw}" height="24" rx="8" fill="{col}" fill-opacity="0.12"/>')
        svg.append(f'<text x="{x+12}" y="{y+16}" font-size="9" font-weight="700" fill="{col}">{tag}</text>')
        svg.append(f'<text x="{x+12}" y="{y+42}" font-size="11" font-weight="700" fill="{INK}">{sub}</text>')
        for idx, l in enumerate(desc.split("\n")):
            svg.append(f'<text x="{x+12}" y="{y+62+idx*16}" font-size="8.5" fill="{SLATE}">• {l}</text>')

    # Central Convergence Core
    cx = 440
    cy = 205
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="36" fill="{NAVY}" stroke="#FFFFFF" stroke-width="3" filter="url(#shadow)"/>')
    svg.append(f'<text x="{cx}" y="{cy-4}" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">PHYSICAL</text>')
    svg.append(f'<text x="{cx}" y="{cy+10}" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">AI</text>')

    # Inward Arrows
    svg.append(f'<line x1="380" y1="160" x2="{cx-26}" y2="{cy-18}" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')
    svg.append(f'<line x1="500" y1="160" x2="{cx+26}" y2="{cy-18}" stroke="{BRONZE}" stroke-width="1.8" marker-end="url(#arr-bronze)"/>')
    svg.append(f'<line x1="440" y1="255" x2="{cx}" y2="{cy+36}" stroke="{CRIMSON}" stroke-width="1.8" marker-end="url(#arr-crimson)"/>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/01-boundary/figures/fig01_three_tribes.svg", "\n".join(svg))

def gen_fig01_eras_evolution():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">THE THREE ERAS OF AUTONOMOUS COMPUTING</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">From Structured Industrial Determinism to Cloud AI and Embodied Physical Agents</text>')

    eras = [
        ("ERA 1: CLASSICAL AUTOMATION", "1970s – 2010s", "Rigid, Deterministic Execution",
         ["Structured factory workcells &amp; caged robots", "Hard-coded ladder logic &amp; PID controllers", "Zero open-world generalization capability", "Safe only through physical human exclusion"],
         SLATE),
        ("ERA 2: CLOUD &amp; DIGITAL AI", "2012 – 2024", "Disembodied Statistical Scaling",
         ["Large Language Models &amp; Generative Diffusion", "Pure software sandbox · Infinite undo &amp; idempotent APIs", "Unbounded tail latencies (> 500 ms acceptable)", "Zero awareness of momentum, mass, or heating"],
         BLUE),
        ("ERA 3: PHYSICAL AI", "2024 – Present", "Embodied Real-Time Agency",
         ["Multi-rate dual-brain architecture (MPU ⟷ MCU)", "Foundation world models with real-time CBF filters", "Hard latency freshness deadlines (d_stop ≤ d_gap)", "Irreversible physical consequence &amp; zero software undo"],
         NAVY)
    ]

    ew = 250
    gap = 20
    start_x = (W - (3 * ew + 2 * gap)) / 2

    for i, (tag, dates, sub, items, col) in enumerate(eras):
        x = start_x + i * (ew + gap)
        y = 70
        h = 330

        svg.append(f'<rect x="{x}" y="{y}" width="{ew}" height="{h}" rx="8" fill="{BG_WHITE}" stroke="{col}" stroke-width="1.3" filter="url(#shadow)"/>')
        svg.append(f'<rect x="{x}" y="{y}" width="{ew}" height="24" rx="8" fill="{col}" fill-opacity="0.12"/>')
        svg.append(f'<text x="{x+ew/2}" y="{y+16}" font-size="8.5" font-weight="700" fill="{col}" text-anchor="middle">{tag}</text>')
        svg.append(f'<text x="{x+ew/2}" y="{y+42}" font-size="12" font-weight="700" fill="{INK}" text-anchor="middle">{dates}</text>')
        svg.append(f'<text x="{x+ew/2}" y="{y+58}" font-size="9" fill="{MUTED}" text-anchor="middle">{sub}</text>')

        cy = y + 80
        for it in items:
            svg.append(f'<text x="{x+12}" y="{cy}" font-size="8.5" fill="{SLATE}">• {it}</text>')
            cy += 24

        if i < 2:
            ax1 = x + ew + 1
            ax2 = ax1 + gap - 2
            ay = y + h/2
            svg.append(f'<line x1="{ax1}" y1="{ay}" x2="{ax2}" y2="{ay}" stroke="{col}" stroke-width="1.8" marker-end="url(#arr-blue)"/>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/01-boundary/figures/fig01_eras_evolution.svg", "\n".join(svg))

def run_all():
    gen_fig00_master_roadmap()
    gen_fig01_pipeline_intro()
    gen_fig01_agent_anatomy()
    gen_fig01_codesign_matrix()
    gen_fig01_three_tribes()
    gen_fig01_eras_evolution()

if __name__ == "__main__":
    run_all()
