# M005 browser timing finding

The fault was in the coordinate-click check, rather than the app's request
lifecycle. The original full flow passed once. A diagnostic run repeated blocked
searches and retries with 250ms network latency and captured trusted mouse/form
events. On trial 5 (the sixth cycle), retry mouse-down, mouse-up and click targeted
`search-scope`, the nearby status paragraph. No new `submit` followed. The old
helper saw `aria-busy=false` from the failed request and returned immediately;
the error was still visible and there were zero case cards.

Error recovery focuses the description, which starts smooth scrolling. Clearing
comparison can also queue a focus scroll. Either can override the check's initial
`scrollIntoView` on a later frame, moving its previously measured coordinates.
The first attempted stable-target fix caught another off-screen target; the final
helper brings it back into view after any queued focus scroll, requires three
stable animation-frame positions and a successful hit test, dispatches real mouse
events, and verifies the trusted click. Search completion additionally requires a
fresh form submission. It never retries a missed click silently or treats an old
idle flag as a new request. No fixed sleep was added to make assertions pass.

The full flow passed after this fix before search changes, with three
failure/retry cycles on each screen size. The final app also passed the full flow
at desktop 1280px and phone 375px with 20 cycles each (40 total), using 150ms
network latency during recovery. Each cycle asserts the preserved description,
visible connection failure, empty cards, a new retry submission, hidden error and
new results. The complete run reports 20 grouped browser checks, including case
sources, dates, self exclusion, related terms, negation, insufficient evidence,
comparison and recovery. Screenshots were inspected on both screen sizes.

Reproduce with installed Chrome/Chromium and Node 22+:

```sh
make browser-test
node scripts/check_app_browser.mjs --retry-rounds=20
```

Both commands start/stop their own local Python server and browser. Local-socket
access is needed. Screenshots are temporary files under `/tmp/ais-*.png`. The
initial new Python test helper also failed on a duplicate cutoff keyword; its
merge order was corrected. Final results: 46 Python tests and 8 JavaScript tests
passed, along with Ruff, syntax, pilot/collection validation and paired evaluation.
No remaining check failures or skipped required checks; no external model run.
