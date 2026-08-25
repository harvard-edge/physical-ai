"""
book/tools/figures/ch09.py
Figures for Chapter 9: Real-Time Safety Enforcement & Reflexes.
"""

from .common import (
    NAVY, BLUE, PETROL, TEAL, BRONZE, AMBER, CRIMSON, CORAL, PURPLE,
    SLATE, MUTED, INK, BG_LIGHT, BG_WHITE, BORDER, BORDER_DARK,
    COMMON_STYLE, COMMON_DEFS, save_svg_and_pdf
)

def gen_fig08_enforcer_timing_waterfall():
    W = 900
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">1000 HZ HARD REAL-TIME REFLEX EXECUTION WATERFALL</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Microsecond Budget Breakdown: 1000 µs Total Loop · Active-Set QP Solver ≤ 175 µs · 0 Dynamic Malloc</text>')

    stages = [
        ("1. SPI / DMA Sensor Latch &amp; CRC Check", 85, NAVY),
        ("2. Forward Kinematics &amp; Jacobian Update", 110, BLUE),
        ("3. Proposal De-serialization from Shared TCM", 45, BRONZE),
        ("4. Active-Set CBF QP Solver (Zero Malloc)", 175, PETROL),
        ("5. Dynamic Stopping Clearance Invariant Check", 60, TEAL),
        ("6. Hardware Watchdog Heartbeat Service", 25, PURPLE),
        ("7. PWM Gate Driver Output &amp; Current Latch", 90, CRIMSON)
    ]

    start_x = 280
    total_w = 480
    cur_cum = 0

    ax_y = 370
    svg.append(f'<line x1="{start_x}" y1="{ax_y}" x2="{start_x+total_w+25}" y2="{ax_y}" stroke="{SLATE}" stroke-width="1.2" marker-end="url(#arr-slate)"/>')
    svg.append(f'<text x="{start_x+total_w+30}" y="{ax_y+4}" font-size="9" font-weight="700" fill="{SLATE}">Time (µs)</text>')

    for t_val in [0, 200, 400, 600, 800, 1000]:
        x_m = start_x + (t_val / 1000.0) * total_w
        svg.append(f'<line x1="{x_m}" y1="{ax_y}" x2="{x_m}" y2="{ax_y+6}" stroke="{SLATE}" stroke-width="1"/>')
        svg.append(f'<text x="{x_m}" y="{ax_y+18}" font-size="8.5" fill="{SLATE}" text-anchor="middle">{t_val}</text>')
        svg.append(f'<line x1="{x_m}" y1="65" x2="{x_m}" y2="{ax_y}" stroke="{BORDER}" stroke-width="0.8" stroke-dasharray="3,3"/>')

    for idx, (name, dur, col) in enumerate(stages):
        y = 70 + idx * 40
        svg.append(f'<text x="{start_x-12}" y="{y+16}" font-size="8.5" font-weight="600" fill="{INK}" text-anchor="end">{name}</text>')
        
        bx = start_x + (cur_cum / 1000.0) * total_w
        bw = (dur / 1000.0) * total_w
        svg.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="24" rx="4" fill="{col}" fill-opacity="0.85" stroke="{col}" stroke-width="1"/>')
        if bw < 30:
            svg.append(f'<text x="{bx-6}" y="{y+16}" font-size="7.5" font-weight="700" fill="{col}" text-anchor="end">+{dur}µs</text>')
        else:
            svg.append(f'<text x="{bx+bw/2}" y="{y+16}" font-size="7.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">+{dur}µs</text>')

        cur_cum += dur

    # Slack Margin
    slack_x = start_x + (cur_cum / 1000.0) * total_w
    slack_w = total_w - (cur_cum / 1000.0) * total_w
    svg.append(f'<rect x="{slack_x}" y="70" width="{slack_w}" height="270" rx="4" fill="{TEAL}" fill-opacity="0.08" stroke="{TEAL}" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="{slack_x+slack_w/2}" y="200" font-size="9" font-weight="700" fill="{TEAL}" text-anchor="middle">REAL-TIME SLACK MARGIN</text>')
    svg.append(f'<text x="{slack_x+slack_w/2}" y="215" font-size="8" fill="{MUTED}" text-anchor="middle">410 µs Headroom (Jitter &lt; 5 µs)</text>')

    # 1 ms Deadline
    svg.append(f'<line x1="{start_x+total_w}" y1="65" x2="{start_x+total_w}" y2="{ax_y}" stroke="{CORAL}" stroke-width="2"/>')
    svg.append(f'<rect x="{start_x+total_w-60}" y="56" width="120" height="20" rx="4" fill="{CORAL}"/>')
    svg.append(f'<text x="{start_x+total_w}" y="70" font-size="8.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">1000 µs DEADLINE</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/09-enforcement/figures/fig08_enforcer_timing_waterfall.svg", "\n".join(svg))

def gen_fig08_cbf_projection():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">CONTROL BARRIER FUNCTION (CBF) MINIMAL-INTERVENTION PROJECTION</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Quadratic Program Filter: min ||u - p_t||² subject to L_f h(x) + L_g h(x) u + α(h(x)) ≥ 0</text>')

    # Left: Geometric Projection Diagram
    lx = 40
    ly = 70
    lw = 400
    lh = 330
    svg.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="8" fill="{BG_WHITE}" stroke="{BORDER}" stroke-width="1.2" filter="url(#shadow)"/>')
    
    # Safe Set C (Green half space)
    svg.append(f'<path d="M {lx+20} {ly+260} L {lx+380} {ly+100} L {lx+20} {ly+100} Z" fill="{TEAL}" fill-opacity="0.1"/>')
    svg.append(f'<line x1="{lx+20}" y1="{ly+260}" x2="{lx+380}" y2="{ly+100}" stroke="{TEAL}" stroke-width="2.5"/>')
    svg.append(f'<text x="{lx+120}" y="{ly+140}" font-size="11" font-weight="700" fill="{TEAL}">SAFE SET C: {{"x | h(x) ≥ 0"}}</text>')
    svg.append(f'<text x="{lx+260}" y="{ly+275}" font-size="10" font-weight="700" fill="{CORAL}">UNSAFE SET: h(x) &lt; 0</text>')

    # Boundary tangent line
    svg.append(f'<circle cx="{lx+200}" cy="{ly+180}" r="6" fill="{INK}"/>')
    svg.append(f'<text x="{lx+190}" y="{ly+175}" font-size="9" font-weight="700" fill="{INK}" text-anchor="end">State x(t)</text>')

    # Proposed action p_t (pointing unsafe)
    svg.append(f'<line x1="{lx+200}" y1="{ly+180}" x2="{lx+300}" y2="{ly+220}" stroke="{BRONZE}" stroke-width="2.5" marker-end="url(#arr-bronze)"/>')
    svg.append(f'<text x="{lx+310}" y="{ly+222}" font-size="9" font-weight="700" fill="{BRONZE}">Proposed p_t (Unsafe!)</text>')

    # Projected action u* (pointing tangent along boundary)
    svg.append(f'<line x1="{lx+200}" y1="{ly+180}" x2="{lx+270}" y2="{ly+149}" stroke="{TEAL}" stroke-width="3" marker-end="url(#arr-teal)"/>')
    svg.append(f'<text x="{lx+280}" y="{ly+130}" font-size="9.5" font-weight="700" fill="{TEAL}">Permitted u* (Projected)</text>')

    # Projection arrow
    svg.append(f'<line x1="{lx+300}" y1="{ly+220}" x2="{lx+270}" y2="{ly+149}" stroke="{PURPLE}" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="{lx+305}" y="{ly+180}" font-size="8" font-weight="700" fill="{PURPLE}">min ||u - p_t||²</text>')

    # Right: Mathematical & Systems Guarantee
    rx = 460
    rw = 380
    svg.append(f'<rect x="{rx}" y="{ly}" width="{rw}" height="{lh}" rx="8" fill="{BG_LIGHT}" stroke="{BORDER}" stroke-width="1.2"/>')
    svg.append(f'<text x="{rx+16}" y="{ly+28}" font-size="11" font-weight="700" fill="{NAVY}">THE BARRIER GUARANTEE</text>')

    points = [
        ("Minimal Intervention Principle:", [
            "If proposed action p_t is safe, u* = p_t with zero distortion.",
            "If p_t violates safety, QP applies minimal correction."
        ]),
        ("Forward Invariance (Nagumo's Theorem):", [
            "If state starts in C (h(x₀) ≥ 0), it remains inside C",
            "for all future time t ≥ 0: h(x(t)) ≥ 0 certified."
        ]),
        ("Deterministic Active-Set QP Solver:", [
            "Formulated with linear constraints in 3–6 variables.",
            "Guaranteed convergence in ≤ 15 iterations (≤ 175 µs)."
        ]),
        ("Zero Dynamic Allocation (malloc=0):", [
            "Matrices pre-allocated in static SRAM.",
            "Zero page faults or heap jitter in real-time loop."
        ])
    ]
    cur_py = ly + 52
    for p_t, lines in points:
        svg.append(f'<text x="{rx+16}" y="{cur_py}" font-size="9" font-weight="700" fill="{INK}">• {p_t}</text>')
        cur_py += 14
        for l in lines:
            svg.append(f'<text x="{rx+24}" y="{cur_py}" font-size="8.5" fill="{SLATE}">{l}</text>')
            cur_py += 13
        cur_py += 6

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/09-enforcement/figures/fig08_cbf_projection.svg", "\n".join(svg))

def gen_fig08_fallback_hierarchy():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">IEC 60204-1 / ISO 13850 EMERGENCY FALLBACK HIERARCHY</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Deterministic Fallback Escalation: From Controlled Position Hold to Hard Silicon Safe Torque Off (STO)</text>')

    levels = [
        ("CATEGORY 2: CONTROLLED STOP", "Normal Operational Pause (Drive Power Maintained)",
         "• Robot decelerates along path to standstill using motor torque\n• Mechanical position hold active; power remains on\n• Triggered by: Soft geofence warning, task pause, minor latency jitter",
         BLUE),
        ("CATEGORY 1: DYNAMIC BRAKE", "Controlled Deceleration + Power Cut at Standstill",
         "• Motors actively brake at a_max (-4.5 m/s²) using regenerative/dynamic braking\n• Mechanical safety brakes engage once speed v = 0, then power is removed\n• Triggered by: Expired intent lease, watchdog timeout (50 ms), trajectory divergence",
         AMBER),
        ("CATEGORY 0: SAFE TORQUE OFF (STO)", "Immediate Hardware Power Disconnect (Uncontrolled)",
         "• Dedicated hardware STO relay drops gate drive voltage instantly\n• Motors coast to stop under pure mechanical brake / friction\n• Triggered by: Physical E-stop button, primary silicon crash, over-current trip",
         CORAL)
    ]

    cur_y = 68
    for tag, sub, desc, col in levels:
        lh = 100
        svg.append(f'<rect x="40" y="{cur_y}" width="{W-80}" height="{lh}" rx="6" fill="{BG_WHITE}" stroke="{col}" stroke-width="1.3" filter="url(#shadow)"/>')
        svg.append(f'<rect x="40" y="{cur_y}" width="6" height="{lh}" rx="3" fill="{col}"/>')
        svg.append(f'<text x="60" y="{cur_y+22}" font-size="11" font-weight="700" fill="{col}">{tag}</text>')
        svg.append(f'<text x="60" y="{cur_y+38}" font-size="9.5" font-weight="600" fill="{INK}">{sub}</text>')
        for idx, l in enumerate(desc.split("\n")):
            svg.append(f'<text x="60" y="{cur_y+56+idx*15}" font-size="8.5" fill="{SLATE}">{l}</text>')
        cur_y += lh + 14

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/09-enforcement/figures/fig08_fallback_hierarchy.svg", "\n".join(svg))

def run_all():
    gen_fig08_enforcer_timing_waterfall()
    gen_fig08_cbf_projection()
    gen_fig08_fallback_hierarchy()

if __name__ == "__main__":
    run_all()
