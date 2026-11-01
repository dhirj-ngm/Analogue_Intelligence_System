import {pressureLabel,differenceLabel,unknownLabels,explainBasisPoints} from "../app/reader.mjs";
// Self-contained offline packet. No network requests, analytics or automatic storage.
export function blankResponse(packet) {
  return {packet_id:packet.packet_id,reviewer_id:"",attestation:{human:false,created_cases_or_rules:null,seen_expected_answers:null,used_ai_judgements:null,prior_exposure:""},
    judgements:packet.queries.flatMap(q=>q.items.map(i=>({query_id:q.query_id,item_id:i.item_id,usefulness:null,reason:"",misleading:null,misleading_reason:"",source_access:null,source_note:""}))),
    queries:packet.queries.map(q=>({query_id:q.query_id,coverage:null,reason:"",missing_cases:""}))};
}

export function restoreResponse(packet,value) {
  if (value?.packet_id!==packet.packet_id || !Array.isArray(value.judgements) || !Array.isArray(value.queries)) throw new Error("This file belongs to a different packet or has an invalid format.");
  const result=blankResponse(packet);
  const seen=new Set();
  for(const row of value.judgements) {
    const key=`${row.query_id}/${row.item_id}`;
    const target=result.judgements.find(r=>r.query_id===row.query_id && r.item_id===row.item_id);
    if(!target || seen.has(key)) throw new Error("This file has an unknown or repeated case response.");
    seen.add(key);
    for(const field of ["reason","misleading_reason","source_note"]) if(row[field]!==undefined && typeof row[field]!=="string") throw new Error("Invalid response text.");
    for(const [field,allowed] of [["usefulness",["useful","partly_useful","not_useful","unsure"]],["misleading",["yes","no","unsure"]],["source_access",["opened","not_opened","unavailable"]]]) {
      if(row[field]!=null && !allowed.includes(row[field])) throw new Error("Invalid case category.");
    }
    for(const field of Object.keys(target)) if(row[field]!==undefined) target[field]=row[field];
  }
  seen.clear();
  for(const row of value.queries) {
    const target=result.queries.find(r=>r.query_id===row.query_id);
    if(!target || seen.has(row.query_id)) throw new Error("This file has an unknown or repeated situation.");
    seen.add(row.query_id);
    if(row.coverage!=null && !["adequate","limited","none","unsure"].includes(row.coverage)) throw new Error("Invalid collection-coverage category.");
    for(const field of ["reason","missing_cases"]) if(row[field]!==undefined && typeof row[field]!=="string") throw new Error("Invalid situation note.");
    for(const field of Object.keys(target)) if(row[field]!==undefined) target[field]=row[field];
  }
  if(typeof value.reviewer_id!=="string" || !value.attestation || typeof value.attestation!=="object") throw new Error("Reviewer details are missing.");
  result.reviewer_id=value.reviewer_id;
  for(const field of Object.keys(result.attestation)) {
    const v=value.attestation[field];
    if(field==="prior_exposure") {if(typeof v!=="string") throw new Error("Invalid prior-exposure note.");}
    else if(v!==null && typeof v!=="boolean") throw new Error("Invalid reviewer declaration.");
    result.attestation[field]=v;
  }
  return result;
}

export function rowComplete(row) {
  return Boolean(row.usefulness && row.reason.trim() && row.misleading && row.source_access
    && (row.misleading==="no" || row.misleading_reason.trim())
    && (row.source_access!=="unavailable" || row.source_note.trim()));
}

export function exportProblems(response) {
  const issues=[];
  const a=response.attestation;
  if(!response.reviewer_id.trim() || a.human!==true || a.created_cases_or_rules!==false || a.seen_expected_answers!==false || a.used_ai_judgements!==false) issues.push("Enter your reviewer code and complete the four declarations. If a declaration is not true, contact your coordinator; do not check it.");
  for(const r of response.judgements) {
    const started=r.usefulness || r.reason || r.misleading || r.misleading_reason || r.source_access || r.source_note;
    if(started && !rowComplete(r)) issues.push(`${r.query_id}, case ${r.item_id}: finish the categories and required explanations, or save a draft.`);
  }
  for(const q of response.queries) if((q.coverage || q.reason || q.missing_cases) && !(q.coverage && q.reason.trim())) issues.push(`${q.query_id}: finish the collection-coverage category and reason, or save a draft.`);
  if(!response.judgements.some(rowComplete) && !response.queries.some(q=>q.coverage && q.reason.trim())) issues.push("The review has no completed judgements or situation notes yet. Use Download draft to save progress.");
  return issues;
}

function startReview() {
  const packet=JSON.parse(document.getElementById("packet-data").textContent);
  let response=blankResponse(packet);
  const $=id=>document.getElementById(id);
  function node(tag,text) {const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;}
  function field(parent,label,value,onchange,options) {
    const wrap=node("label",label),control=node(options?"select":"textarea");
    if(options) for(const [v,t] of [["","Choose…"],...options]) {const opt=node("option",t);opt.value=v;control.append(opt);}
    control.value=value||"";control.addEventListener(options?"change":"input",()=>{onchange(control.value|| (options?null:""));progress();});
    wrap.append(control);parent.append(wrap);return control;
  }
  function link(parent,evidence) {
    if(!evidence || !/^https:\/\//.test(evidence.url)) return;
    const a=node("a","Open original report ↗");a.href=evidence.url;a.target="_blank";a.rel="noopener noreferrer";parent.append(a);
    const p=node("p",`${evidence.locator}${evidence.public_date?` · Published ${evidence.public_date}`:""}`);p.className="help";parent.append(p);
  }
  function list(parent,title,values) {parent.append(node("h4",title));const ul=node("ul");values.forEach(v=>ul.append(node("li",v)));parent.append(ul);}
  function metric(parent,m) {
    const d=node("details");d.append(node("summary",`${m.name}: ${m.value}${m.unit==="percent"?"%":` ${m.unit}`}`));
    for(const [title,value] of [["Scope",m.scope],["Calculation",m.basis],["Compared with",m.comparison]]) d.append(node("p",`${title}: ${explainBasisPoints(value)}`));
    if(m.evidence)link(d,m.evidence);parent.append(d);
  }
  function progress() {
    $("progress").textContent=`${response.judgements.filter(rowComplete).length} of ${response.judgements.length} case judgements complete. Partial reviews are allowed; unjudged cases stay missing.`;
  }
  function render() {
    const q=packet.queries.find(q=>q.query_id===$("query-choice").value);
    $("situation").replaceChildren(node("h2",`Situation ${q.query_id}`),node("p",q.text),node("p",`Information available by ${q.cutoff}. Comparison situation ends ${q.before_period_end}; source periods must end earlier.`));
    $("cases").replaceChildren();
    if(!q.items.length) $("cases").append(node("p","No cases meet these dates. Please leave a situation note below."));
    q.items.forEach((c,index)=>{
      const row=response.judgements.find(r=>r.query_id===q.query_id && r.item_id===c.item_id);
      const article=node("article");article.dataset.itemId=c.item_id;
      article.append(node("h3",`Case ${index+1}: ${c.company}`),node("p",`Report covers ${c.period.start} to ${c.period.end}. Published ${c.published}.`),node("p",`Business covered: ${c.business_scope}`),node("p",pressureLabel(c.fields.pressure.value)));
      link(article,c.fields.pressure.evidence);
      const details=node("details");details.append(node("summary","Figures, company actions, differences and unknowns"));
      for(const [key,title] of [["margin_or_profit","Reported profit"],["other_drivers","What else was changing"],["response","What the company said it did"]]) {details.append(node("h4",title),node("p",pressureLabel(c.fields[key].value)));link(details,c.fields[key].evidence);}
      metric(details,c.metric);c.figures.forEach(m=>metric(details,m));
      c.conflicts.forEach(conflict=>{details.append(node("p",`Source disagreement: ${explainBasisPoints(conflict.value)}`));conflict.sources.forEach(s=>link(details,s));});
      list(details,"Important differences",c.important_differences.map(differenceLabel));list(details,"What remains unknown",unknownLabels(c.unknowns));
      if(c.source.excerpt)details.append(node("blockquote",c.source.excerpt));link(details,c.source);article.append(details);
      field(article,"Is this a useful comparison?",row.usefulness,v=>row.usefulness=v,[["useful","Useful"],["partly_useful","Partly useful"],["not_useful","Not useful"],["unsure","Unsure"]]).dataset.field="usefulness";
      field(article,"Why? Include the matching issue, differences or uncertainty.",row.reason,v=>row.reason=v).dataset.field="reason";
      field(article,"Would presenting this case as a comparison mislead a reader?",row.misleading,v=>row.misleading=v,[["yes","Yes"],["no","No"],["unsure","Unsure"]]).dataset.field="misleading";
      field(article,"Explain yes or unsure",row.misleading_reason,v=>row.misleading_reason=v).dataset.field="misleading_reason";
      field(article,"Original source access",row.source_access,v=>row.source_access=v,[["opened","Opened an original report"],["not_opened","Did not open a report"],["unavailable","Tried but source unavailable"]]).dataset.field="source_access";
      field(article,"Source-access problem or additional uncertainty (required if unavailable)",row.source_note,v=>row.source_note=v).dataset.field="source_note";
      $("cases").append(article);
    });
    const note=response.queries.find(r=>r.query_id===q.query_id);
    $("coverage").replaceChildren(node("h2","What is missing from this collection?"));
    field($("coverage"),"How well do the supplied eligible cases cover this situation?",note.coverage,v=>note.coverage=v,[["adequate","Adequate"],["limited","Limited"],["none","No useful coverage"],["unsure","Unsure"]]);
    field($("coverage"),"Why?",note.reason,v=>note.reason=v);
    field($("coverage"),"Missing case or source suggestions, if known (optional)",note.missing_cases,v=>note.missing_cases=v);
    progress();
  }
  function syncReviewer() {
    response.reviewer_id=$("reviewer-id").value.trim();
    response.attestation={human:$("human").checked,created_cases_or_rules:$("independent").checked?false:null,seen_expected_answers:$("blind").checked?false:null,used_ai_judgements:$("no-ai").checked?false:null,prior_exposure:$("exposure").value};
  }
  function message(text) {$("message").textContent=text;$("message").focus();}
  function download(draft) {
    syncReviewer();const issues=exportProblems(response);
    if(!draft && issues.length){message(issues.slice(0,8).join("\n"));return;}
    const url=URL.createObjectURL(new Blob([JSON.stringify(response,null,2)+"\n"],{type:"application/json"}));
    const a=node("a");a.href=url;a.download=draft?"m008-draft.json":"m008-review.json";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    message(draft?"Draft downloaded. Keep this file to resume; nothing was sent.":"Review exported. Return the file through the agreed review channel. Partial responses will be reported as incomplete.");
  }
  packet.queries.forEach((q,index)=>{const o=node("option",`Situation ${index+1} of ${packet.queries.length} (${q.query_id})`);o.value=q.query_id;$("query-choice").append(o);});
  $("query-choice").addEventListener("change",render);
  $("save-draft").addEventListener("click",()=>download(true));$("export-review").addEventListener("click",()=>download(false));
  $("load-draft").addEventListener("change",async()=>{
    try {
      const f=$("load-draft").files[0];if(!f)return;if(f.size>2000000)throw new Error("This file is too large for a review response.");
      response=restoreResponse(packet,JSON.parse(await f.text()));$("reviewer-id").value=response.reviewer_id;
      $("human").checked=response.attestation.human===true;$("independent").checked=response.attestation.created_cases_or_rules===false;$("blind").checked=response.attestation.seen_expected_answers===false;$("no-ai").checked=response.attestation.used_ai_judgements===false;$("exposure").value=response.attestation.prior_exposure;
      render();message("Saved responses loaded. Nothing was sent.");
    }catch(error){message(`Could not load that file: ${error.message}`);}finally{$("load-draft").value="";}
  });
  render();
}
if(typeof document!=="undefined" && document.getElementById("packet-data")) startReview();
