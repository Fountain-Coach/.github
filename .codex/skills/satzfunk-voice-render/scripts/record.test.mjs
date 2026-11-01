import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp, mkdir,writeFile,readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {run,parseArgs,wavFacts} from './record.mjs';

const sha=b=>createHash('sha256').update(b).digest('hex');
async function host() {
  const root=await mkdtemp(join(tmpdir(),'satzfunk-skill-test-'));
  await mkdir(join(root,'src'));
  await writeFile(join(root,'src','openai-voice.mjs'),
    'export function planSpeech(){}\nexport async function renderSpeech(){}\n');
  const source=join(root,'manuscript.txt');
  const text='On Continuity\n\nRead what is written. The page is the frame.';
  await writeFile(source,text,'utf8');
  const args=op=>[op,'--satzfunk-root',root,'--source',source,
    '--source-sha256',sha(Buffer.from(text)),'--work-id','on-continuity'];
  const id=`on-continuity-${sha(Buffer.from(text)).slice(0,12)}-cedar`;
  const dir=join(root,'drafts','voice-editions',id);
  return {root,source,text,args,id,dir};
}
function wav(frames=24000){
  const result=Buffer.alloc(44+frames*2);
  result.write('RIFF',0);result.writeUInt32LE(result.length-8,4);result.write('WAVEfmt ',8);
  result.writeUInt32LE(16,16);result.writeUInt16LE(1,20);result.writeUInt16LE(1,22);
  result.writeUInt32LE(24000,24);result.writeUInt32LE(48000,28);result.writeUInt16LE(2,32);
  result.writeUInt16LE(16,34);result.write('data',36);result.writeUInt32LE(frames*2,40);
  return result;
}

test('argument validation rejects wrong identity and voices',()=>{
  assert.throws(()=>parseArgs(['render']),/Missing required/);
  assert.throws(()=>parseArgs(['plan','--satzfunk-root','/t','--source','/x',
    '--source-sha256','f'.repeat(64),'--work-id','UPPER']),/Work ID/);
  assert.throws(()=>parseArgs(['plan','--satzfunk-root','/t','--source','/x',
    '--source-sha256','f'.repeat(64),'--work-id','book','--voice','imitate']),/admitted/);
});

test('WAV parser measures actual PCM frames, including streaming sentinel',()=>{
  const bytes=wav(48000);
  assert.equal(wavFacts(bytes).durationSeconds,2);
  bytes.writeUInt32LE(0xffffffff,40);
  assert.equal(wavFacts(bytes).frames,48000);
  assert.throws(()=>wavFacts(Buffer.from('fake audio')),/RIFF/);
});

test('plan is idempotent, exact-source digest is mandatory, no output is fabricated',async()=>{
  const h=await host();
  const first=await run(h.args('plan'));
  assert.equal(first.status,'PLANNED_NO_COST');
  const second=await run(h.args('plan'));
  assert.equal(second.id,first.id);
  const plan=JSON.parse(await readFile(join(h.dir,'plan.json'),'utf8'));
  assert.equal(plan.sourceSHA256,sha(Buffer.from(h.text)));
  await assert.rejects(run([...h.args('render'), '--voice', 'imitate']), /admitted/);
  await writeFile(h.source,h.text+' CHANGED');
  await assert.rejects(run(h.args('render')), /SOURCE_DIGEST_MISMATCH/);
  await assert.rejects(readFile(join(h.dir,'reading.wav')), {code:'ENOENT'});
});

test('one attempt is recorded before unavailable host credential; no automatic retry',async()=>{
  const h=await host();
  await run(h.args('plan'));
  await assert.rejects(run(h.args('render')),/Keychain|macOS/);
  const receipt=JSON.parse(await readFile(join(h.dir,'render-receipt.json'),'utf8'));
  assert.equal(receipt.attempts,1);
  assert.equal(receipt.status,'failed-inspect-before-retry');
  await assert.rejects(run(h.args('render')),/no automatic paid retry/);
});

test('verify rejects a fabricated or drifting receipt, accepts only exact measured audio and receipt',async()=>{
  const h=await host();
  await run(h.args('plan'));
  const raw=wav(72000);
  await writeFile(join(h.dir,'reading.wav'),raw);
  const receipt={schema:'satzfunk.voice-render-receipt.v1',id:h.id,
    sourceSHA256:sha(Buffer.from(h.text)),status:'rendered-private-unreviewed',
    audioSHA256:'0'.repeat(64),sampleRate:24000,frames:72000};
  await writeFile(join(h.dir,'render-receipt.json'),JSON.stringify(receipt));
  await assert.rejects(run(h.args('verify')),/drift/);
  receipt.audioSHA256=sha(raw);
  await writeFile(join(h.dir,'render-receipt.json'),JSON.stringify(receipt));
  const verified=await run(h.args('verify'));
  assert.equal(verified.status,'VERIFIED_AUDIO_BYTES_NOT_AUDITIONED');
  assert.equal(verified.durationSeconds,3);
});
