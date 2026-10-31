// Optional, dependency-free browser smoke check: Node 22+ and a local Chrome/Chromium.
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdtemp, readFile, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const profile = await mkdtemp(join(tmpdir(), "ais-browser-"));
const delay = (ms) => new Promise((r) => setTimeout(r, ms));
const python = spawn(process.env.APP_PYTHON || "python3", ["-c",
  "from ais.app import create_server; s=create_server(0); print(s.server_port,flush=True); s.serve_forever()"],
{ cwd: root, env: { ...process.env, PYTHONPATH: join(root, "src") }, stdio: ["ignore", "pipe", "inherit"] });
let chrome;
let ws;
const checks = [];

async function waitFor(fn, label, timeout = 10000) {
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    if (await fn()) return;
    await delay(100);
  }
  throw new Error(`Timed out: ${label}`);
}

try {
  let port = "";
  python.stdout.on("data", (data) => { port += data.toString(); });
  await waitFor(() => /^\d+\n/.test(port), "local server startup");
  const url = `http://127.0.0.1:${Number(port.trim())}`;
  chrome = spawn(process.env.CHROME_BIN || "/opt/google/chrome/chrome", [
    "--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--no-first-run",
    "--disable-background-networking", "--remote-debugging-port=0", `--user-data-dir=${profile}`, url,
  ], { stdio: "ignore" });
  let launchError;
  chrome.on("error", (error) => { launchError = error; });
  let debugPort;
  await waitFor(async () => {
    if (launchError) throw launchError;
    try { debugPort = Number((await readFile(join(profile, "DevToolsActivePort"), "utf8")).split("\n")[0]); return true; }
    catch { return false; }
  }, "Chrome debugging port");
  const targets = await (await fetch(`http://127.0.0.1:${debugPort}/json/list`)).json();
  const target = targets.find((t) => t.type === "page");
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
  let sequence = 0;
  const pending = new Map();
  const errors = [];
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.method === "Runtime.exceptionThrown") errors.push(data.params.exceptionDetails.text);
    if (data.id && pending.has(data.id)) {
      const task = pending.get(data.id); pending.delete(data.id);
      if (data.error) task.reject(new Error(JSON.stringify(data.error)));
      else task.resolve(data.result);
    }
  };
  const call = (method, params = {}) => new Promise((resolve, reject) => {
    const id = ++sequence;
    pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
  async function evaluate(expression) {
    const result = await call("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
    if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
    return result.result.value;
  }
  const wait = (expression, label) => waitFor(() => evaluate(expression), label);
  const click = (selector) => evaluate(`document.querySelector(${JSON.stringify(selector)}).click()`);
  async function fill(id, value, change = false) {
    await evaluate(`document.getElementById(${JSON.stringify(id)}).value=${JSON.stringify(value)}`);
    if (change) await evaluate(`document.getElementById(${JSON.stringify(id)}).dispatchEvent(new Event('change'))`);
  }
  async function search() {
    await click("#search-button");
    await wait("document.getElementById('results-section').getAttribute('aria-busy')==='false'", "search completion");
  }
  await call("Runtime.enable");
  await call("Page.enable");
  await call("Emulation.setDeviceMetricsOverride", { width: 1280, height: 1000, deviceScaleFactor: 1, mobile: false });
  await wait("document.getElementById('search-button') && !document.getElementById('search-button').disabled", "app ready");
  await click("[data-example]");
  await search();
  assert.ok(await evaluate("document.querySelectorAll('.case-card').length>=3"));
  await click(".case-card summary");
  assert.ok(await evaluate("document.querySelector('.case-card details').open"));
  assert.ok(await evaluate("document.querySelector('.case-detail').textContent.includes('Unknowns and limits')"));
  assert.ok(await evaluate("document.querySelector('.case-detail').textContent.includes('A verbatim excerpt is not included')"));
  assert.ok(await evaluate("[...document.querySelectorAll('.source-link')].every(a=>a.href.startsWith('https://') && a.rel.includes('noopener'))"));
  checks.push("search, case inspection, sourced responses and unknowns");

  await click(".compare-check");
  await evaluate("document.querySelectorAll('.compare-check')[1].click(); document.querySelectorAll('.compare-check')[2].click()");
  assert.ok(await evaluate("document.querySelectorAll('.compare-check:checked').length===3"));
  assert.ok(await evaluate("[...document.querySelectorAll('.compare-check')].filter(i=>!i.checked).every(i=>i.disabled)"));
  await click("#compare-button");
  assert.equal(await evaluate("document.querySelectorAll('#comparison-table thead th').length"), 4);
  assert.ok(await evaluate("document.getElementById('comparison-table').textContent.includes('Basis:')"));
  checks.push("comparison of three cases; metric bases and selection limit");
  const desktop = await call("Page.captureScreenshot", { captureBeyondViewport: true });
  await writeFile(join(tmpdir(), "ais-case-search-desktop.png"), Buffer.from(desktop.data, "base64"));

  await fill("source-case", "CL-2022", true);
  await search();
  assert.ok(await evaluate("![...document.querySelectorAll('.case-card')].some(c=>c.dataset.caseId==='CL-2022')"));
  assert.ok(await evaluate("document.getElementById('eligibility-content').textContent.includes('self: 1')"));
  checks.push("source-case self exclusion and dates");
  await fill("source-case", "");
  await fill("situation", "packaging logistics");
  await fill("cutoff", "2023-01-26");
  await fill("before-period", "2023-01-26");
  await search();
  assert.ok(await evaluate("![...document.querySelectorAll('.case-card')].some(c=>c.dataset.caseId==='CL-2022'||c.dataset.caseId==='UL-2022')"));
  checks.push("publication cutoff");

  await fill("situation", "semiconductor shortages at a bank");
  await search();
  assert.ok(await evaluate("document.querySelectorAll('.case-card').length===0 && document.getElementById('results-status').classList.contains('empty')"));
  assert.ok(await evaluate("document.getElementById('results-status').textContent.includes('Insufficient evidence')"));
  checks.push("unsupported situation; no stale results or comparison");
  await fill("situation", "packaging logistics");
  await fill("before-period", "2025-01-01");
  await search();
  assert.ok(await evaluate("!document.getElementById('error').hidden && document.getElementById('error').textContent.includes('cannot be after')"));
  checks.push("actionable date validation error");

  await call("Emulation.setDeviceMetricsOverride", { width: 375, height: 900, deviceScaleFactor: 1, mobile: true });
  await fill("before-period", "2023-01-26");
  await search();
  await click(".case-card summary");
  assert.ok(await evaluate("document.documentElement.scrollWidth<=window.innerWidth"));
  const mobile = await call("Page.captureScreenshot", { captureBeyondViewport: true });
  await writeFile(join(tmpdir(), "ais-case-search-mobile.png"), Buffer.from(mobile.data, "base64"));
  checks.push("375px layout without page overflow");
  assert.deepEqual(errors, []);
  console.log(JSON.stringify({ passed: checks, screenshots: ["/tmp/ais-case-search-desktop.png", "/tmp/ais-case-search-mobile.png"] }, null, 2));
} finally {
  ws?.close();
  chrome?.kill("SIGTERM");
  python.kill("SIGTERM");
  // Wait for our own child processes to release the temporary browser profile.
  await delay(500);
  await rm(profile, { recursive: true, force: true, maxRetries: 3, retryDelay: 300 });
}
