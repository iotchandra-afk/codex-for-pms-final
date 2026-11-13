/* Browser and print QA for the actual final presentation. All artifacts stay in the repo. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const directory=__dirname,root=path.dirname(directory),temp=path.join(directory,'.browser-temp');
fs.mkdirSync(temp,{recursive:true});process.env.TEMP=temp;process.env.TMP=temp;
const {chromium}=require(process.argv[2]||process.env.ROOK_PLAYWRIGHT_MODULE||'playwright');
const results=[],errors=[],network=[];let context,page;
const expectedTests=16;
const url=pathToFileURL(path.join(root,'final-report.html')).href;
async function test(name,fn){try{await fn();results.push({name,passed:true});console.log('PASS '+name);}catch(e){results.push({name,passed:false,error:e.message});console.log('FAIL '+name+': '+e.message);}}
function escape(s){return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');}
function markdown(text){
 const inline=s=>escape(s).replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2">$1</a>').replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/`([^`]+)`/g,'<code>$1</code>');
 return text.replace(/<!--[\s\S]*?-->/g,'').split(/\r?\n\r?\n/).map(block=>{
  if(/^#{1,6} /.test(block)){const n=block.match(/^#+/)[0].length;return `<h${n}>${inline(block.replace(/^#+ /,''))}</h${n}>`;}
  if(block.trim()==='---')return '<hr>';
  if(block.startsWith('- '))return '<ul>'+block.split(/\r?\n(?=- )/).map(x=>'<li>'+inline(x.replace(/^- /,''))+'</li>').join('')+'</ul>';
  return '<p>'+inline(block.replace(/\r?\n/g,' '))+'</p>';
 }).join('\n');
}
function pageCount(buffer){return (buffer.toString('latin1').match(/\/Type\s*\/Page\b/g)||[]).length;}
async function printMarkdown(rel,name,maxPages){
 const source=fs.readFileSync(path.join(root,rel),'utf8');
 const p=await context.newPage();
 await p.setContent(`<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${name}</title><style>@page{size:A4;margin:14mm}body{font:10.5pt/1.35 Arial,sans-serif;color:#132b36;margin:0}h1{font-size:18pt;margin:0 0 10px}h2{font-size:13pt;margin:13px 0 6px}h3{font-size:11pt;margin:10px 0 5px}p{margin:0 0 8px}ul{padding-left:18px;margin:6px 0 10px}li{margin:0 0 4px}a{color:#13786b;text-decoration:none}hr{border:0;border-top:1px solid #aaa;margin:13px 0}code{font-size:9pt}</style></head><body>${markdown(source)}</body></html>`);
 const pdf=await p.pdf({format:'A4',printBackground:true});const count=pageCount(pdf);
 fs.writeFileSync(path.join(directory,name+'.pdf'),pdf);await p.close();
 assert.ok(count>0&&count<=maxPages,`${name}: expected at most ${maxPages} pages, got ${count}`);
 return count;
}
(async()=>{
 let printPages={};
 try{
 const opts={headless:true,viewport:{width:1440,height:1000},downloadsPath:path.join(temp,'downloads'),args:['--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-breakpad','--disable-crash-reporter']};
 if(!fs.existsSync(chromium.executablePath()))opts.channel='msedge';
 context=await chromium.launchPersistentContext(path.join(temp,'profile'),opts);page=await context.newPage();
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});await context.route(/^https?:/,r=>r.abort());
 await page.goto(url);await page.locator('h1').waitFor();
 await test('01 executive conclusion and seven linked sections render',async()=>{assert.match(await page.locator('h1').innerText(),/Four responders didn't/);assert.equal(await page.locator('main>section').count(),7);assert.equal(await page.locator('.rail nav a').count(),7);await page.screenshot({path:path.join(directory,'report-desktop.png')});});
 await test('02 complementary metric views switch with correct state',async()=>{await page.locator('#viewAccess').click();assert.equal(await page.locator('#viewAccess').getAttribute('aria-pressed'),'true');assert.equal(await page.locator('#accessPanel').isVisible(),true);assert.match(await page.locator('#accessPanel').innerText(),/Farlight/);assert.equal(await page.locator('#headlinePanel').isVisible(),false);await page.locator('#viewHeadline').click();await page.locator('#evidence').screenshot({path:path.join(directory,'report-evidence.png')});});
 await test('03 metric switch supports keyboard activation',async()=>{await page.locator('#viewAccess').focus();await page.keyboard.press('Space');assert.equal(await page.locator('#viewAccess').getAttribute('aria-pressed'),'true');await page.locator('#viewHeadline').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#viewHeadline').getAttribute('aria-pressed'),'true');});
 await test('04 every local report link and anchor resolves',async()=>{const links=await page.locator('[href],[src]').evaluateAll(nodes=>nodes.flatMap(n=>[n.getAttribute('href'),n.getAttribute('src')].filter(Boolean)));for(const link of links){if(/^(https?:|data:)/.test(link))continue;if(link.startsWith('#')){assert.equal(await page.locator('[id="'+link.slice(1)+'"]').count(),1);}else{const resolved=path.resolve(root,link.split('#')[0]);assert.ok(resolved.startsWith(root+path.sep));assert.ok(fs.existsSync(resolved),link);}}});
 await test('05 navigation reaches mechanism and exposes current location',async()=>{await page.locator('.rail nav a[href="#mechanism"]').click();await page.waitForURL('**#mechanism');assert.match(await page.locator('#mechanism h2').innerText(),/trap/);assert.equal(await page.locator('.rail nav [aria-current="location"]').count(),1);await page.locator('#mechanism').screenshot({path:path.join(directory,'report-mechanism.png')});});
 await test('06 prototype walkthrough details expand and working artifact loads',async()=>{await page.locator('#recovery summary').click();assert.match(await page.locator('#recovery details').innerText(),/confirm all five/);const proto=await context.newPage();await proto.goto(pathToFileURL(path.join(root,'05-super-speed/prototype.html')).href);await proto.locator('h1').waitFor();assert.match(await proto.locator('body').innerText(),/Ready Review/);await proto.close();});
 await test('07 local screenshot asset loads without an external request',async()=>{await page.locator('.shot').scrollIntoViewIfNeeded();await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));});
 await test('08 mobile 390px view has no document overflow',async()=>{await page.setViewportSize({width:390,height:844});await page.goto(url);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));await page.screenshot({path:path.join(directory,'report-mobile.png')});});
 await test('09 tablet 768px view has no document overflow',async()=>{await page.setViewportSize({width:768,height:1024});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));});
 await test('10 report print contains both metric views and all seven sections',async()=>{await page.setViewportSize({width:1440,height:1000});await page.emulateMedia({media:'print'});assert.equal(await page.locator('#headlinePanel').isVisible(),true);assert.equal(await page.locator('#accessPanel').isVisible(),true);const pdf=await page.pdf({format:'A4',printBackground:true});printPages.report=pageCount(pdf);assert.ok(printPages.report>0);fs.writeFileSync(path.join(directory,'final-report.pdf'),pdf);await page.emulateMedia({media:'screen'});});
 await test('11 compact AGENTS context prints within two pages',async()=>{printPages.agents=await printMarkdown('AGENTS.md','agents-print',2);});
 await test('12 product brief prints within one page',async()=>{printPages.brief=await printMarkdown('05-super-speed/brief.md','brief-print',1);});
 await test('13 report uses no external resources and raises no browser errors',async()=>{assert.deepEqual(network,[]);assert.deepEqual(errors,[]);});
 await test('14 six prompt-result pairs exactly match the original prompt files',async()=>{const map=JSON.parse(fs.readFileSync(path.join(directory,'prompt-artifact-map.json'),'utf8'));assert.equal(map.modules.length,6);assert.equal(await page.locator('.module-proof').count(),6);for(const entry of map.modules){const original=fs.readFileSync(path.join(root,entry.prompt_file),'utf8').split(/^### \d+\.\s*$/m).slice(1)[entry.prompt_number-1].trim();const card=page.locator('.module-proof[data-module="'+entry.module+'"]');assert.equal(await card.locator('.exact-prompt').textContent(),original);assert.equal(entry.exact_prompt,original);assert.equal(await card.locator('.paired-artifact').getAttribute('href'),entry.artifact);assert.ok(fs.existsSync(path.join(root,entry.artifact)));}await page.locator('.module-proof[data-module="3"]').screenshot({path:path.join(directory,'report-prompt-pair.png')});});
 await test('15 actual embedded prototype completes the proposed 75-second response journey',async()=>{await page.locator('#showPrototype').click();assert.equal(await page.locator('#showPrototype').getAttribute('aria-expanded'),'true');const source=fs.readFileSync(path.join(root,'05-super-speed/prototype.html'),'utf8').replace(/\r\n/g,'\n');assert.equal((await page.locator('#prototypeFrame').getAttribute('srcdoc')).replace(/\r\n/g,'\n'),source);const frame=page.frameLocator('#prototypeFrame');await frame.locator('#requestReview').click();await frame.locator('#tab-responder').click();await frame.locator('#readyAck').check();await frame.locator('#confirmReady').click();await frame.locator('#tab-operations').click();for(const gate of ['availability','capability','region','travel','supply'])await frame.locator('#gate-'+gate).check();await frame.locator('#approveReview').click();await frame.locator('#issueOffer').click();await frame.locator('#advance75').click();assert.match(await frame.locator('[data-testid="offer-timer"]').innerText(),/15/);await frame.locator('#takeOffer').click();const state=await frame.locator('body').evaluate(()=>window.__rook.getSnapshot());assert.equal(state.state.offer.outcome,'taken');assert.equal(state.state.review,'completed');assert.equal(state.historical.length,7);await page.locator('#prototypeEmbed').screenshot({path:path.join(directory,'report-embedded-prototype.png')});});
 await test('16 visuals are embedded and prevention claims retain their limits',async()=>{const images=await page.locator('img').evaluateAll(nodes=>nodes.map(n=>n.getAttribute('src')));assert.ok(images.length>=3&&images.every(src=>src.startsWith('data:image/png;base64,')));assert.match(await page.locator('.skill-guardrails').innerText(),/does not monitor production routing, block releases or guarantee/);assert.deepEqual(network,[]);assert.deepEqual(errors,[]);});
 }catch(error){results.push({name:'Browser setup/completion',passed:false,error:error.message});console.error(error.message);}
 finally{if(context)await context.close();const record={reviewed_at:new Date().toISOString(),tests_run:results.length,passed:results.filter(r=>r.passed).length,failed:results.filter(r=>!r.passed).length,successful:results.length===expectedTests&&results.every(r=>r.passed),results,print_pages:printPages,browser_errors:errors,external_resource_requests:network,scope:'Actual final-report HTML, six verbatim prompt-result pairs, embedded unmodified prototype journey, source links, keyboard interaction, responsive layout and print QA; not an instructor grade or LMS submission.'};fs.writeFileSync(path.join(directory,'report-validation.json'),JSON.stringify(record,null,2)+'\n');console.log(JSON.stringify({tests_run:record.tests_run,passed:record.passed,successful:record.successful,print_pages:printPages}));process.exitCode=record.successful?0:1;}
})();
