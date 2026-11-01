// Presentation and form-state helpers. Source records and ranking are unchanged.
export function dateLabel(iso) {
  if (!iso) return "Date not known";
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric", month: "short", year: "numeric", timeZone: "UTC",
  }).format(new Date(`${iso}T00:00:00Z`));
}

export function periodLabel(period) {
  return `${dateLabel(period.start)} – ${dateLabel(period.end)}`;
}

export function words(items) {
  if (items.length < 2) return items[0] || "";
  return `${items.slice(0, -1).join(", ")} and ${items.at(-1)}`;
}

const DIFFERENCES = new Map([
  ["gross margin adjusted for restructuring; global scope", "This covers the whole company. Its gross margin leaves out restructuring charges."],
  ["profit amount includes restructuring; no margin level inferred", "This is a profit amount, including restructuring costs, rather than a margin percentage."],
  ["adjusted global margin increased despite cost pressure", "This covers the whole company. Its adjusted margin rose even though costs increased."],
  ["annual adjusted profit, not margin", "This is a full-year adjusted profit amount, rather than a margin percentage."],
  ["demand growth contrasts with lower-shipment cases", "The company described growing demand; this differs from reports of falling shipments."],
  ["multiple drivers, including pandemic shipment normalization", "Several things changed together, including pandemic-related changes in shipments."],
  ["global fiscal-year gross margin; product mix matters", "This covers a full financial year and the whole company. The mix of products sold also affected margin."],
  ["regional operating margin; exact interventions and effective dates unknown", "This covers Asia Pacific, rather than the whole company. The precise actions and when they took effect are unknown."],
  ["annual non-GAAP global operating margin", "This covers a full year and the whole company, using its underlying operating-margin measure."],
  ["disruption is different from cost inflation; margin rose overall", "This is a disruption to shipments, rather than rising input costs. Margin rose overall."],
]);

export function differenceLabel(text) {
  return DIFFERENCES.get(text) || text;
}

const PRESSURES = new Map([
  ["raw and packaging material costs increased", "The company reported higher costs for materials and packaging."],
  ["resin, energy, distribution and fiber costs increased", "The company reported higher costs for resin, energy, distribution and fibre."],
  ["raw and packaging material costs rose, including foreign exchange transaction costs", "Materials and packaging cost more, including costs tied to currency transactions."],
  ["higher input costs of USD 795 million were reported", "The company reported US$795 million in higher input costs."],
  ["no input-cost pressure is established for the global challenge in this record", "This record does not establish rising input costs as the problem for the company as a whole."],
  ["commodity, manufacturing and logistics costs rose", "The company reported higher commodity, manufacturing and logistics costs."],
  ["commodity and transportation costs increased", "The company reported higher commodity and transport costs."],
  ["materials and packaging costs increased; logistics costs also rose", "The company said materials and packaging cost more. Logistics costs also rose."],
  ["net material inflation and production/logistics costs increased", "The company reported higher net material costs, along with higher production and logistics costs."],
  ["a cyberattack disrupted shipments; no input-cost inflation mechanism established here", "A cyberattack disrupted shipments. This record does not establish rising input costs as the problem."],
]);

export function pressureLabel(text) {
  return PRESSURES.get(text) || text;
}

export function reportLocator(text) {
  // The reader needs a section in the issuer's report, not a local developer path.
  return text.replace(/; detailed evidence in data\/episodes\.jsonl$/, "");
}

const UNKNOWNS = new Map([
  ["true episode start/end", "When the problem really began and ended."],
  ["isolated effect of response", "How much any one action changed the result."],
  ["later realized outcome", "What happened after the period shown."],
  ["Action-level rationale and later outcomes are not established in these case records.", "Why the company chose each action."],
]);

export function unknownLabels(items) {
  return [...new Set(items.map((item) => UNKNOWNS.get(item) || item))];
}

export function metricFacts(metric) {
  const amount = metric.unit === "percent" ? `${metric.value}%` : `${metric.value} ${metric.unit}`;
  return [
    ["Measure", metric.name],
    ["Number reported", amount],
    ["Part of the business", metric.scope === "consolidated" ? "The whole company" : metric.scope],
    ["Company's calculation", metric.basis],
    ["Compared with", metric.comparison],
  ];
}

export const EXCLUSION_LABELS = {
  self: "The case you started from",
  duplicate_or_continuation: "Another copy or continuing report of the same situation",
  unknown_publication_date: "Report date not known",
  unknown_challenge_date: "Date of the supporting information not known",
  after_cutoff: "Report published after your information date",
  challenge_evidence_after_cutoff: "Supporting information published after your information date",
  not_earlier_observation: "Period does not end before the situation you are comparing",
};

export class SearchDraft {
  constructor(today) {
    this.today = today;
    this.saved = null;
    this.source = "";
  }

  select(current, chosen) {
    if (chosen) {
      if (!this.source) this.saved = { ...current, source_id: "" };
      this.source = chosen.id;
      return { text: chosen.challenge, cutoff: chosen.published, before_period_end: chosen.period_end, source_id: chosen.id };
    }
    this.source = "";
    const restored = this.saved || { ...current, source_id: "" };
    this.saved = null;
    return { ...restored };
  }

  resetDates(current) {
    return { ...this.select(current, null), cutoff: this.today, before_period_end: this.today };
  }
}

export function changeInformationDate(current, previousDate) {
  if (!current.source_id && current.before_period_end === previousDate) {
    return { ...current, before_period_end: current.cutoff };
  }
  return { ...current };
}
