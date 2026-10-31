# Current status

Updated: 31 October 2026.

**M001: Closed as a development pilot.** It includes ten assistant-checked
observations from five companies, five fixed queries, frozen pre-ranking labels,
BM25 and MiniLM runs, error analysis, and reproducible tests. A structured case
version separates cost pressure, reported measure, other drivers and response.
The latest follow-up compares both methods on the same candidates and records
five user-entered numeric grades. Those five grades have no reasons and do not
constitute a complete human benchmark.

**Current limitations:** episode boundaries, later outcomes and reuse rights
need further work. The ten cases are not ten human-reviewed cases; no independent
ranking evaluation or causal claim has been established. See
[evaluation/pilot/pilot-report.md](evaluation/pilot/pilot-report.md).

**Next build:** create a small evidence-based case search and comparison
experience, with visible source links, date/scope differences, missing evidence,
and an explicit insufficient-evidence result. Expand and validate case coverage
before claiming retrieval improvement. Builder proceeds autonomously; the user
need not grade or recheck routine work.

Use [README.md](README.md) for commands. The older multi-role workflow and
planning documents were removed from the working tree; Git history preserves
prior versions.
