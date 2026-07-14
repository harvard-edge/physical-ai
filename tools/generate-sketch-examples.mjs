import fs from "node:fs";
import path from "node:path";

const OUT = path.resolve("book/assets/diagrams/sketch-examples");

const C = {
  ink: "#1b2a4a",
  teal: "#18a999",
  amber: "#e8a33d",
  coral: "#c0562b",
  paper: "#fbfaf6",
  white: "#ffffff",
  muted: "#687386",
  paleTeal: "#dff5f1",
  paleAmber: "#fff1d5",
  paleCoral: "#f8e4dc",
  paleBlue: "#e8edf6",
};

const escapeXml = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;");

const uid = (() => {
  let n = 0;
  return (prefix = "e") => `${prefix}-${++n}`;
})();

class Sketch {
  constructor(title, subtitle) {
    this.title = title;
    this.subtitle = subtitle;
    this.svg = [];
    this.elements = [];
    this.index = 0;
  }

  base(type, x, y, width, height, opts = {}) {
    this.index += 1;
    return {
      id: uid(type),
      type,
      x,
      y,
      width,
      height,
      angle: 0,
      strokeColor: opts.stroke ?? C.ink,
      backgroundColor: opts.fill ?? "transparent",
      fillStyle: "solid",
      strokeWidth: opts.strokeWidth ?? 2,
      strokeStyle: opts.dash ? "dashed" : "solid",
      roughness: opts.roughness ?? 2,
      opacity: opts.opacity ?? 100,
      groupIds: [],
      frameId: null,
      index: `a${String(this.index).padStart(3, "0")}`,
      roundness: type === "rectangle" ? { type: 3 } : null,
      seed: 1000 + this.index * 97,
      version: 1,
      versionNonce: 5000 + this.index * 131,
      isDeleted: false,
      boundElements: [],
      updated: 1,
      link: null,
      locked: false,
    };
  }

  rect(x, y, w, h, opts = {}) {
    const rx = opts.radius ?? 18;
    this.svg.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${opts.fill ?? "none"}" stroke="${opts.stroke ?? C.ink}" stroke-width="${opts.strokeWidth ?? 3}" ${opts.dash ? 'stroke-dasharray="10 8"' : ""} filter="url(#rough)"/>`);
    this.elements.push(this.base("rectangle", x, y, w, h, opts));
  }

  ellipse(x, y, w, h, opts = {}) {
    this.svg.push(`<ellipse cx="${x + w / 2}" cy="${y + h / 2}" rx="${w / 2}" ry="${h / 2}" fill="${opts.fill ?? "none"}" stroke="${opts.stroke ?? C.ink}" stroke-width="${opts.strokeWidth ?? 3}" ${opts.dash ? 'stroke-dasharray="10 8"' : ""} filter="url(#rough)"/>`);
    this.elements.push(this.base("ellipse", x, y, w, h, opts));
  }

  text(x, y, value, opts = {}) {
    const size = opts.size ?? 24;
    const color = opts.color ?? C.ink;
    const weight = opts.weight ?? 500;
    const anchor = opts.anchor ?? "start";
    const lines = String(value).split("\n");
    const lineHeight = opts.lineHeight ?? 1.18;
    const tspans = lines.map((line, i) => `<tspan x="${x}" dy="${i === 0 ? 0 : size * lineHeight}">${escapeXml(line)}</tspan>`).join("");
    this.svg.push(`<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Virgil, Chalkboard, 'Comic Sans MS', sans-serif" font-size="${size}" font-weight="${weight}" fill="${color}">${tspans}</text>`);

    const maxChars = Math.max(...lines.map((line) => line.length), 1);
    const width = opts.width ?? Math.max(20, maxChars * size * 0.58);
    const height = lines.length * size * lineHeight;
    const tx = anchor === "middle" ? x - width / 2 : x;
    this.elements.push({
      ...this.base("text", tx, y - size, width, height, { stroke: color, fill: "transparent", roughness: 0 }),
      fontSize: size,
      fontFamily: 1,
      text: String(value),
      rawText: String(value),
      textAlign: anchor === "middle" ? "center" : "left",
      verticalAlign: "top",
      containerId: null,
      originalText: String(value),
      autoResize: true,
      lineHeight,
    });
  }

  line(x1, y1, x2, y2, opts = {}) {
    const mx = (x1 + x2) / 2 + (opts.bend ?? 0);
    const my = (y1 + y2) / 2 - (opts.bend ?? 0) * 0.35;
    const d = `M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`;
    this.svg.push(`<path d="${d}" fill="none" stroke="${opts.stroke ?? C.ink}" stroke-width="${opts.strokeWidth ?? 3}" stroke-linecap="round" ${opts.dash ? 'stroke-dasharray="10 8"' : ""} filter="url(#rough)"/>`);
    const minX = Math.min(x1, x2);
    const minY = Math.min(y1, y2);
    this.elements.push({
      ...this.base("line", minX, minY, Math.abs(x2 - x1), Math.abs(y2 - y1), opts),
      points: [[x1 - minX, y1 - minY], [x2 - minX, y2 - minY]],
      lastCommittedPoint: null,
      startBinding: null,
      endBinding: null,
      startArrowhead: null,
      endArrowhead: null,
    });
  }

  arrow(x1, y1, x2, y2, opts = {}) {
    const stroke = opts.stroke ?? C.ink;
    const bend = opts.bend ?? 0;
    const mx = (x1 + x2) / 2 + bend;
    const my = (y1 + y2) / 2 - bend * 0.35;
    const d = `M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`;
    const angle = Math.atan2(y2 - my, x2 - mx);
    const a = 13;
    const p1x = x2 - a * Math.cos(angle - 0.55);
    const p1y = y2 - a * Math.sin(angle - 0.55);
    const p2x = x2 - a * Math.cos(angle + 0.55);
    const p2y = y2 - a * Math.sin(angle + 0.55);
    this.svg.push(`<path d="${d}" fill="none" stroke="${stroke}" stroke-width="${opts.strokeWidth ?? 4}" stroke-linecap="round" ${opts.dash ? 'stroke-dasharray="10 8"' : ""} filter="url(#rough)"/>`);
    this.svg.push(`<path d="M ${p1x} ${p1y} L ${x2} ${y2} L ${p2x} ${p2y}" fill="none" stroke="${stroke}" stroke-width="${opts.strokeWidth ?? 4}" stroke-linecap="round" stroke-linejoin="round"/>`);
    const minX = Math.min(x1, x2);
    const minY = Math.min(y1, y2);
    this.elements.push({
      ...this.base("arrow", minX, minY, Math.abs(x2 - x1), Math.abs(y2 - y1), opts),
      points: [[x1 - minX, y1 - minY], [x2 - minX, y2 - minY]],
      lastCommittedPoint: null,
      startBinding: null,
      endBinding: null,
      startArrowhead: null,
      endArrowhead: "arrow",
      elbowed: false,
    });
  }

  pill(x, y, w, label, opts = {}) {
    this.rect(x, y, w, 42, { fill: opts.fill ?? C.white, stroke: opts.stroke ?? C.ink, strokeWidth: 2, radius: 21 });
    this.text(x + w / 2, y + 28, label, { size: 18, weight: 600, color: opts.color ?? opts.stroke ?? C.ink, anchor: "middle", width: w - 16 });
  }

  person(x, y, label = "Maya") {
    this.ellipse(x + 29, y, 54, 54, { fill: C.paleAmber, stroke: C.ink });
    this.line(x + 56, y + 55, x + 56, y + 142, { strokeWidth: 4 });
    this.line(x + 56, y + 78, x + 15, y + 108, { strokeWidth: 4 });
    this.line(x + 56, y + 78, x + 98, y + 103, { strokeWidth: 4 });
    this.line(x + 56, y + 142, x + 26, y + 190, { strokeWidth: 4 });
    this.line(x + 56, y + 142, x + 88, y + 190, { strokeWidth: 4 });
    this.text(x + 56, y + 224, label, { size: 25, weight: 650, anchor: "middle", width: 100 });
  }

  robot(x, y, label = "Reachy") {
    this.line(x + 40, y - 15, x + 22, y - 48, { stroke: C.teal, strokeWidth: 4 });
    this.line(x + 130, y - 15, x + 148, y - 48, { stroke: C.teal, strokeWidth: 4 });
    this.ellipse(x + 10, y, 150, 110, { fill: C.paleTeal, stroke: C.ink });
    this.ellipse(x + 48, y + 37, 18, 18, { fill: C.ink, stroke: C.ink, roughness: 1 });
    this.ellipse(x + 105, y + 37, 18, 18, { fill: C.ink, stroke: C.ink, roughness: 1 });
    this.line(x + 73, y + 77, x + 98, y + 77, { stroke: C.ink, strokeWidth: 3, bend: 4 });
    this.rect(x + 35, y + 120, 100, 72, { fill: C.white, stroke: C.ink, radius: 28 });
    this.text(x + 85, y + 232, label, { size: 25, weight: 650, anchor: "middle", width: 130 });
  }

  note(x, y, w, h, title, body, color = C.amber) {
    const fill = color === C.teal ? C.paleTeal : color === C.coral ? C.paleCoral : color === C.ink ? C.paleBlue : C.paleAmber;
    this.rect(x, y, w, h, { fill, stroke: color, strokeWidth: 2, radius: 8 });
    this.text(x + 18, y + 32, title, { size: 19, weight: 700, color });
    this.text(x + 18, y + 65, body, { size: 17, weight: 500, color: C.ink, lineHeight: 1.22, width: w - 36 });
  }

  finish(name) {
    const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720" role="img" aria-labelledby="title desc">
  <title id="title">${escapeXml(this.title)}</title>
  <desc id="desc">${escapeXml(this.subtitle)}</desc>
  <defs>
    <filter id="rough" x="-4%" y="-4%" width="108%" height="108%">
      <feTurbulence type="fractalNoise" baseFrequency="0.008 0.013" numOctaves="1" seed="12" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="1.8" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="#dce1e8"/>
    </pattern>
  </defs>
  <rect width="1200" height="720" fill="${C.paper}"/>
  <rect x="0" y="0" width="1200" height="720" fill="url(#dots)" opacity="0.5"/>
  <text x="58" y="58" font-family="Virgil, Chalkboard, 'Comic Sans MS', sans-serif" font-size="27" font-weight="700" fill="${C.ink}">${escapeXml(this.title)}</text>
  <text x="58" y="91" font-family="Virgil, Chalkboard, 'Comic Sans MS', sans-serif" font-size="19" font-weight="500" fill="${C.muted}">${escapeXml(this.subtitle)}</text>
  ${this.svg.join("\n  ")}
</svg>`;

    const excalidraw = {
      type: "excalidraw",
      version: 2,
      source: "https://excalidraw.com",
      elements: this.elements,
      appState: {
        gridSize: null,
        viewBackgroundColor: C.paper,
        currentItemFontFamily: 1,
      },
      files: {},
    };

    fs.writeFileSync(path.join(OUT, `${name}.svg`), svg);
    fs.writeFileSync(path.join(OUT, `${name}.excalidraw`), `${JSON.stringify(excalidraw, null, 2)}\n`);
  }
}

function loopCloses() {
  const s = new Sketch("THE LOOP CLOSES", "The action becomes part of the next input.");

  s.person(95, 245);
  s.robot(930, 270);

  s.arrow(220, 300, 900, 300, { stroke: C.teal, strokeWidth: 5, bend: -40 });
  s.pill(475, 205, 230, "SENSE  ·  already aging", { stroke: C.teal, fill: C.paleTeal });
  s.ellipse(760, 195, 70, 70, { fill: C.white, stroke: C.amber });
  s.line(795, 230, 795, 210, { stroke: C.amber, strokeWidth: 3 });
  s.line(795, 230, 812, 241, { stroke: C.amber, strokeWidth: 3 });
  s.text(795, 285, "Δ", { size: 24, weight: 700, color: C.amber, anchor: "middle", width: 40 });

  s.arrow(915, 468, 235, 468, { stroke: C.coral, strokeWidth: 5, bend: 42 });
  s.pill(500, 500, 205, "ACT  ·  consequence", { stroke: C.coral, fill: C.paleCoral });

  s.arrow(172, 438, 172, 345, { stroke: C.amber, strokeWidth: 4, bend: -20 });
  s.text(300, 565, "the world is now different", { size: 22, weight: 650, color: C.coral });
  s.arrow(545, 548, 860, 365, { stroke: C.amber, strokeWidth: 3, dash: true, bend: -35 });
  s.text(754, 585, "next input distribution", { size: 18, weight: 650, color: C.amber });
  s.text(754, 609, "moves with the robot", { size: 18, weight: 500, color: C.ink });

  s.note(275, 115, 210, 86, "PERISHABLE", "the world keeps moving", C.amber);
  s.note(500, 115, 210, 86, "PARTIAL", "belief is not the world", C.ink);
  s.note(725, 115, 230, 86, "ENDOGENOUS", "action shapes what follows", C.coral);

  s.finish("01-loop-closes");
}

function chipSaysNo() {
  const s = new Sketch("THE CHIP THAT SAYS NO", "A proposal crosses a measured privilege boundary.");

  s.rect(75, 130, 1050, 470, { fill: C.white, stroke: C.ink, strokeWidth: 3, radius: 58, dash: true });
  s.text(105, 172, "inside one UNO Q", { size: 23, weight: 700, color: C.ink });

  s.ellipse(115, 210, 310, 235, { fill: C.paleBlue, stroke: C.ink, strokeWidth: 3 });
  s.text(267, 270, "MPU  ·  PROPOSE", { size: 23, weight: 700, color: C.ink, anchor: "middle", width: 250 });
  s.text(267, 315, "reasoner", { size: 20, weight: 600, color: C.muted, anchor: "middle", width: 160 });
  s.note(160, 330, 215, 82, "INTENT", "turn 140°, fast", C.ink);

  s.arrow(410, 327, 560, 327, { stroke: C.amber, strokeWidth: 5 });
  s.text(485, 207, "proposal crosses", { size: 18, weight: 700, color: C.amber, anchor: "middle", width: 150 });
  s.arrow(485, 219, 485, 305, { stroke: C.amber, strokeWidth: 3, bend: -10 });

  s.ellipse(545, 208, 315, 240, { fill: C.paleTeal, stroke: C.teal, strokeWidth: 4 });
  s.text(702, 270, "MCU  ·  DISPOSE", { size: 23, weight: 700, color: C.teal, anchor: "middle", width: 250 });
  s.text(702, 315, "the physical boundary", { size: 19, weight: 600, color: C.muted, anchor: "middle", width: 220 });
  s.text(702, 357, "|turn| ≤ 30°", { size: 26, weight: 700, color: C.ink, anchor: "middle", width: 180 });
  s.line(673, 382, 730, 382, { stroke: C.coral, strokeWidth: 5, bend: 14 });
  s.line(676, 372, 728, 393, { stroke: C.coral, strokeWidth: 5 });
  s.text(790, 400, "no.", { size: 30, weight: 750, color: C.coral });

  s.arrow(845, 327, 1000, 327, { stroke: C.teal, strokeWidth: 5 });
  s.ellipse(995, 255, 82, 145, { fill: C.paleAmber, stroke: C.ink, strokeWidth: 3 });
  s.line(1036, 327, 1060, 296, { stroke: C.ink, strokeWidth: 4 });
  s.line(1036, 327, 1016, 298, { stroke: C.ink, strokeWidth: 4 });
  s.text(1035, 438, "bounded motion", { size: 18, weight: 650, color: C.teal, anchor: "middle", width: 160 });

  s.note(125, 475, 285, 88, "VISIBLE", "the bad command stops here", C.coral);
  s.note(455, 475, 285, 88, "NUMBER", "t_veto = ______ ms", C.amber);
  s.note(785, 475, 285, 88, "DECISION", "enforcement stays on MCU", C.teal);

  s.finish("02-chip-says-no");
}

function placementMap() {
  const s = new Sketch("THE PLACEMENT MAP", "Every sticky note spends from the same physical budgets.");

  s.pill(190, 105, 185, "LATENCY  p99", { stroke: C.teal, fill: C.paleTeal });
  s.pill(390, 105, 170, "ENERGY  J", { stroke: C.amber, fill: C.paleAmber });
  s.pill(575, 105, 190, "EGRESS  B/h", { stroke: C.coral, fill: C.paleCoral });
  s.pill(780, 105, 240, "RECOVERY  t_safe", { stroke: C.ink, fill: C.paleBlue });

  // The map is a field-notebook workspace, not a rigid architecture table.
  s.ellipse(105, 195, 390, 390, { fill: C.paleTeal, stroke: C.teal, strokeWidth: 3, dash: true });
  s.ellipse(410, 220, 380, 350, { fill: C.paleBlue, stroke: C.ink, strokeWidth: 3, dash: true });
  s.ellipse(710, 190, 390, 400, { fill: C.paleAmber, stroke: C.amber, strokeWidth: 3, dash: true });
  s.text(245, 230, "on the body", { size: 23, weight: 700, color: C.teal });
  s.text(545, 255, "nearby", { size: 23, weight: 700, color: C.ink });
  s.text(875, 225, "far away", { size: 23, weight: 700, color: C.amber });

  s.note(150, 285, 210, 82, "SAFETY GATE", "MCU  ·  hard deadline", C.teal);
  s.note(245, 405, 215, 82, "TRACKING", "fast belief update", C.teal);
  s.note(485, 320, 230, 82, "WORLD MODEL", "predict through delay", C.ink);
  s.note(780, 290, 220, 82, "VLM MEANING", "slow semantic path", C.amber);
  s.note(830, 445, 240, 82, "ADAPTATION", "curate → train → return", C.amber);

  s.text(55, 335, "10 ms", { size: 19, weight: 700, color: C.teal });
  s.arrow(88, 330, 150, 330, { stroke: C.teal, strokeWidth: 3 });
  s.text(55, 455, "1 s", { size: 19, weight: 700, color: C.ink });
  s.arrow(88, 450, 245, 450, { stroke: C.ink, strokeWidth: 3, dash: true });
  s.text(55, 550, "days", { size: 19, weight: 700, color: C.amber });
  s.arrow(100, 545, 825, 500, { stroke: C.amber, strokeWidth: 3, dash: true, bend: -20 });

  s.arrow(890, 405, 390, 375, { stroke: C.coral, strokeWidth: 3, dash: true, bend: 58 });
  s.text(570, 610, "move one sticky note", { size: 21, weight: 700, color: C.coral, anchor: "middle", width: 220 });
  s.text(570, 637, "then circle every number that moved", { size: 19, weight: 500, color: C.ink, anchor: "middle", width: 320 });

  s.finish("03-placement-map");
}

fs.mkdirSync(OUT, { recursive: true });
loopCloses();
chipSaysNo();
placementMap();
