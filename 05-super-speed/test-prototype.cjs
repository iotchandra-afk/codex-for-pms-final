/* End-to-end prototype validation; all browser data stays in this module. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const root=__dirname, temp=path.join(root,'.browser-temp'),evidence=path.join(root,'evidence');
fs.mkdirSync(temp,{recursive:true});fs.mkdirSync(evidence,{recursive:true});
process.env.TEMP=temp;process.env.TMP=temp;
const {chromium}=require(process.argv[2]||process.env.ROOK_PLAYWRIGHT_MODULE||'playwright');
const results=[],errors=[],network=[];
let context,page;
const gates=['availability','capability','region','travel','supply'];
async function snap(){return page.evaluate(()=>window.__rook.getSnapshot());}
async function reset(){await page.goto(pathToFileURL(path.join(root,'prototype.html')).href);await page.locator('h1').waitFor();}
async function tab(role){await page.locator('#tab-'+role).click();}
async function request(){await page.locator('#requestReview').click();}
async function ready(){await tab('responder');await page.locator('#readyAck').check();await page.locator('#confirmReady').click();}
async function checkGates(){await tab('operations');for(const g of gates)await page.locator('#gate-'+g).check();}
async function approved(){await request();await ready();await checkGates();await page.locator('#approveReview').click();}
async function offered(){await approved();await page.locator('#issueOffer').click();}
async function test(name,fn){try{await reset();await fn();results.push({name,passed:true});console.log('PASS '+name);}catch(e){results.push({name,passed:false,error:e.message});console.log('FAIL '+name+': '+e.message);}}
(async()=>{
 try{
 const opts={headless:true,viewport:{width:1440,height:1000},downloadsPath:path.join(temp,'downloads'),args:['--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-breakpad','--disable-crash-reporter']};
 if(!fs.existsSync(chromium.executablePath()))opts.channel='msedge';
 context=await chromium.launchPersistentContext(path.join(temp,'profile'),opts);
 page=await context.newPage();
 page.on('pageerror',e=>errors.push(e.message));
 page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});
 await context.route(/^https?:/,route=>route.abort());
 await test('01 verified historical evidence renders',async()=>{
  const s=await snap();assert.equal(s.historical.length,7);assert.equal(s.historical.filter(x=>x.outcome==='missed').length,4);
  assert.match(await page.locator('[data-testid="mite-offers"]').innerText(),/1/);
  assert.match(await page.locator('body').innerText(),/Evidence snapshot: 6 September 2026/);
  await page.screenshot({path:path.join(evidence,'handler-desktop.png'),fullPage:true});
 });
 await test('02 operations cannot approve without request or readiness',async()=>{
  await tab('operations');assert.equal(await page.locator('#approveReview').isDisabled(),true);
  assert.equal(await page.locator('#issueOffer').isDisabled(),true);
 });
 await test('03 completed fit checks do not substitute for responder confirmation',async()=>{
  await request();await checkGates();
  assert.equal(await page.locator('#approveReview').isDisabled(),true);
  assert.equal((await snap()).state.ready,false);
 });
 await test('04 readiness requires an explicit acknowledgement',async()=>{
  await request();await tab('responder');
  assert.equal(await page.locator('#confirmReady').isDisabled(),true);
  await page.locator('#readyAck').check();await page.locator('#confirmReady').click();
  const s=await snap();assert.equal(s.state.review,'ready');assert.equal(s.state.ready,true);
  assert.equal(s.availabilityRecord.status,'Unverified in this prototype');
 });
 await test('05 every fit and maintenance gate is required',async()=>{
  await request();await ready();await tab('operations');
  for(const g of gates){assert.equal(await page.locator('#approveReview').isDisabled(),true);await page.locator('#gate-'+g).check();}
  assert.equal(await page.locator('#approveReview').isDisabled(),false);
  await page.screenshot({path:path.join(evidence,'operations-review.png'),fullPage:true});
 });
 await test('06 approval is bounded and records a decision note',async()=>{
  await request();await ready();await checkGates();
  await page.locator('#reviewNote').fill('Readiness and incident fit checked for one demo opportunity.');
  await page.locator('#approveReview').click();
  const s=await snap();assert.equal(s.state.review,'approved');assert.equal(s.state.expiresAt,120);
  assert.match(s.state.events.at(-1).detail,/one appropriate offer/);
  assert.match(s.state.events.at(-1).detail,/Readiness and incident fit/);
 });
 await test('07 a 75-second response is accepted within the proposed window',async()=>{
  await offered();assert.equal((await snap()).state.role,'responder');
  await page.locator('#advance75').click();assert.match(await page.locator('[data-testid="offer-timer"]').innerText(),/15/);
  await page.screenshot({path:path.join(evidence,'responder-live.png'),fullPage:true});
  await page.locator('#takeOffer').click();
  const s=await snap();assert.equal(s.state.offer.outcome,'taken');assert.equal(s.state.review,'completed');
  assert.equal(s.historical.length,7);assert.equal(s.historical.filter(x=>x.outcome==='taken').length,1);
 });
 await test('08 deadline expiry remains missed and requires follow-up',async()=>{
  await offered();await page.locator('#advance75').click();await page.locator('#advance15').click();
  const s=await snap();assert.equal(s.state.review,'followup');assert.equal(s.state.offer.outcome,'missed');
  assert.equal(s.availabilityRecord.status,'Unverified in this prototype');
  assert.match(await page.locator('.phonebody').innerText(),/No answer arrived/);
  assert.equal(s.state.events.some(e=>e.type==='Explicit decline recorded'),false);
 });
 await test('09 explicit decline stays distinct from missed',async()=>{
  await offered();await page.locator('#declineOffer').click();
  const s=await snap();assert.equal(s.state.offer.outcome,'turned down');assert.equal(s.state.review,'completed');
  assert.equal(s.state.events.at(-1).type,'Explicit decline recorded');
 });
 await test('10 changed fit pauses authorization before an offer',async()=>{
  await approved();await page.locator('#gate-capability').uncheck();
  assert.equal((await snap()).state.review,'paused');assert.equal(await page.locator('#issueOffer').isDisabled(),true);
  await page.locator('#gate-capability').check();await page.locator('#approveReview').click();
  assert.equal((await snap()).state.review,'approved');
 });
 await test('11 changed fit withdraws a live offer without inferring refusal',async()=>{
  await offered();await tab('operations');await page.locator('#gate-travel').uncheck();
  const s=await snap();assert.equal(s.state.review,'followup');assert.equal(s.state.offer.outcome,'withdrawn_fit_change');
  await tab('responder');assert.match(await page.locator('.phonebody').innerText(),/Withdrawn/);
  assert.equal((await page.locator('.phonebody').innerText()).includes('withdrawn_fit_change'),false);
 });
 await test('12 expiry blocks issue and requires fresh review confirmation',async()=>{
  await approved();await page.locator('#advanceWindow').click();
  assert.equal((await snap()).state.review,'expired');assert.equal(await page.locator('#issueOffer').isDisabled(),true);
  await tab('handler');await page.locator('#requestReview').click();
  const s=await snap();assert.equal(s.state.review,'requested');assert.equal(s.state.ready,false);
  assert.equal(Object.values(s.state.gates).some(Boolean),false);assert.equal(s.state.reviewId,'RR-DEMO-002');
 });
 await test('13 historical evidence and availability survive the full journey',async()=>{
  const before=await snap();await offered();await page.locator('#takeOffer').click();const after=await snap();
  assert.deepEqual(after.historical,before.historical);assert.deepEqual(after.availabilityRecord,before.availabilityRecord);
  await tab('operations');assert.equal(await page.locator('#issueOffer').isDisabled(),true);
 });
 await test('14 controlled comparison is explicit and does not change evidence',async()=>{
  const before=await snap();await page.locator('#run75').click();
  const text=await page.locator('#comparison').innerText();assert.match(text,/Missed at 60s/);assert.match(text,/Taken at 75s/);
  assert.deepEqual((await snap()).historical,before.historical);assert.equal((await snap()).state.review,'idle');
 });
 await test('15 keyboard tab navigation follows the selected workspace',async()=>{
  await page.locator('#tab-handler').focus();await page.keyboard.press('ArrowRight');
  assert.equal((await snap()).state.role,'responder');assert.equal(await page.locator('#tab-responder').getAttribute('aria-selected'),'true');
  await page.keyboard.press('End');assert.equal((await snap()).state.role,'operations');
 });
 await test('16 decision notes render as text in the audit receipt',async()=>{
  await request();await ready();await checkGates();
  await page.locator('#reviewNote').fill('<img src=x onerror="window.injected=true">');
  await page.locator('#approveReview').click();await page.locator('#showReceipt').click();
  assert.match(await page.locator('#receiptText').innerText(),/<img src=x/);
  assert.equal(await page.evaluate(()=>window.injected),undefined);
 });
 await test('17 all workspaces fit a 390-pixel viewport',async()=>{
  await page.setViewportSize({width:390,height:844});
  for(const role of ['handler','responder','operations']){
   await tab(role);
   const fit=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
   assert.ok(fit.scroll<=fit.width+1,role+' overflows: '+JSON.stringify(fit));
  }
  await tab('handler');await page.screenshot({path:path.join(evidence,'handler-mobile.png'),fullPage:true});
  await page.setViewportSize({width:1440,height:1000});
 });
 await test('18 reset clears simulated actions but retains the evidence',async()=>{
  await offered();await page.locator('#takeOffer').click();await page.locator('#resetDemo').click();
  const s=await snap();assert.equal(s.state.review,'idle');assert.equal(s.state.events.length,0);assert.equal(s.historical.length,7);
 });

 await test('19 displayed historical events match Module 3 source records',async()=>{
  const source=JSON.parse(fs.readFileSync(path.join(root,'../03-rewind/evidence/pings.json'),'utf8')).filter(r=>r.responder==='Meteor Mite'&&r.sent_at>='2026-08-17');
  const shown=(await snap()).historical;
  assert.deepEqual(shown.map(r=>({id:r.id,outcome:r.outcome,time:r.time})),source.map(r=>({id:r.callout_number,outcome:r.outcome,time:r.sent_at.slice(11,16)})));
 });
 await test('20 paired service measures stay historical after a demo acceptance',async()=>{
  const before=await page.getByLabel('Paired service scorecard').innerText();
  assert.match(before,/72.7%/);assert.match(before,/94.5%/);assert.match(before,/3/);
  await offered();await page.locator('#takeOffer').click();await tab('handler');
  assert.equal(await page.getByLabel('Paired service scorecard').innerText(),before);
 });
 await test('21 responder can pause readiness and must reconfirm it',async()=>{
  await approved();await tab('responder');await page.locator('#pauseReadiness').click();
  let s=await snap();assert.equal(s.state.review,'paused');assert.equal(s.state.ready,false);assert.equal(s.state.gates.availability,false);
  await page.locator('#readyAck').check();await page.locator('#confirmReady').click();
  await tab('operations');assert.equal(await page.locator('#approveReview').isDisabled(),true);
  await page.locator('#gate-availability').check();assert.equal(await page.locator('#approveReview').isDisabled(),false);
 });
 await test('22 responder pause withdraws a live offer without recording refusal',async()=>{
  await offered();await page.locator('#pauseReadiness').click();
  const s=await snap();assert.equal(s.state.review,'followup');assert.equal(s.state.offer.outcome,'withdrawn_readiness');
  assert.equal(s.state.ready,false);assert.match(await page.locator('.phonebody').innerText(),/Readiness paused/);
  assert.equal(s.availabilityRecord.status,'Unverified in this prototype');
  assert.equal(s.state.events.some(e=>e.type==='Explicit decline recorded'),false);
 });
 await test('23 mobile review entry is visible before scrolling',async()=>{
  await page.setViewportSize({width:390,height:844});
  const box=await page.locator('#quickReview').boundingBox();assert.ok(box&&box.y+box.height<844);
  await page.locator('#quickReview').click();assert.equal((await snap()).state.review,'requested');
  await page.setViewportSize({width:1440,height:1000});
 });

 }catch(e){errors.push(e.stack||e.message);}
 finally{
  const out={tests_run:results.length,passed:results.filter(r=>r.passed).length,failed:results.filter(r=>!r.passed).length,results,browser_errors:errors,external_network_requests:network,successful:results.length===23&&results.every(r=>r.passed)&&errors.length===0&&network.length===0,scope:'Browser-level validation of the standalone simulated prototype, not a production integration test.'};
  fs.writeFileSync(path.join(evidence,'prototype-validation.json'),JSON.stringify(out,null,2)+'\n');
  if(context)await context.close();
  console.log(JSON.stringify({tests:out.tests_run,passed:out.passed,failed:out.failed,browser_errors:errors.length,external_requests:network.length,successful:out.successful}));
  process.exitCode=out.successful?0:1;
 }
})();

