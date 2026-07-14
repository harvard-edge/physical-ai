// Maya's Reachy — robot-hosted teach-and-talk interface.

const robot = document.querySelector("#robot");
const log = document.querySelector("#log");
const seed = document.querySelector("#seed");
const pill = document.querySelector("#pill");
const pillText = document.querySelector("#pillText");
const form = document.querySelector("#composer");
const input = document.querySelector("#text");
const sendButton = document.querySelector("#send");
const micButton = document.querySelector("#mic");
const exampleButton = document.querySelector("#example");
const greetButton = document.querySelector("#greet");

let state = "starting";
let mode = "robot";
let cloudConfigured = false;
let supportsRobotListening = false;
let busy = false;
let robotListening = false;

function setPill(kind, text) {
  pill.className = `pill ${kind}`;
  pillText.textContent = text;
}

function finishGesture(mood = "friendly") {
  robot.classList.add(mood === "curious" ? "do-curious" : "do-happy");
  setTimeout(() => robot.classList.remove("do-curious", "do-happy"), 900);
}

function renderStatus(data) {
  const previous = state;
  state = data.state || (data.mode === "simulation" ? "simulation" : "ready");
  mode = data.mode || mode;
  cloudConfigured = Boolean(data.cloud_configured);
  supportsRobotListening = Boolean(data.supports_robot_listening);

  robot.classList.toggle("is-talking", state === "speaking");
  robot.classList.toggle("is-thinking", state === "thinking");
  if (greetButton) greetButton.disabled = ["queued", "listening", "speaking", "thinking"].includes(state);

  if (state === "listening") {
    setPill("is-live", "Listening… speak to your robot");
  } else if (state === "thinking") {
    setPill("is-think", "Cloud brain is thinking…");
  } else if (state === "speaking" || state === "queued") {
    setPill("is-live", "Speaking on Reachy");
  } else if (state === "simulation") {
    setPill("is-sim", cloudConfigured ? "Simulation · Groq ready" : "Simulation · cloud off");
  } else if (state === "error") {
    setPill("is-error", "Needs a little help");
  } else if (state === "stopped") {
    setPill("is-error", "App stopped");
  } else if (state === "ready") {
    setPill(cloudConfigured ? "is-live" : "is-sim",
      cloudConfigured ? "Robot + Groq ready" : "Robot ready · cloud off");
  } else {
    setPill("", "Waking up…");
  }

  if (previous === "speaking" && state === "ready") finishGesture();
}

function clearSeed() {
  if (seed && seed.parentNode) seed.remove();
}

function addBubble(text, who, extraClass = "") {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${who} ${extraClass}`.trim();
  bubble.textContent = text;
  log.appendChild(bubble);
  bubble.scrollIntoView({ behavior: "smooth", block: "end" });
  return bubble;
}

function addMeta(data) {
  const labels = [];
  if (data.source === "groq-cloud") labels.push("Groq understood this");
  if (data.source === "offline-fallback") labels.push("cloud unavailable");
  if (data.learned && data.learned.robot_name) {
    labels.push(`remembered name: ${data.learned.robot_name}`);
  }
  if (data.learned && data.learned.claims) {
    labels.push(`remembered ${data.learned.claims.length} connection${data.learned.claims.length === 1 ? "" : "s"}`);
  }
  labels.push(data.speech_mode === "robot" ? "voice on robot" : "browser voice");

  const row = document.createElement("div");
  row.className = "skills";
  for (const label of labels) {
    const chip = document.createElement("span");
    chip.className = "skill";
    chip.textContent = label;
    row.appendChild(chip);
  }
  log.appendChild(row);
}

function simulateVoice(text, durationSeconds, mood = "friendly") {
  robot.classList.add("is-talking");
  if (!("speechSynthesis" in window)) {
    setTimeout(() => {
      robot.classList.remove("is-talking");
      finishGesture(mood);
    }, durationSeconds * 1000);
    return;
  }
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1;
  utterance.pitch = 1.12;
  utterance.onend = () => {
    robot.classList.remove("is-talking");
    finishGesture(mood);
  };
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
}

async function getStatus() {
  const response = await fetch(`/api/status?_=${Date.now()}`, { cache: "no-store" });
  if (!response.ok) throw new Error("status unavailable");
  renderStatus(await response.json());
}

async function send(text) {
  text = text.trim();
  if (!text || busy) return;
  busy = true;
  sendButton.disabled = true;
  clearSeed();
  addBubble(text, "kid");
  const thinking = addBubble("Thinking…", "bot", "is-pending");
  input.value = "";
  setPill("is-think", "Cloud brain is thinking…");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    thinking.remove();
    if (!data.ok) {
      addBubble(data.error || "Something went wrong.", "bot");
      return;
    }

    addBubble(data.reply, "bot");
    addMeta(data);
    if (data.speech_mode === "browser") {
      simulateVoice(data.reply, data.duration_seconds || 2, data.mood);
    } else {
      robot.classList.add("is-talking");
      setTimeout(() => robot.classList.remove("is-talking"),
        (data.duration_seconds || 2) * 1000 + 700);
    }
  } catch (error) {
    thinking.remove();
    addBubble("I couldn't reach my robot app. Is it still running?", "bot");
  } finally {
    busy = false;
    sendButton.disabled = false;
    input.focus();
  }
}

async function listenOnRobot() {
  if (robotListening) {
    await fetch("/api/listen/stop", { method: "POST" }).catch(() => {});
    setPill("is-think", "Finishing what I heard…");
    return;
  }
  if (busy) return;
  busy = true;
  robotListening = true;
  sendButton.disabled = true;
  micButton.classList.add("is-listening");
  micButton.setAttribute("aria-label", "Stop listening");
  micButton.title = "Stop listening";
  clearSeed();
  const listening = addBubble("Listening…", "bot", "is-pending");
  setPill("is-live", "Listening… speak to your robot");

  try {
    const response = await fetch("/api/listen", { method: "POST" });
    const data = await response.json();
    listening.remove();
    if (!data.ok) {
      addBubble(data.error || "I couldn't hear that. Please try again.", "bot");
      return;
    }
    addBubble(data.transcript, "kid");
    addBubble(data.reply, "bot");
    addMeta(data);
    if (data.speech_mode === "browser") {
      simulateVoice(data.reply, data.duration_seconds || 2, data.mood);
    } else {
      robot.classList.add("is-talking");
      setTimeout(() => robot.classList.remove("is-talking"),
        (data.duration_seconds || 2) * 1000 + 700);
    }
  } catch (error) {
    listening.remove();
    addBubble("I couldn't reach my microphone. Please try again.", "bot");
  } finally {
    busy = false;
    robotListening = false;
    sendButton.disabled = false;
    micButton.classList.remove("is-listening");
    micButton.setAttribute("aria-label", "Tap to talk");
    micButton.title = "Tap to talk";
    input.focus();
  }
}

async function playGreeting() {
  if (busy) return;
  try {
    const response = await fetch("/api/greet", { method: "POST" });
    const data = await response.json();
    if (data.accepted === false) return;
    clearSeed();
    addBubble(data.phrase, "bot");
    if (data.mode === "simulation") {
      simulateVoice(data.phrase, data.duration_seconds || 4.2, "excited");
    }
  } catch (error) {
    setPill("is-error", "Could not reach the app");
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  send(input.value);
});
exampleButton?.addEventListener("click", () => send(exampleButton.textContent));
greetButton?.addEventListener("click", playGreeting);

// The installed app records through Reachy's onboard microphone. Browser speech
// recognition remains a development fallback when the robot backend is absent.
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = true;
  recognition.continuous = false;
  let listening = false;

  micButton.addEventListener("click", () => {
    if (supportsRobotListening) listenOnRobot();
    else if (listening) recognition.stop();
    else try { recognition.start(); } catch (_) { /* already starting */ }
  });
  recognition.onstart = () => {
    listening = true;
    micButton.classList.add("is-listening");
    input.placeholder = "Listening…";
  };
  recognition.onresult = (event) => {
    let transcript = "";
    for (const result of event.results) transcript += result[0].transcript;
    input.value = transcript;
  };
  recognition.onend = () => {
    listening = false;
    micButton.classList.remove("is-listening");
    input.placeholder = "Teach your robot something…";
    if (input.value.trim()) send(input.value);
  };
} else {
  micButton.addEventListener("click", listenOnRobot);
}

getStatus().catch(() => setPill("", "Starting app…"));
setInterval(() => getStatus().catch(() => {}), 400);
input.focus();
