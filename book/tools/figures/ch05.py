"""
book/tools/figures/ch05.py
Figures for Chapter 5: Perception & Spatial Transduction.
"""

from .common import (
    NAVY, BLUE, PETROL, TEAL, BRONZE, AMBER, CRIMSON, CORAL, PURPLE,
    SLATE, MUTED, INK, BG_LIGHT, BG_WHITE, BORDER, BORDER_DARK,
    COMMON_STYLE, COMMON_DEFS, save_svg_and_pdf
)

def gen_fig04_spatial_tokenization():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">SPATIAL AFFORDANCE TOKENIZATION VS 2D CLASSIFICATION</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Extracting SE(3) Contact Affordances &amp; Metric 3D Bounding Boxes for Downstream Kinematic Execution</text>')

    # Left: 2D Classification (Insufficient)
    lx = 30
    lw = 380
    svg.append(f'<rect x="{lx}" y="70" width="{lw}" height="320" rx="8" fill="{CORAL}" fill-opacity="0.04" stroke="{CORAL}" stroke-width="1.2"/>')
    svg.append(f'<text x="{lx+lw/2}" y="92" font-size="11" font-weight="700" fill="{CORAL}" text-anchor="middle">✕ 2D PASSIVE SEMANTIC CLASSIFICATION</text>')
    svg.append(f'<text x="{lx+lw/2}" y="108" font-size="9" fill="{MUTED}" text-anchor="middle">Disembodied Web Vision (e.g. ImageNet, CLIP)</text>')

    svg.append(f'<rect x="{lx+30}" y="130" width="160" height="110" rx="4" fill="{BG_WHITE}" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<rect x="{lx+60}" y="150" width="100" height="70" rx="2" fill="{CORAL}" fill-opacity="0.15" stroke="{CORAL}" stroke-width="1.5"/>')
    svg.append(f'<text x="{lx+110}" y="190" font-size="9" font-weight="700" fill="{CORAL}" text-anchor="middle">"mug" (99.4%)</text>')
    
    flaws = [
        "Zero metric depth (no distance z in meters)",
        "No contact normal vectors n̂ for grasping",
        "Scale ambiguity (toy mug vs industrial vessel)",
        "Blind to robot end-effector kinematics"
    ]
    for idx, fl in enumerate(flaws):
        svg.append(f'<text x="{lx+20}" y="{270+idx*20}" font-size="8.5" fill="{SLATE}">• {fl}</text>')

    # Right: 3D Spatial Tokenization (Sufficient)
    rx = 470
    rw = 380
    svg.append(f'<rect x="{rx}" y="70" width="{rw}" height="320" rx="8" fill="{TEAL}" fill-opacity="0.04" stroke="{TEAL}" stroke-width="1.2"/>')
    svg.append(f'<text x="{rx+rw/2}" y="92" font-size="11" font-weight="700" fill="{TEAL}" text-anchor="middle">✓ 3D SPATIAL AFFORDANCE TOKENIZATION</text>')
    svg.append(f'<text x="{rx+rw/2}" y="108" font-size="9" fill="{MUTED}" text-anchor="middle">Metric Embodied Representation (e.g. DINOv2 3D / PointNet)</text>')

    svg.append(f'<rect x="{rx+30}" y="130" width="160" height="110" rx="4" fill="{BG_WHITE}" stroke="{BORDER}" stroke-width="1"/>')
    # 3D Bounding box
    svg.append(f'<polygon points="{rx+60},{190} {rx+110},{160} {rx+160},{170} {rx+110},{200}" fill="{TEAL}" fill-opacity="0.2" stroke="{TEAL}" stroke-width="1.2"/>')
    svg.append(f'<polygon points="{rx+60},{190} {rx+60},{220} {rx+110},{230} {rx+110},{200}" fill="{TEAL}" fill-opacity="0.1" stroke="{TEAL}" stroke-width="1.2"/>')
    svg.append(f'<polygon points="{rx+110},{200} {rx+110},{230} {rx+160},{200} {rx+160},{170}" fill="{TEAL}" fill-opacity="0.3" stroke="{TEAL}" stroke-width="1.2"/>')
    svg.append(f'<text x="{rx+110}" y="{242}" font-size="8" font-weight="700" fill="{TEAL}" text-anchor="middle">p = [0.42, -0.15, 0.88] m</text>')

    features = [
        "Calibrated SE(3) centroid in world frame",
        "Estimated surface normals &amp; friction cone",
        "Bounding collision primitive for CBF safety filter",
        "Metric affordance lease for trajectory planner"
    ]
    for idx, ft in enumerate(features):
        svg.append(f'<text x="{rx+20}" y="{270+idx*20}" font-size="8.5" fill="{SLATE}">• {ft}</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/05-perception/figures/fig04_spatial_tokenization.svg", "\n".join(svg))

def gen_fig04_sensor_synchronization():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">SENSOR SYNCHRONIZATION: HARDWARE PTP VS SOFTWARE STAMP ILLUSION</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Why Linux User-Space Timestamping Corrupts Multi-Modal Fusion and Injects Spatial Drift</text>')

    # Top: Software Timestamping (Bad)
    ty = 70
    th = 150
    svg.append(f'<rect x="40" y="{ty}" width="{W-80}" height="{th}" rx="8" fill="{CORAL}" fill-opacity="0.04" stroke="{CORAL}" stroke-width="1.2"/>')
    svg.append(f'<text x="60" y="{ty+24}" font-size="11" font-weight="700" fill="{CORAL}">✕ THE SOFTWARE TIMESTAMP ILLUSION (gettimeofday / ROS Header)</text>')
    svg.append(f'<text x="60" y="{ty+40}" font-size="8.5" fill="{MUTED}">Timestamps assigned after OS scheduling, driver context switches, and USB/Ethernet queue delays</text>')

    # Timeline comparison
    t_start = 80
    t_w = 700
    svg.append(f'<line x1="{t_start}" y1="{ty+90}" x2="{t_start+t_w}" y2="{ty+90}" stroke="{SLATE}" stroke-width="1"/>')
    
    # Events
    svg.append(f'<circle cx="{t_start+50}" cy="{ty+90}" r="5" fill="{NAVY}"/>')
    svg.append(f'<text x="{t_start+50}" y="{ty+75}" font-size="8" font-weight="700" fill="{NAVY}" text-anchor="middle">Physical Flash (t₀)</text>')

    svg.append(f'<circle cx="{t_start+180}" cy="{ty+90}" r="5" fill="{BLUE}"/>')
    svg.append(f'<text x="{t_start+180}" y="{ty+75}" font-size="8" font-weight="700" fill="{BLUE}" text-anchor="middle">IMU DMA Arrival (+1.2 ms)</text>')

    svg.append(f'<circle cx="{t_start+450}" cy="{ty+90}" r="5" fill="{CORAL}"/>')
    svg.append(f'<text x="{t_start+450}" y="{ty+75}" font-size="8" font-weight="700" fill="{CORAL}" text-anchor="middle">Camera Frame Stamp (+38.5 ms!)</text>')

    svg.append(f'<rect x="{t_start+470}" y="{ty+105}" width="{t_w-470}" height="28" rx="4" fill="{CORAL}" fill-opacity="0.1"/>')
    svg.append(f'<text x="{t_start+480}" y="{ty+122}" font-size="8.5" font-weight="700" fill="{CORAL}">Temporal Skew: Δt = 37.3 ms ⇒ Epipolar triangulation error &gt; 18 cm!</text>')

    # Bottom: Hardware PTP (Good)
    by = 240
    bh = 160
    svg.append(f'<rect x="40" y="{by}" width="{W-80}" height="{bh}" rx="8" fill="{TEAL}" fill-opacity="0.04" stroke="{TEAL}" stroke-width="1.2"/>')
    svg.append(f'<text x="60" y="{by+24}" font-size="11" font-weight="700" fill="{TEAL}">✓ HARDWARE PTP / IEEE 1588 SYNCHRONIZATION (Cross-Triggered)</text>')
    svg.append(f'<text x="60" y="{by+40}" font-size="8.5" fill="{MUTED}">Timestamps latched in silicon hardware registers directly at photonic / IMU sample strobe</text>')

    svg.append(f'<line x1="{t_start}" y1="{by+90}" x2="{t_start+t_w}" y2="{by+90}" stroke="{SLATE}" stroke-width="1"/>')
    
    svg.append(f'<circle cx="{t_start+50}" cy="{by+90}" r="5" fill="{NAVY}"/>')
    svg.append(f'<text x="{t_start+50}" y="{by+75}" font-size="8" font-weight="700" fill="{NAVY}" text-anchor="middle">Physical Event (t₀)</text>')

    svg.append(f'<circle cx="{t_start+52}" cy="{by+90}" r="4" fill="{TEAL}"/>')
    svg.append(f'<text x="{t_start+52}" y="{by+115}" font-size="8" font-weight="700" fill="{TEAL}" text-anchor="middle">Camera Strobe Latch</text>')

    svg.append(f'<circle cx="{t_start+54}" cy="{by+90}" r="4" fill="{PETROL}"/>')
    svg.append(f'<text x="{t_start+54}" y="{by+130}" font-size="8" font-weight="700" fill="{PETROL}" text-anchor="middle">IMU Timer Latch</text>')

    svg.append(f'<rect x="{t_start+240}" y="{by+105}" width="360" height="28" rx="4" fill="{TEAL}" fill-opacity="0.1"/>')
    svg.append(f'<text x="{t_start+250}" y="{by+122}" font-size="8.5" font-weight="700" fill="{TEAL}">Hardware PTP Skew: Δt &lt; 50 ns ⇒ Spatial triangulation error &lt; 0.2 mm ✓</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/05-perception/figures/fig04_sensor_synchronization.svg", "\n".join(svg))

def gen_fig04_uma_bus():
    # Re-use the UMA bus generator from ch10
    from .ch10 import gen_ch10_uma_bus
    gen_ch10_uma_bus()
    import shutil
    shutil.copyfile("book/chapters/10-placement/figures/fig09_uma_bus_contention.svg", "book/chapters/05-perception/figures/fig04_uma_bus_contention.svg")
    shutil.copyfile("book/chapters/10-placement/figures/fig09_uma_bus_contention.pdf", "book/chapters/05-perception/figures/fig04_uma_bus_contention.pdf")

def gen_fig04_perception_pareto():
    W = 880
    H = 430
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="10" stroke="{BORDER}" stroke-width="1"/>')
    svg.append(f'<text x="{W/2}" y="28" class="title">SPATIAL PERCEPTION MULTI-OBJECTIVE PARETO FRONTIER</text>')
    svg.append(f'<text x="{W/2}" y="44" class="subtitle">Operating Trade-Offs: Model Parameter Size vs Inference Latency vs 3D Metric Accuracy</text>')

    # Plot Axes
    ax_x = 100
    ax_y = 350
    pw = 680
    ph = 260

    svg.append(f'<line x1="{ax_x}" y1="{ax_y}" x2="{ax_x+pw}" y2="{ax_y}" stroke="{SLATE}" stroke-width="1.2" marker-end="url(#arr-slate)"/>')
    svg.append(f'<text x="{ax_x+pw/2}" y="{ax_y+36}" font-size="10.5" font-weight="700" fill="{SLATE}" text-anchor="middle">Inference Latency Δt_infer (ms) → [Faster to Slower]</text>')

    svg.append(f'<line x1="{ax_x}" y1="{ax_y}" x2="{ax_x}" y2="{ax_y-ph}" stroke="{SLATE}" stroke-width="1.2" marker-end="url(#arr-slate)"/>')
    svg.append(f'<text x="{ax_x-45}" y="{ax_y-ph/2}" font-size="10.5" font-weight="700" fill="{SLATE}" transform="rotate(-90 {ax_x-45} {ax_y-ph/2})" text-anchor="middle">3D Metric Accuracy (mAP@0.25) →</text>')

    # Pareto Curve
    pareto_d = f"M {ax_x+40} {ax_y-40} Q {ax_x+220} {ax_y-200} {ax_x+580} {ax_y-240}"
    svg.append(f'<path d="{pareto_d}" fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="6,3"/>')
    svg.append(f'<text x="{ax_x+400}" y="{ax_y-230}" font-size="9" font-weight="700" fill="{BLUE}">Pareto Optimal Frontier</text>')

    # Models on plot
    models = [
        ("MobileNetV4-3D", 5.2, 0.62, NAVY, ax_x+60, ax_y-65),
        ("DINOv2-Small", 14.8, 0.81, TEAL, ax_x+180, ax_y-160),
        ("DINOv2-Base", 28.5, 0.89, BRONZE, ax_x+340, ax_y-215),
        ("PaliGemma-3B", 78.0, 0.94, PURPLE, ax_x+540, ax_y-245)
    ]

    for name, lat, acc, col, px, py in models:
        svg.append(f'<circle cx="{px}" cy="{py}" r="7" fill="{col}" stroke="#FFFFFF" stroke-width="2" filter="url(#shadow)"/>')
        bw = 145
        svg.append(f'<rect x="{px+12}" y="{py-14}" width="{bw}" height="24" rx="4" fill="{BG_WHITE}" stroke="{col}" stroke-width="1"/>')
        svg.append(f'<text x="{px+18}" y="{py+2}" font-size="8.5" font-weight="700" fill="{col}">{name} <tspan font-weight="500" fill="{MUTED}">({lat} ms)</tspan></text>')

    # Shaded Sweet Spot
    svg.append(f'<rect x="{ax_x+120}" y="{ax_y-200}" width="160" height="90" rx="6" fill="{TEAL}" fill-opacity="0.08" stroke="{TEAL}" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="{ax_x+200}" y="{ax_y-115}" font-size="8.5" font-weight="700" fill="{TEAL}" text-anchor="middle">Physical AI Sweet Spot</text>')
    svg.append(f'<text x="{ax_x+200}" y="{ax_y-100}" font-size="7.5" fill="{SLATE}" text-anchor="middle">Latency ≤ 20 ms, mAP ≥ 0.80</text>')

    svg.append('</svg>')
    save_svg_and_pdf("book/chapters/05-perception/figures/fig04_perception_pareto.svg", "\n".join(svg))

def run_all():
    gen_fig04_spatial_tokenization()
    gen_fig04_sensor_synchronization()
    gen_fig04_uma_bus()
    gen_fig04_perception_pareto()

if __name__ == "__main__":
    run_all()
