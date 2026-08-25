"""
book/tools/figures/ch02.py
Figures for Chapter 2: The Five Physical Columns.
"""

from .common import (
    NAVY, BLUE, PETROL, TEAL, BRONZE, AMBER, CRIMSON, CORAL, PURPLE,
    SLATE, MUTED, INK, BG_LIGHT, BG_WHITE, BORDER, BORDER_DARK,
    COMMON_STYLE, COMMON_DEFS, save_svg_and_pdf
)

def gen_fig02_physical_columns():
    W = 900
    H = 460
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">THE FIVE PHYSICAL COLUMNS OF EMBODIED INTELLIGENCE</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">The Fundamental Physical Bounds Governing Every Closed-Loop Cyber-Physical System</text>')

    columns = [
        ("COLUMN 1", "TIME &amp; FRESHNESS", "τ_world Latency Bounds",
         ["Sense-to-actuation delay Δt", "P99.9 tail latency freshness", "Stale observations cause drift", "Hard deadlines: Δt ≤ τ_world"],
         NAVY),
        ("COLUMN 2", "INERTIA &amp; MOMENTUM", "p = mv Kinetic Energy",
         ["Mass cannot stop instantaneously", "Kinetic braking distance d_stop", "Centrifugal &amp; Coriolis forces", "Work envelope geofencing"],
         BLUE),
        ("COLUMN 3", "ACTUATION DYNAMICS", "τ_motor &amp; Friction Limits",
         ["BLDC torque-speed envelopes", "Gearbox backlash &amp; jerk bounds", "Coulomb/viscous joint friction", "Smooth C² acceleration profiles"],
         BRONZE),
        ("COLUMN 4", "ENERGY &amp; THERMODYNAMICS", "P = IV &amp; Joule Heat",
         ["Battery voltage sag under load", "Junction heating T_j = T_a + P·θ_JA", "DVFS thermal throttling cascades", "Regenerative braking limits"],
         AMBER),
        ("COLUMN 5", "SILICON &amp; COMPUTE", "SRAM, AXI &amp; DMA Memory",
         ["Zero dynamic malloc in RT loops", "UMA crossbar bus contention", "Hardware watchdog supervisors", "Deterministic FreeRTOS priority"],
         PURPLE)
    ]

    cw = 158
    gap = 14
    start_x = (W - (5 * cw + 4 * gap)) / 2

    for i, (tag, title, sub, items, col) in enumerate(columns):
        x = start_x + i * (cw + gap)
        y = 66
        h = 330

        svg.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{h}" rx="6" fill="{BG_WHITE}" stroke="{col}" stroke-width="1.2" filter="url(#shadow)"/>')
        svg.append(f'<rect x="{x}" y="{y}" width="{cw}" height="22" rx="6" fill="{col}" fill-opacity="0.12"/>')
        svg.append(f'<text x="{x+cw/2}" y="{y+15}" font-size="8.5" font-weight="700" fill="{col}" text-anchor="middle">{tag}</text>')
        svg.append(f'<text x="{x+cw/2}" y="{y+38}" font-size="10" font-weight="700" fill="{INK}" text-anchor="middle">{title.split("&amp;")[0]}</text>')
        if "&amp;" in title:
            svg.append(f'<text x="{x+cw/2}" y="{y+50}" font-size="10" font-weight="700" fill="{INK}" text-anchor="middle">&amp; {title.split("&amp;")[1]}</text>')
            sub_y = y + 64
        else:
            sub_y = y + 52

        svg.append(f'<text x="{x+cw/2}" y="{sub_y}" font-size="8" fill="{MUTED}" text-anchor="middle">{sub}</text>')

        cy = y + 78
        for it in items:
            svg.append(f'<text x="{x+8}" y="{cy}" font-size="8" fill="{SLATE}">• {it}</text>')
            cy += 20

    # Bottom Invariant
    svg.append(f'<rect x="{start_x}" y="406" width="{5*cw + 4*gap}" height="40" rx="5" fill="{BG_LIGHT}" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="422" font-size="9" font-weight="700" fill="{NAVY}" text-anchor="middle">FIRST-PRINCIPLES PHYSICAL GUARANTEE</text>')
    svg.append(f'<text x="{W/2}" y="436" font-size="8.5" fill="{SLATE}" text-anchor="middle">Software models propose intent; the Five Physical Columns enforce the boundary of physical possibility.</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/02-constraints/figures/fig02_physical_columns.svg", "\n".join(svg))

def gen_fig02_metrology_setup():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">HARDWARE-TRIGGERED SENSE-TO-ACTUATION METROLOGY</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">End-to-End Latency Instrumentation: Optical LED Flash ⟶ Oscilloscope Digital Logic Analyzer</text>')

    # Left: Stimulus (Optical LED)
    lx = 30
    lw = 230
    svg.append(f'<rect x="{lx}" y="70" width="{lw}" height="320" rx="8" fill="{BG_WHITE}" stroke="{AMBER}" stroke-width="1.2" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{lx}" y="70" width="{lw}" height="24" rx="8" fill="{AMBER}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{lx+lw/2}" y="86" font-size="9.5" font-weight="700" fill="{AMBER}" text-anchor="middle">1. HARDWARE STIMULUS</text>')
    svg.append(f'<text x="{lx+14}" y="115" font-size="10.5" font-weight="700" fill="{INK}">High-Speed LED Target</text>')
    svg.append(f'<text x="{lx+14}" y="132" font-size="8.5" fill="{SLATE}">• 100 ns rise-time pulsed LED</text>')
    svg.append(f'<text x="{lx+14}" y="148" font-size="8.5" fill="{SLATE}">• Microcontroller hardware strobe</text>')
    svg.append(f'<text x="{lx+14}" y="164" font-size="8.5" fill="{SLATE}">• Emits pulse at precise t_0</text>')
    svg.append(f'<text x="{lx+14}" y="180" font-size="8.5" fill="{SLATE}">• CH1 Trigger on oscilloscope</text>')
    
    svg.append(f'<circle cx="{lx+lw/2}" cy="260" r="30" fill="{AMBER}" fill-opacity="0.15" stroke="{AMBER}" stroke-width="2"/>')
    svg.append(f'<text x="{lx+lw/2}" y="264" font-size="10" font-weight="700" fill="{AMBER}" text-anchor="middle">LED FLASH</text>')
    svg.append(f'<text x="{lx+lw/2}" y="360" font-size="9" font-weight="600" fill="{INK}" text-anchor="middle">t₀ = 0.000 ms</text>')

    # Center: Device Under Test (Host MPU + MCU)
    cx = 290
    cw = 300
    svg.append(f'<rect x="{cx}" y="70" width="{cw}" height="320" rx="8" fill="{BG_WHITE}" stroke="{NAVY}" stroke-width="1.3" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{cx}" y="70" width="{cw}" height="24" rx="8" fill="{NAVY}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{cx+cw/2}" y="86" font-size="9.5" font-weight="700" fill="{NAVY}" text-anchor="middle">2. PHYSICAL AI AGENT (DUT)</text>')
    
    stages = [
        ("Camera CMOS Sensor Exposure", "MIPI CSI-2 transfer: 16.6 ms", NAVY),
        ("Vision Tokenizer &amp; VLM Planning", "Neural model inference: 28.4 ms", BLUE),
        ("Shared Memory TCM IPC Transfer", "Lock-free seqlock: 0.12 ms", BRONZE),
        ("MCU 1 kHz Barrier QP Enforcer", "Active-set safety filter: 0.18 ms", PETROL),
        ("PWM Gate Driver Motor Stage", "Current loop response: 0.85 ms", CRIMSON)
    ]
    for idx, (t, d, col) in enumerate(stages):
        by = 105 + idx * 45
        svg.append(f'<rect x="{cx+12}" y="{by}" width="{cw-24}" height="38" rx="4" fill="{BG_LIGHT}" stroke="{BORDER}" stroke-width="1"/>')
        svg.append(f'<text x="{cx+20}" y="{by+16}" font-size="9" font-weight="700" fill="{col}">{t}</text>')
        svg.append(f'<text x="{cx+20}" y="{by+30}" font-size="8" fill="{SLATE}">{d}</text>')

    svg.append(f'<text x="{cx+cw/2}" y="350" font-size="9.5" font-weight="700" fill="{NAVY}" text-anchor="middle">GPIO Toggle Pin at Motor Step</text>')
    svg.append(f'<text x="{cx+cw/2}" y="365" font-size="9" fill="{MUTED}" text-anchor="middle">CH2 Input on oscilloscope</text>')

    # Right: Metrology Instrument (Oscilloscope)
    rx = 620
    rw = 230
    svg.append(f'<rect x="{rx}" y="70" width="{rw}" height="320" rx="8" fill="{BG_WHITE}" stroke="{TEAL}" stroke-width="1.2" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{rx}" y="70" width="{rw}" height="24" rx="8" fill="{TEAL}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{rx+rw/2}" y="86" font-size="9.5" font-weight="700" fill="{TEAL}" text-anchor="middle">3. RIGOROUS METROLOGY</text>')
    svg.append(f'<text x="{rx+14}" y="115" font-size="10.5" font-weight="700" fill="{INK}">Digital Storage Scope</text>')
    svg.append(f'<text x="{rx+14}" y="132" font-size="8.5" fill="{SLATE}">• 1 GSa/s hardware timebase</text>')
    svg.append(f'<text x="{rx+14}" y="148" font-size="8.5" fill="{SLATE}">• True photon-to-torque wall clock</text>')
    svg.append(f'<text x="{rx+14}" y="164" font-size="8.5" fill="{SLATE}">• Zero software logging jitter</text>')
    svg.append(f'<text x="{rx+14}" y="180" font-size="8.5" fill="{SLATE}">• Captures P99.9 tail distribution</text>')

    svg.append(f'<rect x="{rx+15}" y="210" width="{rw-30}" height="100" rx="4" fill="{INK}" stroke="{BORDER_DARK}" stroke-width="1"/>')
    svg.append(f'<line x1="{rx+25}" y1="240" x2="{rx+70}" y2="240" stroke="{AMBER}" stroke-width="1.5"/>')
    svg.append(f'<line x1="{rx+70}" y1="240" x2="{rx+70}" y2="225" stroke="{AMBER}" stroke-width="1.5"/>')
    svg.append(f'<line x1="{rx+70}" y1="225" x2="{rx+205}" y2="225" stroke="{AMBER}" stroke-width="1.5"/>')
    svg.append(f'<text x="{rx+30}" y="235" font-size="7.5" font-weight="700" fill="{AMBER}">CH1 (LED)</text>')

    svg.append(f'<line x1="{rx+25}" y1="285" x2="{rx+160}" y2="285" stroke="{TEAL}" stroke-width="1.5"/>')
    svg.append(f'<line x1="{rx+160}" y1="285" x2="{rx+160}" y2="270" stroke="{TEAL}" stroke-width="1.5"/>')
    svg.append(f'<line x1="{rx+160}" y1="270" x2="{rx+205}" y2="270" stroke="{TEAL}" stroke-width="1.5"/>')
    svg.append(f'<text x="{rx+30}" y="280" font-size="7.5" font-weight="700" fill="{TEAL}">CH2 (Torque)</text>')

    svg.append(f'<line x1="{rx+70}" y1="295" x2="{rx+160}" y2="295" stroke="#FFFFFF" stroke-width="1" marker-start="url(#arr-teal)" marker-end="url(#arr-teal)"/>')
    svg.append(f'<text x="{rx+115}" y="306" font-size="8" font-weight="700" fill="#FFFFFF" text-anchor="middle">Δt_wall = 46.15 ms</text>')

    svg.append(f'<text x="{rx+rw/2}" y="360" font-size="9" font-weight="600" fill="{INK}" text-anchor="middle">True Wall Latency</text>')

    # Connectors
    svg.append(f'<line x1="{lx+lw}" y1="230" x2="{cx}" y2="230" stroke="{AMBER}" stroke-width="1.5" marker-end="url(#arr-bronze)"/>')
    svg.append(f'<line x1="{cx+cw}" y1="230" x2="{rx}" y2="230" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#arr-navy)"/>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/02-constraints/figures/fig02_metrology_setup.svg", "\n".join(svg))

def gen_fig02_latency_waterfall():
    W = 900
    H = 440
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">7-STAGE SENSE-TO-ACTUATION LATENCY WATERFALL &amp; THE FRESHNESS WALL</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Cumulative Wall-Clock Breakdown: Why P99 Tail Latency Directly Dictates Stopping Distance</text>')

    stages = [
        ("1. Photonic Integration &amp; CMOS Exposure", 16.6, NAVY),
        ("2. MIPI CSI-2 DMA Serialization", 4.2, NAVY),
        ("3. Spatial Tokenizer (DINOv2 / MobileNet)", 14.8, BLUE),
        ("4. Trajectory Chunk Planning (ACT / Diffusion)", 22.5, BRONZE),
        ("5. Shared SRAM Seqlock IPC Transfer", 0.4, BRONZE),
        ("6. MCU Real-Time Safety Filter (1 kHz QP)", 0.2, PETROL),
        ("7. Inverter Gate Driver &amp; Current Rise", 1.3, CRIMSON)
    ]

    start_x = 280
    total_w = 480
    total_time = sum(s[1] for s in stages)  # 60.0 ms
    cur_cum = 0

    # Axis
    ax_y = 380
    svg.append(f'<line x1="{start_x}" y1="{ax_y}" x2="{start_x+total_w+20}" y2="{ax_y}" stroke="{SLATE}" stroke-width="1.2" marker-end="url(#arr-slate)"/>')
    svg.append(f'<text x="{start_x+total_w+28}" y="{ax_y+4}" font-size="9" font-weight="700" fill="{SLATE}">Latency (ms)</text>')

    for t_mark in [0, 10, 20, 30, 40, 50, 60]:
        x_m = start_x + (t_mark / 60.0) * total_w
        svg.append(f'<line x1="{x_m}" y1="{ax_y}" x2="{x_m}" y2="{ax_y+6}" stroke="{SLATE}" stroke-width="1"/>')
        svg.append(f'<text x="{x_m}" y="{ax_y+18}" font-size="8.5" fill="{SLATE}" text-anchor="middle">{t_mark}</text>')
        svg.append(f'<line x1="{x_m}" y1="65" x2="{x_m}" y2="{ax_y}" stroke="{BORDER}" stroke-width="0.8" stroke-dasharray="3,3"/>')

    for idx, (name, dur, col) in enumerate(stages):
        y = 75 + idx * 42
        # Label
        svg.append(f'<text x="{start_x-12}" y="{y+16}" font-size="9" font-weight="600" fill="{INK}" text-anchor="end">{name}</text>')
        
        # Waterfall Bar
        bx = start_x + (cur_cum / 60.0) * total_w
        bw = (dur / 60.0) * total_w
        svg.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="26" rx="4" fill="{col}" fill-opacity="0.85" stroke="{col}" stroke-width="1"/>')
        if bw < 35:
            svg.append(f'<text x="{bx-6}" y="{y+17}" font-size="8" font-weight="700" fill="{col}" text-anchor="end">+{dur} ms</text>')
        else:
            svg.append(f'<text x="{bx+bw/2}" y="{y+17}" font-size="8" font-weight="700" fill="#FFFFFF" text-anchor="middle">+{dur} ms</text>')

        cur_cum += dur

    # Freshness Wall Marker at 60 ms
    fx = start_x + total_w
    svg.append(f'<line x1="{fx}" y1="65" x2="{fx}" y2="{ax_y}" stroke="{CORAL}" stroke-width="2"/>')
    svg.append(f'<rect x="{fx-70}" y="56" width="140" height="20" rx="4" fill="{CORAL}"/>')
    svg.append(f'<text x="{fx}" y="70" font-size="8.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">FRESHNESS WALL: 60 ms</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/02-constraints/figures/fig02_latency_waterfall.svg", "\n".join(svg))

def gen_fig02_stopping_distance():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">DYNAMIC STOPPING DISTANCE: REACTION LAG + KINETIC BRAKING</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">d_stop(t) = v(t) · Δt_latency + v(t)² / (2 a_max) ≤ d_clearance</text>')

    # 2 Sub-components
    # Left: Linear Reaction Lag
    lx = 40
    lw = 370
    svg.append(f'<rect x="{lx}" y="70" width="{lw}" height="140" rx="8" fill="{BLUE}" fill-opacity="0.05" stroke="{BLUE}" stroke-width="1.2" filter="url(#shadow)"/>')
    svg.append(f'<text x="{lx+16}" y="92" font-size="11" font-weight="700" fill="{BLUE}">1. SENSE-TO-ACTUATION REACTION DISTANCE</text>')
    svg.append(f'<text x="{lx+16}" y="112" font-size="12" font-weight="700" fill="{INK}">d_reaction = v₀ · Δt_wall</text>')
    svg.append(f'<text x="{lx+16}" y="132" font-size="8.5" fill="{SLATE}">• Vehicle travels at initial speed during computation lag</text>')
    svg.append(f'<text x="{lx+16}" y="148" font-size="8.5" fill="{SLATE}">• Linear growth with latency: doubling latency doubles distance</text>')
    svg.append(f'<text x="{lx+16}" y="164" font-size="8.5" fill="{SLATE}">• Example: at 1.5 m/s, Δt=80 ms ⇒ d_reaction = 12.0 cm</text>')

    # Right: Quadratic Kinetic Braking
    rx = 470
    rw = 370
    svg.append(f'<rect x="{rx}" y="70" width="{rw}" height="140" rx="8" fill="{CRIMSON}" fill-opacity="0.05" stroke="{CRIMSON}" stroke-width="1.2" filter="url(#shadow)"/>')
    svg.append(f'<text x="{rx+16}" y="92" font-size="11" font-weight="700" fill="{CRIMSON}">2. PHYSICAL KINETIC BRAKING DISTANCE</text>')
    svg.append(f'<text x="{rx+16}" y="112" font-size="12" font-weight="700" fill="{INK}">d_braking = v₀² / (2 · a_max)</text>')
    svg.append(f'<text x="{rx+16}" y="132" font-size="8.5" fill="{SLATE}">• Dissipating kinetic energy E_k = 1/2 m v² against friction μ</text>')
    svg.append(f'<text x="{rx+16}" y="148" font-size="8.5" fill="{SLATE}">• Quadratic growth with velocity: doubling speed quadruples distance</text>')
    svg.append(f'<text x="{rx+16}" y="164" font-size="8.5" fill="{SLATE}">• Example: at 1.5 m/s, a_max=3.0 m/s² ⇒ d_braking = 37.5 cm</text>')

    # Bottom Combined Envelope Graphic
    by = 230
    bw = W - 80
    bh = 170
    svg.append(f'<rect x="40" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{BG_LIGHT}" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="{by+24}" font-size="11" font-weight="700" fill="{NAVY}" text-anchor="middle">TOTAL DYNAMIC STOPPING CLEARANCE ENVELOPE</text>')

    # Distance Bar Representation
    bar_y = by + 50
    bar_w = 640
    bar_x = (W - bar_w) / 2

    # Obstacle line
    svg.append(f'<line x1="{bar_x+bar_w}" y1="{bar_y-20}" x2="{bar_x+bar_w}" y2="{bar_y+60}" stroke="{CORAL}" stroke-width="3"/>')
    svg.append(f'<text x="{bar_x+bar_w}" y="{bar_y-26}" font-size="9" font-weight="700" fill="{CORAL}" text-anchor="middle">OBSTACLE WALL (d_clearance = 60 cm)</text>')

    # Reaction bar (12 cm = 128 px)
    rw_px = 128
    svg.append(f'<rect x="{bar_x}" y="{bar_y}" width="{rw_px}" height="36" rx="4" fill="{BLUE}" fill-opacity="0.85"/>')
    svg.append(f'<text x="{bar_x+rw_px/2}" y="{bar_y+22}" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">Reaction: 12.0 cm</text>')

    # Braking bar (37.5 cm = 400 px)
    bw_px = 400
    svg.append(f'<rect x="{bar_x+rw_px}" y="{bar_y}" width="{bw_px}" height="36" rx="4" fill="{CRIMSON}" fill-opacity="0.85"/>')
    svg.append(f'<text x="{bar_x+rw_px+bw_px/2}" y="{bar_y+22}" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">Kinetic Braking: 37.5 cm</text>')

    # Safety Margin (10.5 cm = 112 px)
    mw_px = bar_w - rw_px - bw_px
    svg.append(f'<rect x="{bar_x+rw_px+bw_px}" y="{bar_y}" width="{mw_px}" height="36" rx="4" fill="{TEAL}" fill-opacity="0.85"/>')
    svg.append(f'<text x="{bar_x+rw_px+bw_px+mw_px/2}" y="{bar_y+22}" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">Margin: +10.5 cm ✓</text>')

    svg.append(f'<text x="{W/2}" y="{by+130}" font-size="9.5" font-weight="700" fill="{INK}" text-anchor="middle">Total Stopping Distance: d_stop = 49.5 cm ≤ Clearance: 60.0 cm (Certified Safe)</text>')
    svg.append(f'<text x="{W/2}" y="{by+146}" font-size="8.5" fill="{MUTED}" text-anchor="middle">If latency spikes to 200 ms (P99.9 tail), d_reaction becomes 30 cm ⇒ d_stop = 67.5 cm > 60 cm ⇒ COLLISION!</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/02-constraints/figures/fig02_stopping_distance.svg", "\n".join(svg))

def run_all():
    gen_fig02_physical_columns()
    gen_fig02_metrology_setup()
    gen_fig02_latency_waterfall()
    gen_fig02_stopping_distance()

if __name__ == "__main__":
    run_all()
