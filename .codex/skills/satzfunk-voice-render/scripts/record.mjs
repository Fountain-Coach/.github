#!/usr/bin/env node
/**
 * Satzfunk source-bound voice recording, through the existing host adapter.
 * No alternate OpenAI HTTP implementation, no shell credential interpolation.
 * Supports deterministic plan / one-attempt render / verify.
 */
import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { dirname, isAbsolute, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const SKILL = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const sha = data => createHash('sha256').update(data).digest('hex');
const hex64 = /^[a-f0-9]{64}$/;
const slug = /^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$/;
const expectedSource = new Set(['--satzfunk-root', '--source', '--source-sha256', '--work-id']);
const allowedOptions = new Set([...expectedSource, '--voice', '--instructions-file']);

export function parseArgs(argv) {
  const [operation, ...rest] = argv;
  if (!['plan', 'render', 'verify'].includes(operation)) throw Error('Select plan, render, or verify');
  const options = {};
  for (let i = 0; i < rest.length; i += 2) {
    const flag = rest[i];
    if (!allowedOptions.has(flag) || !rest[i+1] || rest[i+1].startsWith('--') || flag in options)
      throw Error('Invalid or duplicated option: ' + String(flag));
    options[flag] = rest[i+1];
  }
  for (const flag of expectedSource) if (!options[flag]) throw Error('Missing required option: ' + flag);
  if (!hex64.test(options['--source-sha256'])) throw Error('Expected exact lowercase source SHA-256');
  if (!slug.test(options['--work-id'])) throw Error('Work ID must be a short lowercase hyphenated identity');
  const voice = options['--voice'] ?? 'cedar';
  if (!['cedar', 'marin'].includes(voice)) throw Error('Voice must be an admitted Satzfunk preset: cedar or marin');
  return { operation, root:resolve(options['--satzfunk-root']), source:resolve(options['--source']),
    sourceSHA256:options['--source-sha256'], workID:options['--work-id'], voice,
    instructionPath: resolve(options['--instructions-file'] ?? join(SKILL, 'assets', 'british-vergil.txt')) };
}

export function wavFacts(bytes) {
  if (!Buffer.isBuffer(bytes)) bytes = Buffer.from(bytes);
  if (bytes.length < 46 || bytes.toString('ascii', 0, 4) !== 'RIFF' ||
      bytes.toString('ascii', 8, 12) !== 'WAVE') throw Error('Not RIFF/WAVE data');
  let offset = 12, fmt = null, dataStart = -1, dataBytes = -1;
  while (offset + 8 <= bytes.length) {
    const kind = bytes.toString('ascii', offset, offset+4);
    const length = bytes.readUInt32LE(offset+4);
    const start = offset + 8;
    if (kind === 'fmt ') {
      if (length < 16 || start + length > bytes.length) throw Error('Invalid WAV fmt');
      fmt = { codec:bytes.readUInt16LE(start), channels:bytes.readUInt16LE(start+2),
        sampleRate:bytes.readUInt32LE(start+4), bitsPerSample:bytes.readUInt16LE(start+14) };
    }
    if (kind === 'data') {
      dataStart = start;
      dataBytes = length === 0xffffffff || length === 0 ? bytes.length - start : length;
      break;
    }
    if (length > bytes.length - start) throw Error('WAV chunk exceeds file');
    offset = start + length + (length & 1);
  }
  if (!fmt || dataStart < 0 || fmt.codec !== 1 || fmt.channels !== 1 ||
      fmt.bitsPerSample !== 16 || fmt.sampleRate !== 24000 ||
      dataBytes > bytes.length - dataStart || dataBytes < 48000 || dataBytes % 2 !== 0)
    throw Error('Expected measured mono PCM16 24kHz WAV, at least one second');
  const frames = dataBytes / 2;
  return { sampleRate:fmt.sampleRate, channels:fmt.channels, frames,
    durationSeconds:frames / fmt.sampleRate, pcmBytes:dataBytes };
}

function keychainCredential() {
  if (process.platform !== 'darwin') throw Error('The approved Keychain host is macOS; no fallback');
  const declared = [
    ['Reframe', 'modernization.settings.openaiApiKey'],
    ['com.fountain-coach.stage-native', 'openai.apiKey']
  ];
  for (const [service, account] of declared) {
    try {
      const key = execFileSync('/usr/bin/security',
        ['find-generic-password','-s',service,'-a',account,'-w'],
        {encoding:'utf8',stdio:['ignore','pipe','pipe'],timeout:25000}).trim();
      if (key.length <= 12) throw Error('Declared Keychain entry is empty');
      return key;
    } catch(error) {
      if (error.status === 44) continue;
      throw Error('Keychain credential retrieval refused by host; no alternate path');
    }
  }
  throw Error('No credential at the two declared Keychain references');
}

async function createContext(a) {
  if (!isAbsolute(a.root) || !isAbsolute(a.source)) throw Error('Absolute source and Satzfunk paths required');
  const sourceBytes = await readFile(a.source);
  const observed = sha(sourceBytes);
  if (observed !== a.sourceSHA256) throw Error('SOURCE_DIGEST_MISMATCH; paid action refused');
  const text = sourceBytes.toString('utf8');
  if (Buffer.from(text, 'utf8').compare(sourceBytes) !== 0 ||
      text.length === 0 || text.length > 4096 || !text.trim() || text.includes('\u0000'))
    throw Error('Source must be exact UTF-8 and 1-4096 characters');
  const instructionsBytes = await readFile(a.instructionPath);
  const instructions = instructionsBytes.toString('utf8').trim();
  if (!instructions || instructions.length > 2000 || instructions.includes('\u0000'))
    throw Error('Voice directions invalid');
  const ownerFile = await readFile(join(a.root,'src','openai-voice.mjs'));
  if (!ownerFile.includes(Buffer.from('export function planSpeech')) ||
      !ownerFile.includes(Buffer.from('export async function renderSpeech')))
    throw Error('Existing Satzfunk adapter unavailable; no substitute API path');
  const id = `${a.workID}-${a.sourceSHA256.slice(0,12)}-${a.voice}`;
  const dir = resolve(a.root, 'drafts', 'voice-editions', id);
  const outfile = join(dir, 'reading.wav');
  const sourcePlan = {
    schema:'satzfunk.source-bound-voice-plan.v1', id,
    workID:a.workID, narrator:'Vergil', voiceProfile:'British Vergil',
    sourceSHA256:a.sourceSHA256, characters:text.length, provider:'OpenAI',
    model:'gpt-4o-mini-tts', voice:a.voice, directionsSHA256:sha(instructionsBytes),
    requests:1, privateRehearsalAuthorized:true, publicReleaseAuthorized:false,
    disclosure:'AI-generated voice; not the author',
    status:'candidate; voice and exact spoken fidelity require audition'
  };
  return { a, text, instructions, dir, outfile, plan:sourcePlan,
    planFile:join(dir,'plan.json'), receiptFile:join(dir,'render-receipt.json') };
}

async function existingPlan(ctx) {
  try {
    const previous = JSON.parse(await readFile(ctx.planFile, 'utf8'));
    if (JSON.stringify(previous) !== JSON.stringify(ctx.plan))
      throw Error('Previous candidate plan differs; refuse changed input');
    return true;
  } catch(e) { if (e.code === 'ENOENT') return false; throw e; }
}

export async function run(argv, { getCredential = keychainCredential, loadAdapter = async root => import(pathToFileURL(join(root,'src','openai-voice.mjs'))) } = {}) {
  const args = parseArgs(argv);
  const ctx = await createContext(args);
  // Always inspect plan / existing output before any paid effect.
  const existed = await existingPlan(ctx);
  if (args.operation === 'plan') {
    if (!existed) {
      await mkdir(ctx.dir,{recursive:true});
      await writeFile(ctx.planFile,JSON.stringify(ctx.plan,null,2)+'\n',{flag:'wx'});
    }
    return {...ctx.plan,status:'PLANNED_NO_COST'};
  }
  if (args.operation === 'verify') {
    if (!existed) throw Error('No recorded source plan');
    const receipt = JSON.parse(await readFile(ctx.receiptFile,'utf8'));
    const bytes = await readFile(ctx.outfile);
    const facts = wavFacts(bytes);
    if (receipt.status !== 'rendered-private-unreviewed' ||
        receipt.audioSHA256 !== sha(bytes) || receipt.sourceSHA256 !== ctx.plan.sourceSHA256 ||
        receipt.frames !== facts.frames || receipt.sampleRate !== facts.sampleRate)
      throw Error('Audio/receipt drift; playback not admitted');
    return {status:'VERIFIED_AUDIO_BYTES_NOT_AUDITIONED',sourceSHA256:ctx.plan.sourceSHA256,
      audioSHA256:sha(bytes),...facts};
  }
  if (!existed) throw Error('Run plan first and review its exact source hash');
  for (const p of [ctx.receiptFile, ctx.outfile]) {
    try { await access(p); throw Error('Attempt or output exists: no automatic paid retry'); }
    catch(e) {if (e.code !== 'ENOENT') throw e;}
  }
  // Import the *existing* Satzfunk capability; do not implement another client.
  const {planSpeech,renderSpeech} = await loadAdapter(args.root);
  planSpeech({text:ctx.text,voice:args.voice,instructions:ctx.instructions,format:'wav'});
  const receipt={schema:'satzfunk.voice-render-receipt.v1',id:ctx.plan.id,
    sourceSHA256:ctx.plan.sourceSHA256,voice:args.voice,
    status:'attempt-recorded',attempts:1,startedAt:new Date().toISOString()};
  await writeFile(ctx.receiptFile,JSON.stringify(receipt,null,2)+'\n',{flag:'wx'});
  try {
    let key = getCredential();
    try {
      process.chdir(args.root);
      process.env.OPENAI_API_KEY = key; key = null;
      await renderSpeech({text:ctx.text,voice:args.voice,instructions:ctx.instructions,
        format:'wav',out:ctx.outfile});
    } finally {delete process.env.OPENAI_API_KEY; key = null;}
    const bytes = await readFile(ctx.outfile);
    const facts = wavFacts(bytes);
    Object.assign(receipt,{status:'rendered-private-unreviewed',audioSHA256:sha(bytes),
      audioBytes:bytes.length,finishedAt:new Date().toISOString(),
      sampleRate:facts.sampleRate,frames:facts.frames,durationSeconds:facts.durationSeconds});
    await writeFile(ctx.receiptFile,JSON.stringify(receipt,null,2)+'\n');
    return {status:'RENDERED_PRIVATE_UNREVIEWED',sourceSHA256:ctx.plan.sourceSHA256,
      audioSHA256:receipt.audioSHA256,durationSeconds:facts.durationSeconds,
      draftPath:ctx.outfile};
  } catch(e) {
    receipt.status='failed-inspect-before-retry';
    receipt.failure=String(e.message).replace(/sk-[A-Za-z0-9_-]+/g,'[redacted]');
    receipt.finishedAt=new Date().toISOString();
    await writeFile(ctx.receiptFile,JSON.stringify(receipt,null,2)+'\n');
    throw Error('Recording did not complete; inspect sanitized receipt. '+receipt.failure);
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  run(process.argv.slice(2)).then(v=>console.log(JSON.stringify(v,null,2)))
    .catch(e=>{console.error('REFUSED:',e.message);process.exitCode=1;});
}
