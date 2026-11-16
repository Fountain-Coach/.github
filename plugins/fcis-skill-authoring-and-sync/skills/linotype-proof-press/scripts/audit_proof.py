#!/usr/bin/env python3
"""Independent exact-folio provenance audit for a Fountain Press proof run.

No publishing, source changes or visual approval. Supports arbitrary 1000+ pages.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
from collections import defaultdict
import sys


def sha(data):return hashlib.sha256(data).hexdigest()


def audit(root:Path, require_complete:bool=False, write:bool=False):
    root=root.resolve(strict=True)
    run=json.loads((root/'run.json').read_text('utf8'))
    if run.get('schema')!='fountain.press.proof-run.v1':raise ValueError('Unsupported proof run schema')
    platforms=run.get('platforms',[]);works=run.get('expectedWorks',[])
    if not platforms or not works or len({w['id'] for w in works})!=len(works):raise ValueError('Invalid admitted proof inventory')
    wanted={(p,w['id']) for p in platforms for w in works}
    if set(run['expectedFolios'])!=set(platforms):raise ValueError('Missing platform proof inventory')
    seen=set();seenShots=set();addresses=defaultdict(set);intervals=defaultdict(list);unranged=defaultdict(list);entries=[];missingFiles=[];findings=defaultdict(int)
    with (root/'pages.jsonl').open(encoding='utf8') as stream:
        for line_number,line in enumerate(stream,1):
            if not line.strip():continue
            row=json.loads(line)
            if row.get('schema')!='fountain.press.folio-proof.v1':raise ValueError(f'Unexpected page record line {line_number}')
            key=(row['platform'],row['work']);identity=(*key,row['folio'])
            if key not in wanted:raise ValueError('Unadmitted work/platform: '+str(key))
            expected=run['expectedFolios'][key[0]][key[1]]
            if row['total']!=expected['count'] or row['sourceSHA256']!=expected.get('sourceSha'):
                raise ValueError('Page source or count drift: '+str(identity))
            if not isinstance(row['folio'],int) or not 1<=row['folio']<=expected['count']:
                raise ValueError('Out-of-range folio: '+str(identity))
            if identity in seen:raise ValueError('Duplicate physical folio: '+str(identity))
            seen.add(identity)
            rel=Path(row['screenshot'])
            if str(rel) in seenShots:raise ValueError('Duplicate screenshot path: '+str(rel))
            seenShots.add(str(rel))
            actual=(root/rel).resolve()
            if actual.is_symlink() or not actual.is_relative_to(root) or not actual.is_file():
                missingFiles.append(str(rel))
            else:
                data=actual.read_bytes()
                if len(data)<8 or data[:8]!=b'\x89PNG\r\n\x1a\n' or sha(data)!=row['screenshotSHA256']:
                    missingFiles.append(str(rel))
            for item in row.get('sourceFragments',[]):
                if item.get('id'):
                    addresses[key].add(item['id'])
                    if isinstance(item.get('from'),int) and isinstance(item.get('to'),int):
                        intervals[(*key,item['id'])].append((item['from'],item['to']))
                    else:
                        unranged[(*key,item['id'])].append(item.get('textLength'))
            for severity in ('blocking','review'):
                for finding in row.get(severity,[]):findings[severity+':'+finding]+=1
            entries.append(row)
    defects=[];incomplete=[];sourceCoverage={'rangeVerified':0,'singleUnrangedTextVerified':0,'identifierOnly':0,'unverifiedExamples':[]}
    for p,work in sorted(wanted):
        source=run['expectedFolios'][p].get(work)
        if source is None:incomplete.append(f'{p}/{work}: no composed folio count');continue
        n=source['count']
        if not isinstance(n,int) or n<1:raise ValueError('Invalid composed folio count '+str((p,work)))
        absent=[i for i in range(1,n+1) if (p,work,i) not in seen]
        if absent:incomplete.append(f'{p}/{work}: missing {len(absent)} folios (first: {absent[:8]})')
        expected_ids=set(source.get('sourceBlocks',[]));not_seen=expected_ids-addresses[(p,work)]
        if not_seen:incomplete.append(f'{p}/{work}: {len(not_seen)} source blocks unrepresented (first: {sorted(not_seen)[:6]})')
        for expected in source.get('sourceRanges',[]):
            source_id=expected['id'];start=expected['from'];end=expected['to']
            if not all(isinstance(v,int) for v in (start,end)) or start>end:
                defects.append(f'{p}/{work}: invalid source range {source_id}');continue
            ranges=sorted(intervals[(*((p,work)),source_id)])
            pos=start
            for begin,finish in ranges:
                if begin!=pos or finish<begin or finish>end:
                    defects.append(f'{p}/{work}: lost, duplicated or out-of-order source interval {source_id} at {begin}:{finish} (expected next {pos})')
                    break
                pos=finish
            else:
                if pos!=end:incomplete.append(f'{p}/{work}: source range {source_id} ends at {pos} of {end}')
        # A source identity alone does not prove that all characters survived
        # pagination. Verify actual contiguous character offsets whenever the
        # compositor exposes them; fail closed on gaps or overlaps.
        for source_item in source.get('sourceBlockLengths',[]):
            ident=source_item['id'];raw=source_item['length'];trim=source_item['trimmedLength']
            if not isinstance(raw,int) or not isinstance(trim,int) or raw<0 or trim<0:
                defects.append(f'{p}/{work}: invalid original source length {ident}');continue
            spans=sorted(intervals[(p,work,ident)])
            if spans:
                position=0;bad=False
                for begin,finish in spans:
                    if begin!=position or finish<=begin or finish>raw:
                        defects.append(f'{p}/{work}: source character gap/overlap {ident} at {begin}:{finish}, expected next {position} of {raw}')
                        bad=True;break
                    position=finish
                if not bad:
                    if position not in (raw,trim):
                        defects.append(f'{p}/{work}: lost source tail {ident}: reached {position}, expected {raw} or {trim}')
                    else:sourceCoverage['rangeVerified']+=1
            else:
                pieces=unranged[(p,work,ident)]
                if (source_item.get('tag') not in ('figure','svg') and len(pieces)==1
                    and isinstance(pieces[0],int) and pieces[0] in (raw,trim)):
                    sourceCoverage['singleUnrangedTextVerified']+=1
                else:
                    sourceCoverage['identifierOnly']+=1
                    if len(sourceCoverage['unverifiedExamples'])<12:
                        sourceCoverage['unverifiedExamples'].append(f'{p}/{work}/{ident} ({source_item.get("tag")})')
        if source.get('pageErrors'):defects.append(f'{p}/{work}: browser errors {source["pageErrors"][:4]}')
    if missingFiles:defects.append('Missing or modified PNG proofs: '+repr(missingFiles[:10]))
    if findings and any(k.startswith('blocking:') for k in findings):defects.append('Blocking geometry/asset findings remain')
    total_expected=sum(run['expectedFolios'][p][w['id']]['count'] for p in platforms for w in works if w['id'] in run['expectedFolios'][p])
    if total_expected!=len(seen):incomplete.append(f'Expected {total_expected} physical folios, captured {len(seen)}')
    scope_partial=run.get('limit',0)>0 or bool(run.get('requestedWorks')) or len(platforms)!=4
    if scope_partial:incomplete.append('Explicit scoped run; not a complete edition/platform acceptance')
    if run.get('state')=='FAILED':defects.append('Browser capture failed: '+str(run.get('failure','unknown'))[:250])
    if run.get('state')=='IN_PROGRESS':incomplete.append('Browser capture not finished')
    status='BLOCKED' if defects else 'INCOMPLETE' if incomplete else 'INVENTORY_COMPLETE_REVIEW_REQUIRED'
    summary={'schema':'fountain.press.proof-audit.v1','state':status,'machineChecks':'EXACT_FOLIO_AND_SCREENSHOT_COVERAGE',
      'editorialAcceptance':'NOT_ESTABLISHED','physicalIpadAcceptance':'NOT_ESTABLISHED',
      'runSourceReleaseID':run.get('edition',{}).get('sourceReleaseID'),
      'expectedWorks':len(works),'testedPlatforms':platforms,'expectedFolios':total_expected,'capturedFolios':len(seen),
      'failedEvidence':defects,'incomplete':incomplete,'findings':dict(sorted(findings.items())),
      'characterCoverage':sourceCoverage}
    if write:
        output=root/'audit.json'
        if output.exists():raise ValueError('Refusing overwrite existing audit receipt')
        output.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
        out=root/'index.html'
        if out.exists():raise ValueError('Refusing overwrite existing contact-sheet view')
        body=[]
        for row in sorted(entries,key=lambda r:(r['platform'],r['work'],r['folio'])):
            label=f"{row['platform']} / {row['work']} / {row['folio']:05d} of {row['total']}"
            sev='blocking' if row.get('blocking') else 'review' if row.get('review') else 'measured'
            body.append(f'<figure class="{sev}"><img loading="lazy" src="{html.escape(row["screenshot"],quote=True)}" alt="{html.escape(label,quote=True)}"><figcaption>{html.escape(label)} · {sev}</figcaption></figure>')
        out.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>Fountain Press — Private Proof Sheets</title><style>body{background:#eee9df;color:#262927;font:15px Georgia,serif;margin:2rem}h1{font-weight:normal}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1.5rem}figure{margin:0}img{width:100%;height:auto;box-shadow:0 3px 8px #0002}figcaption{font-size:11px;line-height:1.5;padding:.5em}.blocking{outline:2px solid #a00}.review{outline:1px dashed #876}</style><h1>Fountain Press — Proof sheets</h1><p>Machine inventory and per-folio visual evidence only. Not an editorial approval.</p><main>'+''.join(body)+'</main></html>')
    if require_complete and status!='INVENTORY_COMPLETE_REVIEW_REQUIRED':raise ValueError('Proof not complete: '+json.dumps(summary))
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--require-complete',action='store_true');p.add_argument('--write',action='store_true');a=p.parse_args()
    try:result=audit(a.directory,a.require_complete,a.write)
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:raise SystemExit('REFUSED: '+str(exc))
    print(json.dumps(result,indent=2,ensure_ascii=False))
