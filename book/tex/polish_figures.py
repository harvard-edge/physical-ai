#!/usr/bin/env python3
"""
Polish all TikZ figures for Physical AI Systems:
- TeX Gyre Heros + sfmath clean typography
- Zero hyphenation artifacts (guaranteed via mbox and balanced lines)
- Precise node alignment and balanced whitespace
- Publication-grade badges, lines, and callouts
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
CH01_FIG_DIR = os.path.join(BOOK_DIR, "chapters", "01-boundary", "figures")
os.makedirs(CH01_FIG_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. FIG 01: AGENT ANATOMY (PROPOSAL-PERMISSION ARCHITECTURE)
# -----------------------------------------------------------------------------
ANATOMY_TEX = r'''\documentclass[tikz,border=12pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{tgheros}
\usepackage{sfmath}
\usepackage{amsmath}
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

\newcommand{\mputag}[1]{\colorbox{ethbronze!15}{\scriptsize\bfseries\color{ethbronze}\,#1\,}}
\newcommand{\mcutag}[1]{\colorbox{ethpetrol!15}{\scriptsize\bfseries\color{ethpetrol}\,#1\,}}

\begin{document}
\begin{tikzpicture}[
  font=\sffamily,
  >=Stealth,
  organ/.style={
    draw=cardborder,
    fill=white,
    rounded corners=5pt,
    line width=0.9pt,
    inner sep=8pt,
    align=center,
    text=ethdarkblue
  }
]

  % Top Banner: Stage 7 Governance
  \node[organ, draw=ethpurple, fill=ethpurple!6, text width=7.4in, line width=1.1pt] (s7) {
    {\normalsize\bfseries\color{ethpurple}7. GOVERNANCE, LINEAGE \& RELEASE GATE}\\[2pt]
    {\footnotesize STPA Hazard Mitigation $\cdot$ Bumpless Human Joystick Override $\cdot$ Defensible Release Case (\textbf{LOOP-01} $\to$ \textbf{REL-01})}
  };

  % --- TOP PIPELINE ROW: Ingestion to State ---
  \node[organ, text width=2.22in, below=0.35in of s7.south west, anchor=north west] (s1) {
    {\bfseries\color{ethdarkblue}1. SENSING}\\[2pt]
    {\footnotesize Photons / Voltages to DMA}\\[2pt]
    {\scriptsize\color{ethslate}MIPI CSI-2 $\cdot$ I2C $\cdot$ SPI Bus Priority}
  };

  \node[organ, text width=2.22in, right=0.37in of s1] (s2) {
    {\bfseries\color{ethdarkblue}2. PERCEPTION \& ENCODERS}\\[2pt]
    {\footnotesize Raw Tensors to Spatial Tokens}\\[2pt]
    {\scriptsize\color{ethslate}ViT Encoders $\cdot$ \mbox{DINOv2} $\cdot$ 3D Affordances}
  };

  \node[organ, text width=2.22in, right=0.37in of s2] (s3) {
    {\bfseries\color{ethdarkblue}3. WORLD MODELS \& STATE}\\[2pt]
    {\footnotesize Latent Belief \& $SE(3)$ Frame Trees}\\[2pt]
    {\scriptsize\color{ethslate}JEPA / RSSM Dynamics $\cdot$ TTL Validity Leases}
  };

  % --- MIDDLE PIPELINE ROW: Untrusted Proposal Engine (MPU) ---
  \node[organ, draw=ethbronze, fill=ethbronze!6, text width=3.51in, below=0.45in of s3.south east, anchor=north east] (s4) {
    \mputag{SYSTEM 2 $\cdot$ LINUX MPU}\\[3pt]
    {\bfseries\color{ethbronze}4. SEMANTIC DELIBERATION}\\[2pt]
    {\scriptsize\color{ethslate}Vision-Language Foundation Models $\cdot$ Open-Vocabulary Goals $\cdot$ Expiring Leases ($t_{\text{expire}}$)}
  };

  \node[organ, draw=ethbronze, fill=ethbronze!6, text width=3.51in, left=0.38in of s4] (s5) {
    \mputag{SYSTEM 1.5 $\cdot$ LINUX MPU / NPU}\\[3pt]
    {\bfseries\color{ethbronze}5. TRAJECTORY DECODERS}\\[2pt]
    {\scriptsize\color{ethslate}Diffusion Policies $\cdot$ \mbox{ACT Action Chunking} ($H$-steps) $\cdot$ $\mathcal{C}^2$ Jerk Continuity}
  };

  % --- LOWER ROW: Trusted Real-Time Enforcer (MCU) ---
  \node[organ, draw=ethpetrol, fill=ethpetrol!8, line width=1.3pt, text width=7.4in, below=0.68in of s5.south west, anchor=north west] (s6) {
    \mcutag{SYSTEM 1 $\cdot$ REAL-TIME MCU (BARE-METAL / FreeRTOS)}\\[3pt]
    {\bfseries\color{ethpetrol}6. REAL-TIME REFLEX \& SAFETY ENFORCEMENT}\\[2pt]
    {\scriptsize\color{ethslate}1 kHz Reflex Timing Loop $\cdot$ Control Barrier Functions ($h(x) \ge 0$) $\cdot$ Dynamic Stopping Distance $d_{\text{stop}}(v_t) \le d_{\text{clearance}} \cdot$ Hardware Veto ($u_t$)}
  };

  % --- PHYSICAL WORLD ROW ---
  \node[organ, draw=harvardcrimson, fill=harvardcrimson!6, line width=1.3pt, text width=7.4in, below=0.38in of s6.south west, anchor=north west] (world) {
    {\bfseries\color{harvardcrimson}THE PHYSICAL WORLD ($W_t \to W_{t+1}$)}\\[2pt]
    {\scriptsize\color{ethslate}Kinetic Momentum ($p = mv$) $\cdot$ Joule Heat Dissipation ($I^2R$) $\cdot$ Matter Mutation $\cdot$ Friction ($\mu$) $\cdot$ Collision Dynamics}
  };

  % Proposal-Permission Privilege Boundary (Red Dashed Line)
  \coordinate (bleft) at ($(s6.north west) + (0, 0.34in)$);
  \coordinate (bright) at ($(s6.north east) + (0, 0.34in)$);
  \draw[dashed, line width=1.3pt, harvardcrimson!85] (bleft) -- (bright);

  \node[font=\sffamily\bfseries\scriptsize, fill=white, draw=harvardcrimson!40, rounded corners=3pt, inner sep=3.5pt, text=harvardcrimson] 
    at ($(bleft)!0.55!(bright)$) 
    {THE PROPOSAL--PERMISSION PRIVILEGE BOUNDARY (NO DIRECT MOTOR ACCESS)};

  % Feed-forward Data Flow Arrows
  \draw[->, line width=1.1pt, ethdarkblue] (s1.east) -- node[above, font=\sffamily\scriptsize\bfseries\color{ethdarkblue}]{Raw Frames} (s2.west);
  \draw[->, line width=1.1pt, ethdarkblue] (s2.east) -- node[above, font=\sffamily\scriptsize\bfseries\color{ethdarkblue}]{3D Tokens} (s3.west);
  \draw[->, line width=1.1pt, ethdarkblue] (s3.south) -- node[right, font=\sffamily\scriptsize\bfseries\color{ethdarkblue}]{State Vector} (s3.south |- s4.north);
  \draw[->, line width=1.1pt, ethbronze] (s4.west) -- node[above, font=\sffamily\scriptsize\bfseries\color{ethbronze}]{Intent Goal} (s5.east);
  \draw[->, line width=1.5pt, dashed, harvardcrimson] (s5.south) -- node[left=6pt, pos=0.35, font=\sffamily\bfseries\scriptsize\color{harvardcrimson}]{Expiring Proposal $p_t$} (s5.south |- s6.north);
  \draw[->, line width=1.5pt, ethpetrol] (s6.south) -- node[right, font=\sffamily\bfseries\scriptsize\color{ethpetrol}]{Permitted Action $u_t = \text{permit}(p_t)$} (world.north);

  % Closed-loop Endogenous Feedback Arrow
  \draw[->, line width=1.2pt, harvardcrimson] (world.west) -- ++(-0.35in,0) |- (s1.west)
    node[pos=0.25, above, rotate=90, font=\sffamily\bfseries\scriptsize\color{harvardcrimson}, align=center]{Endogenous Sensory Shift ($A_t \to W_{t+1} \to O_{t+1}$)};

\end{tikzpicture}
\end{document}
'''

# -----------------------------------------------------------------------------
# 2. FIG 02: ERAS EVOLUTION (4 ERAS OF AI SYSTEMS)
# -----------------------------------------------------------------------------
ERAS_TEX = r'''\documentclass[tikz,border=12pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{tgheros}
\usepackage{sfmath}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,backgrounds,calc}
\usepackage{xcolor}

\renewcommand{\familydefault}{\sfdefault}

% Harvard Crimson & ETH Zurich Color Palette
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
  card/.style={
    draw=cardborder,
    fill=cardbg,
    rounded corners=6pt,
    line width=0.8pt,
    text width=2.20in,
    inner sep=9pt,
    align=left
  },
  frontiercard/.style={
    draw=harvardcrimson,
    fill=harvardcrimson!4,
    rounded corners=6pt,
    line width=1.4pt,
    text width=2.28in,
    inner sep=9pt,
    align=left
  }
]

  % --- Phase 1: Disembodied ML ---
  \node[card] (p1) {
    {\scriptsize\bfseries\color{ethslate}\colorbox{ethslate!12}{\,PHASE 1 $\cdot$ 2012--2020\,}}\\[5pt]
    {\normalsize\bfseries\color{ethdarkblue}Disembodied ML}\\[1pt]
    {\scriptsize\bfseries\color{ethslate}The Cloud Era}\\[5pt]
    {\scriptsize\color{ethslate}\raggedright
    \textbf{Systems Focus:}\\
    High-throughput serving of digital predictions ($x \to y$)\\[5pt]
    $\bullet$ \textbf{Substrate:} Cloud GPU Clusters\\
    $\bullet$ \textbf{Workloads:} ResNet, BERT, RecSys\\
    $\bullet$ \textbf{Boundary:} Stateless API / Screen\\
    $\bullet$ \textbf{Failure Mode:} \texttt{try/catch} $\to$ Retry\\
    $\bullet$ \textbf{Physical Action:} None (Digital bits)
    }
  };

  % --- Phase 2: Edge Perception ---
  \node[card, right=0.52in of p1] (p2) {
    {\scriptsize\bfseries\color{ethpetrol}\colorbox{ethpetrol!12}{\,PHASE 2 $\cdot$ 2018--2023\,}}\\[5pt]
    {\normalsize\bfseries\color{ethdarkblue}Edge Perception}\\[1pt]
    {\scriptsize\bfseries\color{ethpetrol}The TinyML Era}\\[5pt]
    {\scriptsize\color{ethslate}\raggedright
    \textbf{Systems Focus:}\\
    Compressing models onto constrained microcontrollers\\[5pt]
    $\bullet$ \textbf{Substrate:} Bare-Metal MCUs / DSPs\\
    $\bullet$ \textbf{Workloads:} Wake-words, Anomaly\\
    $\bullet$ \textbf{Boundary:} Open-loop edge sensing\\
    $\bullet$ \textbf{Failure Mode:} Dropped wake-up / Alert\\
    $\bullet$ \textbf{Physical Action:} Passive telemetry
    }
  };

  % --- Phase 3: Generative Deliberation ---
  \node[card, right=0.52in of p2] (p3) {
    {\scriptsize\bfseries\color{ethblue}\colorbox{ethblue!12}{\,PHASE 3 $\cdot$ 2023--2026\,}}\\[5pt]
    {\normalsize\bfseries\color{ethdarkblue}Deliberation}\\[1pt]
    {\scriptsize\bfseries\color{ethblue}The Foundation Era}\\[5pt]
    {\scriptsize\color{ethslate}\raggedright
    \textbf{Systems Focus:}\\
    Spatial reasoning using multimodal foundation models\\[5pt]
    $\bullet$ \textbf{Substrate:} Edge MPUs / NPUs\\
    $\bullet$ \textbf{Workloads:} VLMs, Spatial Transformers\\
    $\bullet$ \textbf{Boundary:} Semantic planning ($1\text{ Hz}$)\\
    $\bullet$ \textbf{Failure Mode:} Hallucination, $P_{99}$ tails\\
    $\bullet$ \textbf{Physical Action:} Unverified proposals
    }
  };

  % --- Phase 4: Physical AI Systems ---
  \node[frontiercard, right=0.52in of p3] (p4) {
    {\scriptsize\bfseries\color{harvardcrimson}\colorbox{harvardcrimson!15}{\,PHASE 4 $\cdot$ NOW (THE FRONTIER)\,}}\\[5pt]
    {\normalsize\bfseries\color{harvardcrimson}Physical AI Systems}\\[1pt]
    {\scriptsize\bfseries\color{harvardcrimson}Closed-Loop Actuation}\\[5pt]
    {\scriptsize\color{ethslate}\raggedright
    \textbf{Systems Focus:}\\
    Learned proposals governed by real-time safety enforcers\\[5pt]
    $\bullet$ \textbf{Substrate:} Linux MPU + Real-Time MCU\\
    $\bullet$ \textbf{Workloads:} Multi-Rate VLA + 1 kHz CBF\\
    $\bullet$ \textbf{Boundary:} Delegated physical authority\\
    $\bullet$ \textbf{Failure Mode:} Gearbox shear / Collisions\\
    $\bullet$ \textbf{Physical Action:} Matter \& kinetic energy
    }
  };

  % Transition Arrows with Clean Spacing
  \draw[->, line width=1.4pt, ethslate!60] (p1.east) -- node[above=4pt, font=\sffamily\bfseries\scriptsize\color{ethslate}, midway]{Compress} (p2.west);
  \draw[->, line width=1.4pt, ethpetrol!70] (p2.east) -- node[above=4pt, font=\sffamily\bfseries\scriptsize\color{ethpetrol}, midway]{Reason} (p3.west);
  \draw[->, line width=1.8pt, harvardcrimson!90] (p3.east) -- node[above=4pt, font=\sffamily\bfseries\scriptsize\color{harvardcrimson}, midway]{Close Loop} (p4.west);

  % Bottom Epistemic Divider Bar
  \node[draw=cardborder, fill=white, rounded corners=4pt, line width=0.8pt, inner sep=6pt, anchor=north, font=\sffamily\scriptsize\bfseries, text=ethdarkblue] 
    at ($(p1.south)!0.5!(p3.south) - (0, 0.22in)$) {
      $\longleftarrow$ \textbf{Open-Loop \& Digital Sandboxes} (Software retries, idempotent computation, no motor coils)
    };
  \node[draw=harvardcrimson, fill=harvardcrimson!10, rounded corners=4pt, line width=1pt, inner sep=6pt, anchor=north, font=\sffamily\scriptsize\bfseries, text=harvardcrimson] 
    at ($(p4.south) - (0, 0.22in)$) {
      \textbf{Physical Causality} ($W_t \to W_{t+1}$, No \texttt{ctrl+z}) $\longrightarrow$
    };

\end{tikzpicture}
\end{document}
'''

# -----------------------------------------------------------------------------
# 3. FIG 03: THREE TRIBES SYNTHESIS
# -----------------------------------------------------------------------------
TRIBES_TEX = r'''\documentclass[tikz,border=12pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{tgheros}
\usepackage{sfmath}
\usepackage{amsmath}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,backgrounds,calc}
\usepackage{xcolor}

\renewcommand{\familydefault}{\sfdefault}

% Harvard Crimson & ETH Zurich Color Palette
\definecolor{harvardcrimson}{HTML}{A51C30}
\definecolor{ethdarkblue}{HTML}{1F407A}
\definecolor{ethblue}{HTML}{215CAF}
\definecolor{ethpetrol}{HTML}{007A87}
\definecolor{ethbronze}{HTML}{B87333}
\definecolor{ethslate}{HTML}{475569}
\definecolor{cardbg}{HTML}{F8FAFC}
\definecolor{cardborder}{HTML}{CBD5E1}
\definecolor{frontierbg}{HTML}{FEF2F2}

\begin{document}
\begin{tikzpicture}[
  font=\sffamily,
  >=Stealth,
  tribecard/.style={
    draw=cardborder,
    fill=cardbg,
    rounded corners=6pt,
    line width=0.9pt,
    text width=2.34in,
    inner sep=9pt,
    align=left
  },
  synthesiscard/.style={
    draw=harvardcrimson,
    fill=frontierbg,
    rounded corners=6pt,
    line width=1.4pt,
    text width=7.72in,
    inner sep=10pt,
    align=left
  },
  arrowlabel/.style={
    font=\sffamily\scriptsize\bfseries,
    fill=white,
    inner sep=2.5pt,
    rounded corners=2pt
  }
]

  % --- TRIBE 1: The Brain (ML / AI) ---
  \node[tribecard, draw=ethblue!70] (brain) {
    {\scriptsize\bfseries\color{ethblue}\colorbox{ethblue!10}{\,TRIBE 1 $\cdot$ THE BRAIN\,}}\\[4pt]
    {\normalsize\bfseries\color{ethdarkblue}The ML / AI Engineer}\\[1pt]
    {\scriptsize\bfseries\color{ethslate}Computer Science \& Modern AI}\\[5pt]
    {\scriptsize\color{ethslate}\raggedright
    \textbf{Core Strength:}\\
    Semantic Competence \& Representation\\
    $\bullet$ Vision-Language Models (VLMs)\\
    $\bullet$ Diffusion / ACT Trajectory Chunks\\
    $\bullet$ Latent World Models (JEPAs)\\[4pt]
    \textbf{\color{harvardcrimson}The Critical Blindspot:}\\
    \textit{The Digital Sandbox Illusion}---assuming simulation guarantees safety and exceptions are harmless.}
  };

  % --- TRIBE 2: The Nervous System (Embedded / ECE) ---
  \node[tribecard, draw=ethpetrol!80, right=0.35in of brain] (nervous) {
    {\scriptsize\bfseries\color{ethpetrol}\colorbox{ethpetrol!10}{\,TRIBE 2 $\cdot$ THE NERVOUS SYSTEM\,}}\\[4pt]
    {\normalsize\bfseries\color{ethdarkblue}The Embedded / ECE Engineer}\\[1pt]
    {\scriptsize\bfseries\color{ethslate}Silicon \& Real-Time Systems}\\[5pt]
    {\scriptsize\color{ethslate}\raggedright
    \textbf{Core Strength:}\\
    Silicon Privilege \& Multi-Rate IPC\\
    $\bullet$ Microsecond Clocks \& $P_{99}$ Metrology\\
    $\bullet$ Zero-Copy DMA \& Shared SRAM\\
    $\bullet$ Hardware Peripheral Bus Firewalls\\[4pt]
    \textbf{\color{harvardcrimson}The Critical Blindspot:}\\
    \textit{The Static Automation Illusion}---treating systems as rigid loops unable to handle open worlds.}
  };

  % --- TRIBE 3: The Body & Control (Robotics / Mechanical) ---
  \node[tribecard, draw=ethbronze!80, right=0.35in of nervous] (body) {
    {\scriptsize\bfseries\color{ethbronze}\colorbox{ethbronze!10}{\,TRIBE 3 $\cdot$ THE BODY \& CONTROL\,}}\\[4pt]
    {\normalsize\bfseries\color{ethdarkblue}The Robotics Engineer}\\[1pt]
    {\scriptsize\bfseries\color{ethslate}Dynamics, Invariants \& Control}\\[5pt]
    {\scriptsize\color{ethslate}\raggedright
    \textbf{Core Strength:}\\
    Physical Laws \& Safety Envelopes\\
    $\bullet$ Work-Energy \& Inertia $\mathbf{M}(\mathbf{q})$\\
    $\bullet$ Control Barrier Functions ($h(x) \ge 0$)\\
    $\bullet$ Thermal Limits ($I^2t$) \& Jerk Limits\\[4pt]
    \textbf{\color{harvardcrimson}The Critical Blindspot:}\\
    \textit{The Closed-World Illusion}---distrusting \mbox{learned models} as black boxes; fragile when open-world environments deviate.}
  };

  % --- SYNTHESIS BANNER: Physical AI Systems ---
  \node[synthesiscard, below=0.38in of nervous.south] (synthesis) {
    \begin{minipage}{0.99\linewidth}
      \centering
      {\normalsize\bfseries\color{harvardcrimson}THE PHYSICAL AI SYSTEMS SYNTHESIS}\\[2pt]
      {\scriptsize\bfseries\color{ethdarkblue}Bridging the Brain, Nervous System, and Body across the Proposal--Permission Boundary}\\[5pt]
      \rule{0.96\linewidth}{0.4pt}\\[6pt]
      \begin{tabular*}{\linewidth}{@{}p{2.46in}@{\hfill}p{2.46in}@{\hfill}p{2.46in}@{}}
        \scriptsize\textbf{\color{ethblue}1. Unverified Proposals (Brain)} & 
        \scriptsize\textbf{\color{ethpetrol}2. Real-Time Transport (Nerves)} & 
        \scriptsize\textbf{\color{ethbronze}3. Physical Invariants (Body)} \\[2pt]
        \scriptsize\raggedright High-capacity VLMs \& Diffusion ACT emit candidate action chunks ($p_t$) on Linux MPU. &
        \scriptsize\raggedright Lock-free SRAM ring buffers and hardware watchdogs bound tail latency ($P_{99}$). &
        \scriptsize\raggedright 1 kHz MCU projects proposals onto safe sets $\Pi_{\mathcal{U}_{\text{safe}}}(p_t)$ via CBFs before gate drive.
      \end{tabular*}\\[7pt]
      {\small\bfseries\color{ethdarkblue}Universal Definition of Success: } 
      {\small\color{harvardcrimson}\textbf{Open-World Semantic Competence} $\;\mathbf{AND}\;$ \textbf{Strict Physical Invariant Survival}}
    \end{minipage}
  };

  % Connecting Arrows from Tribes to Synthesis
  \draw[->, line width=1.2pt, draw=ethblue] (brain.south) -- ++(0,-0.16in) -| ($(synthesis.north west) + (1.25in, 0)$)
    node[pos=0.25, arrowlabel, text=ethblue] {Semantic Proposals ($p_t$)};

  \draw[->, line width=1.2pt, draw=ethpetrol] (nervous.south) -- (synthesis.north)
    node[pos=0.45, arrowlabel, text=ethpetrol] {Multi-Rate IPC \& Watchdogs};

  \draw[->, line width=1.2pt, draw=ethbronze] (body.south) -- ++(0,-0.16in) -| ($(synthesis.north east) + (-1.25in, 0)$)
    node[pos=0.25, arrowlabel, text=ethbronze] {1 kHz CBF Safe Sets ($h(x) \ge 0$)};

\end{tikzpicture}
\end{document}
'''

def build_all():
    files = [
        ("fig01_agent_anatomy.tex", ANATOMY_TEX),
        ("fig01_eras_evolution.tex", ERAS_TEX),
        ("fig01_three_tribes.tex", TRIBES_TEX),
    ]
    
    for filename, content in files:
        tex_path = os.path.join(CH01_FIG_DIR, filename)
        with open(tex_path, "w") as f:
            f.write(content)
        
        stem = filename.replace(".tex", "")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", filename], cwd=CH01_FIG_DIR, check=True)
        subprocess.run(["pdftoppm", "-png", "-r", "150", f"{stem}.pdf", f"preview_{stem}"], cwd=CH01_FIG_DIR, check=True)
        print(f"Generated {filename} -> {stem}.pdf & preview_{stem}-1.png")

if __name__ == "__main__":
    build_all()
