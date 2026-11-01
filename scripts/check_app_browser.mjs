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
  async function click(selector) {
    const point = await evaluate(`(() => {
      const el = document.querySelector(${JSON.stringify(selector)});
      if (!el) throw new Error('Missing control');
      el.scrollIntoView({block:'center',behavior:'instant'});
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) throw new Error('Control is hidden');
      return {x:r.x+r.width/2,y:r.y+r.height/2};
    })()`);
    await call('Input.dispatchMouseEvent', {type:'mousePressed',...point,button:'left',clickCount:1});
    await call('Input.dispatchMouseEvent', {type:'mouseReleased',...point,button:'left',clickCount:1});
  }
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
  await wait("document.getElementById('search-button') && !document.getElementById('search-button').disabled", "app ready");
  async function screenshot(name, full = true) {
    const shot = await call("Page.captureScreenshot", { captureBeyondViewport: full });
    await writeFile(join(tmpdir(), name), Buffer.from(shot.data, "base64"));
  }
  async function openOptions() {
    if (!await evaluate(`document.getElementById('search-options').open`)) await click("#search-options > summary");
  }
  for (const [device, width] of [["desktop",1280],["mobile",375]]) {
    await call("Emulation.setDeviceMetricsOverride", { width, height: 900, deviceScaleFactor: 1, mobile: device === "mobile" });
    await openOptions();
    await click("#reset-dates");
    await click("#search-options > summary");
    await click("[data-example]");
    await wait("document.querySelectorAll('.case-card').length>=3 && document.getElementById('results-section').getAttribute('aria-busy')==='false'", "example runs a search");
    assert.equal(await evaluate(`document.getElementById('how-it-works').open`), false);
    assert.equal(await evaluate(`document.body.innerText.includes('BM25')`), false);
    assert.equal(await evaluate(`document.body.innerText.includes('eligible observations')`), false);
    await screenshot(`ais-case-search-${device}.png`);
    await click(".case-reading > summary");
    assert.equal(await evaluate(`getComputedStyle(document.getElementById('selection-bar')).position`), "static");
    assert.ok(await evaluate(`document.querySelector('.case-reading').open`));
    assert.ok(await evaluate(`document.querySelector('.case-detail').textContent.includes("What we don't know")`));
    assert.ok(await evaluate(`document.querySelector('.case-detail').textContent.includes("We haven't included an exact quote")`));
    await click(".case-detail .source-location > summary");
    assert.ok(await evaluate(`document.querySelector('.case-detail .source-location').open`));
    assert.ok(await evaluate(`[...document.querySelectorAll('.source-link')].every(a=>a.href.startsWith('https://') && a.rel.includes('noopener'))`));
    await click(".case-detail .metric-details > summary");
    assert.ok(await evaluate(`document.querySelector('.metric-details').innerText.includes("Company's calculation")`));
    assert.equal(await evaluate(`document.body.innerText.includes('BM25') || document.body.innerText.includes('data/episodes.jsonl')`), false);
    if (device === "mobile") {
      await evaluate(`document.querySelector('.case-detail').scrollIntoView({block:'start',behavior:'instant'})`);
      await screenshot("ais-reader-case-mobile.png", false);
    }
    checks.push(`${device}: one-click example, readable case, original source and metric definitions`);

    await click(".compare-check");
    assert.equal(await evaluate(`getComputedStyle(document.getElementById('selection-bar')).position`), "sticky");
    assert.ok(await evaluate(`document.getElementById('compare-button').disabled && document.getElementById('selection-help').textContent.includes('one more')`));
    await click(".case-card:nth-child(2) .compare-check");
    await click(".case-card:nth-child(3) .compare-check");
    assert.equal(await evaluate(`document.querySelectorAll('.compare-check:checked').length`), 3);
    assert.ok(await evaluate(`[...document.querySelectorAll('.compare-check')].filter(i=>!i.checked).every(i=>i.disabled)`));
    await click("#compare-button");
    await wait("(() => {const r=document.getElementById('comparison-title').getBoundingClientRect(); return r.top>=0 && r.bottom<window.innerHeight;})()", "comparison scroll finishes");
    assert.equal(await evaluate(`document.querySelectorAll('#comparison-table thead th').length`), 4);
    assert.ok(await evaluate(`document.getElementById('comparison-table').textContent.includes("What we don't know")`));
    assert.ok(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`));
    if (device === "mobile") {
      assert.equal(await evaluate(`getComputedStyle(document.querySelector('.compare-case-label')).display`), "block");
      assert.ok(await evaluate(`[...document.querySelectorAll('#comparison-table td')].every(td=>td.getBoundingClientRect().width<=window.innerWidth)`));
    }
    await screenshot(`ais-reader-comparison-${device}.png`, false);
    await click("#clear-comparison");
    assert.ok(await evaluate(`document.getElementById('comparison').hidden && document.querySelectorAll('.compare-check:checked').length===0`));
    checks.push(`${device}: three-case selection, comparison layout, definitions and clearing`);

    await click("#how-it-works > summary");
    await click(".technical-details > summary");
    assert.ok(await evaluate(`document.getElementById('how-it-works').innerText.includes('BM25')`));
    assert.ok(await evaluate(`document.getElementById('method-checks').innerText.includes('Keyword scores')`));
    await click(".technical-details > summary");
    await click("#how-it-works > summary");
    checks.push(`${device}: optional method, dates, exclusions and scores`);

    await openOptions();
    await fill("situation", "My packaging logistics problem");
    await fill("cutoff", "2023-03-01", true);
    await fill("before-period", "2023-01-01");
    await fill("source-case", "CL-2022", true);
    assert.equal(await evaluate(`document.getElementById('cutoff').value`), "2023-01-27");
    assert.equal(await evaluate(`document.getElementById('before-period').value`), "2022-12-31");
    await search();
    assert.ok(await evaluate(`![...document.querySelectorAll('.case-card')].some(c=>c.dataset.caseId==='CL-2022')`));
    assert.ok(await evaluate(`document.getElementById('method-checks').textContent.includes('The case you started from: 1')`));
    await openOptions();
    await fill("source-case", "", true);
    assert.equal(await evaluate(`document.getElementById('situation').value`), "My packaging logistics problem");
    assert.equal(await evaluate(`document.getElementById('cutoff').value`), "2023-03-01");
    assert.equal(await evaluate(`document.getElementById('before-period').value`), "2023-01-01");
    checks.push(`${device}: source dates, self exclusion and restoration of personal draft`);

    await click("#reset-dates");
    const previous = await evaluate(`document.getElementById('cutoff').value`);
    await fill("cutoff", "2023-01-26", true);
    assert.equal(await evaluate(`document.getElementById('before-period').value`), "2023-01-26");
    assert.notEqual(previous, "2023-01-26");
    await fill("situation", "packaging logistics");
    await search();
    assert.ok(await evaluate(`![...document.querySelectorAll('.case-card')].some(c=>c.dataset.caseId==='CL-2022'||c.dataset.caseId==='UL-2022')`));
    await openOptions();
    await fill("before-period", "2025-01-01");
    await click("#search-options > summary");
    await search();
    assert.ok(await evaluate(`!document.getElementById('error').hidden && document.getElementById('error-message').textContent.includes('earlier end date')`));
    assert.ok(await evaluate(`document.getElementById('search-options').open && document.activeElement.id==='before-period' && document.activeElement.getAttribute('aria-invalid')==='true'`));
    await fill("before-period", "2023-01-26");
    await fill("cutoff", "");
    await click("#search-options > summary");
    await search();
    assert.ok(await evaluate(`document.getElementById('search-options').open && document.activeElement.id==='cutoff'`));
    checks.push(`${device}: linked dates, cutoff, visible field-specific errors and focus`);

    await fill("cutoff", "2000-01-01");
    await fill("before-period", "2000-01-01");
    await search();
    assert.ok(await evaluate(`document.querySelectorAll('.case-card').length===0 && document.getElementById('results-status').textContent.includes('these dates') && document.getElementById('try-example').hidden`));
    await click("#change-dates");
    assert.ok(await evaluate(`document.getElementById('search-options').open && document.activeElement.id==='cutoff'`));
    await click("#reset-dates");
    await fill("situation", "semiconductor shortages at a bank");
    await search();
    assert.ok(await evaluate(`document.querySelectorAll('.case-card').length===0 && document.getElementById('results-status').classList.contains('empty')`));
    assert.ok(await evaluate(`document.getElementById('results-status').textContent.includes("don't have enough evidence") && document.getElementById('comparison').hidden`));
    await click("#try-example");
    await wait("document.querySelectorAll('.case-card').length>=3 && document.getElementById('results-section').getAttribute('aria-busy')==='false'", "retry with example");
    assert.ok(await evaluate(`document.getElementById('error').hidden`));
    checks.push(`${device}: distinct date/coverage empty states and recovery`);
  }
  await call("Network.enable");
  await call("Network.setBlockedURLs", {urls:["*/api/search"]});
  await fill("situation", "Keep my packaging description");
  await search();
  assert.ok(await evaluate(`document.getElementById('error-message').textContent.includes("couldn't reach") && document.getElementById('situation').value==='Keep my packaging description' && document.querySelectorAll('.case-card').length===0`));
  await call("Network.setBlockedURLs", {urls:[]});
  await search();
  assert.ok(await evaluate(`document.getElementById('error').hidden && document.querySelectorAll('.case-card').length>0`));
  checks.push("connection failure preserves the description and supports retry");
  assert.deepEqual(errors, []);
  console.log(JSON.stringify({ passed: checks, screenshots: ["/tmp/ais-case-search-desktop.png", "/tmp/ais-case-search-mobile.png", "/tmp/ais-reader-comparison-desktop.png", "/tmp/ais-reader-comparison-mobile.png"] }, null, 2));
} finally {
  ws?.close();
  chrome?.kill("SIGTERM");
  python.kill("SIGTERM");
  await delay(500);
  await rm(profile, { recursive: true, force: true, maxRetries: 3, retryDelay: 300 });
}
