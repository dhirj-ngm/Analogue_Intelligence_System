// Synthetic review-form exercise only. No labels enter study submissions.
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdtemp, readFile, writeFile, rm, mkdir } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const packetDirectory = resolve(process.env.REVIEW_DIRECTORY || join(root, "evaluation/relevance-m008/reviewer"));
const profile = await mkdtemp(join(tmpdir(), "ais-browser-"));
const delay = (ms) => new Promise((r) => setTimeout(r, ms));
const python = spawn(process.env.APP_PYTHON || "python3", ["-c",
  "from functools import partial; from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer; import sys; s=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=sys.argv[1])); print(s.server_port,flush=True); s.serve_forever()", packetDirectory],
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
  const url = `http://127.0.0.1:${Number(port.trim())}/packet.html`;
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
  await call("Runtime.enable");
  await call("Page.enable");
  await wait("document.getElementById('query-choice')?.options.length===10 && document.querySelector('#cases article')", "review packet ready");
  for (const [device,width] of [["desktop",1280],["mobile",375]]) {
    await call("Emulation.setDeviceMetricsOverride", {width,height:900,deviceScaleFactor:1,mobile:device==="mobile"});
    const downloads=join(profile,device);await mkdir(downloads,{recursive:true});
    await call("Browser.setDownloadBehavior", {behavior:"allow",downloadPath:downloads});
    await fill("query-choice","Q01",true);
    await wait("document.querySelectorAll('#cases article').length===17", "full eligible collection rendered");
    assert.ok(await evaluate(`[...document.querySelectorAll('#cases a')].every(a=>a.href.startsWith('https://') && a.rel.includes('noopener'))`));
    assert.equal(await evaluate(`document.body.innerText.includes('BM25')`),false);
    await fill("reviewer-id","");
    await click("#export-review");
    assert.ok(await evaluate(`document.getElementById('message').innerText.includes('reviewer code')`));
    await fill("reviewer-id","SYNTHETIC_BROWSER_ONLY");
    for(const id of ["human","independent","blind","no-ai"]) if(!await evaluate(`document.getElementById('${id}').checked`)) await click(`#${id}`);
    for(const [field,value] of Object.entries({usefulness:"unsure",reason:"SYNTHETIC TEST ONLY, not a human judgement.",misleading:"unsure",misleading_reason:"Synthetic form uncertainty",source_access:"unavailable",source_note:"Synthetic access-note test"})) {
      await evaluate(`(()=>{const el=document.querySelector('#cases article [data-field="${field}"]');el.value=${JSON.stringify(value)};el.dispatchEvent(new Event(el.tagName==='SELECT'?'change':'input',{bubbles:true}));})()`);
    }
    await fill("query-choice","Q09",true);
    assert.equal(await evaluate(`document.querySelectorAll('#cases article').length`),2);
    await fill("query-choice","Q01",true);
    assert.equal(await evaluate(`document.querySelector('#cases article [data-field="usefulness"]').value`),"unsure");
    await click("#save-draft");
    const draft=join(downloads,"m008-draft.json");
    await waitFor(async()=>{try{return JSON.parse(await readFile(draft,"utf8")).reviewer_id==="SYNTHETIC_BROWSER_ONLY";}catch{return false;}},"actual draft download");
    const saved=JSON.parse(await readFile(draft,"utf8"));
    assert.equal(saved.judgements.filter(j=>j.usefulness).length,1);
    assert.equal(saved.judgements.length,154);
    await fill("reviewer-id","");
    const documentNode=await call("DOM.getDocument");
    const input=await call("DOM.querySelector",{nodeId:documentNode.root.nodeId,selector:"#load-draft"});
    await call("DOM.setFileInputFiles",{nodeId:input.nodeId,files:[draft]});
    await wait("document.getElementById('message').innerText.includes('Saved responses loaded')", "draft restored");
    assert.equal(await evaluate(`document.getElementById('reviewer-id').value`),"SYNTHETIC_BROWSER_ONLY");
    const wrong=join(downloads,"wrong.json");await writeFile(wrong,JSON.stringify({packet_id:"wrong"}));
    await call("DOM.setFileInputFiles",{nodeId:input.nodeId,files:[wrong]});
    await wait("document.getElementById('message').innerText.includes('different packet')", "wrong packet rejected");
    assert.equal(await evaluate(`document.querySelector('#cases article [data-field="usefulness"]').value`),"unsure");
    await click("#export-review");
    const exported=join(downloads,"m008-review.json");
    await waitFor(async()=>{try{return JSON.parse(await readFile(exported,"utf8")).packet_id===saved.packet_id;}catch{return false;}},"actual partial-review export");
    assert.deepEqual(JSON.parse(await readFile(exported,"utf8")),saved);
    await click("#cases article > details > summary");
    assert.ok(await evaluate(`document.querySelector('#cases article > details').innerText.includes('What remains unknown')`));
    assert.ok(await evaluate(`document.documentElement.scrollWidth<=innerWidth`));
    await evaluate(`document.getElementById('situation').scrollIntoView({block:'start',behavior:'instant'})`);
    const shot=await call("Page.captureScreenshot",{captureBeyondViewport:false});
    await writeFile(join(tmpdir(),`ais-m008-review-${device}.png`),Buffer.from(shot.data,"base64"));
    checks.push(`${device}: evidence, full pool, dates, missing declarations, uncertainty, query switching, draft download/restore, wrong-packet rejection, partial export and layout`);
  }
  assert.deepEqual(errors,[]);
  console.log(JSON.stringify({passed:checks,note:"All form labels were synthetic tests, deleted with the temporary profile; no human judgements collected."},null,2));
} finally {
  ws?.close();chrome?.kill("SIGTERM");python.kill("SIGTERM");await delay(500);
  await rm(profile,{recursive:true,force:true,maxRetries:3,retryDelay:300});
}
