"""
book/tools/figures/ch01.py
Textbook-grade vector figures for Chapter 1: Boundary.
"""

from .common import (
    NAVY, BLUE, PETROL, TEAL, BRONZE, AMBER, CRIMSON, CORAL, PURPLE,
    SLATE, MUTED, INK, BG_LIGHT, BG_WHITE, BORDER, BORDER_DARK,
    COMMON_STYLE, COMMON_DEFS, save_svg_and_pdf
)

def gen_fig01_causal_loop():
    """
    Figure 1.3: The Closed Causal Loop of Physical AI versus Open-Loop Digital ML.
    Clear two-panel comparison with zero text collisions and generous routing margins.
    """
    W = 920
    H = 580
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="8" stroke="{BORDER}" stroke-width="1"/>')

    # =========================================================================
    # PANEL (a): OPEN-LOOP DIGITAL ML (Advisory Computation Behind Glass)
    # =========================================================================
    p1_y = 18
    p1_h = 125
    svg.append(f'<rect x="20" y="{p1_y}" width="{W-40}" height="{p1_h}" rx="6" fill="{BG_LIGHT}" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="35" y="{p1_y+20}" font-size="11" font-weight="700" fill="{BLUE}">(a) Open-Loop Digital ML: Advisory Computation Behind Glass</text>')
    svg.append(f'<text x="35" y="{p1_y+34}" font-size="8.5" fill="{MUTED}">Statistically evaluated on static benchmark distributions; errors bounded by memory rollback; zero physical force.</text>')

    # 4 Cards for Panel A
    c_w = 185
    c_h = 58
    c_y = p1_y + 46

    # Card A1: Exogenous Input
    svg.append(f'<rect x="35" y="{c_y}" width="{c_w}" height="{c_h}" rx="5" fill="{BG_WHITE}" stroke="{BLUE}" stroke-width="1.2"/>')
    svg.append(f'<text x="{35+c_w/2}" y="{c_y+17}" font-size="9.5" font-weight="700" fill="{BLUE}" text-anchor="middle">Exogenous Input</text>')
    svg.append(f'<text x="{35+c_w/2}" y="{c_y+32}" font-size="8.5" fill="{SLATE}" text-anchor="middle">Static Benchmark x ~ P(X)</text>')
    svg.append(f'<text x="{35+c_w/2}" y="{c_y+46}" font-size="8" fill="{MUTED}" text-anchor="middle">Independent &amp; Identical</text>')

    # Arrow A1 -> A2
    svg.append(f'<line x1="{35+c_w}" y1="{c_y+29}" x2="{35+c_w+35}" y2="{c_y+29}" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#arr-blue)"/>')
    svg.append(f'<text x="{35+c_w+17}" y="{c_y+21}" font-size="7.5" fill="{MUTED}" text-anchor="middle">batch</text>')

    # Card A2: Neural Model
    a2_x = 35 + c_w + 35
    svg.append(f'<rect x="{a2_x}" y="{c_y}" width="{c_w}" height="{c_h}" rx="5" fill="{BG_WHITE}" stroke="{AMBER}" stroke-width="1.2"/>')
    svg.append(f'<text x="{a2_x+c_w/2}" y="{c_y+17}" font-size="9.5" font-weight="700" fill="{AMBER}" text-anchor="middle">Neural Model</text>')
    svg.append(f'<text x="{a2_x+c_w/2}" y="{c_y+32}" font-size="8.5" fill="{SLATE}" text-anchor="middle">LLM / VLM / Classifier</text>')
    svg.append(f'<text x="{a2_x+c_w/2}" y="{c_y+46}" font-size="8" fill="{MUTED}" text-anchor="middle">y_hat = f_theta(x)</text>')

    # Arrow A2 -> A3
    svg.append(f'<line x1="{a2_x+c_w}" y1="{c_y+29}" x2="{a2_x+c_w+35}" y2="{c_y+29}" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#arr-blue)"/>')
    svg.append(f'<text x="{a2_x+c_w+17}" y="{c_y+21}" font-size="7.5" fill="{MUTED}" text-anchor="middle">infer</text>')

    # Card A3: Advisory Output
    a3_x = a2_x + c_w + 35
    svg.append(f'<rect x="{a3_x}" y="{c_y}" width="{c_w}" height="{c_h}" rx="5" fill="{BG_WHITE}" stroke="{BORDER_DARK}" stroke-width="1.2"/>')
    svg.append(f'<text x="{a3_x+c_w/2}" y="{c_y+17}" font-size="9.5" font-weight="700" fill="{INK}" text-anchor="middle">Advisory Output</text>')
    svg.append(f'<text x="{a3_x+c_w/2}" y="{c_y+32}" font-size="8.5" fill="{SLATE}" text-anchor="middle">Pixels / JSON / Text Tokens</text>')
    svg.append(f'<text x="{a3_x+c_w/2}" y="{c_y+46}" font-size="8" fill="{MUTED}" text-anchor="middle">y_hat in Y</text>')

    # Arrow A3 -> A4
    svg.append(f'<line x1="{a3_x+c_w}" y1="{c_y+29}" x2="{a3_x+c_w+35}" y2="{c_y+29}" stroke="{SLATE}" stroke-width="1.5" marker-end="url(#arr-slate)"/>')
    svg.append(f'<text x="{a3_x+c_w+17}" y="{c_y+21}" font-size="7.5" fill="{MUTED}" text-anchor="middle">render</text>')

    # Card A4: Human / Sandbox
    a4_x = a3_x + c_w + 35
    svg.append(f'<rect x="{a4_x}" y="{c_y}" width="{c_w}" height="{c_h}" rx="5" fill="{BG_WHITE}" stroke="{TEAL}" stroke-width="1.2"/>')
    svg.append(f'<text x="{a4_x+c_w/2}" y="{c_y+17}" font-size="9.5" font-weight="700" fill="{TEAL}" text-anchor="middle">Human / Sandbox</text>')
    svg.append(f'<text x="{a4_x+c_w/2}" y="{c_y+32}" font-size="8.5" fill="{SLATE}" text-anchor="middle">Dismiss / Accept / Re-run</text>')
    svg.append(f'<text x="{a4_x+c_w/2}" y="{c_y+46}" font-size="8" font-weight="600" fill="{TEAL}" text-anchor="middle">Idempotent (p = 0, W = 0)</text>')

    # =========================================================================
    # PANEL (b): CLOSED CAUSAL LOOP OF PHYSICAL AI
    # =========================================================================
    p2_y = 158
    p2_h = 405
    svg.append(f'<rect x="20" y="{p2_y}" width="{W-40}" height="{p2_h}" rx="6" fill="{BG_WHITE}" stroke="{BORDER_DARK}" stroke-width="1"/>')
    svg.append(f'<text x="35" y="{p2_y+20}" font-size="11" font-weight="700" fill="{CRIMSON}">(b) Closed Causal Loop of Physical AI: Delegated Force and Endogenous Feedback</text>')
    svg.append(f'<text x="35" y="{p2_y+34}" font-size="8.5" fill="{MUTED}">Inference commands physical energy; errors permanently alter environment state; action history endogenously dictates future sensory inputs o_t+1.</text>')

    # --- TOP ROW: COMPUTATIONAL TIER ---
    t_y = p2_y + 48
    t_w = 235
    t_h = 66

    # Box 1: Endogenous Sensing
    bx1_x = 90
    svg.append(f'<rect x="{bx1_x}" y="{t_y}" width="{t_w}" height="{t_h}" rx="5" fill="{BG_LIGHT}" stroke="{BLUE}" stroke-width="1.2"/>')
    svg.append(f'<text x="{bx1_x+10}" y="{t_y+17}" font-size="9.5" font-weight="700" fill="{BLUE}">1. Endogenous Sensing</text>')
    svg.append(f'<text x="{bx1_x+10}" y="{t_y+33}" font-size="8.5" fill="{SLATE}">Photons · IMU · Joint Encoders</text>')
    svg.append(f'<text x="{bx1_x+10}" y="{t_y+49}" font-size="8.5" font-weight="600" fill="{BLUE}">o_t ~ P(O | s_t, W_t)</text>')

    # Arrow 1 -> 2
    svg.append(f'<line x1="{bx1_x+t_w}" y1="{t_y+t_h/2}" x2="{bx1_x+t_w+35}" y2="{t_y+t_h/2}" stroke="{BLUE}" stroke-width="1.5" marker-end="url(#arr-blue)"/>')
    svg.append(f'<text x="{bx1_x+t_w+17}" y="{t_y+t_h/2-8}" font-size="7.5" fill="{MUTED}" text-anchor="middle">DMA</text>')

    # Box 2: Untrusted Brain
    bx2_x = bx1_x + t_w + 35
    svg.append(f'<rect x="{bx2_x}" y="{t_y}" width="{t_w}" height="{t_h}" rx="5" fill="{BG_LIGHT}" stroke="{AMBER}" stroke-width="1.2"/>')
    svg.append(f'<text x="{bx2_x+10}" y="{t_y+17}" font-size="9.5" font-weight="700" fill="{AMBER}">2. Untrusted Brain (MPU/NPU)</text>')
    svg.append(f'<text x="{bx2_x+10}" y="{t_y+33}" font-size="8.5" fill="{SLATE}">Learned Policy / Diffusion / VLA</text>')
    svg.append(f'<text x="{bx2_x+10}" y="{t_y+49}" font-size="8.5" font-weight="600" fill="{AMBER}">Candidate Proposal a_hat ~ pi(o_t)</text>')

    # Arrow 2 -> 3
    svg.append(f'<line x1="{bx2_x+t_w}" y1="{t_y+t_h/2}" x2="{bx2_x+t_w+35}" y2="{t_y+t_h/2}" stroke="{AMBER}" stroke-width="1.5" marker-end="url(#arr-amber)"/>')
    svg.append(f'<text x="{bx2_x+t_w+17}" y="{t_y+t_h/2-8}" font-size="7.5" fill="{MUTED}" text-anchor="middle">p_t</text>')

    # Box 3: Real-Time Nervous System
    bx3_x = bx2_x + t_w + 35
    svg.append(f'<rect x="{bx3_x}" y="{t_y}" width="{t_w}" height="{t_h}" rx="5" fill="{BG_LIGHT}" stroke="{PETROL}" stroke-width="1.2"/>')
    svg.append(f'<text x="{bx3_x+10}" y="{t_y+17}" font-size="9.5" font-weight="700" fill="{PETROL}">3. Nervous System (MCU)</text>')
    svg.append(f'<text x="{bx3_x+10}" y="{t_y+33}" font-size="8.5" fill="{SLATE}">Invariant Check: h(x) &gt;= 0 @ 1 kHz</text>')
    svg.append(f'<text x="{bx3_x+10}" y="{t_y+49}" font-size="8.5" font-weight="600" fill="{PETROL}">d_stop(v) &lt;= d_clear ==&gt; Permitted u_t</text>')

    # --- THE CAUSAL BOUNDARY BANNER ---
    b_y = t_y + t_h + 20
    b_h = 36
    svg.append(f'<line x1="40" y1="{b_y-7}" x2="{W-40}" y2="{b_y-7}" stroke="{CRIMSON}" stroke-width="1" stroke-dasharray="4,3"/>')
    svg.append(f'<text x="{W/2}" y="{b_y-11}" font-size="8" font-weight="700" fill="{CRIMSON}" text-anchor="middle" letter-spacing="1px">--- NON-REVERSIBLE ENERGY RELEASE THRESHOLD ---</text>')

    svg.append(f'<rect x="40" y="{b_y}" width="{W-80}" height="{b_h}" rx="4" fill="{CRIMSON}" fill-opacity="0.08" stroke="{CRIMSON}" stroke-width="1.3"/>')
    svg.append(f'<text x="{W/2}" y="{b_y+15}" font-size="10" font-weight="700" fill="{CRIMSON}" text-anchor="middle">THE CAUSAL BOUNDARY: MEMORY-MAPPED ACTUATOR REGISTER WRITE</text>')
    svg.append(f'<text x="{W/2}" y="{b_y+29}" font-size="8" fill="{SLATE}" text-anchor="middle">DAC Reference Latch · PWM Capture/Compare Duty Latch (u_t) · Gate Driver Control Word · Dead-Time Insertion</text>')

    # Permission latch down arrow from Box 3 into Causal Boundary
    svg.append(f'<line x1="{bx3_x+t_w/2}" y1="{t_y+t_h}" x2="{bx3_x+t_w/2}" y2="{b_y}" stroke="{PETROL}" stroke-width="1.8" marker-end="url(#arr-petrol)"/>')
    svg.append(f'<text x="{bx3_x+t_w/2+6}" y="{b_y-12}" font-size="7.5" font-weight="600" fill="{PETROL}">latch u_t</text>')

    # --- BOTTOM ROW: PHYSICAL DYNAMICS TIER ---
    bot_y = b_y + b_h + 24
    bot_w = 235
    bot_h = 70

    # Latch output arrow from Boundary to Box 4
    svg.append(f'<line x1="{bx1_x+bot_w/2}" y1="{b_y+b_h}" x2="{bx1_x+bot_w/2}" y2="{bot_y}" stroke="{CRIMSON}" stroke-width="1.8" marker-end="url(#arr-crimson)"/>')
    svg.append(f'<text x="{bx1_x+bot_w/2+6}" y="{bot_y-8}" font-size="7.5" font-weight="600" fill="{CRIMSON}">PWM duty</text>')

    # Box 4: Actuator Transduction
    svg.append(f'<rect x="{bx1_x}" y="{bot_y}" width="{bot_w}" height="{bot_h}" rx="5" fill="{BG_WHITE}" stroke="{CRIMSON}" stroke-width="1.2"/>')
    svg.append(f'<text x="{bx1_x+10}" y="{bot_y+17}" font-size="9.5" font-weight="700" fill="{CRIMSON}">4. Actuator Transduction</text>')
    svg.append(f'<text x="{bx1_x+10}" y="{bot_y+33}" font-size="8.5" fill="{SLATE}">Lorentz Force: F = I (L x B)</text>')
    svg.append(f'<text x="{bx1_x+10}" y="{bot_y+49}" font-size="8.5" fill="{SLATE}">Joule Heat: Delta Q = I^2 R Delta t</text>')

    # Arrow 4 -> 5
    svg.append(f'<line x1="{bx1_x+bot_w}" y1="{bot_y+bot_h/2}" x2="{bx2_x}" y2="{bot_y+bot_h/2}" stroke="{CRIMSON}" stroke-width="1.5" marker-end="url(#arr-crimson)"/>')
    svg.append(f'<text x="{bx1_x+bot_w+17}" y="{bot_y+bot_h/2-8}" font-size="7.5" fill="{MUTED}" text-anchor="middle">torque tau</text>')

    # Box 5: Mechanical Dynamics
    svg.append(f'<rect x="{bx2_x}" y="{bot_y}" width="{bot_w}" height="{bot_h}" rx="5" fill="{BG_WHITE}" stroke="{CRIMSON}" stroke-width="1.2"/>')
    svg.append(f'<text x="{bx2_x+10}" y="{bot_y+17}" font-size="9.5" font-weight="700" fill="{CRIMSON}">5. Mechanical Dynamics</text>')
    svg.append(f'<text x="{bx2_x+10}" y="{bot_y+33}" font-size="8.5" fill="{SLATE}">Torque tau = M(q)q_ddot + C(q,q_dot)</text>')
    svg.append(f'<text x="{bx2_x+10}" y="{bot_y+49}" font-size="8.5" fill="{SLATE}">Kinetic Momentum: p = mv</text>')

    # Arrow 5 -> 6
    svg.append(f'<line x1="{bx2_x+bot_w}" y1="{bot_y+bot_h/2}" x2="{bx3_x}" y2="{bot_y+bot_h/2}" stroke="{CRIMSON}" stroke-width="1.5" marker-end="url(#arr-crimson)"/>')
    svg.append(f'<text x="{bx2_x+bot_w+17}" y="{bot_y+bot_h/2-8}" font-size="7.5" fill="{MUTED}" text-anchor="middle">work F dx</text>')

    # Box 6: Physical Environment
    svg.append(f'<rect x="{bx3_x}" y="{bot_y}" width="{bot_w}" height="{bot_h}" rx="5" fill="{BG_WHITE}" stroke="{CRIMSON}" stroke-width="1.2"/>')
    svg.append(f'<text x="{bx3_x+10}" y="{bot_y+17}" font-size="9.5" font-weight="700" fill="{CRIMSON}">6. Physical Environment</text>')
    svg.append(f'<text x="{bx3_x+10}" y="{bot_y+33}" font-size="8.5" fill="{SLATE}">Environment State: W_t -&gt; W_t+1</text>')
    svg.append(f'<text x="{bx3_x+10}" y="{bot_y+49}" font-size="8.5" fill="{SLATE}">Delay as Distance: Delta x = int v dt</text>')

    # =========================================================================
    # WIDE OUTER FEEDBACK LOOP (ENDOGENOUS SENSORY SHIFT)
    # Clear routing around the bottom margin with generous clearance
    # =========================================================================
    loop_y = bot_y + bot_h + 28
    loop_x = 42

    # Line 1: Down from Box 6
    svg.append(f'<line x1="{bx3_x+bot_w/2}" y1="{bot_y+bot_h}" x2="{bx3_x+bot_w/2}" y2="{loop_y}" stroke="{PETROL}" stroke-width="2"/>')
    # Line 2: Across to the right of banner
    svg.append(f'<line x1="{bx3_x+bot_w/2}" y1="{loop_y}" x2="{W/2+250}" y2="{loop_y}" stroke="{PETROL}" stroke-width="2"/>')
    # Line 3: Across from left of banner to left margin
    svg.append(f'<line x1="{W/2-250}" y1="{loop_y}" x2="{loop_x}" y2="{loop_y}" stroke="{PETROL}" stroke-width="2"/>')
    # Line 4: Up the left margin
    svg.append(f'<line x1="{loop_x}" y1="{loop_y}" x2="{loop_x}" y2="{t_y+t_h/2}" stroke="{PETROL}" stroke-width="2"/>')
    # Line 5: Into Box 1
    svg.append(f'<line x1="{loop_x}" y1="{t_y+t_h/2}" x2="{bx1_x}" y2="{t_y+t_h/2}" stroke="{PETROL}" stroke-width="2" marker-end="url(#arr-petrol)"/>')

    # Centered Feedback Badge
    svg.append(f'<rect x="{W/2-245}" y="{loop_y-11}" width="490" height="22" rx="4" fill="{BG_WHITE}" stroke="{PETROL}" stroke-width="1.2" filter="url(#shadow)"/>')
    svg.append(f'<text x="{W/2}" y="{loop_y+4}" font-size="8.5" font-weight="700" fill="{PETROL}" text-anchor="middle">ENDOGENOUS SENSORY FEEDBACK: o_t+1 ~ P(O | s_t+1, W_t+1) [Actions reshape future observations]</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/01-boundary/figures/fig01_causal_loop.svg", "\n".join(svg))


def gen_fig01_scope_venn():
    """
    Figure 1.6: The Physical AI Scope Test (3-set Venn / Euler Diagram).
    Pristine textbook-grade diagram: clean circular sets, no overlapping text cards, generous padding.
    """
    W = 880
    H = 530
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="8" stroke="{BORDER}" stroke-width="1"/>')

    # Header
    svg.append(f'<text x="{W/2}" y="26" class="title">THE PHYSICAL AI SCOPE TEST: TRIPARTITE ARCHITECTURAL CRITERION</text>')
    svg.append(f'<text x="{W/2}" y="42" class="subtitle">Physical AI exists strictly at the three-way intersection of Learned Policies, Consequential Feedback, and Delegated Authority</text>')

    # 3 Circles: Centers and Radii
    R = 135
    cx1 = 355
    cy1 = 210

    cx2 = 525
    cy2 = 210

    cx3 = 440
    cy3 = 320

    # Draw 3 translucent circles
    svg.append(f'<circle cx="{cx1}" cy="{cy1}" r="{R}" fill="{BLUE}" fill-opacity="0.08" stroke="{BLUE}" stroke-width="1.6"/>')
    svg.append(f'<circle cx="{cx2}" cy="{cy2}" r="{R}" fill="{CRIMSON}" fill-opacity="0.08" stroke="{CRIMSON}" stroke-width="1.6"/>')
    svg.append(f'<circle cx="{cx3}" cy="{cy3}" r="{R}" fill="{PETROL}" fill-opacity="0.08" stroke="{PETROL}" stroke-width="1.6"/>')

    # =========================================================================
    # SET HEADERS (OUTER LABELS)
    # =========================================================================
    # Top Left Set: Learned Models
    svg.append(f'<text x="190" y="58" font-size="10.5" font-weight="700" fill="{BLUE}" text-anchor="middle">CRITERION 1: LEARNED MODELS</text>')
    svg.append(f'<text x="190" y="72" font-size="8.5" fill="{SLATE}" text-anchor="middle">Unspecifiable neural policies</text>')
    svg.append(f'<text x="190" y="84" font-size="8.5" fill="{MUTED}" text-anchor="middle">Acquired inductively from data</text>')

    # Top Right Set: Delegated Authority
    svg.append(f'<text x="690" y="58" font-size="10.5" font-weight="700" fill="{CRIMSON}" text-anchor="middle">CRITERION 2: DELEGATED AUTHORITY</text>')
    svg.append(f'<text x="690" y="72" font-size="8.5" fill="{SLATE}" text-anchor="middle">Automated actuator register writes</text>')
    svg.append(f'<text x="690" y="84" font-size="8.5" fill="{MUTED}" text-anchor="middle">Zero synchronous human in the loop</text>')

    # Bottom Set: Consequential Physical Feedback
    svg.append(f'<text x="440" y="478" font-size="10.5" font-weight="700" fill="{PETROL}" text-anchor="middle">CRITERION 3: CONSEQUENTIAL PHYSICAL FEEDBACK</text>')
    svg.append(f'<text x="440" y="493" font-size="8.5" fill="{SLATE}" text-anchor="middle">Actions alter external world state (s_t+1 ~ P(s|s_t,a_t)) under mechanics, momentum (p=mv), and thermodynamics</text>')

    # =========================================================================
    # PURE SINGLE-SET OUTER REGIONS
    # =========================================================================
    # 1. Pure Digital ML (Top Left)
    svg.append(f'<text x="250" y="190" font-size="9.5" font-weight="700" fill="{BLUE}" text-anchor="middle">Pure Digital ML</text>')
    svg.append(f'<text x="250" y="204" font-size="8" fill="{MUTED}" text-anchor="middle">LLMs · Vision Classifiers</text>')
    svg.append(f'<text x="250" y="216" font-size="8" fill="{MUTED}" text-anchor="middle">(No authority, no feedback)</text>')

    # 2. Open-Loop Actuation (Top Right)
    svg.append(f'<text x="630" y="190" font-size="9.5" font-weight="700" fill="{CRIMSON}" text-anchor="middle">Open-Loop Actuation</text>')
    svg.append(f'<text x="630" y="204" font-size="8" fill="{MUTED}" text-anchor="middle">Dumb Relays · Fixed Timers</text>')
    svg.append(f'<text x="630" y="216" font-size="8" fill="{MUTED}" text-anchor="middle">(No model, no feedback)</text>')

    # 3. Passive Mechanics (Bottom)
    svg.append(f'<text x="440" y="390" font-size="9.5" font-weight="700" fill="{PETROL}" text-anchor="middle">Passive Mechanics</text>')
    svg.append(f'<text x="440" y="404" font-size="8" fill="{MUTED}" text-anchor="middle">Spring-Mass Dampers · Thermal Insulation</text>')

    # =========================================================================
    # TWO-SET INTERSECTION REGIONS (ADJACENT DISCIPLINES)
    # =========================================================================
    # Region A: Top Intersection (Learned + Delegated, No Physical Feedback)
    svg.append(f'<rect x="370" y="120" width="140" height="44" rx="4" fill="{BG_WHITE}" stroke="{PURPLE}" stroke-width="1" filter="url(#shadow)"/>')
    svg.append(f'<text x="440" y="135" font-size="8.5" font-weight="700" fill="{PURPLE}" text-anchor="middle">Digital Autonomous</text>')
    svg.append(f'<text x="440" y="147" font-size="7.5" fill="{SLATE}" text-anchor="middle">High-Freq Algorithmic Trading</text>')
    svg.append(f'<text x="440" y="157" font-size="7.5" fill="{MUTED}" text-anchor="middle">Cloud Autoscalers (Rollback p=0)</text>')

    # Region B: Left-Bottom Intersection (Learned + Feedback, No Delegated Authority)
    svg.append(f'<rect x="210" y="315" width="145" height="44" rx="4" fill="{BG_WHITE}" stroke="{AMBER}" stroke-width="1" filter="url(#shadow)"/>')
    svg.append(f'<text x="282" y="330" font-size="8.5" font-weight="700" fill="{AMBER}" text-anchor="middle">Advisory Decision</text>')
    svg.append(f'<text x="282" y="342" font-size="7.5" fill="{SLATE}" text-anchor="middle">Driver Drowsiness Alert HUD</text>')
    svg.append(f'<text x="282" y="352" font-size="7.5" fill="{MUTED}" text-anchor="middle">Surgical Diagnostic Guidance</text>')

    # Region C: Right-Bottom Intersection (Feedback + Delegated, No Learned Policy)
    svg.append(f'<rect x="525" y="315" width="145" height="44" rx="4" fill="{BG_WHITE}" stroke="{TEAL}" stroke-width="1.1" filter="url(#shadow)"/>')
    svg.append(f'<text x="597" y="330" font-size="8.5" font-weight="700" fill="{TEAL}" text-anchor="middle">Classical Control</text>')
    svg.append(f'<text x="597" y="342" font-size="7.5" fill="{SLATE}" text-anchor="middle">1 kHz Quadrotor PID · MPC</text>')
    svg.append(f'<text x="597" y="352" font-size="7.5" fill="{MUTED}" text-anchor="middle">Watt Governor (Lyapunov Safe)</text>')

    # =========================================================================
    # THREE-WAY INTERSECTION (PHYSICAL AI CORE)
    # =========================================================================
    core_cx = 440
    core_cy = 250
    svg.append(f'<rect x="{core_cx-75}" y="{core_cy-30}" width="150" height="60" rx="6" fill="{NAVY}" stroke="{BORDER_DARK}" stroke-width="1.5" filter="url(#shadow)"/>')
    svg.append(f'<text x="{core_cx}" y="{core_cy-10}" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1px">PHYSICAL AI</text>')
    svg.append(f'<text x="{core_cx}" y="{core_cy+6}" font-size="8" fill="#E2E8F0" text-anchor="middle">Autonomous Vehicles · Humanoids</text>')
    svg.append(f'<text x="{core_cx}" y="{core_cy+18}" font-size="8" fill="#93C5FD" text-anchor="middle">Dynamic Contact Manipulators</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/01-boundary/figures/fig01_scope_venn.svg", "\n".join(svg))


def run_all():
    gen_fig01_causal_loop()
    gen_fig01_scope_venn()

if __name__ == "__main__":
    run_all()
