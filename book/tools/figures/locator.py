"""
book/tools/figures/locator.py
Pipeline Locator Banner Generator for Chapters 01 through 13.
"""

from .common import (
    NAVY, BLUE, PETROL, TEAL, BRONZE, AMBER, CRIMSON, CORAL, PURPLE,
    SLATE, MUTED, INK, BG_LIGHT, BG_WHITE, BORDER, BORDER_DARK,
    COMMON_STYLE, COMMON_DEFS, save_svg_and_pdf
)

def gen_pipeline_locator(active_stage, active_pill, target_path):
    W = 880
    H = 125
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">']
    svg.append(COMMON_STYLE)
    svg.append(COMMON_DEFS)
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG_WHITE}" rx="8" stroke="{BORDER}" stroke-width="1"/>')

    # Top Header
    svg.append(f'<text x="24" y="24" class="section-hdr">END-TO-END EMBODIED PIPELINE LOCATOR</text>')

    # Active Pill Badge on top right
    pill_w = len(active_pill) * 6.5 + 20
    pill_x = W - 24 - pill_w
    svg.append(f'<rect x="{pill_x}" y="12" width="{pill_w}" height="18" rx="9" fill="{NAVY}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{pill_x+pill_w/2}" y="24" class="badge-text" fill="{NAVY}">{active_pill}</text>')

    # 7 Pipeline Stage Cards
    stages = [
        ("TRANSDUCTION", "Photons → Bits"),
        ("PERCEPTION", "Spatial Tokens"),
        ("MEMORY", "SE(3) World Model"),
        ("REASONING", "Intent Leases"),
        ("PLANNING", "Action Chunks"),
        ("REFLEXES", "Safety Enforcer"),
        ("PHYSICS", "Plant Dynamics")
    ]

    card_w = 106
    gap = 8
    start_x = (W - (7 * card_w + 6 * gap)) / 2
    card_y = 42
    card_h = 64

    for i, (name, sub) in enumerate(stages):
        cx = start_x + i * (card_w + gap)
        is_active = (i == active_stage)

        if is_active:
            stroke_col = NAVY
            stroke_w = "1.8"
            bg_col = f"{NAVY}15"
            txt_col = NAVY
            weight = "700"
            sub_col = INK
        else:
            stroke_col = BORDER
            stroke_w = "1"
            bg_col = BG_LIGHT
            txt_col = MUTED
            weight = "600"
            sub_col = MUTED

        svg.append(f'<rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" rx="6" fill="{bg_col}" stroke="{stroke_col}" stroke-width="{stroke_w}"/>')

        if is_active:
            svg.append(f'<rect x="{cx}" y="{card_y}" width="{card_w}" height="4" rx="2" fill="{NAVY}"/>')

        svg.append(f'<text x="{cx+card_w/2}" y="{card_y+26}" font-size="8.5" font-weight="{weight}" fill="{txt_col}" text-anchor="middle">{name}</text>')
        svg.append(f'<text x="{cx+card_w/2}" y="{card_y+46}" font-size="8" fill="{sub_col}" text-anchor="middle">{sub}</text>')

        if i < 6:
            ax1 = cx + card_w + 1
            ax2 = ax1 + gap - 2
            ay = card_y + card_h / 2
            arr_col = NAVY if (is_active or i == active_stage - 1) else BORDER_DARK
            marker = "url(#arr-navy)" if arr_col == NAVY else "url(#arr-slate)"
            svg.append(f'<line x1="{ax1}" y1="{ay}" x2="{ax2}" y2="{ay}" stroke="{arr_col}" stroke-width="1.2" marker-end="{marker}"/>')

    svg.append('</svg>')
    save_svg_and_pdf(target_path, "\n".join(svg))

def run_all():
    locators = [
        (0, "CHAPTER 01 · THE BOUNDARY", "book/chapters/01-boundary/figures/fig_pipeline_locator.svg"),
        (0, "CHAPTER 02 · THE FIVE PHYSICAL CONSTRAINTS", "book/chapters/02-constraints/figures/fig_pipeline_locator.svg"),
        (1, "CHAPTER 03 · FOUNDATIONS OF COGNITIVE AGENCY", "book/chapters/03-cognition/figures/fig_pipeline_locator.svg"),
        (2, "CHAPTER 04 · MULTI-RATE SYSTEM HIERARCHY", "book/chapters/04-hierarchy/figures/fig_pipeline_locator.svg"),
        (1, "CHAPTER 05 · SPATIAL PERCEPTION & TRANSDUCTION", "book/chapters/05-perception/figures/fig_pipeline_locator.svg"),
        (2, "CHAPTER 06 · TEMPORAL MEMORY & WORLD MODELS", "book/chapters/06-state/figures/fig_pipeline_locator.svg"),
        (3, "CHAPTER 07 · INTENT & SEMANTIC REASONING", "book/chapters/07-intent/figures/fig_pipeline_locator.svg"),
        (4, "CHAPTER 08 · ACTION GENERATION & TRAJECTORY PLANNING", "book/chapters/08-planning/figures/fig_pipeline_locator.svg"),
        (5, "CHAPTER 09 · REAL-TIME SAFETY ENFORCEMENT & REFLEXES", "book/chapters/09-enforcement/figures/fig_pipeline_locator.svg"),
        (4, "CHAPTER 10 · HETEROGENEOUS COMPUTE PLACEMENT", "book/chapters/10-placement/figures/fig_pipeline_locator.svg"),
        (5, "CHAPTER 11 · RUNTIME GOVERNANCE & HUMAN AUTHORITY", "book/chapters/11-governance/figures/fig_pipeline_locator.svg"),
        (5, "CHAPTER 12 · WHOLE-SYSTEM QUALIFICATION & ASSURANCE", "book/chapters/12-assurance/figures/fig_pipeline_locator.svg"),
        (6, "CHAPTER 13 · FRONTIER COGNITION & CAPSTONE INTEGRATION", "book/chapters/13-frontier/figures/fig_pipeline_locator.svg")
    ]
    for stage, pill, path in locators:
        gen_pipeline_locator(stage, pill, path)

if __name__ == "__main__":
    run_all()
