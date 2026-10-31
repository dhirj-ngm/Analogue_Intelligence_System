"use strict";

const $ = (id) => document.getElementById(id);
const selected = new Set();
let catalog = [];
let currentResults = [];
let activeRequest = 0;

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
}

function sourceLink(evidence, label = "Open source ↗") {
  const link = node("a", label, "source-link");
  link.href = evidence.url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  const wrap = node("div");
  wrap.append(link, node("span", evidence.locator, "evidence-locator"));
  return wrap;
}

function fieldBlock(title, field) {
  const block = node("div", undefined, "detail-block");
  block.append(node("h4", title), node("p", field.value));
  if (field.evidence) {
    block.append(sourceLink(field.evidence));
    block.append(node("span", `Published ${field.evidence.public_date} · ${field.kind.replaceAll("_", " ")}`, "evidence-locator"));
  }
  return block;
}

function bulletList(items) {
  const list = node("ul");
  items.forEach((item) => list.append(node("li", item)));
  return list;
}

function metricText(c) {
  const m = c.metric;
  return `${m.name}: ${m.value} ${m.unit}. Scope: ${m.scope}. Basis: ${m.basis}. Comparison: ${m.comparison}.`;
}

function updateSelection() {
  $("compare-button").textContent = `Compare selected (${selected.size}/3)`;
  $("compare-button").disabled = selected.size < 2;
  document.querySelectorAll(".compare-check").forEach((input) => {
    input.checked = selected.has(input.value);
    input.disabled = selected.size >= 3 && !input.checked;
  });
  if (selected.size < 2) $("comparison").hidden = true;
  else if (!$("comparison").hidden) renderComparison();
}

function renderCard(c, index) {
  const card = node("article", undefined, "case-card");
  card.dataset.caseId = c.id;
  const main = node("div", undefined, "card-main");
  const heading = node("div", undefined, "card-heading");
  const title = node("div");
  title.append(node("p", `CANDIDATE ${String(index + 1).padStart(2, "0")} · ${c.id}`, "case-kicker"), node("h3", c.company),
    node("p", `${c.period.start} – ${c.period.end}`, "date-line"), node("p", `Published ${c.published}`, "date-line"));
  const label = node("label", undefined, "compare-label");
  const input = node("input");
  input.type = "checkbox";
  input.value = c.id;
  input.className = "compare-check";
  input.setAttribute("aria-label", `Compare ${c.company} ${c.id}`);
  input.addEventListener("change", () => {
    if (input.checked && selected.size < 3) selected.add(c.id);
    else selected.delete(c.id);
    updateSelection();
  });
  label.append(input, node("span", "Compare"));
  heading.append(title, label);
  const differences = node("div", undefined, "differences");
  differences.append(node("strong", "IMPORTANT DIFFERENCE"), node("p", c.important_differences[0]));
  main.append(heading, node("span", `Pressure terms: ${c.matching_pressure_terms.join(", ")}`, "pressure-match"),
    node("p", c.fields.pressure.value, "pressure"), differences);
  const details = node("details");
  details.append(node("summary", "Inspect evidence, response & unknowns"));
  const body = node("div", undefined, "case-detail");
  body.append(fieldBlock("Matching pressure · issuer disclosure", c.fields.pressure),
    fieldBlock("Reported measure", c.fields.margin_or_profit),
    node("p", metricText(c), "evidence-locator"),
    fieldBlock("Other reported drivers", c.fields.other_drivers),
    fieldBlock("Reported response · excluded from ranking", c.fields.response));
  const limits = node("div", undefined, "detail-block");
  limits.append(node("h4", "Important differences"), bulletList(c.important_differences));
  const unknowns = node("div", undefined, "detail-block");
  unknowns.append(node("h4", "Unknowns and limits"), bulletList(c.unknowns));
  const evidence = node("div", undefined, "detail-block");
  evidence.append(node("h4", "Evidence excerpt · source wording"));
  if (c.source.excerpt) evidence.append(node("blockquote", c.source.excerpt, "source-quote"));
  else evidence.append(node("p", "A verbatim excerpt is not included in this pilot record. Open the source at the locator below.", "evidence-locator"));
  evidence.append(sourceLink(c.source));
  if (c.unmatched_terms.length) {
    evidence.append(node("p", `Not matched in pressure text: ${c.unmatched_terms.join(", ")}. This is a wording gap, not proof of incompatibility.`, "evidence-locator"));
  }
  body.append(limits, unknowns, evidence,
    node("p", `BM25 score ${c.score.toFixed(3)} · uncalibrated keyword score. ${c.review_status.replaceAll("_", " ")}.`, "review-note"));
  details.append(body);
  card.append(main, details);
  return card;
}

function renderComparison() {
  const cases = currentResults.filter((c) => selected.has(c.id));
  const table = $("comparison-table");
  table.replaceChildren();
  const head = node("thead");
  const header = node("tr");
  header.append(node("th", "Comparison dimension"));
  cases.forEach((c) => { const th = node("th", `${c.company} · ${c.id}`); th.scope = "col"; header.append(th); });
  head.append(header);
  const body = node("tbody");
  const rows = [
    ["Publication date", (c) => c.published],
    ["Reporting period", (c) => `${c.period.start} – ${c.period.end}`],
    ["Pressure / source", (c) => fieldBlock("Issuer disclosure", c.fields.pressure)],
    ["Reported measure", (c) => metricText(c)],
    ["Other drivers / source", (c) => fieldBlock("Issuer disclosure", c.fields.other_drivers)],
    ["Important differences", (c) => bulletList(c.important_differences)],
    ["Reported response / source", (c) => fieldBlock("Not used to rank", c.fields.response)],
    ["Unknowns", (c) => bulletList(c.unknowns)],
    ["Source", (c) => sourceLink(c.source)],
  ];
  rows.forEach(([title, value]) => {
    const row = node("tr");
    const th = node("th", title); th.scope = "row"; row.append(th);
    cases.forEach((c) => { const td = node("td"); const result = value(c); td.append(typeof result === "string" ? document.createTextNode(result) : result); row.append(td); });
    body.append(row);
  });
  table.append(head, body);
  $("comparison").hidden = false;
}

function renderResults(data) {
  currentResults = data.results;
  selected.clear();
  $("comparison").hidden = true;
  updateSelection();
  $("results").replaceChildren(...data.results.map(renderCard));
  $("results-status").textContent = `${data.message} ${data.results.length} shown · ${data.eligible_count} eligible observations.`;
  $("results-status").classList.toggle("empty", data.status === "insufficient_evidence");
  $("method-note").textContent = data.method;
  $("method-note").hidden = false;
  const audit = $("eligibility-content");
  const reasons = Object.entries(data.excluded).map(([reason, count]) => `${reason.replaceAll("_", " ")}: ${count}`);
  audit.replaceChildren(node("p", `Publication cutoff: ${data.query.cutoff}. Reporting periods must end before ${data.query.before_period_end}.`),
    bulletList(reasons.length ? reasons : ["No cases excluded by dates or known duplicate groups."]));
  $("eligibility").hidden = false;
}

$("search-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const request = ++activeRequest;
  $("error").hidden = true;
  $("search-button").disabled = true;
  $("search-button").textContent = "Searching…";
  $("results-section").setAttribute("aria-busy", "true");
  // Clear prior results/selection so a failed request cannot leave stale comparisons.
  currentResults = [];
  selected.clear();
  $("results").replaceChildren();
  $("comparison").hidden = true;
  $("eligibility").hidden = true;
  $("method-note").hidden = true;
  $("results-status").textContent = "Checking dates and searching the case collection…";
  updateSelection();
  try {
    const payload = Object.fromEntries(new FormData($("search-form")));
    const response = await fetch("/api/search", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const data = await response.json();
    if (request !== activeRequest) return;
    if (!response.ok) throw new Error(data.error || "Search failed. Try again.");
    renderResults(data);
  } catch (error) {
    if (request !== activeRequest) return;
    $("error").textContent = error.message;
    $("error").hidden = false;
    $("results-status").textContent = "Search could not be completed. Check the message above and try again.";
  } finally {
    if (request === activeRequest) {
      $("search-button").disabled = false;
      $("search-button").textContent = "Find historical cases ↗";
      $("results-section").setAttribute("aria-busy", "false");
    }
  }
});

document.querySelectorAll("[data-example]").forEach((button) => button.addEventListener("click", () => {
  $("source-case").value = "";
  $("situation").value = button.dataset.example;
  $("situation").focus();
}));
$("source-case").addEventListener("change", () => {
  const chosen = catalog.find((c) => c.id === $("source-case").value);
  if (chosen) {
    $("situation").value = chosen.challenge;
    $("cutoff").value = chosen.published;
    $("before-period").value = chosen.period_end;
  }
});
$("compare-button").addEventListener("click", () => { renderComparison(); $("comparison").scrollIntoView({ block: "start" }); });
$("clear-comparison").addEventListener("click", () => {
  selected.clear(); updateSelection();
  (document.querySelector(".compare-check") || $("situation")).focus();
});

async function initialize() {
  try {
    const response = await fetch("/api/catalog");
    if (!response.ok) throw new Error("The local case collection could not be loaded. Refresh to retry.");
    const data = await response.json();
    catalog = data.cases;
    $("corpus-count").textContent = `${data.total} observations · ${data.companies} companies`;
    $("cutoff").value = data.default_date;
    $("before-period").value = data.default_date;
    catalog.forEach((c) => { const option = node("option", `${c.company} · ${c.id}`); option.value = c.id; $("source-case").append(option); });
    $("search-button").disabled = false;
  } catch (error) {
    $("error").textContent = error.message;
    $("error").hidden = false;
  }
}
initialize();
