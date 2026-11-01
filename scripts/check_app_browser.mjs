// Optional, dependency-free browser smoke check: Node 22+ and a local Chrome/Chromium.
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdtemp, readFile, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const audit = process.argv.includes("--audit-m008")
  ? JSON.parse(await readFile(join(root,"evaluation/audit-m008/snapshot.json"),"utf8")).queries : [];
const currentAudit = audit.length ? JSON.parse(await readFile(join(root,"evaluation/search-m010/results.json"),"utf8")).historical.filter(r=>r.group==="m008") : [];
const retryRounds = Number(process.argv.find((arg) => arg.startsWith("--retry-rounds="))?.split("=")[1] || 3);
assert.ok(Number.isInteger(retryRounds) && retryRounds >= 1 && retryRounds <= 30);
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
  let clickId = 0;
  async function click(selector) {
    const id = ++clickId;
    const point = await evaluate(`(async () => {
      const el = document.querySelector(${JSON.stringify(selector)});
      if (!el) throw new Error('Missing control');
      el.scrollIntoView({block:'center',behavior:'instant'});
      let previous, stable = 0;
      const deadline = performance.now() + 3000;
      while (performance.now() < deadline) {
        await new Promise(requestAnimationFrame);
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height || el.disabled) throw new Error('Control is hidden or disabled');
        const point = {x:r.x+r.width/2,y:r.y+r.height/2};
        // A queued focus scroll can override the first scrollIntoView on the
        // next animation frame. Bring the control back before hit-testing it.
        if (point.y<0 || point.y>=innerHeight || point.x<0 || point.x>=innerWidth) {
          el.scrollIntoView({block:'center',behavior:'instant'});
          stable=0; previous=undefined; continue;
        }
        const hit = document.elementFromPoint(point.x, point.y);
        stable = previous && Math.abs(previous.x-point.x)<0.1 && Math.abs(previous.y-point.y)<0.1
          && (hit===el || el.contains(hit)) ? stable+1 : 0;
        previous = point;
        if (stable >= 3) {
          el.addEventListener('click', e => { if(e.isTrusted) window.__browserClick=${id}; }, {once:true});
          return point;
        }
      }
      const r=el.getBoundingClientRect();
      throw new Error('Click target did not settle: ' + ${JSON.stringify(selector)} + ' ' + JSON.stringify({rect:r.toJSON(),hit:previous && document.elementFromPoint(previous.x,previous.y)?.outerHTML.slice(0,200),scrollY}));
    })()`);
    await call('Input.dispatchMouseEvent', {type:'mousePressed',...point,button:'left',clickCount:1});
    await call('Input.dispatchMouseEvent', {type:'mouseReleased',...point,button:'left',clickCount:1});
    await wait(`window.__browserClick===${id}`, `trusted click on ${selector}`);
  }
  async function fill(id, value, change = false) {
    await evaluate(`document.getElementById(${JSON.stringify(id)}).value=${JSON.stringify(value)}`);
    if (change) await evaluate(`document.getElementById(${JSON.stringify(id)}).dispatchEvent(new Event('change'))`);
  }
  async function search() {
    const previous = await evaluate("window.__searchSubmissions");
    await click("#search-button");
    await wait(`window.__searchSubmissions===${previous+1} && document.getElementById('results-section').getAttribute('aria-busy')==='false'`, "new search submission and completion");
  }
  await call("Runtime.enable");
  await call("Page.enable");
  await wait("document.getElementById('search-button') && !document.getElementById('search-button').disabled", "app ready");
  await evaluate("window.__searchSubmissions=0; document.getElementById('search-form').addEventListener('submit',()=>window.__searchSubmissions++,true)");
  await call("Network.enable");
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

    await openOptions();
    await click("#reset-dates");
    await fill("situation", "cocoa");
    await search();
    assert.equal(await evaluate(`document.querySelectorAll('.case-card').length`), 1);
    assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`), "HSY-2025-Q1");
    await click(".case-reading > summary");
    assert.ok(await evaluate(`document.querySelector('.source-conflict').innerText.includes('1,780 basis points (17.8 percentage points)') && document.querySelector('.source-conflict').innerText.includes('1,790 basis points (17.9 percentage points)')`));
    assert.ok(await evaluate(`document.querySelector('.case-detail').innerText.includes('33.7%') && document.querySelector('.case-detail').innerText.includes('not independent proof')`));
    await click(".other-figures > summary");
    assert.ok(await evaluate(`document.querySelector('.other-figures').innerText.includes('41.2%')`));
    await click(".other-figures .metric-details > summary");
    assert.ok(await evaluate(`document.querySelector('.other-figures').innerText.includes('Non-GAAP')`));
    assert.ok(await evaluate(`document.querySelectorAll('.source-conflict a').length===2 && [...document.querySelectorAll('.source-conflict a')].every(a=>a.target==='_blank' && a.href.startsWith('https://'))`));
    assert.ok(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`));
    await evaluate(`document.querySelector('.source-conflict').scrollIntoView({block:'start',behavior:'instant'})`);
    await screenshot(`ais-collection-conflict-${device}.png`, false);
    checks.push(`${device}: cocoa case, separate reported/adjusted figures, visible source disagreement and unit explanations`);

    await openOptions();
    await fill("cutoff", "2025-04-30", true);
    await search();
    assert.equal(await evaluate(`document.querySelectorAll('.case-card').length`), 0);
    await fill("cutoff", "2025-05-01", true);
    await search();
    assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`), "HSY-2025-Q1");
    await fill("source-case", "HSY-2025-Q1", true);
    await search();
    assert.ok(await evaluate(`![...document.querySelectorAll('.case-card')].some(c=>c.dataset.caseId==='HSY-2025-Q1') && document.getElementById('method-checks').textContent.includes('The case you started from: 1')`));
    await click("#reset-dates");
    await fill("situation", "milk flour electricity");
    await search();
    assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`), "GIS-2007");
    assert.ok(await evaluate(`document.querySelector('.pressure-match').textContent.includes('milk → dairy') && document.querySelector('.pressure-match').textContent.includes('flour → grains') && document.querySelector('.pressure-match').textContent.includes('electricity → energy')`));
    assert.ok(await evaluate(`document.querySelector('.card-main').innerText.includes('do not establish that it measured your exact input') && document.getElementById('result-caution').innerText.includes('whether costs rose or fell')`));
    assert.ok(await evaluate(`document.getElementById('query-reading').innerText.includes('direction not specified') && document.querySelector('.direction-match').innerText.includes('Your direction is not specified')`));
    await screenshot(`ais-related-search-${device}.png`, false);
    for (const [text,id,link] of [["chocolate ingredient inflation","HSY-2025-Q1","chocolate → cocoa"],["bottled-water freight and fuel","NES-WATERS-2011-H1","fuel → oil"]]) {
      await fill("situation",text);
      await search();
      assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`), id);
      assert.ok(await evaluate(`document.querySelector('.pressure-match').textContent.includes(${JSON.stringify(link)})`));
      assert.ok(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`));
    }
    await fill("situation", "No chocolate input-cost inflation is established.");
    await search();
    assert.equal(await evaluate(`document.querySelectorAll('.case-card').length`),0);
    checks.push(`${device}: new-case publication boundary, self exclusion, three related-term searches and negation`);

    const contextDate = await evaluate(`document.getElementById('cutoff').value`);
    for (const [text,reason] of [["Coffee costs are falling.","opposite direction"],["Milk sales are rising.","Sales, selling prices"],["Freight and fuel costs at an airline.","outside"],["Milk costs changed.","which way"]]) {
      await fill("situation",text);
      await search();
      assert.ok(await evaluate(`document.querySelectorAll('.case-card').length===0 && document.getElementById('results-status').textContent.includes(${JSON.stringify(reason)}) && !document.getElementById('query-reading').hidden && document.getElementById('comparison').hidden`));
      assert.equal(await evaluate(`document.getElementById('cutoff').value`), contextDate);
      assert.ok(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`));
    }
    await screenshot(`ais-context-empty-${device}.png`, false);
    checks.push(`${device}: cost direction, sales role, outside industry and unclear wording give honest empty results`);

    await fill("situation", "Not milk but packaging is more expensive.");
    await search();
    assert.ok(await evaluate(`document.querySelectorAll('.case-card')[2].dataset.caseId==='CL-2022' && !document.querySelector('[data-case-id="GIS-2007"]')`));
    assert.ok(await evaluate(`document.getElementById('query-reading').innerText.includes('Left out: “not milk”') && document.querySelector('.direction-match').innerText.includes('rising costs in both')`));
    await screenshot(`ais-context-mixed-${device}.png`, false);
    await fill("situation", "Milk costs fell while energy bills rose.");
    await search();
    assert.deepEqual((await evaluate(`[...document.querySelectorAll('.case-card')].map(c=>c.dataset.caseId)`)).sort(),["DF-2015","KC-2011"]);
    assert.ok(await evaluate(`document.getElementById('query-reading').innerText.includes('falling costs') && document.getElementById('query-reading').innerText.includes('rising costs')`));
    checks.push(`${device}: mixed negation keeps positive packaging, packaging rank is transparent, opposite inputs veto partial matches`);

    await fill("situation", "cocoa grains oil");
    await search();
    assert.deepEqual((await evaluate(`[...document.querySelectorAll('.case-card')].map(c=>c.dataset.caseId)`)).sort(), ["GIS-2007", "HSY-2025-Q1", "NES-WATERS-2011-H1"]);
    await click(".case-card[data-case-id='NES-WATERS-2011-H1'] .case-reading > summary");
    assert.ok(await evaluate(`document.querySelector('[data-case-id="NES-WATERS-2011-H1"] .case-detail').innerText.includes('140 basis points (1.4 percentage points)')`));
    for (const id of ["GIS-2007", "HSY-2025-Q1", "NES-WATERS-2011-H1"]) await click(`.case-card[data-case-id='${id}'] .compare-check`);
    await click("#compare-button");
    const comparison = await evaluate(`document.getElementById('comparison-table').innerText`);
    assert.ok(comparison.includes('bottled-water division') && comparison.includes('full financial year') && comparison.includes('sources disagree'));
    assert.ok(comparison.includes('Connection to your description') && comparison.includes('Your direction is not specified'));
    assert.ok(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`));
    await screenshot(`ais-collection-comparison-${device}.png`, false);
    await evaluate(`document.querySelector('#comparison-table [data-comparison-field="profit"]').scrollIntoView({block:'start',behavior:'instant'})`);
    await screenshot(`ais-collection-figures-${device}.png`, false);
    checks.push(`${device}: three new cases compared with business scope, accounting differences and conflict retained`);
    await click("#clear-comparison");

    // M007: actual records, not synthetic substitutes or company-specific ranking.
    for (const [text,id] of [["Coffee input costs are rising.","SJM-COFFEE-2011"],["Cattle costs are rising.","TSN-BEEF-2024-Q1"],["Aluminium costs are rising.","COKE-2022"],["Milk costs are falling.","DF-2015"]]) {
      await fill("situation",text);
      await search();
      assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`),id);
      await click(".case-reading > summary");
      await click(".case-detail .source-location > summary");
      assert.ok(await evaluate(`document.querySelector('.case-detail .source-location').innerText.includes('p. ')`), `source page locator for ${id}`);
      assert.ok(await evaluate(`document.querySelector('.case-detail .source-link').href.startsWith('https://www.sec.gov/Archives/')`));
      assert.ok(await evaluate(`document.querySelector('.case-detail').innerText.includes("What we don't know")`));
      assert.ok(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`));
    }
    checks.push(`${device}: all four M007 situations searched, precise original source links and unknowns readable`);

    await openOptions();
    await fill("situation","Coffee costs rise.");
    await fill("cutoff","2011-06-27",true);
    await search();
    assert.equal(await evaluate(`document.querySelectorAll('.case-card').length`),0);
    await openOptions();
    await fill("cutoff","2011-06-28",true);
    await search();
    assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`),"SJM-COFFEE-2011");
    await openOptions();
    await fill("source-case","SJM-COFFEE-2011",true);
    await search();
    assert.equal(await evaluate(`document.querySelectorAll('.case-card').length`),0);
    await openOptions();
    await fill("source-case","",true);
    await click("#reset-dates");
    checks.push(`${device}: M007 publication boundary and starting-case exclusion`);

    await fill("situation","milk");
    await search();
    assert.deepEqual((await evaluate(`[...document.querySelectorAll('.case-card')].map(c=>c.dataset.caseId)`)).sort(),["DF-2015","GIS-2007"]);
    for (const id of ["DF-2015","GIS-2007"]) await click(`.case-card[data-case-id='${id}'] .compare-check`);
    await click("#compare-button");
    assert.ok(await evaluate(`document.getElementById('comparison-table').innerText.includes('falling costs') && document.getElementById('comparison-table').innerText.includes('rising costs')`));
    await click("#comparison-table .other-figures > summary");
    await click("#comparison-table .other-figures .metric-details > summary");
    assert.ok(await evaluate(`document.getElementById('comparison-table').innerText.includes('16.34 USD per 100 lb') && document.getElementById('comparison-table').innerText.includes('NOT the price Dean actually paid')`));
    assert.ok(await evaluate(`document.querySelector('#comparison-table .other-figures .field-help').innerText.includes('This price is quoted per 100 pounds')`));
    await evaluate(`document.querySelector('#comparison-table .other-figures').scrollIntoView({block:'start',behavior:'instant'})`);
    await screenshot(`ais-m007-dairy-${device}.png`,false);
    await click("#clear-comparison");

    await fill("situation","coffee cattle aluminum");
    await search();
    for (const id of ["SJM-COFFEE-2011","TSN-BEEF-2024-Q1","COKE-2022"]) await click(`.case-card[data-case-id='${id}'] .compare-check`);
    await click("#compare-button");
    const expandedComparison = await evaluate(`document.getElementById('comparison-table').innerText`);
    assert.ok(expandedComparison.includes('operating loss of US$206 million') && expandedComparison.includes('27.8%') && expandedComparison.includes('36.7%'));
    assert.ok(expandedComparison.includes('write-down') && expandedComparison.includes('bottler') && expandedComparison.includes('quarterly'));
    assert.ok(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`));
    await screenshot(`ais-m007-comparison-${device}.png`,false);
    await evaluate(`document.querySelector('#comparison-table [data-comparison-field="profit"]').scrollIntoView({block:'start',behavior:'instant'})`);
    for (const cell of [2,3,4]) await click(`#comparison-table [data-comparison-field="profit"] td:nth-child(${cell}) > .detail-block > .metric-details > summary`);
    assert.ok(await evaluate(`document.getElementById('comparison-table').innerText.includes('-206 USD million')`));
    await evaluate(`document.querySelector('#comparison-table [data-comparison-field="profit"]').scrollIntoView({block:'start',behavior:'instant'})`);
    await screenshot(`ais-m007-measures-${device}.png`,false);
    await click("#clear-comparison");
    for (const text of ["Potato input costs rise.","Beef input costs rise."]) {
      await fill("situation",text);
      await search();
      assert.equal(await evaluate(`document.querySelectorAll('.case-card').length`),0);
      assert.ok(await evaluate(`!document.getElementById('empty-actions').hidden`));
    }
    checks.push(`${device}: M007 dairy and three-metric comparisons, benchmark distinction, unsupported and documented missed wording`);

    await openOptions();
    await click("#reset-dates");
    const supplierQuery="We bottle water. Our freight supplier also serves airlines. Freight and fuel costs are rising.";
    await fill("situation",supplierQuery);
    await search();
    assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`),"NES-WATERS-2011-H1");
    await fill("cutoff","2011-08-09",true);await fill("before-period","2011-08-09");
    await search();assert.equal(await evaluate(`document.querySelectorAll('.case-card').length`),0);
    await fill("cutoff","2011-08-10",true);await fill("before-period","2011-08-10");
    await search();assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`),"NES-WATERS-2011-H1");
    await fill("source-case","NES-WATERS-2011-H1",true);await search();
    assert.ok(await evaluate(`!document.querySelector('[data-case-id="NES-WATERS-2011-H1"]') && document.getElementById('method-checks').textContent.includes('The case you started from: 1')`));
    await click("#reset-dates");
    await fill("situation","We operate an airline. Fuel costs rise.");await search();
    assert.ok(await evaluate(`document.querySelectorAll('.case-card').length===0 && document.getElementById('results-status').innerText.includes('outside')`));
    checks.push(`${device}: M009 supplier/customer roles, true airline exclusion, publication-day and self safeguards`);

    await fill("situation","Milk costs fell while energy bills rose.");await search();
    assert.ok(await evaluate(`document.querySelector('[data-case-id="DF-2015"] .coverage').innerText.includes('Not established here: energy') && document.querySelector('[data-case-id="KC-2011"] .coverage').innerText.includes('Not established here: milk')`));
    assert.ok(await evaluate(`document.getElementById('result-caution').innerText.includes('combined pressures')`));
    for(const id of ["DF-2015","KC-2011"]) await click(`.case-card[data-case-id='${id}'] .compare-check`);
    await click("#compare-button");
    assert.ok(await evaluate(`document.getElementById('comparison-table').innerText.includes('Partial comparison') && document.querySelector('.comparison-note').innerText.includes('combining partial cases')`));
    assert.ok(await evaluate(`document.documentElement.scrollWidth<=innerWidth`));
    await screenshot(`ais-m009-partial-${device}.png`,false);
    await click("#clear-comparison");
    await fill("situation","Milk and potato costs are rising.");await search();
    assert.ok(await evaluate(`document.querySelector('.coverage').innerText.includes('potato costs') && document.querySelector('.coverage').innerText.includes('Partial comparison')`));
    checks.push(`${device}: M009 supported/missing pressures per result and comparison; combined-case caution; unknown input stays unsupported`);

    const liveQuery="Our beef plant buys live animals. Beef raw-material costs are rising.";
    await fill("situation",liveQuery);await search();
    assert.ok(await evaluate(`document.querySelectorAll('.case-card').length===0 && !document.getElementById('input-clarification').hidden && document.getElementById('clarification-message').innerText.includes('cattle')`));
    const savedDate=await evaluate(`document.getElementById('cutoff').value`);
    const beforeEdit=await evaluate(`window.__searchSubmissions`);
    await screenshot(`ais-m009-clarify-${device}.png`,false);
    await click("#clarify-input");
    assert.equal(await evaluate(`document.activeElement.id`),"situation");
    assert.equal(await evaluate(`document.getElementById('situation').value`),liveQuery);
    assert.equal(await evaluate(`window.__searchSubmissions`),beforeEdit);
    assert.equal(await evaluate(`document.getElementById('cutoff').value`),savedDate);
    await fill("situation","Cattle input costs are rising.");await search();
    assert.ok(await evaluate(`document.querySelector('.case-card').dataset.caseId==='TSN-BEEF-2024-Q1' && document.getElementById('input-clarification').hidden`));
    await fill("situation","Beef selling prices are rising.");await search();
    assert.ok(await evaluate(`document.querySelectorAll('.case-card').length===0 && document.getElementById('input-clarification').hidden`));
    await fill("situation","We buy live animals. Milk costs are falling.");await search();
    assert.ok(await evaluate(`document.querySelector('.case-card').dataset.caseId==='DF-2015' && !document.getElementById('input-clarification').hidden && document.querySelector('.coverage').innerText.includes('Still unclear')`));
    checks.push(`${device}: M009 live-animal clarification requires an explicit edit; dates/draft retained; beef outputs separate; unresolved input prevents full coverage`);

    await openOptions();
    await click("#reset-dates");
    await fill("situation","Milk costs are rising not falling.");await search();
    assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`),"GIS-2007");
    assert.ok(await evaluate(`!document.querySelector('[data-case-id="DF-2015"]') && document.getElementById('query-reading').innerText.includes('rising costs')`));
    await fill("situation","Milk costs fell, energy bills rose.");await search();
    assert.ok(await evaluate(`document.querySelector('[data-case-id="DF-2015"] .coverage').innerText.includes('Not established here: energy') && document.querySelector('[data-case-id="KC-2011"] .coverage').innerText.includes('Not established here: milk') && !document.querySelector('[data-case-id="GIS-2007"]')`));
    for (const id of ["DF-2015","KC-2011"]) await click(`.case-card[data-case-id='${id}'] .compare-check`);
    await click("#compare-button");
    assert.ok(await evaluate(`document.querySelector('.comparison-note').innerText.includes('combining partial cases') && document.documentElement.scrollWidth<=innerWidth`));
    await screenshot(`ais-m010-comparison-${device}.png`,false);
    await click("#clear-comparison");
    checks.push(`${device}: M010 unpunctuated denied alternative; comma directions stay per-input in results/comparison`);

    const unclear="Milk costs fell, prices rose.";
    await fill("situation",unclear);await search();
    assert.ok(await evaluate(`document.querySelectorAll('.case-card').length===0 && document.getElementById('clarification-title').innerText==='Clarify which costs changed' && document.getElementById('clarification-message').innerText.includes('one change per clause')`));
    const directionDraft = await evaluate(`JSON.stringify({text:document.getElementById('situation').value,cutoff:document.getElementById('cutoff').value,period:document.getElementById('before-period').value,submissions:window.__searchSubmissions})`);
    await screenshot(`ais-m010-direction-${device}.png`,false);
    await click("#clarify-input");
    assert.equal(await evaluate(`document.activeElement.id`),"situation");
    assert.equal(await evaluate(`JSON.stringify({text:document.getElementById('situation').value,cutoff:document.getElementById('cutoff').value,period:document.getElementById('before-period').value,submissions:window.__searchSubmissions})`),directionDraft);
    await fill("situation","We are an airline supplier. Fuel costs rise.");await search();
    assert.ok(await evaluate(`document.querySelectorAll('.case-card').length===0 && document.getElementById('clarification-title').innerText==='Clarify whose situation this is' && document.getElementById('clarify-input').innerText==='Edit the business description'`));
    await screenshot(`ais-m010-scope-${device}.png`,false);
    await click("#clarify-input");
    assert.equal(await evaluate(`document.activeElement.id`),"situation");
    await fill("situation","Our bottled-water business uses a logistics firm whose customers include airlines. Freight and fuel costs rise.");await search();
    assert.equal(await evaluate(`document.querySelector('.case-card').dataset.caseId`),"NES-WATERS-2011-H1");
    assert.ok(await evaluate(`document.getElementById('input-clarification').hidden`));
    await fill("situation","We operate an airline. Fuel costs rise not fall.");await search();
    assert.equal(await evaluate(`document.querySelectorAll('.case-card').length`),0);
    await fill("situation","Our customers pay more for milk.");await search();
    assert.equal(await evaluate(`document.querySelectorAll('.case-card').length`),0);
    checks.push(`${device}: M010 direction/business clarification preserves draft/dates with no submission; explicit role edit works; real outside business and selling context remain excluded`);

    if (audit.length) {
      await openOptions();
      await click("#reset-dates");
      for (const row of audit) {
        await fill("situation",row.payload.text);
        await fill("cutoff",row.payload.cutoff,true);
        await fill("before-period",row.payload.before_period_end);
        await search();
        const expected=currentAudit.find(c=>c.id===row.id).new.ranked;
        assert.deepEqual(await evaluate(`[...document.querySelectorAll('.case-card')].map(c=>c.dataset.caseId)`),expected.map(c=>c.id),row.id);
        assert.equal(await evaluate(`document.getElementById('cutoff').value`),row.payload.cutoff);
        assert.ok(await evaluate(`document.documentElement.scrollWidth<=innerWidth && document.getElementById('error').hidden`));
        if (["A06","A08"].includes(row.id)) {
          await evaluate(`document.getElementById('results-title').scrollIntoView({block:'start',behavior:'instant'})`);
          await screenshot(`ais-m008-audit-${row.id}-${device}.png`,false);
        }
      }
      checks.push(`${device}: eight AI audit searches reproduce displayed cases, empty results and date controls; these are observations, not quality grades`);
    }

    // Error focus starts smooth scrolling. Keep real clicks and slow responses:
    // wait for a stable target and a fresh submission, never an old idle flag.
    await call("Network.emulateNetworkConditions", {offline:false,latency:150,downloadThroughput:-1,uploadThroughput:-1});
    for (let trial=0; trial<retryRounds; trial++) {
      await call("Network.setBlockedURLs", {urls:["*/api/search"]});
      await fill("situation", "Keep my packaging description");
      await search();
      assert.ok(await evaluate(`document.getElementById('error-message').textContent.includes("couldn't reach") && document.getElementById('situation').value==='Keep my packaging description' && document.querySelectorAll('.case-card').length===0 && document.getElementById('query-reading').hidden`));
      await call("Network.setBlockedURLs", {urls:[]});
      await search();
      assert.ok(await evaluate(`document.getElementById('error').hidden && document.querySelectorAll('.case-card').length>0`));
    }
    await call("Network.emulateNetworkConditions", {offline:false,latency:0,downloadThroughput:-1,uploadThroughput:-1});
    checks.push(`${device}: ${retryRounds} connection-failure/retry cycles with delayed responses and trusted clicks`);
  }
  assert.deepEqual(errors, []);
  console.log(JSON.stringify({ passed: checks, screenshots: ["/tmp/ais-case-search-desktop.png", "/tmp/ais-case-search-mobile.png", "/tmp/ais-reader-comparison-desktop.png", "/tmp/ais-reader-comparison-mobile.png"] }, null, 2));
} finally {
  ws?.close();
  chrome?.kill("SIGTERM");
  python.kill("SIGTERM");
  await delay(500);
  await rm(profile, { recursive: true, force: true, maxRetries: 3, retryDelay: 300 });
}
