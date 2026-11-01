import test from "node:test";
import assert from "node:assert/strict";
import {blankResponse,restoreResponse,rowComplete,exportProblems} from "../assets/review/review.mjs";
const packet={packet_id:"synthetic-test-only",queries:[{query_id:"Q1",items:[{item_id:"A"},{item_id:"B"}]}]};

test("blank drafts contain no implied judgements or human attestation",()=>{
  const r=blankResponse(packet);
  assert.equal(r.judgements.length,2);assert.ok(r.judgements.every(j=>j.usefulness===null));
  assert.equal(r.attestation.human,false);assert.equal(r.attestation.created_cases_or_rules,null);
  assert.ok(exportProblems(r).length>0);
});
test("restoring drafts preserves text/uncertainty and cannot change the packet",()=>{
  const r=blankResponse(packet);r.judgements[0].reason="</script> stays text";r.judgements[0].usefulness="unsure";
  assert.deepEqual(restoreResponse(packet,r),r);
  assert.throws(()=>restoreResponse(packet,{...r,packet_id:"wrong"}),/different packet/);
  assert.throws(()=>restoreResponse(packet,{...r,judgements:[...r.judgements,r.judgements[0]]}),/repeated case/);
  assert.throws(()=>restoreResponse(packet,{...r,judgements:[{...r.judgements[0],item_id:"unknown"}]}),/unknown/);
  assert.throws(()=>restoreResponse(packet,{...r,judgements:[{...r.judgements[0],usefulness:"excellent"}]}),/Invalid case category/);
});
test("partial export retains unjudged cases; started judgements require rationales",()=>{
  const r=blankResponse(packet);r.reviewer_id="SYNTHETIC_ONLY";
  r.attestation={human:true,created_cases_or_rules:false,seen_expected_answers:false,used_ai_judgements:false,prior_exposure:"synthetic test"};
  const row=r.judgements[0];Object.assign(row,{usefulness:"partly_useful",reason:"Synthetic partial overlap.",misleading:"no",source_access:"not_opened"});
  assert.ok(rowComplete(row));assert.deepEqual(exportProblems(r),[]);
  assert.equal(r.judgements[1].usefulness,null);
  row.misleading="unsure";assert.ok(exportProblems(r).some(p=>p.includes("required explanations")));
  row.misleading_reason="Synthetic uncertainty";row.source_access="unavailable";
  assert.ok(!rowComplete(row));row.source_note="Synthetic access failure";assert.ok(rowComplete(row));
});
