#!/usr/bin/env python3
"""
book/tools/figures/master_locator.py
Generates the publication-grade 4-tier stacked architectural locator diagram
for all 17 chapters of Physical AI Systems.
"""

import os
import subprocess
import re

NAVY = "#1F407A"         # ETH dark blue - Primary structural
BLUE = "#215CAF"         # Ingestion / Perception
PETROL = "#007A87"       # MCU / Real-time reflex / Memory
TEAL = "#10B981"         # Verified / Safe
BRONZE = "#B87333"       # Planning / Intent / Proposal
AMBER = "#D97706"        # Warning / Contention
CRIMSON = "#A51C30"      # Physical World / Fault / Veto / Active highlight
PURPLE = "#5B4B8A"       # Governance / Release Gate
SLATE = "#475569"        # Body text / Secondary lines
MUTED = "#64748B"        # Subtitles / Secondary labels
INK = "#0F172A"          # Dark Title text
BG_LIGHT = "#F8FAFC"     # Card Background
BG_WHITE = "#FFFFFF"     # Container Background
BORDER = "#CBD5E1"       # Subtle card border
BORDER_DARK = "#94A3B8"  # Prominent border
ACTIVE_BG = "#FEF2F2"    # Light crimson highlight background

COMMON_STYLE = """
<style>
  text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  .hdr-title { font-size: 11px; font-weight: 700; fill: #1F407A; letter-spacing: 0.05em; }
  .badge-text { font-size: 9px; font-weight: 700; text-anchor: middle; letter-spacing: 0.03em; }
  .tier-title { font-size: 8.5px; font-weight: 700; fill: #475569; letter-spacing: 0.04em; }
  .card-title { font-size: 8.5px; font-weight: 700; text-anchor: middle; }
  .card-sub { font-size: 7.5px; text-anchor: middle; }
  .banner-text { font-size: 8.5px; font-weight: 700; text-anchor: middle; }
  .loop-text { font-size: 7.5px; font-weight: 700; fill: #A51C30; }
  .boundary-text { font-size: 7.5px; font-weight: 700; fill: #A51C30; text-anchor: middle; letter-spacing: 0.04em; }
</style>
"""

COMMON_DEFS = """
<defs>
  <marker id="arr-navy" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1F407A"/>
  </marker>
  <marker id="arr-crimson" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#A51C30"/>
  </marker>
  <marker id="arr-slate" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#94A3B8"/>
  </marker>
</defs>
"""

def sanitize_svg_xml(svg_str):
    def fix_text_body(match):
        open_tag = match.group(1)
        body = match.group(2)
        close_tag = match.group(3)
        body = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', body)
        body = re.sub(r'<(?!\/?tspan\b)', '&lt;', body)
        return f'{open_tag}{body}{close_tag}'

    pattern = re.compile(r'(<text\b[^>]*>)(.*?)(</text>)', re.DOTALL)
    return pattern.sub(fix_text_body, svg_str)

def generate_master_locator(chapter_num, chapter_title, active_targets, out_svg_path):
    W = 880
    H = 205
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" stroke="{BORDER}" stroke-width="1"/>')

    # Top Header
    badge_label = f"CHAPTER {chapter_num:02d} · {chapter_title.upper()}"
    pill_w = len(badge_label) * 6.2 + 20
    pill_x = W - 20 - pill_w
    svg.append(f'<text x="20" y="20" class="hdr-title">PHYSICAL AI SYSTEMS ARCHITECTURE LOCATOR</text>')
    svg.append(f'<rect x="{pill_x}" y="9" width="{pill_w}" height="17" fill="{NAVY}" fill-opacity="0.10" stroke="{NAVY}" stroke-width="0.8"/>')
    svg.append(f'<text x="{pill_x + pill_w/2}" y="21" class="badge-text" fill="{NAVY}">{badge_label}</text>')

    # -------------------------------------------------------------------------
    # Tier 1: Governance & Defensible Release Gate (Ch 14–17)
    # -------------------------------------------------------------------------
    is_gov_active = "GOVERNANCE" in active_targets or "ALL" in active_targets
    gov_stroke = CRIMSON if is_gov_active else BORDER
    gov_bg = ACTIVE_BG if is_gov_active else BG_LIGHT
    gov_txt = CRIMSON if is_gov_active else PURPLE
    gov_sw = "1.8" if is_gov_active else "0.9"

    svg.append(f'<rect x="40" y="32" width="800" height="24" fill="{gov_bg}" stroke="{gov_stroke}" stroke-width="{gov_sw}"/>')
    if is_gov_active:
        svg.append(f'<rect x="40" y="32" width="800" height="3" fill="{CRIMSON}"/>')
    svg.append(f'<text x="440" y="47" class="banner-text" fill="{gov_txt}">SYSTEM GOVERNANCE &amp; DEFENSIVE RELEASE GATE · Human Intervention (§14) · Verification Ladders (§15) · Release Case (§16) · Residual Frontier (§17)</text>')

    # -------------------------------------------------------------------------
    # Tier 2: Cognitive Deliberation & Ingestion (Ch 5, 8, 9, 10, 11)
    # -------------------------------------------------------------------------
    cog_cards = [
        ("DATA &amp; INGESTION", "Teleoperation &amp; Fingerprints", "DATA"),
        ("SPATIAL PERCEPTION", "Tokens &amp; Zero-Copy DMA", "PERCEPTION"),
        ("TEMPORAL MEMORY", "SE(3) Belief &amp; Occlusion", "MEMORY"),
        ("INTENT &amp; GOALS", "Expiring Leases &amp; 3D Goals", "INTENT"),
        ("TRAJECTORY PLANNER", "Action Chunks &amp; Jerk Splines", "PLANNING")
    ]
    card_w = 152
    card_gap = 10
    start_x = 40
    cog_y = 63
    cog_h = 36

    for i, (name, sub, tag) in enumerate(cog_cards):
        cx = start_x + i * (card_w + card_gap)
        is_active = tag in active_targets or "COGNITIVE" in active_targets or "ALL" in active_targets
        stroke_col = CRIMSON if is_active else BORDER
        bg_col = ACTIVE_BG if is_active else BG_LIGHT
        txt_col = CRIMSON if is_active else NAVY
        sw = "1.8" if is_active else "0.9"

        svg.append(f'<rect x="{cx}" y="{cog_y}" width="{card_w}" height="{cog_h}" fill="{bg_col}" stroke="{stroke_col}" stroke-width="{sw}"/>')
        if is_active:
            svg.append(f'<rect x="{cx}" y="{cog_y}" width="{card_w}" height="2.5" fill="{CRIMSON}"/>')
        svg.append(f'<text x="{cx + card_w/2}" y="{cog_y + 15}" class="card-title" fill="{txt_col}">{name}</text>')
        svg.append(f'<text x="{cx + card_w/2}" y="{cog_y + 28}" class="card-sub" fill="{SLATE}">{sub}</text>')

        # Inter-card arrow
        if i < 4:
            ax1 = cx + card_w + 1
            ax2 = ax1 + card_gap - 2
            ay = cog_y + cog_h / 2
            arr_marker = "url(#arr-crimson)" if is_active else "url(#arr-slate)"
            arr_col = CRIMSON if is_active else BORDER_DARK
            svg.append(f'<line x1="{ax1}" y1="{ay}" x2="{ax2}" y2="{ay}" stroke="{arr_col}" stroke-width="1.0" marker-end="{arr_marker}"/>')

    # -------------------------------------------------------------------------
    # Privilege Split Divider Line (Ch 1, 3, 4, 12)
    # -------------------------------------------------------------------------
    split_y = 107
    is_split_active = "BOUNDARY" in active_targets or "ALL" in active_targets
    line_col = CRIMSON if is_split_active else "#DC262688"
    line_w = "1.5" if is_split_active else "1.0"

    svg.append(f'<line x1="40" y1="{split_y}" x2="840" y2="{split_y}" stroke="{line_col}" stroke-dasharray="4,3" stroke-width="{line_w}"/>')
    svg.append(f'<rect x="290" y="{split_y - 8}" width="300" height="16" fill="{BG_WHITE}" stroke="{line_col}" stroke-width="0.8"/>')
    svg.append(f'<text x="440" y="{split_y + 3.5}" class="boundary-text">PROPOSAL–PERMISSION PRIVILEGE BOUNDARY (GATED WRITE)</text>')

    # -------------------------------------------------------------------------
    # Tier 3: Real-Time Reflex & Nervous System (Ch 4, 12, 13)
    # -------------------------------------------------------------------------
    ref_cards = [
        ("1 kHz REFLEX ENFORCER", "Control Barrier Functions (h ≥ 0) · Certified Setpoint u*", "REFLEX", 470),
        ("SILICON PLACEMENT &amp; BUS QoS", "Crossbar Arbitration · Memory Isolation · Hard Timers", "PLACEMENT", 320)
    ]
    ref_y = 118
    ref_h = 36
    r_cx = 40

    for name, sub, tag, rw in ref_cards:
        is_active = tag in active_targets or "NERVOUS" in active_targets or "ALL" in active_targets
        stroke_col = CRIMSON if is_active else BORDER
        bg_col = ACTIVE_BG if is_active else BG_LIGHT
        txt_col = CRIMSON if is_active else PETROL
        sw = "1.8" if is_active else "0.9"

        svg.append(f'<rect x="{r_cx}" y="{ref_y}" width="{rw}" height="{ref_h}" fill="{bg_col}" stroke="{stroke_col}" stroke-width="{sw}"/>')
        if is_active:
            svg.append(f'<rect x="{r_cx}" y="{ref_y}" width="{rw}" height="2.5" fill="{CRIMSON}"/>')
        svg.append(f'<text x="{r_cx + rw/2}" y="{ref_y + 15}" class="card-title" fill="{txt_col}">{name}</text>')
        svg.append(f'<text x="{r_cx + rw/2}" y="{ref_y + 28}" class="card-sub" fill="{SLATE}">{sub}</text>')
        r_cx += rw + 10

    # -------------------------------------------------------------------------
    # Tier 4: The Physical World & Body Dynamics (Ch 1, 2, 6, 7)
    # -------------------------------------------------------------------------
    is_body_active = "BODY" in active_targets or "PHYSICAL" in active_targets or "ALL" in active_targets
    body_stroke = CRIMSON if is_body_active else BORDER
    body_bg = ACTIVE_BG if is_body_active else BG_LIGHT
    body_txt = CRIMSON if is_body_active else INK
    body_sw = "1.8" if is_body_active else "0.9"
    body_y = 162
    body_h = 32

    svg.append(f'<rect x="40" y="{body_y}" width="800" height="{body_h}" fill="{body_bg}" stroke="{body_stroke}" stroke-width="{body_sw}"/>')
    if is_body_active:
        svg.append(f'<rect x="40" y="{body_y}" width="800" height="2.5" fill="{CRIMSON}"/>')
    svg.append(f'<text x="440" y="{body_y + 14}" class="card-title" fill="{body_txt}">THE PHYSICAL WORLD (THE BODY) · Matter, Momentum, Heat &amp; Friction (§01, §02)</text>')
    svg.append(f'<text x="440" y="{body_y + 25}" class="card-sub" fill="{SLATE}">Irreversible Energy Exchange · Stopping Distance (d_stop ≤ d_clear) · Thermal Limit (I²R) · Sim-to-Real Reality Gap (§06, §07)</text>')

    # -------------------------------------------------------------------------
    # Closed-Loop Feedback Path: Endogenous Sensory Shift
    # -------------------------------------------------------------------------
    svg.append(f'<path d="M 40 {body_y + 16} L 20 {body_y + 16} L 20 {cog_y + 18} L 36 {cog_y + 18}" fill="none" stroke="{CRIMSON}" stroke-width="1.2" marker-end="url(#arr-crimson)"/>')
    svg.append(f'<text x="26" y="{split_y + 3}" class="loop-text" transform="rotate(-90 26,{split_y + 3})" text-anchor="middle">ENDOGENOUS SENSORY SHIFT (o_t+1)</text>')

    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(out_svg_path), exist_ok=True)
    content = sanitize_svg_xml("\n".join(svg))
    with open(out_svg_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    
    pdf_path = os.path.splitext(out_svg_path)[0] + ".pdf"
    res = subprocess.run(["rsvg-convert", "-f", "pdf", "-o", pdf_path, out_svg_path], capture_output=True)
    if res.returncode != 0:
        subprocess.run(["inkscape", "--export-filename=" + pdf_path, out_svg_path], capture_output=True)
    print(f"Generated master locator: {out_svg_path} -> {pdf_path}")

if __name__ == "__main__":
    chapter_specs = [
        (1, "Boundary", ["PHYSICAL", "BOUNDARY"], "book/chapters/01-boundary/figures/fig_locator.svg"),
        (2, "Body", ["BODY", "PHYSICAL"], "book/chapters/02-body/figures/fig_locator.svg"),
        (3, "Brain", ["COGNITIVE"], "book/chapters/03-brain/figures/fig_locator.svg"),
        (4, "Nervous System", ["REFLEX", "NERVOUS", "BOUNDARY"], "book/chapters/04-nervous/figures/fig_locator.svg"),
        (5, "Data", ["DATA"], "book/chapters/05-data/figures/fig_locator.svg"),
        (6, "Training", ["COGNITIVE", "PHYSICAL"], "book/chapters/06-training/figures/fig_locator.svg"),
        (7, "Evaluation", ["COGNITIVE", "PHYSICAL", "GOVERNANCE"], "book/chapters/07-evaluation/figures/fig_locator.svg"),
        (8, "Perception", ["PERCEPTION"], "book/chapters/08-perception/figures/fig_locator.svg"),
        (9, "Memory", ["MEMORY"], "book/chapters/09-memory/figures/fig_locator.svg"),
        (10, "Intent", ["INTENT"], "book/chapters/10-intent/figures/fig_locator.svg"),
        (11, "Planning", ["PLANNING"], "book/chapters/11-planning/figures/fig_locator.svg"),
        (12, "Enforcement", ["REFLEX", "BOUNDARY"], "book/chapters/12-enforcement/figures/fig_locator.svg"),
        (13, "Placement", ["PLACEMENT"], "book/chapters/13-placement/figures/fig_locator.svg"),
        (14, "Intervention", ["GOVERNANCE", "BOUNDARY"], "book/chapters/14-intervention/figures/fig_locator.svg"),
        (15, "Verification", ["GOVERNANCE", "REFLEX"], "book/chapters/15-verification/figures/fig_locator.svg"),
        (16, "Release", ["GOVERNANCE"], "book/chapters/16-release/figures/fig_locator.svg"),
        (17, "Frontier", ["ALL"], "book/chapters/17-frontier/figures/fig_locator.svg")
    ]

    for num, title, targets, path in chapter_specs:
        generate_master_locator(num, title, targets, path)
    print("All 17 master locators regenerated successfully.")
