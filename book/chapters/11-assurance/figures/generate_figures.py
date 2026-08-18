#!/usr/bin/env python3
"""
Generate and compile polished TikZ figures for Chapter 11 (Assurance & Release):
- fig11_qualification_ladder: The 4-Rung Qualification Ladder
- fig11_cross_layer_faults: Cross-Layer Seeded Fault Injection
- fig11_cae_safety_case: Claim-Argument-Evidence (CAE) Safety Case Architecture
"""

import os
import subprocess

FIG_DIR = "/Users/VJ/GitHub/PhysicalAI/book/chapters/11-assurance/figures"
os.makedirs(FIG_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. FIG 11-1: THE 4-RUNG QUALIFICATION LADDER
# -----------------------------------------------------------------------------
LADDER_TEX = r'''\documentclass[tikz,border=14pt]{standalone}
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
  laddercard/.style={
    draw=cardborder,
    fill=white,
    rounded corners=6pt,
    line width=0.9pt,
    text width=2.25in,
    minimum height=3.85in,
    inner sep=8pt,
    align=center,
    anchor=north
  }
]

  % Top Title Banner
  \node[draw=ethdarkblue, fill=ethdarkblue!5, rounded corners=5pt, line width=1pt, text width=10.60in, inner sep=7pt, align=center] (title) at (5.35in, 0) {
    {\normalsize\bfseries\color{ethdarkblue}\faIcon{layer-group}\;\; THE 4-RUNG QUALIFICATION LADDER FOR PHYSICAL AI}\\[2pt]
    {\scriptsize\color{ethslate}Progressive Verification from Offline Log Replay to Active Shadow Fleet Deployment}
  };

  % --- RUNG 1: HISTORICAL LOG REPLAY ---
  \node[laddercard] (r1) at (1.25in, -0.65in) {
    {\scriptsize\bfseries\color{ethslate}\colorbox{ethslate!15}{\,\faIcon{history}\; RUNG 1 $\cdot$ BASELINE\,}}\\[4pt]
    {\small\bfseries\color{ethdarkblue}Historical Log Replay}\\[1pt]
    {\scriptsize\color{ethslate}Offline Dataset Metrology}\\[3pt]
    {\tiny\bfseries\color{ethdarkblue}\faIcon{check}\; Gate 0: Affordance Error $< 2\text{ cm}$}\\[6pt]
    {\scriptsize\color{ethslate}\raggedright
\textbf{Execution Substrate:}\\
$\bullet$ Static logged sensor streams\\
$\bullet$ Offline GPU training server\\
$\bullet$ Open-loop prediction loss\\[5pt]
\textbf{Verification Focus:}\\
$\bullet$ Model affordance accuracy\\
$\bullet$ Latent token prediction error\\
$\bullet$ Offline inference throughput\\[5pt]
\textbf{Blind Spot / Limit:}\\
$\bullet$ Zero closed-loop causality\\
$\bullet$ Blind to physical momentum\\
$\bullet$ Misses $P_{99}$ latency tails
    }
  };

  % --- RUNG 2: DOMAIN-RANDOMIZED SIMULATION ---
  \node[laddercard] (r2) at (3.95in, -0.65in) {
    {\scriptsize\bfseries\color{ethblue}\colorbox{ethblue!15}{\,\faIcon{cubes}\; RUNG 2 $\cdot$ CLOSED LOOP\,}}\\[4pt]
    {\small\bfseries\color{ethdarkblue}Physics Simulation}\\[1pt]
    {\scriptsize\color{ethblue}Domain Randomization}\\[3pt]
    {\tiny\bfseries\color{ethblue}\faIcon{check-double}\; Gate 1: $> 98\%$ Pass ($10^4$ Seeds)}\\[6pt]
    {\scriptsize\color{ethslate}\raggedright
\textbf{Execution Substrate:}\\
$\bullet$ \mbox{MuJoCo} / \mbox{Isaac Sim} physics\\
$\bullet$ Multi-GPU parallel rollouts\\
$\bullet$ Randomized mass, friction, light\\[5pt]
\textbf{Verification Focus:}\\
$\bullet$ Closed-loop policy stability\\
$\bullet$ Dynamic collision avoidance\\
$\bullet$ Generalization over $10^4$ seeds\\[5pt]
\textbf{Blind Spot / Limit:}\\
$\bullet$ Sim-to-real physics gap\\
$\bullet$ Idealized compute/bus timing\\
$\bullet$ Misses silicon fault modes
    }
  };

  % --- RUNG 3: HARDWARE-IN-THE-LOOP (HIL) ---
  \node[laddercard] (r3) at (6.65in, -0.65in) {
    {\scriptsize\bfseries\color{ethbronze}\colorbox{ethbronze!15}{\,\faIcon{microchip}\; RUNG 3 $\cdot$ TARGET SILICON\,}}\\[4pt]
    {\small\bfseries\color{ethdarkblue}Hardware-in-the-Loop}\\[1pt]
    {\scriptsize\color{ethbronze}Real Silicon + Plant Emulator}\\[3pt]
    {\tiny\bfseries\color{ethbronze}\faIcon{shield-alt}\; Gate 2: $100\%$ Fault Containment}\\[6pt]
    {\scriptsize\color{ethslate}\raggedright
\textbf{Execution Substrate:}\\
$\bullet$ Production MPU + Real-Time MCU\\
$\bullet$ $10\text{ kHz}$ FPGA plant emulator\\
$\bullet$ Real SPI, CAN, and MIPI buses\\[5pt]
\textbf{Verification Focus:}\\
$\bullet$ Seeded cross-layer faults\\
$\bullet$ MCU safety watchdog timing\\
$\bullet$ Memory DMA bus contention\\[5pt]
\textbf{Blind Spot / Limit:}\\
$\bullet$ Synthetic visual assets\\
$\bullet$ Emulated optical lighting\\
$\bullet$ Bounded human interaction
    }
  };

  % --- RUNG 4: SHADOW FLEET DEPLOYMENT ---
  \node[laddercard] (r4) at (9.35in, -0.65in) {
    {\scriptsize\bfseries\color{harvardcrimson}\colorbox{harvardcrimson!15}{\,\faIcon{shield-alt}\; RUNG 4\,}}\\[4pt]
    {\small\bfseries\color{harvardcrimson}Shadow Fleet Mode}\\[1pt]
    {\scriptsize\color{harvardcrimson}Passive Real-World Fleet}\\[3pt]
    {\tiny\bfseries\color{harvardcrimson}\faIcon{award}\; Gate 3: 0 Divergence / $500\text{ hrs}$}\\[6pt]
    {\scriptsize\color{ethslate}\raggedright
\textbf{Execution Substrate:}\\
$\bullet$ Physical robot in active fleet\\
$\bullet$ Real-world warehouse ODD\\
$\bullet$ Inferences run in background\\[5pt]
\textbf{Verification Focus:}\\
$\bullet$ Uncontained divergence audit\\
$\bullet$ Long-tail corner case capture\\
$\bullet$ Zero actuator safety authority\\[5pt]
\textbf{Blind Spot / Limit:}\\
$\bullet$ Policy cannot actuate world\\
$\bullet$ Dependent on fleet coverage\\
$\bullet$ Requires data privacy filters
    }
  };

  % Clean Un-Occluded Promotion Arrows Between Rungs
  \draw[->, line width=1.5pt, ethslate!70] (r1.east) -- (r2.west);
  \draw[->, line width=1.5pt, ethblue!80] (r2.east) -- (r3.west);
  \draw[->, line width=1.7pt, harvardcrimson!90] (r3.east) -- (r4.west);

  % Bottom Summary Strip
  \node[draw=cardborder, fill=white, rounded corners=4pt, line width=0.8pt, text width=10.60in, inner sep=6pt, anchor=north, align=center] 
    at (5.35in, -4.75in) {
    {\scriptsize\textbf{\color{ethdarkblue}\faIcon{clipboard-check}\; THE PROMOTION PRINCIPLE:}\;\; A high score on Rung 1 or 2 is a necessary prerequisite but never sufficient proof of release. Only Rungs 3 and 4 provide defensible physical evidence for the \textbf{Deploy / Condition / Refuse} release verdict.}
  };

\end{tikzpicture}
\end{document}
'''

# -----------------------------------------------------------------------------
# 2. FIG 11-2: CROSS-LAYER SEEDED FAULT INJECTION
# -----------------------------------------------------------------------------
FAULTS_TEX = r'''\documentclass[tikz,border=14pt]{standalone}
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
\definecolor{faultCoral}{HTML}{DC2626}

\begin{document}
\begin{tikzpicture}[
  font=\sffamily,
  >=Stealth,
  layercard/.style={
    draw=faultCoral!70,
    fill=faultCoral!5,
    rounded corners=4pt,
    line width=0.9pt,
    text width=2.45in,
    inner sep=6pt,
    align=left
  },
  systemcard/.style={
    draw=ethdarkblue,
    fill=white,
    rounded corners=5pt,
    line width=1pt,
    text width=3.30in,
    inner sep=7pt,
    align=left
  },
  enforcercard/.style={
    draw=safeTeal,
    fill=safeTeal!8,
    rounded corners=5pt,
    line width=1.4pt,
    text width=3.30in,
    inner sep=8pt,
    align=left
  },
  faulttag/.style={
    font=\sffamily\bfseries\tiny,
    fill=white,
    draw=faultCoral!60,
    text=faultCoral,
    rounded corners=2pt,
    inner sep=2pt
  }
]

  % Top Title Banner
  \node[draw=ethdarkblue, fill=ethdarkblue!5, rounded corners=5pt, line width=1pt, text width=10.00in, inner sep=7pt, align=center] (title) at (5.00in, 0) {
    {\normalsize\bfseries\color{ethdarkblue}\faIcon{bomb}\;\; CROSS-LAYER SEEDED FAULT INJECTION ARCHITECTURE}\\[2pt]
    {\scriptsize\color{ethslate}Stress-Testing Every Architectural Layer to Verify Deterministic MCU Safety Containment}
  };

  % --- LEFT COLUMN: 4 FAULT INJECTION LAYERS ---
  \node[layercard, below=0.25in of title.south west, anchor=north west] (l1) {
    {\scriptsize\bfseries\color{faultCoral}\faIcon{video}\; LAYER 1: SENSORY \& TRANSDUCTION}\\[2pt]
    {\tiny\color{ethslate}
    $\bullet$ Dropped MIPI camera frames ($> 100\text{ ms}$)\\
    $\bullet$ Optical blinding glare / sudden lux drop\\
    $\bullet$ PTP IEEE-1588 clock skew ($> 5\text{ ms}$)\\
    $\bullet$ Depth map sensor dropout / lens mud
    }
  };

  \node[layercard, below=0.15in of l1] (l2) {
    {\scriptsize\bfseries\color{faultCoral}\faIcon{microchip}\; LAYER 2: COMPUTE, BUS \& MEMORY}\\[2pt]
    {\tiny\color{ethslate}
    $\bullet$ Linux kernel panic / thread crash\\
    $\bullet$ Synthetic DMA memory bus saturation\\
    $\bullet$ \texttt{malloc} allocation stalls \& page faults\\
    $\bullet$ SPI / CAN-FD CRC checksum corruption
    }
  };

  \node[layercard, below=0.15in of l2] (l3) {
    {\scriptsize\bfseries\color{faultCoral}\faIcon{brain}\; LAYER 3: MODEL \& ALGORITHMIC}\\[2pt]
    {\tiny\color{ethslate}
    $\bullet$ Hallucinated 3D bounding boxes\\
    $\bullet$ Out-of-workspace trajectory proposals\\
    $\bullet$ Discontinuous acceleration jumps\\
    $\bullet$ Adversarial visual perturbation patches
    }
  };

  \node[layercard, below=0.15in of l3] (l4) {
    {\scriptsize\bfseries\color{faultCoral}\faIcon{bolt}\; LAYER 4: ELECTRICAL \& PHYSICAL}\\[2pt]
    {\tiny\color{ethslate}
    $\bullet$ Motor driver over-temperature ($> 105^\circ\text{C}$)\\
    $\bullet$ Battery bus voltage sag / brownout ($< 10.5\text{ V}$)\\
    $\bullet$ Sudden external collision load torque\\
    $\bullet$ Encoder phase loss / line break
    }
  };

  % --- CENTER COLUMN: DUAL-BRAIN ARCHITECTURE ---
  \node[systemcard] (mpu) at (5.30in, -1.05in) {
    {\scriptsize\bfseries\color{ethbronze}\faIcon{server}\; APPLICATION PROCESSOR (Linux MPU $\cdot$ System 2/1.5)}\\[2pt]
    {\tiny\color{ethslate}
    $\bullet$ Runs Vision Transformers, Deliberation \& Action Chunking\\
    $\bullet$ Untrusted, stochastic, prone to crashes and latency tails\\
    $\bullet$ Emits candidate trajectory buffer $\mathbf{p}_t$ over shared IPC link
    }
  };

  \node[enforcercard, below=0.22in of mpu] (mcu) {
    {\small\bfseries\color{safeTeal}\faIcon{shield-alt}\; REAL-TIME SAFETY ENFORCER (MCU $\cdot$ System 1)}\\[3pt]
    {\scriptsize\color{ethslate}\raggedright
    \textbf{1. Control Barrier Function Invariant ($h(x) \ge 0$):}\\
    \hspace*{6pt}Projects candidate $\mathbf{p}_t$ onto forward invariant safe set $\mathcal{C}$\\[2pt]
    \textbf{2. Dynamic Stopping Clearance Check ($d_{\text{gap}} > d_{\text{stop}}$):}\\
    \hspace*{6pt}Vetoes proposals exceeding braking envelope\\[2pt]
    \textbf{3. Zero-Software Hardware Watchdog Monitor:}\\
    \hspace*{6pt}Trips Category 1 dynamic stop if MPU heartbeat $> 50\text{ ms}$
    }
  };

  \node[draw=ethdarkblue, fill=ethdarkblue!8, rounded corners=4pt, line width=1pt, text width=3.30in, inner sep=6pt, below=0.18in of mcu] (plant) {
    {\scriptsize\bfseries\color{ethdarkblue}\faIcon{cogs}\; PHYSICAL PLANT \& ACTUATION ($W_t \to W_{t+1}$)}\\[2pt]
    {\tiny\color{ethslate}
    $\bullet$ Closed-loop motor current loops $\cdot$ Mechanical brakes $\cdot$ Verified safe stop
    }
  };

  % Fault Injection Injection Arrows (clean orthogonal paths)
  \draw[->, line width=1.1pt, dashed, faultCoral] (l1.east) -- node[pos=0.45, above, faulttag] {\faIcon{syringe}\; Camera Drop} ++(0.95in, 0) |- (mpu.west);
  \draw[->, line width=1.1pt, dashed, faultCoral] (l2.east) -- node[pos=0.45, above, faulttag] {\faIcon{syringe}\; Kernel Panic} ++(0.70in, 0) |- ($(mpu.south west)!0.5!(mcu.north west)$);
  \draw[->, line width=1.1pt, dashed, faultCoral] (l3.east) -- node[pos=0.45, above, faulttag] {\faIcon{syringe}\; Hallucination} ++(0.95in, 0) |- (mcu.west);
  \draw[->, line width=1.1pt, dashed, faultCoral] (l4.east) -- node[pos=0.45, above, faulttag] {\faIcon{syringe}\; Voltage Sag} ++(0.95in, 0) |- (plant.west);

  % Safety Handoff Arrows
  \draw[->, line width=1.2pt, ethbronze, dashed] (mpu.south) -- node[midway, fill=white, draw=cardborder, rounded corners=2pt, font=\sffamily\bfseries\tiny, text=ethbronze] {Candidate $\mathbf{p}_t$} (mcu.north);
  \draw[->, line width=1.5pt, safeTeal] (mcu.south) -- node[midway, fill=white, draw=safeTeal, rounded corners=2pt, font=\sffamily\bfseries\tiny, text=safeTeal] {Permitted $\mathbf{u}_t$ / E-Stop} (plant.north);

  % RIGHT COLUMN: PASS CRITERIA CARD
  \node[draw=safeTeal, fill=white, rounded corners=5pt, line width=1.1pt, text width=2.15in, anchor=north west] at (7.65in, -0.65in) {
    {\scriptsize\bfseries\color{safeTeal}\faIcon{check-double}\; PASS CRITERION}\\[4pt]
    {\scriptsize\color{ethslate}\raggedright
    \textbf{100\% Containment Rate:}\\
    $\bullet$ Zero collisions ($d_{\text{gap}} > 0$)\\
    $\bullet$ Bounded stopping time\\
    $\bullet$ Controlled halt $< 50\text{ ms}$\\[6pt]
    \textbf{Zero Uncontained Escapes:}\\
    Any single uncontained fault trips a \textbf{REFUSE} release verdict.\\[6pt]
    \textbf{Hardware Watchdog:}\\
    Dedicated non-maskable timer operates \mbox{independently} of Linux OS.
    }
  };

\end{tikzpicture}
\end{document}
'''

# -----------------------------------------------------------------------------
# 3. FIG 11-3: CLAIM-ARGUMENT-EVIDENCE (CAE) SAFETY CASE
# -----------------------------------------------------------------------------
CAE_TEX = r'''\documentclass[tikz,border=14pt]{standalone}
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
  claimnode/.style={
    draw=harvardcrimson,
    fill=harvardcrimson!10,
    rounded corners=5pt,
    line width=1.3pt,
    text width=9.20in,
    inner sep=8pt,
    align=center
  },
  argnode/.style={
    draw=ethblue,
    fill=ethblue!8,
    rounded corners=4pt,
    line width=1pt,
    text width=2.10in,
    minimum height=1.20in,
    inner sep=6pt,
    align=left,
    anchor=north
  },
  evidencenode/.style={
    draw=safeTeal,
    fill=safeTeal!8,
    rounded corners=3pt,
    line width=0.8pt,
    text width=2.10in,
    minimum height=1.35in,
    inner sep=5pt,
    align=left,
    anchor=north
  },
  verdictnode/.style={
    draw=ethdarkblue,
    fill=white,
    rounded corners=5pt,
    line width=1.2pt,
    text width=9.20in,
    inner sep=7pt,
    align=center
  }
]

  % Top Title Banner
  \node[draw=ethdarkblue, fill=ethdarkblue!5, rounded corners=5pt, line width=1pt, text width=10.00in, inner sep=7pt, align=center] (title) at (5.00in, 0) {
    {\normalsize\bfseries\color{ethdarkblue}\faIcon{sitemap}\;\; CLAIM-ARGUMENT-EVIDENCE (CAE) SAFETY CASE ARCHITECTURE}\\[2pt]
    {\scriptsize\color{ethslate}Linking High-Level Safety Claims to Defensible Bench Metrology and Signed Release Verdicts}
  };

  % Top Level Claim
  \node[claimnode, below=0.20in of title] (c_top) {
    {\small\bfseries\color{harvardcrimson}\faIcon{bullseye}\; TOP-LEVEL SAFETY CLAIM ($C_{\text{top}}$)}\\[2pt]
    {\footnotesize\bfseries "The Physical AI Agent operates acceptably safe within Operational Design Domain $\mathcal{X}_{\text{ODD}}$."}
  };

  % --- 4 ARGUMENT NODES ---
  \node[argnode] (a1) at (1.10in, -1.80in) {
    {\scriptsize\bfseries\color{ethblue}\faIcon{shield-alt}\; ARGUMENT $A_1$}\\[2pt]
    {\tiny\bfseries Fault Containment}\\[4pt]
    {\tiny\color{ethslate}All single-point hardware and software crashes are \mbox{deterministically} arrested by the MCU safety enforcer within $50\text{ ms}$.}
  };

  \node[argnode] (a2) at (3.70in, -1.80in) {
    {\scriptsize\bfseries\color{ethblue}\faIcon{tachometer-alt}\; ARGUMENT $A_2$}\\[2pt]
    {\tiny\bfseries Latency Freshness}\\[4pt]
    {\tiny\color{ethslate}The $P_{99.9}$ sense-to-actuation latency $\Delta t_{\text{wall}}$ remains strictly bounded so stopping distance $d_{\text{stop}} \le d_{\text{gap}}$.}
  };

  \node[argnode] (a3) at (6.30in, -1.80in) {
    {\scriptsize\bfseries\color{ethblue}\faIcon{user-shield}\; ARGUMENT $A_3$}\\[2pt]
    {\tiny\bfseries Human Authority}\\[4pt]
    {\tiny\color{ethslate}Human operators retain un-preemptible authority via \mbox{bumpless} joystick override and dedicated hardware E-stop circuits.}
  };

  \node[argnode] (a4) at (8.90in, -1.80in) {
    {\scriptsize\bfseries\color{ethblue}\faIcon{compass}\; ARGUMENT $A_4$}\\[2pt]
    {\tiny\bfseries ODD Enforcement}\\[4pt]
    {\tiny\color{ethslate}Real-time interoceptive and exteroceptive health monitors detect out-of-ODD transitions and trigger safe deceleration.}
  };

  % --- 4 EVIDENCE NODES ---
  \node[evidencenode] (e1) at (1.10in, -3.25in) {
    {\scriptsize\bfseries\color{safeTeal}\faIcon{file-medical-alt}\; EVIDENCE $E_1$}\\[2pt]
    {\tiny\bfseries HIL Fault Log (\texttt{REL-01})}\\[4pt]
    {\tiny\color{ethslate}
    $\bullet$ $1000/1000$ faults contained\\
    $\bullet$ 0 collisions recorded\\
    $\bullet$ Max stopping time: $42\text{ ms}$\\
    $\bullet$ Watchdog trip: $50\text{ ms}$
    }
  };

  \node[evidencenode] (e2) at (3.70in, -3.25in) {
    {\scriptsize\bfseries\color{safeTeal}\faIcon{chart-line}\; EVIDENCE $E_2$}\\[2pt]
    {\tiny\bfseries Metrology CDF (\texttt{REQ-01})}\\[4pt]
    {\tiny\color{ethslate}
    $\bullet$ $P_{50} = 22\text{ ms}$\\
    $\bullet$ $P_{99.9} = 72\text{ ms} < 80\text{ ms}$\\
    $\bullet$ Margin: $+18\text{ cm}$ \mbox{clearance}\\
    $\bullet$ Zero seqlock overruns
    }
  };

  \node[evidencenode] (e3) at (6.30in, -3.25in) {
    {\scriptsize\bfseries\color{safeTeal}\faIcon{gamepad}\; EVIDENCE $E_3$}\\[2pt]
    {\tiny\bfseries Override Logs (\texttt{AUTH-01})}\\[4pt]
    {\tiny\color{ethslate}
    $\bullet$ $50/50$ seamless takeovers\\
    $\bullet$ Peak jerk $< 15\text{ rad/s}^3$\\
    $\bullet$ Zero gearbox shock damage\\
    $\bullet$ Tamper-evident hash log
    }
  };

  \node[evidencenode] (e4) at (8.90in, -3.25in) {
    {\scriptsize\bfseries\color{safeTeal}\faIcon{cloud-sun}\; EVIDENCE $E_4$}\\[2pt]
    {\tiny\bfseries ODD Monitor Logs}\\[4pt]
    {\tiny\color{ethslate}
    $\bullet$ Dark/glare detection $< 20\text{ ms}$\\
    $\bullet$ Friction drop fallback\\
    $\bullet$ Thermal derating at $85^\circ\text{C}$\\
    $\bullet$ Category 1 stop verified
    }
  };

  % Connecting Lines: Claim -> Arguments
  \draw[->, line width=1.1pt, harvardcrimson] (c_top.south) -- (a1.north);
  \draw[->, line width=1.1pt, harvardcrimson] (c_top.south) -- (a2.north);
  \draw[->, line width=1.1pt, harvardcrimson] (c_top.south) -- (a3.north);
  \draw[->, line width=1.1pt, harvardcrimson] (c_top.south) -- (a4.north);

  % Connecting Lines: Arguments -> Evidence
  \draw[->, line width=1.1pt, ethblue] (a1.south) -- (e1.north);
  \draw[->, line width=1.1pt, ethblue] (a2.south) -- (e2.north);
  \draw[->, line width=1.1pt, ethblue] (a3.south) -- (e3.north);
  \draw[->, line width=1.1pt, ethblue] (a4.south) -- (e4.north);

  % Bottom Release Verdict Node
  \node[verdictnode, below=0.20in of e2.south, anchor=north] (verdict) at (5.00in, -4.85in) {
    {\small\bfseries\color{ethdarkblue}\faIcon{signature}\;\; THE 3 ACCOUNTABLE RELEASE VERDICTS}\\[3pt]
    {\scriptsize
    \textbf{\color{safeTeal}\faIcon{check-circle}\; DEPLOY} (All evidence thresholds met; unconstrained ODD) \quad$\vert$\quad
    \textbf{\color{ethbronze}\faIcon{exclamation-circle}\; CONDITION} (Restricted speed / active human supervisor) \quad$\vert$\quad
    \textbf{\color{harvardcrimson}\faIcon{times-circle}\; REFUSE} (Gate failure; deployment blocked)
    }
  };

  \draw[->, line width=1.1pt, safeTeal] (e1.south) -- (e1.south |- verdict.north);
  \draw[->, line width=1.1pt, safeTeal] (e2.south) -- (verdict.north);
  \draw[->, line width=1.1pt, safeTeal] (e3.south) -- (verdict.north);
  \draw[->, line width=1.1pt, safeTeal] (e4.south) -- (e4.south |- verdict.north);

\end{tikzpicture}
\end{document}
'''

def build_all():
    files = {
        "fig11_qualification_ladder.tex": LADDER_TEX,
        "fig11_cross_layer_faults.tex": FAULTS_TEX,
        "fig11_cae_safety_case.tex": CAE_TEX
    }
    
    for filename, content in files.items():
        filepath = os.path.join(FIG_DIR, filename)
        with open(filepath, "w") as f:
            f.write(content.strip() + "\n")
        print(f"Wrote {filepath}")
        
        pdf_path = filepath.replace(".tex", ".pdf")
        svg_path = filepath.replace(".tex", ".svg")
        subprocess.run(["lualatex", "-interaction=nonstopmode", filename], cwd=FIG_DIR, check=True)
        subprocess.run(["pdftocairo", "-svg", filename.replace(".tex", ".pdf"), filename.replace(".tex", ".svg")], cwd=FIG_DIR, check=True)
        print(f"Compiled {pdf_path} and {svg_path}")

if __name__ == "__main__":
    build_all()
