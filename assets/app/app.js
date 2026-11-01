"use strict";

import {
  dateLabel, periodLabel, words, differenceLabel, pressureLabel, reportLocator, unknownLabels, metricFacts,
  EXCLUSION_LABELS, SearchDraft, changeInformationDate,
} from "/reader.mjs";

const $ = (id) => document.getElementById(id);
const selected = new Set();
const fieldIds = { text: "situation", cutoff: "cutoff", before_period_end: "before-period", source_id: "source-case" };
let catalog = [];
let currentResults = [];
let activeRequest = 0;
let draft;
let previousDate;

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
}

function values() {
  return Object.fromEntries(new FormData($("search-form")));
}

function applyValues(next) {
  for (const [field, id] of Object.entries(fieldIds)) {
    if (field in next) $(id).value = next[field] || "";
  }
  previousDate = $("cutoff").value;
  updateScope();
}

function updateScope() {
  const source = catalog.find((c) => c.id === $("source-case").value);
  $("search-scope").textContent = source
    ? `Starting from ${source.company}. That case and its continuing reports will be left out.`
    : $("cutoff").value ? `Using reports published by ${dateLabel($("cutoff").value)}. Change dates above if you need to look back.`
      : "Choose an information date in the options above.";
}

function sourceLink(evidence, label = "Read the company report ↗") {
  const link = node("a", label, "source-link");
  link.href = evidence.url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  const wrap = node("div", undefined, "source-reference");
  const location = node("details", undefined, "source-location");
  location.append(node("summary", "Where to look in the report"), node("p", reportLocator(evidence.locator)));
  if (evidence.public_date) location.append(node("p", `Published ${dateLabel(evidence.public_date)}`));
  wrap.append(link, location);
  return wrap;
}

function fieldBlock(title, field) {
  const block = node("div", undefined, "detail-block");
  block.append(node("h4", title), node("p", pressureLabel(field.value)));
  if (field.evidence) block.append(sourceLink(field.evidence));
  return block;
}

function bulletList(items) {
  const list = node("ul");
  items.forEach((item) => list.append(node("li", item)));
  return list;
}

function metricDetails(c) {
  const details = node("details", undefined, "metric-details");
  details.append(node("summary", "What this number measures"));
  const facts = node("dl");
  metricFacts(c.metric).forEach(([label, value]) => facts.append(node("dt", label), node("dd", value)));
  details.append(facts, node("p", "A margin is profit as a share of sales. A profit amount and a margin percentage measure different things. For margins, 100 basis points means one percentage point. Adjusted figures leave out some items; check the company's definition.", "field-help"));
  return details;
}

function updateSelection() {
  $("selection-bar").hidden = !currentResults.length;
  $("selection-bar").classList.toggle("has-selection", selected.size > 0);
  $("selection-help").textContent = selected.size === 0 ? "Choose two or three cases to see them together."
    : selected.size === 1 ? "One case chosen. Choose one more to compare."
      : `${selected.size} cases chosen. Ready to compare.`;
  $("compare-button").textContent = selected.size < 2 ? "Compare cases" : `Compare ${selected.size} cases`;
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
  title.append(node("p", `CASE ${index + 1}`, "case-kicker"), node("h3", c.company),
    node("p", `Period covered: ${periodLabel(c.period)}`, "date-line"));
  const label = node("label", undefined, "compare-label");
  const input = node("input");
  input.type = "checkbox";
  input.value = c.id;
  input.className = "compare-check";
  input.setAttribute("aria-label", `Choose ${c.company}, ${periodLabel(c.period)}, for comparison`);
  input.addEventListener("change", () => {
    if (input.checked && selected.size < 3) selected.add(c.id);
    else selected.delete(c.id);
    updateSelection();
  });
  label.append(input, node("span", "Choose"));
  heading.append(title, label);
  const differences = node("div", undefined, "differences");
  differences.append(node("strong", "WHAT MAKES THIS DIFFERENT"), node("p", differenceLabel(c.important_differences[0])));
  main.append(heading, node("p", `In common: both descriptions mention ${words(c.matching_pressure_terms)}.`, "pressure-match"),
    node("p", pressureLabel(c.fields.pressure.value), "pressure"), differences);
  const details = node("details", undefined, "case-reading");
  details.append(node("summary", "Read the case and its sources"));
  const body = node("div", undefined, "case-detail");
  body.append(node("p", `From a company report published ${dateLabel(c.published)}. These summaries describe what the company reported; they are not independent proof of what caused the result.`, "field-help"),
    fieldBlock("What was happening", c.fields.pressure),
    fieldBlock("What the company reported about profit", c.fields.margin_or_profit), metricDetails(c),
    fieldBlock("What else was changing", c.fields.other_drivers),
    fieldBlock("What the company said it did", c.fields.response),
    node("p", "A reported action does not show how much it helped, or whether it would help in your situation.", "visible-caution"));
  const limits = node("div", undefined, "detail-block");
  limits.append(node("h4", "Why the comparison may fall short"), bulletList(c.important_differences.map(differenceLabel)));
  const unknowns = node("div", undefined, "detail-block");
  unknowns.append(node("h4", "What we don't know"), bulletList(unknownLabels(c.unknowns)));
  const evidence = node("div", undefined, "detail-block");
  evidence.append(node("h4", "Check the original report"));
  if (c.source.excerpt) evidence.append(node("p", "A short excerpt, in the report's own words:", "field-help"), node("blockquote", c.source.excerpt, "source-quote"));
  else evidence.append(node("p", "We haven't included an exact quote for this case. Follow the link and use the section name to find the evidence.", "field-help"));
  evidence.append(sourceLink(c.source));
  body.append(limits, unknowns, evidence);
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
  header.append(node("th", "What to compare"));
  cases.forEach((c) => {
    const th = node("th"); th.scope = "col";
    th.append(node("span", c.company), node("small", periodLabel(c.period)));
    header.append(th);
  });
  head.append(header);
  const body = node("tbody");
  const rows = [
    ["What was happening", (c) => fieldBlock("From the company report", c.fields.pressure)],
    ["What was reported about profit", (c) => { const block = fieldBlock("Reported figure", c.fields.margin_or_profit); block.append(metricDetails(c)); return block; }],
    ["What else was changing", (c) => fieldBlock("From the company report", c.fields.other_drivers)],
    ["Why the comparison may fall short", (c) => bulletList(c.important_differences.map(differenceLabel))],
    ["What the company said it did", (c) => fieldBlock("Reported action", c.fields.response)],
    ["What we don't know", (c) => bulletList(unknownLabels(c.unknowns))],
    ["When this happened", (c) => `Period covered: ${periodLabel(c.period)}. Report published ${dateLabel(c.published)}.`],
    ["Read the evidence", (c) => sourceLink(c.source)],
  ];
  rows.forEach(([title, value]) => {
    const row = node("tr"); row.setAttribute("role", "row");
    const th = node("th", title); th.scope = "row"; th.setAttribute("role", "rowheader"); row.append(th);
    cases.forEach((c) => {
      const td = node("td"); td.setAttribute("role", "cell");
      const mobileLabel = node("span", `${c.company} · ${dateLabel(c.period.end)}`, "compare-case-label");
      mobileLabel.setAttribute("aria-hidden", "true");
      const result = value(c);
      td.append(mobileLabel, typeof result === "string" ? document.createTextNode(result) : result);
      row.append(td);
    });
    body.append(row);
  });
  table.append(head, body);
  $("comparison").hidden = false;
}

function renderChecks(data) {
  const checks = $("method-checks");
  const reasons = Object.entries(data.excluded).map(([reason, count]) => `${EXCLUSION_LABELS[reason] || reason}: ${count}`);
  checks.replaceChildren(node("p", `${data.eligible_count} cases passed the date and duplicate checks. Reports must be public by ${dateLabel(data.query.cutoff)}, and periods must end before ${dateLabel(data.query.before_period_end)}.`),
    bulletList(reasons.length ? reasons : ["No cases were removed by those checks."]));
  if (data.results.length) {
    checks.append(node("h4", "Keyword scores · BM25"), bulletList(data.results.map((c) => `${c.company} (${c.id}): ${c.score.toFixed(3)}. ${c.review_status.replaceAll("_", " ")}.`)));
    checks.append(node("h4", "Words not found in each matching pressure description"), bulletList(data.results.map((c) => `${c.company}: ${c.unmatched_terms.join(", ") || "none"}. Different wording does not prove the situations are incompatible.`)));
  }
}

function renderResults(data) {
  currentResults = data.results;
  selected.clear();
  $("comparison").hidden = true;
  $("results").replaceChildren(...data.results.map(renderCard));
  updateSelection();
  $("results-title").textContent = data.results.length ? `${data.results.length} cases to explore` : "No comparison to show yet";
  $("results-status").textContent = data.message;
  $("results-status").classList.toggle("empty", data.status === "insufficient_evidence");
  $("result-caution").hidden = !data.results.length;
  $("empty-actions").hidden = Boolean(data.results.length);
  $("try-example").hidden = data.empty_reason === "no_eligible_cases";
  $("edit-search").hidden = false;
  renderChecks(data);
  $("results-title").focus({ preventScroll: true });
  $("results-section").scrollIntoView({ block: "start", behavior: "instant" });
}

function clearError() {
  $("error").hidden = true;
  $("reload").hidden = true;
  Object.values(fieldIds).forEach((id) => {
    $(id).removeAttribute("aria-invalid");
    const described = $(id).getAttribute("aria-describedby") || "";
    $(id).setAttribute("aria-describedby", described.replace(/\s*error-message/g, "").trim());
  });
}

function showError(message, field, reload = false) {
  $("error-message").textContent = message;
  $("error").hidden = false;
  $("reload").hidden = !reload;
  const input = $(fieldIds[field] || "situation");
  if (input.closest("#search-options")) $("search-options").open = true;
  input.setAttribute("aria-invalid", "true");
  input.setAttribute("aria-describedby", `${input.getAttribute("aria-describedby") || ""} error-message`.trim());
  input.focus();
}

$("search-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const request = ++activeRequest;
  clearError();
  $("search-button").disabled = true;
  $("search-button").textContent = "Finding cases…";
  $("results-section").setAttribute("aria-busy", "true");
  currentResults = [];
  selected.clear();
  $("results").replaceChildren();
  $("comparison").hidden = true;
  $("empty-actions").hidden = true;
  $("result-caution").hidden = true;
  $("results-status").classList.remove("empty");
  $("results-status").textContent = "Looking through the company reports…";
  $("method-checks").replaceChildren(node("p", "This search is still running."));
  updateSelection();
  try {
    const response = await fetch("/api/search", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(values()) });
    const data = await response.json();
    if (request !== activeRequest) return;
    if (!response.ok) {
      showError(data.error || "We couldn't run that search. Please try again.", data.field);
      $("results-status").textContent = "Check the message in the search box, then try again.";
      $("method-checks").replaceChildren(node("p", "This search did not complete."));
      return;
    }
    renderResults(data);
  } catch {
    if (request !== activeRequest) return;
    showError("We couldn't reach the case collection. Check that the app is running, then try again.", "text");
    $("results-status").textContent = "The search did not finish. Your description is still in the search box.";
    $("method-checks").replaceChildren(node("p", "This search did not complete."));
  } finally {
    if (request === activeRequest) {
      $("search-button").disabled = false;
      $("search-button").textContent = "Find cases ↗";
      $("results-section").setAttribute("aria-busy", "false");
    }
  }
});

function runExample(text) {
  applyValues({ ...draft.select(values(), null), text, source_id: "" });
  $("search-form").requestSubmit();
}

document.querySelectorAll("[data-example]").forEach((button) => button.addEventListener("click", () => runExample(button.dataset.example)));
$("try-example").addEventListener("click", () => runExample(document.querySelector("[data-example]").dataset.example));
$("source-case").addEventListener("change", () => applyValues(draft.select(values(), catalog.find((c) => c.id === $("source-case").value))));
$("cutoff").addEventListener("change", () => applyValues(changeInformationDate(values(), previousDate)));
$("reset-dates").addEventListener("click", () => { clearError(); applyValues(draft.resetDates(values())); });
$("edit-search").addEventListener("click", () => $("situation").focus());
$("change-dates").addEventListener("click", () => { $("search-options").open = true; $("cutoff").focus(); });
$("compare-button").addEventListener("click", () => {
  renderComparison();
  $("comparison-title").focus({ preventScroll: true });
  $("comparison").scrollIntoView({ block: "start", behavior: "instant" });
});
$("clear-comparison").addEventListener("click", () => { selected.clear(); updateSelection(); (document.querySelector(".compare-check") || $("situation")).focus(); });
$("reload").addEventListener("click", () => window.location.reload());

async function initialize() {
  try {
    const response = await fetch("/api/catalog");
    if (!response.ok) throw new Error("collection unavailable");
    const data = await response.json();
    catalog = data.cases;
    draft = new SearchDraft(data.default_date);
    $("corpus-count").textContent = `${data.total} short cases · ${data.companies} companies`;
    applyValues({ cutoff: data.default_date, before_period_end: data.default_date });
    catalog.forEach((c) => {
      const option = node("option", `${c.company} · period ending ${dateLabel(c.period_end)}`);
      option.value = c.id; $("source-case").append(option);
    });
    $("search-button").disabled = false;
    $("reset-dates").disabled = false;
    document.querySelectorAll("[data-example]").forEach((button) => { button.disabled = false; });
  } catch {
    showError("We couldn't load the cases. Check that the app is running, then reload the page.", "text", true);
    $("search-scope").textContent = "The case collection is not available yet.";
  }
}
initialize();
