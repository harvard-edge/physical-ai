// Maya's Reachy - the chat UI logic.
//
// One job today: send what the kid types or says to the backend, then play the
// robot's reaction on screen (and, when the real robot is offline, voice it in
// the browser so the demo still lands). The on-screen robot mirrors the same
// gesture the metal performs.

const $ = (sel) => document.querySelector(sel);

const robot    = $("#robot");
const log      = $("#log");
const seed     = $("#seed");
const form     = $("#composer");
const input    = $("#text");
const sendBtn  = $("#send");
const micBtn   = $("#mic");
const pill     = $("#pill");
const pillText = $("#pillText");
const dot      = $("#dot");
const example  = $("#example");

let mode = "ready"; // "ready" | "simulation" — updated from the server

// ---- status pill ----------------------------------------------------------

function setPill(state) {
  if (state === "simulation") {
    pill.classList.remove("is-live");
    pill.classList.add("is-sim");
    pillText.textContent = "Simulating — robot's not here";
  } else if (state === "robot") {
    pill.classList.remove("is-sim");
    pill.classList.add("is-live");
    pillText.textContent = "Robot connected";
  } else {
    pillText.textContent = "Ready when you are";
  }
}

fetch("/api/status")
  .then((r) => r.json())
  .then((s) => { mode = s.mode; setPill(mode === "simulation" ? "simulation" : "ready"); })
  .catch(() => setPill("ready"));

// ---- transcript -----------------------------------------------------------

function clearSeed() {
  if (seed && seed.parentNode) seed.remove();
}

function addBubble(text, who) {
  const el = document.createElement("div");
  el.className = `bubble ${who}`;
  el.textContent = text;
  log.appendChild(el);
  el.scrollIntoView({ behavior: "smooth", block: "end" });
  return el;
}

function addSkills(skills) {
  const row = document.createElement("div");
  row.className = "skills";
  for (const s of skills) {
    const chip = document.createElement("span");
    chip.className = "skill";
    chip.textContent = s;
    row.appendChild(chip);
  }
  log.appendChild(row);
  row.scrollIntoView({ behavior: "smooth", block: "end" });
}

// ---- robot animation (mirror the hardware gesture) ------------------------

function oneShot(cls) {
  robot.classList.add(cls);
  const clear = () => robot.classList.remove(cls);
  // clear when any child animation ends, with a fallback timer
  robot.addEventListener("animationend", clear, { once: true });
  setTimeout(clear, 900);
}

function estimateSpeechMs(text) {
  const words = text.trim().split(/\s+/).length;
  return Math.min(6000, Math.max(1100, words * 340));
}

function animateReaction(text, closer) {
  robot.classList.add("is-talking");
  const done = () => {
    robot.classList.remove("is-talking");
    if (closer === "tilt") oneShot("do-tilt");
    else if (closer === "wiggle") oneShot("do-wiggle");
    else oneShot("do-nod");
  };

  // In simulation, sync the talking animation to the browser voice.
  if (mode === "simulation" && "speechSynthesis" in window) {
    const u = new SpeechSynthesisUtterance(text);
    u.rate = 1;
    u.pitch = 1.15;
    u.onend = done;
    // guard against browsers that never fire onend
    setTimeout(() => { if (robot.classList.contains("is-talking")) done(); }, estimateSpeechMs(text) + 1500);
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
  } else {
    setTimeout(done, estimateSpeechMs(text));
  }
}

const CLOSER = { curious: "tilt", excited: "wiggle", friendly: "wiggle", warm: "nod" };

// ---- sending --------------------------------------------------------------

let busy = false;

async function send(text) {
  text = text.trim();
  if (!text || busy) return;
  busy = true;
  sendBtn.disabled = true;
  clearSeed();
  addBubble(text, "kid");
  input.value = "";

  try {
    const res = await fetch("/api/say", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();

    if (!data.ok) {
      addBubble(data.error || "Something went wrong.", "bot");
      return;
    }

    mode = data.mode;
    setPill(data.mode === "robot" ? "robot" : "simulation");

    addBubble(data.spoken, "bot");
    addSkills(data.skills || []);
    animateReaction(data.spoken, CLOSER[data.mood] || "nod");
  } catch (err) {
    addBubble("I couldn't reach the robot's computer. Is the server running?", "bot");
  } finally {
    busy = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  send(input.value);
});

if (example) {
  example.addEventListener("click", () => send(example.textContent));
}

// ---- mic: browser speech-to-text (Web Speech API) -------------------------

const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SR) {
  // No speech recognition here: keep typing, hide the mic honestly.
  micBtn.hidden = true;
} else {
  const rec = new SR();
  rec.lang = "en-US";
  rec.interimResults = true;
  rec.continuous = false;

  let listening = false;

  micBtn.addEventListener("click", () => {
    if (listening) { rec.stop(); return; }
    try { rec.start(); } catch (_) { /* already starting */ }
  });

  rec.onstart = () => {
    listening = true;
    micBtn.classList.add("is-listening");
    micBtn.setAttribute("aria-label", "Listening — tap to stop");
    input.placeholder = "Listening…";
  };
  rec.onresult = (e) => {
    let transcript = "";
    for (const r of e.results) transcript += r[0].transcript;
    input.value = transcript;
  };
  rec.onerror = () => { /* surfaced by onend resetting the UI */ };
  rec.onend = () => {
    listening = false;
    micBtn.classList.remove("is-listening");
    micBtn.setAttribute("aria-label", "Tap to talk");
    input.placeholder = "Say something to your robot…";
    const said = input.value.trim();
    if (said) send(said);  // auto-send what was heard
  };
}

input.focus();
