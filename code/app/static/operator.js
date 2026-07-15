const $ = (id) => document.getElementById(id);
const text = (id, value) => { $(id).textContent = value; };
const safe = (value, fallback = "—") => value === null || value === undefined || value === "" ? fallback : String(value);

function checkRow(check) {
  const row = document.createElement("div"); row.className = "check-row";
  const main = document.createElement("div"); main.className = "check-main";
  const dot = document.createElement("span"); dot.className = `check-dot ${check.status === "degraded" ? "degraded" : check.status === "fail" ? "fail" : ""}`;
  const copy = document.createElement("div");
  const id = document.createElement("div"); id.className = "check-id"; id.textContent = safe(check.id);
  const observed = document.createElement("div"); observed.className = "check-observed"; observed.textContent = safe(check.observed);
  copy.append(id, observed); main.append(dot, copy); row.append(main);
  const state = document.createElement("span"); state.className = `check-state ${check.status === "degraded" ? "degraded" : ""}`; state.textContent = safe(check.status, "unknown"); row.append(state); return row;
}
function activityRow(event) { const row = document.createElement("div"); row.className = "activity-item"; const dot = document.createElement("span"); dot.className = "activity-marker"; const copy = document.createElement("div"); const title = document.createElement("strong"); title.textContent = safe(event.type || event.kind, "system event"); const detail = document.createElement("p"); detail.textContent = safe(event.summary || event.detail || event.timestamp, "recorded locally"); copy.append(title, detail); row.append(dot, copy); return row; }
async function get(path) { const response = await fetch(path, { cache: "no-store" }); if (!response.ok) throw new Error(`${path} ${response.status}`); return response.json(); }
async function refresh() {
  try {
    const [doctor, brain, activity, maintenance] = await Promise.all([get("/api/doctor"), get("/api/brain"), get("/api/activity"), get("/api/maintenance")]);
    const checks = Array.isArray(doctor.checks) ? doctor.checks : []; const counts = brain.counts || {}; const events = Array.isArray(activity.events) ? activity.events : [];
    text("state", safe(doctor.state, "UNKNOWN")); $("mode-badge").className = `mode-badge ${doctor.state === "READY" ? "ready" : ""}`;
    const degraded = String(doctor.state).toUpperCase() !== "READY"; text("alert-title", degraded ? "MiOS is running in a limited mode" : "MiOS is ready"); text("alert-copy", degraded ? "The local software is healthy, but robot hardware is not connected. No physical motion will be attempted." : "All required runtime and safety checks are passing.");
    text("metric-health", `${checks.filter(c => c.status === "pass").length}/${checks.length}`); text("metric-health-detail", degraded ? "one or more limited" : "all checks passing"); text("metric-concepts", safe(counts.entities ?? counts.concepts, 0)); text("metric-episodes", safe(counts.episodes, 0)); text("metric-events", events.length); text("brain-total", `${safe(counts.entities ?? counts.concepts, 0)} + ${safe(counts.claims, 0)}`); text("checks-status", degraded ? "DEGRADED" : "HEALTHY");
    $("checks").replaceChildren(...checks.map(checkRow));
    const breakdown = [["Episodes", counts.episodes], ["Entities", counts.entities ?? counts.concepts], ["Claims", counts.claims], ["Skills", counts.skills]]; $("brain-breakdown").replaceChildren(...breakdown.map(([label, value]) => { const el = document.createElement("div"); el.className = "brain-stat"; const strong = document.createElement("strong"); strong.textContent = safe(value, "0"); const span = document.createElement("span"); span.textContent = label; el.append(strong, span); return el; }));
    const concepts = Array.isArray(brain.concepts) ? brain.concepts : []; $("concepts").replaceChildren(...concepts.slice(0, 8).map((concept) => { const chip = document.createElement("span"); chip.className = "concept-chip"; chip.textContent = safe(concept.label || concept.digest || concept); return chip; }));
    $("activity-list").replaceChildren(...(events.length ? events.slice(0, 8).map(activityRow) : [Object.assign(document.createElement("p"), { className: "empty", textContent: "No events recorded in the current window." })]));
    text("maintenance-status", maintenance.maintenance_supported ? "AVAILABLE" : "NOT ENABLED"); text("maintenance-copy", maintenance.maintenance_supported ? "Maintenance controls are available to an authorized operator." : "The development server is read-only; maintenance controls are intentionally disabled."); text("updated", `Updated ${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`);
  } catch (error) { text("state", "OFFLINE"); text("alert-title", "MiOS console cannot reach the runtime"); text("alert-copy", "The local service may be stopped. Check the development server and refresh."); text("updated", "Connection failed"); console.error(error); }
}
$("refresh").addEventListener("click", refresh); refresh(); setInterval(refresh, 5000);
