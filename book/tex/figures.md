# Physical AI Figure Design & Color Standards

Every diagram in the Physical AI Systems project is an engineering blueprint. Figures must communicate architectural privilege, physical consequences, and multi-rate cadences with absolute clarity, crisp vector rendering, and publication-grade aesthetics.

---

## 1. The Harvard & ETH Academic Semantic Palette

Diagrams follow a rigorous semantic color system combining **Harvard Crimson** and **ETH Zurich Blue/Petrol** with functional roles:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE PHYSICAL AI COLOR WHEEL                               │
├─────────────────┬───────────┬───────────────┬──────────────────────────────────────────┤
│ Semantic Role   │ Color     │ HEX / RGB     │ Engineering & Architectural Meaning      │
├─────────────────┼───────────┼───────────────┼──────────────────────────────────────────┤
│ Consequence     │ Crimson   │ #A51C30       │ Physical irreversibility (W_t -> W_t+1), │
│ & Boundary      │           │ (165, 28, 48) │ momentum (p=mv), heat (I^2R), faults     │
├─────────────────┼───────────┼───────────────┼──────────────────────────────────────────┤
│ Structural      │ Dark Blue │ #1F407A       │ Chassis, SoC hardware, buses, framing,   │
│ & Backbone      │           │ (31, 64, 122) │ system boundaries, architectural headers │
├─────────────────┼───────────┼───────────────┼──────────────────────────────────────────┤
│ Planning        │ ETH Blue  │ #215CAF       │ System 1.5 Mid-Cadence (20-50 Hz), ACT,  │
│ & Trajectory    │           │ (33, 92, 175) │ diffusion action chunks, belief states   │
├─────────────────┼───────────┼───────────────┼──────────────────────────────────────────┤
│ Permission      │ Petrol    │ #007A87       │ System 1 Fast-Cadence (1000 Hz MCU),     │
│ & Metrology     │ / Teal    │ (0, 122, 135) │ CBF safety envelopes, ground truth       │
├─────────────────┼───────────┼───────────────┼──────────────────────────────────────────┤
│ Proposal        │ Bronze    │ #B87333       │ System 2 Slow-Cadence (0.5-2 Hz VLM),    │
│ & Intent        │ / Amber   │ (184, 115, 51)│ expiring leases, untrusted proposals     │
├─────────────────┼───────────┼───────────────┼──────────────────────────────────────────┤
│ Governance      │ Purple    │ #5B4B8A       │ Human supervisor, takeover state machine,│
│ & Arbitration   │           │ (91, 75, 138) │ cryptographic provenance, release gates  │
└─────────────────┴───────────┴───────────────┴──────────────────────────────────────────┘
```

### Neutral Inks & Surfaces

| Token | HEX Code | RGB | Usage |
| :--- | :--- | :--- | :--- |
| **`ink`** | `#1A202C` | `(26, 32, 44)` | Primary node text, bold titles, critical annotations |
| **`softink` / `ethslate`** | `#475569` | `(71, 85, 105)` | Secondary labels, descriptions, dimensions, timings |
| **`paleink`** | `#A0AEC0` | `(160, 174, 192)` | Subtle gridlines, axis lines, minor dividers |
| **`cardbg`** | `#F8FAFC` | `(248, 250, 252)` | Default node / card background fill |
| **`cardborder`** | `#CBD5E1` | `(203, 213, 225)` | Clean hairline borders (`0.8pt`–`1.0pt`) |
| **`frontierbg`** | `#FEF2F2` | `(254, 242, 242)` | Crimson-tinted background for physical boundary / danger |
| **`surfacebg`** | `#FFFFFF` | `(255, 255, 255)` | Pure white badges and overlay pills |

---

## 2. Semantic Color Mapping Rules

Never color nodes arbitrarily. Every hue conveys an explicit system property:

1. **Untrusted Proposals (Bronze `#B87333`):**
   * Used for foundation models, VLMs, transformers, neural policies, and candidate trajectory chunks.
   * Visual badge: `draw=ethbronze!80, fill=ethbronze!5`.
2. **Trajectory Planning (Blue `#215CAF`):**
   * Used for medium-cadence action chunk unrolling, temporal belief tracking, and smooth spline generation.
   * Visual badge: `draw=ethblue!80, fill=ethblue!5`.
3. **Safety Permission & Real-Time MCU (Petrol `#007A87`):**
   * Used for 1 kHz FreeRTOS tasks, Control Barrier Function (CBF) safe set projection ($\Pi_{\mathcal{U}_{\text{safe}}}$), gate driver PWM outputs, and measured sensor ground truth.
   * Visual badge: `draw=ethpetrol!90, fill=ethpetrol!5`.
4. **Physical Consequence & Invariants (Crimson `#A51C30`):**
   * Used for the physical world ($W_t \to W_{t+1}$), kinetic momentum, motor thermal limits ($I^2 R$), safety violations, emergency stops (Category 0/1/2), and fault injections.
   * Visual badge: `draw=harvardcrimson, fill=frontierbg`.
5. **Structural Chassis (Dark Blue `#1F407A`):**
   * Used for top-level diagram title banners, hardware bus backbones (DMA, AXI, CAN), and enclosing system frames.

---

## 3. Typography & Math in Figures

* **Font Family:** Clean sans-serif matching the book's display font (`TeX Gyre Heros` / `Avenir Next` / `Helvetica`).
* **Mathematics:** Use `sfmath` so all LaTeX equations in diagrams render in clean sans-serif math (e.g., `$\mathbf{p} = m\mathbf{v}$`, `$1000\text{ Hz}$`, `$h(\mathbf{x}) \ge 0$`). Never mix serif math into vector figures.
* **Hierarchical Sizing:**
  - **Banner Title:** `\normalsize\bfseries`
  - **Node Header:** `\small\bfseries` or `\footnotesize\bfseries`
  - **Body Text:** `\scriptsize`
  - **Subtext / Captions:** `\tiny\color{ethslate}`
* **Units:** Explicit SI units formatted as math text: `$1000\text{ Hz}$`, `$P_{99} \le 5\text{ ms}$`, `$1.2\text{ m/s}$`.

---

## 4. Standard TikZ Figure Template

Copy and adapt this canonical template when authoring new figures:

```latex
\documentclass[tikz,border=12pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{tgheros}
\usepackage{sfmath}
\usepackage{amsmath}
\usepackage{fontawesome5}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,backgrounds,calc}
\usepackage{xcolor}

\renewcommand{\familydefault}{\sfdefault}

% Exact Harvard & ETH Semantic Palette
\definecolor{harvardcrimson}{HTML}{A51C30}
\definecolor{ethdarkblue}{HTML}{1F407A}
\definecolor{ethblue}{HTML}{215CAF}
\definecolor{ethpetrol}{HTML}{007A87}
\definecolor{ethbronze}{HTML}{B87333}
\definecolor{ethpurple}{HTML}{5B4B8A}
\definecolor{ethslate}{HTML}{475569}
\definecolor{cardbg}{HTML}{F8FAFC}
\definecolor{cardborder}{HTML}{CBD5E1}
\definecolor{frontierbg}{HTML}{FEF2F2}

\begin{document}
\begin{tikzpicture}[
  font=\sffamily,
  >=Stealth,
  card/.style={
    draw=cardborder,
    fill=cardbg,
    rounded corners=5pt,
    line width=0.9pt,
    inner sep=8pt,
    align=left
  },
  pill/.style={
    fill=white,
    draw=cardborder,
    rounded corners=3pt,
    inner sep=3pt,
    font=\sffamily\scriptsize\bfseries
  }
]

  % Nodes and visual flows go here...

\end{tikzpicture}
\end{document}
```

---

## 5. Build & Output Rules

1. **Store Source in `figures/`:** Every figure lives in `book/chapters/XX-name/figures/figXX_name.tex`.
2. **Compile to Vector PDF and SVG:**
   ```bash
   lualatex figXX_name.tex
   pdftocairo -svg figXX_name.pdf figXX_name.svg
   ```
3. **Reference SVG in Markdown:** Always link the `.svg` in `.qmd` files (Quarto and Pandoc automatically use `.pdf` for LaTeX builds and `.svg` for HTML builds):
   ```markdown
   ![**Figure Title.** Figure caption detailing mechanisms.](figures/figXX_name.svg){#fig-example width=100%}
   ```
