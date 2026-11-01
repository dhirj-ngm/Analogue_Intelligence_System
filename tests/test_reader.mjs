import test from "node:test";
import assert from "node:assert/strict";
import { SearchDraft, changeInformationDate, dateLabel, metricFacts, pressureLabel, reportLocator, unknownLabels } from "../assets/app/reader.mjs";

const own = { text: "My packaging problem", cutoff: "2023-03-01", before_period_end: "2022-10-01", source_id: "" };
const colgate = { id: "CL-2022", challenge: "Source challenge", published: "2023-01-27", period_end: "2022-12-31" };
const earlier = { id: "CL-2008", challenge: "Earlier challenge", published: "2008-10-30", period_end: "2008-09-30" };

test("switching between starting cases restores the reader's own description and dates", () => {
  const state = new SearchDraft("2026-11-01");
  const first = state.select(own, colgate);
  assert.equal(first.text, colgate.challenge);
  assert.equal(first.cutoff, colgate.published);
  assert.equal(first.before_period_end, colgate.period_end);
  const second = state.select(first, earlier);
  second.text = "An edit to a source case";
  assert.deepEqual(state.select(second, null), own);
  assert.equal(own.text, "My packaging problem");
});

test("a linked end date follows the information date, while an explicit or source-case end is kept", () => {
  assert.equal(changeInformationDate({ ...own, cutoff: "2020-01-01", before_period_end: "2023-03-01" }, "2023-03-01").before_period_end, "2020-01-01");
  assert.equal(changeInformationDate({ ...own, cutoff: "2020-01-01" }, own.cutoff).before_period_end, own.before_period_end);
  assert.equal(changeInformationDate({ ...own, source_id: "CL-2022", cutoff: "2020-01-01", before_period_end: own.cutoff }, own.cutoff).before_period_end, own.cutoff);
});

test("resetting dates leaves source mode and restores the reader's own text", () => {
  const state = new SearchDraft("2026-11-01");
  const chosen = state.select(own, colgate);
  assert.deepEqual(state.resetDates(chosen), { ...own, cutoff: "2026-11-01", before_period_end: "2026-11-01" });
});

test("date labels stay on the source day across time zones and unknown dates stay unknown", () => {
  const oldZone = process.env.TZ;
  try {
    process.env.TZ = "Pacific/Honolulu";
    assert.equal(dateLabel("2023-01-01"), "1 Jan 2023");
    assert.equal(dateLabel(null), "Date not known");
  } finally {
    if (oldZone === undefined) delete process.env.TZ;
    else process.env.TZ = oldZone;
  }
});

test("reader labels preserve metric units, accounting definition and uncertainty", () => {
  const metric = { name: "gross margin", value: 26, unit: "percent", scope: "consolidated", basis: "excluding restructuring charges", comparison: "same period prior year" };
  const facts = metricFacts(metric);
  assert.deepEqual(facts[1], ["Number reported", "26%"]);
  assert.equal(facts[3][1], metric.basis);
  assert.equal(facts[4][1], metric.comparison);
  assert.equal(metricFacts({ ...metric, value: 662, unit: "USD million" })[1][1], "662 USD million");
  assert.equal(unknownLabels(["isolated effect of response"])[0], "How much any one action changed the result.");
  assert.deepEqual(unknownLabels(["A new unresolved question"]), ["A new unresolved question"]);
});

test("pressure summaries keep reported amounts, negation and unknown wording", () => {
  assert.match(pressureLabel("higher input costs of USD 795 million were reported"), /US\$795 million/);
  assert.match(pressureLabel("a cyberattack disrupted shipments; no input-cost inflation mechanism established here"), /does not establish/);
  assert.equal(pressureLabel("Unresolved pressure from a new source"), "Unresolved pressure from a new source");
  assert.equal(reportLocator("Asia Pacific commentary; detailed evidence in data/episodes.jsonl"), "Asia Pacific commentary");
});
