#!/usr/bin/env python3
"""
Generate Chapter 2 figures for Physical AI Systems:
- fig02_latency_waterfall (The 7-Stage Sense-to-Actuation Latency Waterfall)
- fig02_stopping_distance (Dynamic Stopping Distance Physics: Reaction + Braking)
- fig02_metrology_setup (Hardware-Triggered Logic Analyzer GPIO Instrumentation)

Outputs both vector PDF and native SVG (via pdftocairo), plus PNG for visual inspection.
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
CH02_FIG_DIR = os.path.join(BOOK_DIR, "chapters", "02-metrology", "figures")
os.makedirs(CH02_FIG_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. FIG 02.1: SENSE-TO-ACTUATION LATENCY WATERFALL (P50 vs P99 TAILS)
# -----------------------------------------------------------------------------
WATERFALL_TEX = r'''\documentclass[tikz,border=12pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{tgheros}
\usepackage{sfmath}
\usepackage{amsmath}
\usepackage{fontawesome5}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,backgrounds,calc}
\usepackage{xcolor}

\renewcommand{\familydefault}{\sfdefault}

% Harvard Crimson & ETH Zurich Academic Semantic Palette
\definecolor{harvardcrimson}{HTML}{A51C30}
\definecolor{ethdarkblue}{HTML}{1F407A}
\definecolor{ethblue}{HTML}{215CAF}
\definecolor{ethpetrol}{HTML}{007A87}
\definecolor{ethbronze}{HTML}{B87333}
\definecolor{ethpurple}{HTML}{5B4B8A}
\definecolor{ethslate}{HTML}{475569}
\definecolor{cardbg}{HTML}{F8FAFC}
\definecolor{cardborder}{HTML}{CBD5E1}
\definecolor{safeTeal}{HTML}{10B981}

\begin{document}
\begin{tikzpicture}[
  font=\sffamily,
  >=Stealth,
  stagebox/.style={
    draw=cardborder,
    fill=cardbg,
    rounded corners=4pt,
    line width=0.8pt,
    text width=1.12in,
    minimum height=1.65in,
    inner sep=6pt,
    align=center,
    anchor=north
  }
]

  % Top Title Banner
  \node[draw=ethdarkblue, fill=ethdarkblue!5, rounded corners=5pt, line width=1pt, text width=8.70in, inner sep=7pt, align=center] (title) at (4.35in, 0) {
    {\normalsize\bfseries\color{ethdarkblue}\faIcon{clock}\;\; THE 7-STAGE SENSE-TO-ACTUATION LATENCY WATERFALL}\\[2pt]
    {\scriptsize\color{ethslate}Where Does the Time Go? Deconstructing the Physical, Memory, Neural, and Silicon Bottlenecks}
  };

  % 7 Stages Across the Pipeline
  \node[stagebox, draw=ethblue!70] (st1) at (0, -0.65in) {
    {\scriptsize\bfseries\color{ethblue}\faIcon{satellite-dish}\; STAGE 1}\\[3pt]
    {\scriptsize\bfseries Transduce}\\[4pt]
    {\tiny\color{ethslate}Photodiode Well Exposure \& IMU Deflection}\\[6pt]
    \rule{0.9\linewidth}{0.3pt}\\[4pt]
    {\scriptsize\textbf{\color{safeTeal}$P_{50}$: $8\text{ ms}$}}\\[1pt]
    {\scriptsize\textbf{\color{harvardcrimson}$P_{99}$: $15\text{ ms}$}}
  };

  \node[stagebox, draw=ethpetrol!70] (st2) at (1.26in, -0.65in) {
    {\scriptsize\bfseries\color{ethpetrol}\faIcon{microchip}\; STAGE 2}\\[3pt]
    {\scriptsize\bfseries DMA Ingest}\\[4pt]
    {\tiny\color{ethslate}MIPI CSI-2 Bus Transfer into Shared DRAM}\\[6pt]
    \rule{0.9\linewidth}{0.3pt}\\[4pt]
    {\scriptsize\textbf{\color{safeTeal}$P_{50}$: $3\text{ ms}$}}\\[1pt]
    {\scriptsize\textbf{\color{harvardcrimson}$P_{99}$: $8\text{ ms}$}}
  };

  \node[stagebox, draw=ethblue!80] (st3) at (2.52in, -0.65in) {
    {\scriptsize\bfseries\color{ethblue}\faIcon{eye}\; STAGE 3}\\[3pt]
    {\scriptsize\bfseries Perception}\\[4pt]
    {\tiny\color{ethslate}ViT Encoders \& DINOv2\\[1pt]3D Spatial Tokens}\\[6pt]
    \rule{0.9\linewidth}{0.3pt}\\[4pt]
    {\scriptsize\textbf{\color{safeTeal}$P_{50}$: $12\text{ ms}$}}\\[1pt]
    {\scriptsize\textbf{\color{harvardcrimson}$P_{99}$: $25\text{ ms}$}}
  };

  \node[stagebox, draw=ethbronze!90] (st4) at (3.78in, -0.65in) {
    {\scriptsize\bfseries\color{ethbronze}\faIcon{brain}\; STAGE 4}\\[3pt]
    {\scriptsize\bfseries Policy VLA}\\[4pt]
    {\tiny\color{ethslate}Diffusion ACT / VLA\\[1pt]Action Chunk Pass}\\[6pt]
    \rule{0.9\linewidth}{0.3pt}\\[4pt]
    {\scriptsize\textbf{\color{safeTeal}$P_{50}$: $22\text{ ms}$}}\\[1pt]
    {\scriptsize\textbf{\color{harvardcrimson}$P_{99}$: $60\text{ ms}$}}
  };

  \node[stagebox, draw=ethpurple!80] (st5) at (5.04in, -0.65in) {
    {\scriptsize\bfseries\color{ethpurple}\faIcon{network-wired}\; STAGE 5}\\[3pt]
    {\scriptsize\bfseries Inter-IPC}\\[4pt]
    {\tiny\color{ethslate}Shared SRAM Mailbox\\[1pt]RPMSG MPU-to-MCU}\\[6pt]
    \rule{0.9\linewidth}{0.3pt}\\[4pt]
    {\scriptsize\textbf{\color{safeTeal}$P_{50}$: $0.8\text{ ms}$}}\\[1pt]
    {\scriptsize\textbf{\color{harvardcrimson}$P_{99}$: $2.0\text{ ms}$}}
  };

  \node[stagebox, draw=ethpetrol!90] (st6) at (6.30in, -0.65in) {
    {\scriptsize\bfseries\color{ethpetrol}\faIcon{shield-alt}\; STAGE 6}\\[3pt]
    {\scriptsize\bfseries Enforce}\\[4pt]
    {\tiny\color{ethslate}1 kHz CBF Filter \&\\[1pt]Stopping Distance}\\[6pt]
    \rule{0.9\linewidth}{0.3pt}\\[4pt]
    {\scriptsize\textbf{\color{safeTeal}$P_{50}$: $0.4\text{ ms}$}}\\[1pt]
    {\scriptsize\textbf{\color{harvardcrimson}$P_{99}$: $1.0\text{ ms}$}}
  };

  \node[stagebox, draw=harvardcrimson!80] (st7) at (7.56in, -0.65in) {
    {\scriptsize\bfseries\color{harvardcrimson}\faIcon{cogs}\; STAGE 7}\\[3pt]
    {\scriptsize\bfseries Actuator}\\[4pt]
    {\tiny\color{ethslate}Motor Stator $L/R$ Coil\\[1pt]Current Rise to Torque}\\[6pt]
    \rule{0.9\linewidth}{0.3pt}\\[4pt]
    {\scriptsize\textbf{\color{safeTeal}$P_{50}$: $6\text{ ms}$}}\\[1pt]
    {\scriptsize\textbf{\color{harvardcrimson}$P_{99}$: $15\text{ ms}$}}
  };

  % Timeline Comparisons at Bottom with Generous Vertical Clearance
  % NOMINAL P50 BAR
  \node[anchor=west, font=\sffamily\bfseries\scriptsize, text=safeTeal] at (0, -2.90in) {\faIcon{check-circle}\; Nominal Path ($P_{50} = 52.2\text{ ms}$):};
  \draw[fill=safeTeal!20, draw=safeTeal, line width=1pt, rounded corners=3pt] (2.40in, -3.00in) rectangle ++(3.13in, 0.22in);
  \node[font=\sffamily\bfseries\tiny, text=safeTeal!90] at (3.96in, -2.89in) {Safe Closed-Loop Margin ($52.2\text{ ms} \ll \tau_{\text{world}}$)};

  % TAIL P99 BAR
  \node[anchor=west, font=\sffamily\bfseries\scriptsize, text=harvardcrimson] at (0, -3.25in) {\faIcon{exclamation-triangle}\; Tail Path ($P_{99} = 126.0\text{ ms}$):};
  \draw[fill=harvardcrimson!20, draw=harvardcrimson, line width=1pt, rounded corners=3pt] (2.40in, -3.35in) rectangle ++(6.30in, 0.22in);
  \node[font=\sffamily\bfseries\tiny, text=harvardcrimson] at (5.55in, -3.24in) {CRITICAL TIMING VIOLATION ($126.0\text{ ms} > \tau_{\text{world}}$)};

  % World Deadline Vertical Marker (Safely Positioned Below Stage 7)
  \draw[dashed, line width=1.3pt, draw=harvardcrimson!90] (7.40in, -2.68in) -- (7.40in, -3.50in);
  \node[font=\sffamily\bfseries\tiny, fill=white, draw=harvardcrimson, rounded corners=2pt, inner sep=2pt, text=harvardcrimson] at (7.40in, -2.60in) {World Deadline $\tau_{\text{world}} = 100\text{ ms}$};

\end{tikzpicture}
\end{document}
'''

# -----------------------------------------------------------------------------
# 2. FIG 02.2: DYNAMIC STOPPING DISTANCE PHYSICS (REACTION + BRAKING)
# -----------------------------------------------------------------------------
STOPPING_TEX = r'''\documentclass[tikz,border=12pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{tgheros}
\usepackage{sfmath}
\usepackage{amsmath}
\usepackage{fontawesome5}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,backgrounds,calc}
\usepackage{xcolor}

\renewcommand{\familydefault}{\sfdefault}

% Harvard Crimson & ETH Zurich Academic Semantic Palette
\definecolor{harvardcrimson}{HTML}{A51C30}
\definecolor{ethdarkblue}{HTML}{1F407A}
\definecolor{ethblue}{HTML}{215CAF}
\definecolor{ethpetrol}{HTML}{007A87}
\definecolor{ethbronze}{HTML}{B87333}
\definecolor{ethslate}{HTML}{475569}
\definecolor{cardbg}{HTML}{F8FAFC}
\definecolor{cardborder}{HTML}{CBD5E1}
\definecolor{safeTeal}{HTML}{10B981}

\begin{document}
\begin{tikzpicture}[
  font=\sffamily,
  >=Stealth
]

  % Top Title Banner
  \node[draw=ethdarkblue, fill=ethdarkblue!5, rounded corners=5pt, line width=1pt, text width=8.50in, inner sep=7pt, align=center] (title) at (4.25in, 0) {
    {\normalsize\bfseries\color{ethdarkblue}\faIcon{tachometer-alt}\;\; DYNAMIC STOPPING DISTANCE PHYSICS ($d_{\text{stop}}$)}\\[2pt]
    {\scriptsize\color{ethslate}Translating Milliseconds of Information Staleness into Physical Centimeters of Collision Hazard}
  };

  % Equation Box
  \node[draw=cardborder, fill=cardbg, rounded corners=4pt, line width=0.8pt, text width=8.50in, inner sep=6pt, align=center, below=0.15in of title] (eq) {
    {\small $d_{\text{stop}}(t) \;=\; \underbrace{v(t) \cdot t_{\text{delay}}(t)}_{\text{\textbf{\color{ethblue}1. Reaction Distance (Linear in Latency $\Delta t$)}}} \;+\; \underbrace{\frac{v(t)^2}{2 \cdot a_{\text{max}}}}_{\text{\textbf{\color{ethbronze}2. Braking Distance (Quadratic in Velocity $v$)}}}$}
  };

  % --- SCENARIO 1: Nominal Execution (P50 = 30 ms) ---
  \node[anchor=west, font=\sffamily\bfseries\scriptsize, text=ethdarkblue] at (0, -1.60in) {\faIcon{check-circle}\; \textbf{Nominal Case ($v = 1.0\text{ m/s}, t_{\text{delay}} = 30\text{ ms}, a_{\text{max}} = 2.0\text{ m/s}^2$)}:};
  
  % Reaction Bar
  \draw[fill=ethblue!20, draw=ethblue, line width=1pt, rounded corners=2pt] (0, -2.00in) rectangle ++(1.20in, 0.28in)
    node[midway, font=\sffamily\bfseries\tiny, text=ethblue] {$d_{\text{react}} = 0.03\text{ m}$};
  % Braking Bar
  \draw[fill=ethbronze!25, draw=ethbronze, line width=1pt, rounded corners=2pt] (1.22in, -2.00in) rectangle ++(4.20in, 0.28in)
    node[midway, font=\sffamily\bfseries\tiny, text=ethbronze] {$d_{\text{brake}} = 0.25\text{ m}$};
  
  % Total Stop Tag (Safely to the right of nominal bar)
  \node[draw=safeTeal, fill=safeTeal!15, rounded corners=2pt, font=\sffamily\bfseries\tiny, text=safeTeal, inner sep=2.5pt, anchor=west] at (5.50in, -1.86in) {
    \textbf{Total $d_{\text{stop}} = 0.28\text{ m}$ (Safe: Clearance $= 0.35\text{ m}$)}
  };

  % --- SCENARIO 2: Tail Latency Spike (P99 = 230 ms) ---
  \node[anchor=west, font=\sffamily\bfseries\scriptsize, text=harvardcrimson] at (0, -2.45in) {\faIcon{exclamation-triangle}\; \textbf{Tail Spike Case ($v = 1.0\text{ m/s}, t_{\text{delay}} = 230\text{ ms}, a_{\text{max}} = 2.0\text{ m/s}^2$)}:};
  
  % Reaction Bar (Expanded)
  \draw[fill=harvardcrimson!20, draw=harvardcrimson, line width=1pt, rounded corners=2pt] (0, -2.85in) rectangle ++(3.80in, 0.28in)
    node[midway, font=\sffamily\bfseries\tiny, text=harvardcrimson] {$d_{\text{react}} = 0.23\text{ m}$ ($+20\text{ cm}$ Blind Travel)};
  % Braking Bar (Offset label so it doesn't collide with the dashed line at 7.00in)
  \draw[fill=ethbronze!25, draw=ethbronze, line width=1pt, rounded corners=2pt] (3.82in, -2.85in) rectangle ++(4.20in, 0.28in)
    node[pos=0.25, font=\sffamily\bfseries\tiny, text=ethbronze] {$d_{\text{brake}} = 0.25\text{ m}$};

  % Total Stop Tag (Crash Breach)
  \node[draw=harvardcrimson, fill=harvardcrimson!15, rounded corners=2pt, font=\sffamily\bfseries\tiny, text=harvardcrimson, inner sep=2.5pt, anchor=west] at (8.15in, -2.71in) {
    \textbf{$d_{\text{stop}} = 0.48\text{ m}$ (CRASH!)}
  };

  % Physical Clearance Limit Line (At 7.00in distance mark)
  \draw[dashed, line width=1.5pt, draw=harvardcrimson] (7.00in, -1.45in) -- (7.00in, -3.05in);
  \node[font=\sffamily\bfseries\tiny, fill=white, draw=harvardcrimson, rounded corners=2pt, inner sep=2.5pt, text=harvardcrimson] at (7.00in, -1.35in) {
    \faIcon{ban}\; Physical Obstacle Clearance Barrier ($0.35\text{ m}$)
  };

\end{tikzpicture}
\end{document}
'''

# -----------------------------------------------------------------------------
# 3. FIG 02.3: HARDWARE-TRIGGERED METROLOGY TOPOLOGY
# -----------------------------------------------------------------------------
METROLOGY_TEX = r'''\documentclass[tikz,border=12pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{tgheros}
\usepackage{sfmath}
\usepackage{amsmath}
\usepackage{fontawesome5}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,backgrounds,calc}
\usepackage{xcolor}

\renewcommand{\familydefault}{\sfdefault}

% Harvard Crimson & ETH Zurich Academic Semantic Palette
\definecolor{harvardcrimson}{HTML}{A51C30}
\definecolor{ethdarkblue}{HTML}{1F407A}
\definecolor{ethblue}{HTML}{215CAF}
\definecolor{ethpetrol}{HTML}{007A87}
\definecolor{ethbronze}{HTML}{B87333}
\definecolor{ethslate}{HTML}{475569}
\definecolor{cardbg}{HTML}{F8FAFC}
\definecolor{cardborder}{HTML}{CBD5E1}

\begin{document}
\begin{tikzpicture}[
  font=\sffamily,
  >=Stealth,
  box/.style={
    draw=cardborder,
    fill=cardbg,
    rounded corners=5pt,
    line width=0.9pt,
    text width=3.45in,
    minimum height=2.45in,
    inner sep=9pt,
    align=left,
    anchor=north,
    text=ethdarkblue
  }
]

  % Top Title Banner
  \node[draw=ethdarkblue, fill=ethdarkblue!5, rounded corners=5pt, line width=1pt, text width=8.50in, inner sep=7pt, align=center] (title) at (4.25in, 0) {
    {\normalsize\bfseries\color{ethdarkblue}\faIcon{microchip}\;\; HARDWARE-TRIGGERED METROLOGY TOPOLOGY}\\[2pt]
    {\scriptsize\color{ethslate}Escaping Software Timestamp Delusions via Logic Analyzer GPIO Toggles and Shunt Current Probes}
  };

  % Left Card: The Machine Under Test
  \node[box] (dut) at (0, -0.65in) {
    {\small\bfseries\color{ethdarkblue}\faIcon{server}\; Physical AI Machine Under Test}\\[3pt]
    {\scriptsize\bfseries\color{ethslate}Arduino UNO Q Dual-Brain Platform}\\[6pt]
    \textbf{\color{ethblue}1. Sensor Frame Interrupt (GPIO 1):}\\[1pt]
    {\tiny Toggled inside camera driver ISR on DMA start.}\\[4pt]
    \textbf{\color{ethbronze}2. MPU Inference Emit (GPIO 2):}\\[1pt]
    {\tiny Toggled in Linux kernel upon writing RPMSG mailbox.}\\[4pt]
    \textbf{\color{ethpetrol}3. MCU Enforcement Veto / Pass (GPIO 3):}\\[1pt]
    {\tiny Toggled inside FreeRTOS 1 kHz ISR on CBF evaluation.}\\[4pt]
    \textbf{\color{harvardcrimson}4. Inverter Gate Drive Out (PWM Pins):}\\[1pt]
    {\tiny Direct hardware timer registers driving MOSFET bridge.}
  };

  % Right Card: External Test Equipment (Positioned with 1.30in gap)
  \node[box, draw=ethpetrol, fill=ethpetrol!5] (scope) at (4.75in, -0.65in) {
    {\small\bfseries\color{ethpetrol}\faIcon{chart-line}\; External Ground-Truth Metrology}\\[3pt]
    {\scriptsize\bfseries\color{ethslate}Multi-Channel Logic Analyzer \& Oscilloscope}\\[6pt]
    \textbf{\color{ethblue}CH 1 (Digital):} Transduction Pulse $\to$ True $t_{\text{transduce}}$\\[3pt]
    \textbf{\color{ethbronze}CH 2 (Digital):} Proposal Generation $\to$ True $t_{\text{inference}}$\\[3pt]
    \textbf{\color{ethpetrol}CH 3 (Digital):} MCU Permission $\to$ True $t_{\text{enforce}}$\\[3pt]
    \textbf{\color{harvardcrimson}CH 4 (Analog):} Current Shunt $\to$ Motor Coil $L/R$ Rise Time\\[6pt]
    \rule{0.95\linewidth}{0.3pt}\\[4pt]
    {\scriptsize\textbf{\color{ethdarkblue}Guaranteed Result: Zero Operating System Jitter.}}
  };

  % Connecting Probes with Clear Spacing
  \draw[->, line width=1.2pt, ethblue] ($(dut.north east) + (0, -0.45in)$) -- ($(scope.north west) + (0, -0.45in)$)
    node[midway, font=\sffamily\bfseries\tiny, fill=white, draw=ethblue!40, rounded corners=2pt, inner sep=2pt, text=ethblue] {Probe 1: Ingest};

  \draw[->, line width=1.2pt, ethbronze] ($(dut.north east) + (0, -0.95in)$) -- ($(scope.north west) + (0, -0.95in)$)
    node[midway, font=\sffamily\bfseries\tiny, fill=white, draw=ethbronze!40, rounded corners=2pt, inner sep=2pt, text=ethbronze] {Probe 2: Inference};

  \draw[->, line width=1.2pt, ethpetrol] ($(dut.north east) + (0, -1.45in)$) -- ($(scope.north west) + (0, -1.45in)$)
    node[midway, font=\sffamily\bfseries\tiny, fill=white, draw=ethpetrol!40, rounded corners=2pt, inner sep=2pt, text=ethpetrol] {Probe 3: Enforce};

  \draw[->, line width=1.2pt, harvardcrimson] ($(dut.north east) + (0, -1.95in)$) -- ($(scope.north west) + (0, -1.95in)$)
    node[midway, font=\sffamily\bfseries\tiny, fill=white, draw=harvardcrimson!40, rounded corners=2pt, inner sep=2pt, text=harvardcrimson] {Probe 4: Coil Current};

\end{tikzpicture}
\end{document}
'''

def build_all():
    figures = {
        "fig02_latency_waterfall.tex": WATERFALL_TEX,
        "fig02_stopping_distance.tex": STOPPING_TEX,
        "fig02_metrology_setup.tex": METROLOGY_TEX
    }
    
    for filename, tex in figures.items():
        tex_path = os.path.join(CH02_FIG_DIR, filename)
        pdf_name = filename.replace(".tex", ".pdf")
        svg_name = filename.replace(".tex", ".svg")
        png_name = filename.replace(".tex", "_preview")
        
        with open(tex_path, "w") as f:
            f.write(tex.strip() + "\n")
        print(f"Wrote {tex_path}")
        
        subprocess.run(["lualatex", "-interaction=nonstopmode", filename], cwd=CH02_FIG_DIR, check=True)
        subprocess.run(["pdftocairo", "-svg", pdf_name, svg_name], cwd=CH02_FIG_DIR, check=True)
        subprocess.run(["pdftoppm", "-png", "-r", "200", pdf_name, png_name], cwd=CH02_FIG_DIR, check=True)
        print(f"Compiled {pdf_name} -> {svg_name} and {png_name}-1.png")

if __name__ == "__main__":
    build_all()
