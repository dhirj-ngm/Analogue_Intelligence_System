# Project working rules

Updated: 31 October 2026. D017 supersedes earlier multi-thread workflow gates.

## Two threads

- **Discussion:** understand the project, explore ideas, explain results and decide material changes with Dheeraj.
- **Builder:** complete an assigned module end to end: research, data, code, tests, self-review and concise records. Continue through internal tasks without handoff or permission gates.

Use one writer in a checkout. No separate Manager, Records, Domain or Reviewer thread is required. Do not spawn agents unless explicitly requested. Assistant self-review is not independent or human review.

## Read and maintain only what matters

Start with this file and STATUS.md. Read PROJECT_BRIEF.md and the active module specification when needed. DECISIONS.md records material choices only. Existing domain/research notes are reference material; dated handoffs are history, not active instructions. Do not create a handoff document for each task.

Builder owns STATUS.md and module progress. Keep status short: delivered results, actual checks, limitations and next work. Preserve historical work without requiring users to read it. Explicit user instructions override old gates.

## Deliver whole modules

Use Planned → In Progress → Delivered. Delivered means the stated implementation and checks are finished; record user acceptance separately and never invent it. Report unmet criteria explicitly. M001 is authorized through its final pilot report, including source selection, curation, evaluation and baseline implementation. Routine reversible choices belong to Builder.

Ask only for genuinely necessary missing information, material changes to product goals, paid services, credentials, destructive operations or permissions enforced by tools. Continue independent work while an answer is pending. No MCP is required if available tools suffice.

## Evidence and evaluation

Keep source URLs, locators, publication dates, reporting periods, units and review provenance. Separate management attribution, observation, forecast and analyst interpretation. Preserve unknowns. Never infer response effectiveness from chronology.

Do not count continuing reports as independent episodes. Exclude self/duplicate candidates and enforce public-information cutoffs. Exclude response/outcome information from baseline ranking text. Freeze queries, candidate eligibility and relevance labels before rankings. Compare methods on identical candidates; report errors and small-sample limitations.

Assistant-curated and assistant-reviewed pilot records may support development, but must never be labelled human-reviewed or an independently validated benchmark. Human feedback already recorded remains bounded to what was actually accepted. Check source access conditions; do not archive or redistribute full documents without a supported basis.

## Implementation

Use src/ for code, tests/ for meaningful deterministic tests, scripts/ for utilities, data/ for evidence and evaluation/ for experiments. Choose the smallest adequate implementation. Document setup, test, lint and run commands in README.md. Verify dates, eligibility, leakage, metrics and malformed inputs. Run relevant checks and report unrun checks honestly.

Preserve user changes. Keep environments, caches and secrets out of Git. Do not commit or publish unless requested. Finish with concrete results and limitations, not another thread assignment.
