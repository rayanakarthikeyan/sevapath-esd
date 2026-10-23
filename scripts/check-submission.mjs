// Guard the judge-facing evidence and reproducible setup on each push.
import {readFileSync,existsSync,readdirSync} from 'node:fs';
import {resolve,dirname,join} from 'node:path';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';

const root=resolve(import.meta.dirname,'..');
const read=path=>readFileSync(join(root,path),'utf8');
const checks=[];
function check(name,fn){try{fn();checks.push({check:name,status:'PASS'});}catch(error){checks.push({check:name,status:'FAIL',reason:error.message});}}
const required=[
  'README.md','.env.example','package.json','package-lock.json','src/main.js','src/api.js','src/knowledge.js',
  'migrations/20261023135800_create-sevapath.sql','tests/core.test.mjs','scripts/test-cloud.mjs',
  'docs/API.md','docs/DATABASE.md','docs/TESTING.md','docs/TEST-CASES.md','docs/PROBLEM-EVIDENCE.md',
  'docs/PRIVACY.md','docs/PILOT.md','docs/DEMO.md','submission/BUILD-CHECKLIST.md',
  'submission/STATUS.md','submission/SevaPath-Submission-Brief.pdf',
  'docs/evidence/local-tests.txt','docs/evidence/cloud-results.json','docs/evidence/build.txt',
  'docs/evidence/home-desktop.png','docs/evidence/plan-cloud-restored.png','docs/evidence/plan-telugu-mobile.png'
];
check('Required build artifacts exist',()=>{for(const path of required)assert.ok(existsSync(join(root,path)),`Missing ${path}`);});
check('Judge-facing local Markdown links resolve',()=>{
  const docs=['README.md',...['docs','submission'].flatMap(dir=>readdirSync(join(root,dir)).filter(n=>n.endsWith('.md')).map(n=>`${dir}/${n}`))];
  for(const path of docs){
    for(const match of read(path).matchAll(/!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)/g)){
      const target=match[1].replace(/^<|>$/g,'');
      if(/^(https?:|mailto:|#)/.test(target))continue;
      const local=decodeURIComponent(target.split('#')[0]);
      assert.ok(existsSync(resolve(root,dirname(path),local)),`Broken link in ${path}: ${target}`);
    }
  }
});
check('Dependency versions are pinned and match the lockfile',()=>{
  const pkg=JSON.parse(read('package.json'));const locked=JSON.parse(read('package-lock.json')).packages[''];
  for(const section of ['dependencies','devDependencies']){
    assert.deepEqual(pkg[section],locked[section],`${section} differs from package-lock.json`);
    for(const [name,version] of Object.entries(pkg[section]||{}))assert.match(version,/^\d+\.\d+\.\d+$/,`${name} must use an exact version`);
  }
});
check('Private configuration and generated builds are not tracked',()=>{
  const tracked=execFileSync('git',['ls-files','-z'],{cwd:root,encoding:'utf8'}).split('\0').filter(Boolean);
  const forbidden=tracked.filter(p=>p!=='.env.example'&&(/(^|\/)\.env(?:\.|$)/.test(p)||/^(\.insforge|\.openai|node_modules|dist)\//.test(p)));
  assert.deepEqual(forbidden,[],'Remove private configuration/build output from Git');
});
check('Recorded local and cloud test outcomes are passing',()=>{
  const tap=read('docs/evidence/local-tests.txt');assert.match(tap,/# fail 0(?:\r?\n|$)/);assert.ok(/# pass [1-9]\d*/.test(tap));
  const cloud=JSON.parse(read('docs/evidence/cloud-results.json'));
  assert.equal(cloud.failed,0);assert.ok(cloud.results.length>0);
  assert.equal(cloud.passed,cloud.results.length);assert.ok(cloud.results.every(r=>r.status==='PASS'));
  assert.ok(!Number.isNaN(Date.parse(cloud.testedAt)));
});
check('Submission PDF is present and readable as a PDF container',()=>{
  const bytes=readFileSync(join(root,'submission/SevaPath-Submission-Brief.pdf'));
  assert.ok(bytes.subarray(0,5).equals(Buffer.from('%PDF-')));assert.ok(bytes.length>1000);
});
check('API contract includes concrete HTTP endpoints',()=>{
  const text=read('docs/API.md');assert.ok(text.includes('/api/database/rpc/sevapath_draft'));assert.ok(text.includes('/api/database/records/service_sources'));
});
for(const result of checks)console.log(`${result.status}: ${result.check}${result.reason?` - ${result.reason}`:''}`);
console.log(`${checks.filter(r=>r.status==='PASS').length}/${checks.length} submission checks passed. Historical evidence checks do not replace fresh runtime tests.`);
if(checks.some(r=>r.status==='FAIL'))process.exitCode=1;
