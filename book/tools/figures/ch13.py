"""
book/tools/figures/ch13.py
Figures for Chapter 13: Capstone Whole-System Integration & Oral Defense.
"""

from .common import (
    NAVY, BLUE, PETROL, TEAL, BRONZE, AMBER, CRIMSON, CORAL, PURPLE,
    SLATE, MUTED, INK, BG_LIGHT, BG_WHITE, BORDER, BORDER_DARK,
    COMMON_STYLE, COMMON_DEFS, save_svg_and_pdf
)

def gen_ch13_dual_brain():
    W = 900
    H = 460
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="30" class="title">CAPSTONE DUAL-BRAIN HETEROGENEOUS SYSTEM ARCHITECTURE</text>')
    svg.append(f'<text x="{W/2}" y="46" class="subtitle">Arduino Uno Q / STM32 NPU: Cortex-A MPU Deliberation ⟷ Shared TCM SRAM ⟷ Real-Time Cortex-M MCU Reflex Enforcer</text>')

    lx = 25
    lw = 270
    lh = 330
    svg.append(f'<rect x="{lx}" y="68" width="{lw}" height="{lh}" rx="8" fill="{BG_WHITE}" stroke="{NAVY}" stroke-width="1.3" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{lx}" y="68" width="{lw}" height="26" rx="8" fill="{NAVY}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{lx+lw/2}" y="86" font-size="10" font-weight="700" fill="{NAVY}" text-anchor="middle">1. HOST PROCESSOR (Linux MPU / NPU)</text>')
    svg.append(f'<text x="{lx+14}" y="115" font-size="11.5" font-weight="700" fill="{INK}">High-Throughput Deliberation</text>')
    svg.append(f'<text x="{lx+14}" y="130" font-size="8.5" font-weight="600" fill="{NAVY}">Cadence: 20–50 Hz · Non-Real-Time</text>')

    mpu_items = [
        "MIPI CSI-2 Camera DMA Ingestion",
        "Spatial Tokenizer (DINOv2 / MobileNet)",
        "SE(3) Dynamic Kinematic Frame Tree",
        "VLM Semantic Intent Grounding",
        "Diffusion / ACT Action Chunks (H=16)",
        "Asynchronous State Re-Anchoring"
    ]
    for idx, it in enumerate(mpu_items):
        svg.append(f'<text x="{lx+14}" y="{154+idx*22}" font-size="8.5" fill="{SLATE}">• {it}</text>')

    svg.append(f'<rect x="{lx+10}" y="{68+lh-46}" width="{lw-20}" height="36" rx="5" fill="{BG_LIGHT}" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{lx+lw/2}" y="{68+lh-28}" font-size="8.5" font-weight="700" fill="{CORAL}" text-anchor="middle">STOCHASTIC / UNTRUSTED SUBSTRATE</text>')
    svg.append(f'<text x="{lx+lw/2}" y="{68+lh-14}" font-size="7.5" fill="{MUTED}" text-anchor="middle">Subject to page faults, GC stalls, and tail spikes</text>')

    cx = 315
    cw = 270
    ch = 330
    svg.append(f'<rect x="{cx}" y="68" width="{cw}" height="{ch}" rx="8" fill="{BG_LIGHT}" stroke="{BORDER_DARK}" stroke-width="1.3" stroke-dasharray="4,2"/>')
    svg.append(f'<text x="{cx+cw/2}" y="92" font-size="11" font-weight="700" fill="{INK}" text-anchor="middle">SHARED MEMORY (TCM / SRAM)</text>')
    svg.append(f'<text x="{cx+cw/2}" y="108" font-size="8.5" fill="{MUTED}" text-anchor="middle">Lock-Free Inter-Core Mailbox &amp; Seqlock</text>')

    channels = [
        ("Candidate Action Buffer p_t", "H=16 Chunk Poses + Velocities (128 bytes)", BRONZE),
        ("Expiring Intent Lease t_expire", "Monotonic Timestamp Dead-Man Switch (8 bytes)", PURPLE),
        ("World Model State ẑ_t", "Fused SE(3) Bounding Primitives (64 bytes)", BLUE),
        ("Hardware Heartbeat Counter", "20 Hz Monotonic Ping (4 bytes)", CORAL),
        ("Proprioceptive Telemetry", "1 kHz Odometry &amp; Motor Currents (32 bytes)", PETROL)
    ]
    for idx, (t, d, col) in enumerate(channels):
        by = 125 + idx * 44
        svg.append(f'<rect x="{cx+12}" y="{by}" width="{cw-24}" height="36" rx="4" fill="{BG_WHITE}" stroke="{BORDER}" stroke-width="1"/>')
        svg.append(f'<rect x="{cx+12}" y="{by}" width="4" height="36" rx="2" fill="{col}"/>')
        svg.append(f'<text x="{cx+22}" y="{by+15}" font-size="8.5" font-weight="700" fill="{col}">{t}</text>')
        svg.append(f'<text x="{cx+22}" y="{by+28}" font-size="7.5" fill="{SLATE}">{d}</text>')

    rx = 605
    rw = 270
    rh = 330
    svg.append(f'<rect x="{rx}" y="68" width="{rw}" height="{rh}" rx="8" fill="{BG_WHITE}" stroke="{PETROL}" stroke-width="1.4" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{rx}" y="68" width="{rw}" height="26" rx="8" fill="{PETROL}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{rx+rw/2}" y="86" font-size="10" font-weight="700" fill="{PETROL}" text-anchor="middle">2. REFLEX ENFORCER (Real-Time MCU)</text>')
    svg.append(f'<text x="{rx+14}" y="115" font-size="11.5" font-weight="700" fill="{INK}">Deterministic Safety Enforcer</text>')
    svg.append(f'<text x="{rx+14}" y="130" font-size="8.5" font-weight="600" fill="{PETROL}">Cadence: 1000 Hz · Hard Real-Time (Jitter &lt; 5 µs)</text>')

    mcu_items = [
        "1000 Hz FreeRTOS Strict Priority Task",
        "Active-Set CBF QP Solver (h(x) ≥ 0)",
        "Dynamic Stopping Clearance Veto (d_stop ≤ d_gap)",
        "Watchdog Heartbeat Monitor (50 ms Timeout)",
        "Bumpless C² Takeover Smoothing S(α)",
        "PWM Gate Driver Current Loop Control"
    ]
    for idx, it in enumerate(mcu_items):
        svg.append(f'<text x="{rx+14}" y="{154+idx*22}" font-size="8.5" fill="{SLATE}">• {it}</text>')

    svg.append(f'<rect x="{rx+10}" y="{68+rh-46}" width="{rw-20}" height="36" rx="5" fill="{TEAL}" fill-opacity="0.08" stroke="{TEAL}" stroke-width="1"/>')
    svg.append(f'<text x="{rx+rw/2}" y="{68+rh-28}" font-size="8.5" font-weight="700" fill="{TEAL}" text-anchor="middle">CERTIFIED SAFETY GUARANTEE</text>')
    svg.append(f'<text x="{rx+rw/2}" y="{68+rh-14}" font-size="7.5" fill="{SLATE}" text-anchor="middle">Zero dynamic malloc · Strict forward invariance</text>')

    svg.append(f'<line x1="{lx+lw}" y1="180" x2="{cx}" y2="180" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#arr-navy)"/>')
    svg.append(f'<line x1="{cx+cw}" y1="180" x2="{rx}" y2="180" stroke="{PETROL}" stroke-width="1.6" marker-end="url(#arr-petrol)"/>')
    svg.append(f'<line x1="{rx}" y1="280" x2="{cx+cw}" y2="280" stroke="{PETROL}" stroke-width="1.6" marker-end="url(#arr-petrol)"/>')
    svg.append(f'<line x1="{cx}" y1="280" x2="{lx+lw}" y2="280" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#arr-navy)"/>')

    by = 412
    svg.append(f'<rect x="{lx}" y="{by}" width="{W-50}" height="38" rx="6" fill="{CRIMSON}" fill-opacity="0.06" stroke="{CRIMSON}" stroke-width="1.2"/>')
    svg.append(f'<text x="{W/2}" y="{by+16}" font-size="10" font-weight="700" fill="{CRIMSON}" text-anchor="middle">ACTUATORS &amp; PHYSICAL ENVIRONMENT (W_t → W_t+1)</text>')
    svg.append(f'<text x="{W/2}" y="{by+30}" font-size="8.5" fill="{SLATE}" text-anchor="middle">BLDC Motors · Inverter Bridges · Contact Friction · Mechanical Inertia · Thermal Dissipation</text>')

    svg.append(f'<line x1="{rx+rw/2}" y1="{68+rh}" x2="{rx+rw/2}" y2="{by}" stroke="{PETROL}" stroke-width="1.8" marker-end="url(#arr-petrol)"/>')
    svg.append(f'<line x1="{lx+lw/2}" y1="{by}" x2="{lx+lw/2}" y2="{68+lh}" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arr-navy)"/>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/13-frontier/figures/fig99_dual_brain_integration.svg", "\n".join(svg))

def gen_ch13_defense_matrix():
    W = 920
    H = 460
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="30" class="title">THE CAPSTONE WHOLE-SYSTEM DEFENSE DOSSIER &amp; AUDIT MATRIX</text>')
    svg.append(f'<text x="{W/2}" y="46" class="subtitle">The Complete 11-Artifact Engineering Portfolio Audited by 4 Interdisciplinary Examiners</text>')

    dossier_items = [
        ("CHARTER-01", "Architecture Charter &amp; Boundary", NAVY),
        ("REQ-01", "Metrology &amp; Latency Budget", NAVY),
        ("ARCH-01", "Cognitive Pipeline &amp; Tension", BLUE),
        ("IPC-01", "Multi-Rate SRAM IPC Contract", BLUE),
        ("OBS-01", "Transduction &amp; Spatial Memory", BLUE),
        ("STATE-01", "SE(3) Frame Tree &amp; World Model", BLUE),
        ("INTENT-01", "Expiring Intent Lease Contract", BRONZE),
        ("PLAN-01", "C² Quintic Action Chunking", BRONZE),
        ("ENF-01", "1 kHz Zero-Malloc Barrier QP", PETROL),
        ("AUTH-01", "Bumpless Transfer &amp; FSM", PURPLE),
        ("QUAL-01", "CAE Safety Case &amp; HIL Logs", CRIMSON)
    ]

    dx = 30
    dy = 70
    dw = 220
    dh = 370
    svg.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="8" fill="{BG_WHITE}" stroke="{NAVY}" stroke-width="1.3" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="26" rx="8" fill="{NAVY}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{dx+dw/2}" y="{dy+18}" font-size="9.5" font-weight="700" fill="{NAVY}" text-anchor="middle">11-ARTIFACT DOSSIER</text>')

    for idx, (code, title, col) in enumerate(dossier_items):
        by = dy + 32 + idx * 30
        svg.append(f'<rect x="{dx+8}" y="{by}" width="{dw-16}" height="24" rx="4" fill="{col}" fill-opacity="0.08" stroke="{col}" stroke-width="0.8"/>')
        svg.append(f'<text x="{dx+14}" y="{by+16}" font-size="8" font-weight="700" fill="{col}">{code}</text>')
        svg.append(f'<text x="{dx+70}" y="{by+16}" font-size="7.5" fill="{INK}">{title}</text>')

    ex = 270
    ew = 370
    eh = 370
    svg.append(f'<rect x="{ex}" y="{dy}" width="{ew}" height="{eh}" rx="8" fill="{BG_WHITE}" stroke="{PURPLE}" stroke-width="1.3" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{ex}" y="{dy}" width="{ew}" height="26" rx="8" fill="{PURPLE}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{ex+ew/2}" y="{dy+18}" font-size="9.5" font-weight="700" fill="{PURPLE}" text-anchor="middle">4 INTERDISCIPLINARY EXAMINERS</text>')

    examiners = [
        ("Examiner A · Systems &amp; Hardware", "Embedded Systems Auditor", "Audits: Lock-free SRAM, AXI QoS, zero malloc, 1 kHz QP latency, watchdog timing", BRONZE),
        ("Examiner B · AI &amp; Perception", "Machine Learning Auditor", "Audits: 3D tokenization, VLM grounding, world model covariance, action chunking", BLUE),
        ("Examiner C · Controls &amp; Robotics", "Robotics & Dynamics Auditor", "Audits: Kinematic reachability, C² jerk bounds, CBF invariant h(x) ≥ 0, bumpless transfer", PETROL),
        ("Examiner D · Safety &amp; Governance", "Safety & Assurance Regulator", "Audits: CAE safety case, cross-layer fault injection, DAgger flywheel, data privacy", CRIMSON)
    ]
    for idx, (ex_t, ex_sub, ex_d, col) in enumerate(examiners):
        by = dy + 36 + idx * 80
        svg.append(f'<rect x="{ex+10}" y="{by}" width="{ew-20}" height="70" rx="6" fill="{BG_LIGHT}" stroke="{BORDER}" stroke-width="1"/>')
        svg.append(f'<rect x="{ex+10}" y="{by}" width="4" height="70" rx="2" fill="{col}"/>')
        svg.append(f'<text x="{ex+22}" y="{by+20}" font-size="10" font-weight="700" fill="{col}">{ex_t}</text>')
        svg.append(f'<text x="{ex+22}" y="{by+36}" font-size="8.5" font-weight="600" fill="{INK}">{ex_sub}</text>')
        svg.append(f'<text x="{ex+22}" y="{by+52}" font-size="8" fill="{SLATE}">{ex_d}</text>')

    rx = 660
    rw = 230
    rh = 370
    svg.append(f'<rect x="{rx}" y="{dy}" width="{rw}" height="{rh}" rx="8" fill="{BG_WHITE}" stroke="{BORDER_DARK}" stroke-width="1.3" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{rx}" y="{dy}" width="{rw}" height="26" rx="8" fill="{BORDER_DARK}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{rx+rw/2}" y="{dy+18}" font-size="9.5" font-weight="700" fill="{INK}" text-anchor="middle">DEFENSE VERDICT GATE</text>')

    verdicts = [
        ("✓ DEPLOY", "Full Unconditional Release", "All 11 artifacts verified; 1000/1000 fault containment; P99.9 latency within budget.", TEAL),
        ("⚠ CONDITION", "Restricted ODD Deployment", "Minor telemetry gaps; restricted velocity &lt; 0.5 m/s; mandatory human co-pilot.", AMBER),
        ("✕ REFUSE", "Release Vetoed", "Single uncontained fault escape; seqlock overrun; memory leak; C² jerk violation.", CORAL)
    ]
    for idx, (v_t, v_sub, v_d, col) in enumerate(verdicts):
        by = dy + 36 + idx * 105
        svg.append(f'<rect x="{rx+10}" y="{by}" width="{rw-20}" height="95" rx="6" fill="{col}" fill-opacity="0.06" stroke="{col}" stroke-width="1.2"/>')
        svg.append(f'<text x="{rx+20}" y="{by+22}" font-size="12" font-weight="700" fill="{col}">{v_t}</text>')
        svg.append(f'<text x="{rx+20}" y="{by+38}" font-size="9" font-weight="600" fill="{INK}">{v_sub}</text>')
        words = v_d.split()
        l1 = " ".join(words[:4])
        l2 = " ".join(words[4:8])
        l3 = " ".join(words[8:])
        svg.append(f'<text x="{rx+20}" y="{by+56}" font-size="8" fill="{SLATE}">{l1}</text>')
        svg.append(f'<text x="{rx+20}" y="{by+68}" font-size="8" fill="{SLATE}">{l2}</text>')
        svg.append(f'<text x="{rx+20}" y="{by+80}" font-size="8" fill="{SLATE}">{l3}</text>')

    svg.append(f'<line x1="{dx+dw}" y1="250" x2="{ex}" y2="250" stroke="{NAVY}" stroke-width="1.8" marker-end="url(#arr-navy)"/>')
    svg.append(f'<line x1="{ex+ew}" y1="250" x2="{rx}" y2="250" stroke="{PURPLE}" stroke-width="1.8" marker-end="url(#arr-purple)"/>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/13-frontier/figures/fig99_defense_dossier_matrix.svg", "\n".join(svg))

def gen_ch13_fault_timeline():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">ENDOGENOUS REAL-TIME INTERVENTION &amp; RECOVERY</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Digital Oscilloscope Logic Analyzer Trace: Host Linux MPU Panic → Deterministic Real-Time MCU Safe Halt</text>')

    # Oscilloscope Display Box
    ox = 40
    oy = 64
    ow = W - 80
    oh = 345
    svg.append(f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="8" fill="#0F172A" stroke="{BORDER_DARK}" stroke-width="1.5"/>')

    for gx in range(ox+40, ox+ow, 60):
        svg.append(f'<line x1="{gx}" y1="{oy+10}" x2="{gx}" y2="{oy+oh-25}" stroke="#1E293B" stroke-width="1"/>')
    for gy in range(oy+30, oy+oh-25, 40):
        svg.append(f'<line x1="{ox+10}" y1="{gy}" x2="{ox+ow-10}" y2="{gy}" stroke="#1E293B" stroke-width="1"/>')

    t_fault = ox + 220
    svg.append(f'<line x1="{t_fault}" y1="{oy+10}" x2="{t_fault}" y2="{oy+oh-25}" stroke="{CORAL}" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<rect x="{t_fault-60}" y="{oy+12}" width="120" height="18" rx="3" fill="{CORAL}"/>')
    svg.append(f'<text x="{t_fault}" y="{oy+24}" font-size="8" font-weight="700" fill="#FFFFFF" text-anchor="middle">SEEDED FAULT (t₀)</text>')

    t_detect = ox + 420
    svg.append(f'<line x1="{t_detect}" y1="{oy+10}" x2="{t_detect}" y2="{oy+oh-25}" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<rect x="{t_detect-50}" y="{oy+12}" width="100" height="18" rx="3" fill="{AMBER}"/>')
    svg.append(f'<text x="{t_detect}" y="{oy+24}" font-size="8" font-weight="700" fill="#FFFFFF" text-anchor="middle">WATCHDOG (50ms)</text>')

    t_halt = ox + 580
    svg.append(f'<line x1="{t_halt}" y1="{oy+10}" x2="{t_halt}" y2="{oy+oh-25}" stroke="{TEAL}" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<rect x="{t_halt-45}" y="{oy+12}" width="90" height="18" rx="3" fill="{TEAL}"/>')
    svg.append(f'<text x="{t_halt}" y="{oy+24}" font-size="8" font-weight="700" fill="#FFFFFF" text-anchor="middle">SAFE HALT (v=0)</text>')

    traces = [
        ("CH1: Host MPU Heartbeat", CORAL, [
            (ox+30, 48, ox+70, 48), (ox+70, 48, ox+70, 32), (ox+70, 32, ox+110, 32), (ox+110, 32, ox+110, 48),
            (ox+110, 48, ox+150, 48), (ox+150, 48, ox+150, 32), (ox+150, 32, ox+190, 32), (ox+190, 32, ox+190, 48),
            (ox+190, 48, t_fault, 48), (t_fault, 48, t_fault, 48), (t_fault, 48, ox+ow-20, 48)
        ], 38, "Heartbeat stops dead on Linux segfault / crash"),

        ("CH2: Shared SRAM Seqlock", BRONZE, [
            (ox+30, 108, t_fault, 108), (t_fault, 108, t_detect, 108), (t_detect, 108, ox+ow-20, 108)
        ], 98, "Version counter freezes at v_last"),

        ("CH3: MCU Authority FSM", AMBER, [
            (ox+30, 168, t_detect, 168), (t_detect, 168, t_detect, 152), (t_detect, 152, ox+ow-20, 152)
        ], 158, "Trips to CAT 1 Dynamic Braking State"),

        ("CH4: Gate Driver PWM &amp; Current", PETROL, [
            (ox+30, 228, t_detect, 228), (t_detect, 228, t_detect, 212), (t_detect, 212, t_halt, 236), (t_halt, 236, ox+ow-20, 244)
        ], 218, "Regenerative reverse torque applied to zero speed"),

        ("CH5: Vehicle Velocity v(t)", TEAL, [
            (ox+30, 280, t_detect, 280), (t_detect, 280, t_halt, 305), (t_halt, 305, ox+ow-20, 305)
        ], 278, "Smooth C² deceleration: d_stop = 8.4 cm ≤ 25 cm clearance ✓")
    ]

    for ch_name, col, segments, text_y, desc in traces:
        svg.append(f'<text x="{ox+20}" y="{oy+text_y}" font-size="9.5" font-weight="700" fill="{col}">{ch_name}</text>')
        svg.append(f'<text x="{ox+220}" y="{oy+text_y}" font-size="8.5" fill="#94A3B8">{desc}</text>')
        for x1, y1, x2, y2 in segments:
            svg.append(f'<line x1="{x1}" y1="{oy+y1+10}" x2="{x2}" y2="{oy+y2+10}" stroke="{col}" stroke-width="2"/>')

    svg.append(f'<text x="{ox+ow/2}" y="{oy+oh-10}" font-size="9" font-weight="600" fill="#94A3B8" text-anchor="middle">Total Fault Containment Time: Δt = 42.8 ms &lt; 50.0 ms Hard Limit (Certified Release Criterion Met)</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/13-frontier/figures/fig99_seeded_fault_timeline.svg", "\n".join(svg))

def run_all():
    gen_ch13_dual_brain()
    gen_ch13_defense_matrix()
    gen_ch13_fault_timeline()

if __name__ == "__main__":
    run_all()
