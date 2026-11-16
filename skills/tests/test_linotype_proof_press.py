"""Seventh canonical FCIS Skill: an exhaustive folio-audit procedure, not approval."""
import importlib.util
import json
import hashlib
import base64
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
SKILL=ROOT/'.codex/skills/linotype-proof-press'
spec=importlib.util.spec_from_file_location('proof_audit',(SKILL/'scripts/audit_proof.py'))
module=importlib.util.module_from_spec(spec)
import sys
prior_bytecode=sys.dont_write_bytecode
try:
    sys.dont_write_bytecode=True  # Canonical Skill trees may not contain generated __pycache__.
    spec.loader.exec_module(module)
finally:
    sys.dont_write_bytecode=prior_bytecode
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9a6LZDoAAAAASUVORK5CYII=')


def populate(root,count=2,platforms=('ipad-portrait','ipad-landscape','desktop','phone'),omit=None):
    root.mkdir(parents=True,exist_ok=True)
    work='essay--source-proof'
    run={'schema':'fountain.press.proof-run.v1','state':'MACHINE_INVENTORY_COMPLETE',
         'platforms':list(platforms),'expectedWorks':[{'id':work,'book':'essays'}],
         'requestedWorks':None,'limit':0,'edition':{'sourceReleaseID':'private-v216'},
         'expectedFolios':{p:{work:{'count':count,'sourceSha':'sha','sourceBlocks':['source.p1'],'pageErrors':[],'captured':count}} for p in platforms}}
    (root/'run.json').write_text(json.dumps(run))
    lines=[]
    for p in platforms:
        for n in range(1,count+1):
            if omit==(p,n):continue
            rel=f'folios/{p}/{work}/folio-{n:05d}.png'
            dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(PNG)
            lines.append(json.dumps({'schema':'fountain.press.folio-proof.v1','platform':p,'work':work,
              'folio':n,'total':count,'sourceSHA256':'sha','sourceFragments':[{'id':'source.p1'}],
              'screenshot':rel,'screenshotSHA256':hashlib.sha256(PNG).hexdigest(),
              'blocking':[],'review':[]},separators=(',',':')))
    (root/'pages.jsonl').write_text('\n'.join(lines)+'\n')
    return run

class ProofPressSkillTests(unittest.TestCase):
    def test_explicit_seventh_identity_not_an_extra_publisher(self):
        text=(SKILL/'SKILL.md').read_text()
        for key in ('name: linotype-proof-press','1,000+ pages','scripts/audit_proof.py',
                    'source-addressed','EDITORIAL_REVIEW_REQUIRED',
                    'INVENTORY_COMPLETE_REVIEW_REQUIRED','physical iPad',
                    'another Reader','white space','EstatePublisher'):
            self.assertIn(key.lower(),text.lower())
        ref=(SKILL/'references/proof-contract.md').read_text()
        self.assertIn('1,000+ leaf runs',ref)
        self.assertIn('a low occupancy warning is a',ref)

    def test_ubuntu_macmini_is_only_current_owner_wlan_proof_host(self):
        policy=(SKILL/'SKILL.md').read_text()
        for phrase in ('benedikt-Macmini', 'MacBook Pro', 'must **not** render',
                       '192.168.8.50:8200', '/home/benedikt/fountain-press-proof/runs/',
                       'one isolated browser process per admitted work',
                       'host guard must reject', 'physical-device witness'):
            self.assertIn(phrase.lower(),policy.lower())
        self.assertIn('report the proof blocked',policy)
        self.assertIn('not an automatic workstation fallback',policy)

    def test_thousand_plus_per_platform_is_exactly_counted_without_editorial_self_approval(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);populate(root,count=1001)
            result=module.audit(root,require_complete=True)
            self.assertEqual(result['state'],'INVENTORY_COMPLETE_REVIEW_REQUIRED')
            self.assertEqual(result['expectedFolios'],4004)
            self.assertEqual(result['capturedFolios'],4004)
            self.assertEqual(result['editorialAcceptance'],'NOT_ESTABLISHED')

    def test_missing_one_leaf_of_two_refuses_completion(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);populate(root,omit=('ipad-landscape',2))
            result=module.audit(root)
            self.assertEqual(result['state'],'INCOMPLETE')
            with self.assertRaisesRegex(ValueError,'Proof not complete'):
                module.audit(root,require_complete=True)

    def test_single_corrupted_screenshot_refused(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);populate(root)
            (root/'folios/phone/essay--source-proof/folio-00002.png').write_bytes(b'fake')
            result=module.audit(root)
            self.assertEqual(result['state'],'BLOCKED')
            self.assertIn('Missing or modified PNG',str(result['failedEvidence']))

    def test_source_character_offsets_full_coverage_and_gap_refusal(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);populate(root)
            run=json.loads((root/'run.json').read_text())
            for platform in run['platforms']:
                entry=run['expectedFolios'][platform]['essay--source-proof']
                entry['sourceBlockLengths']=[{'id':'source.p1','length':10,'trimmedLength':10,'tag':'p'}]
            (root/'run.json').write_text(json.dumps(run))
            rows=[json.loads(x) for x in (root/'pages.jsonl').read_text().splitlines()]
            for row in rows:
                row['sourceFragments']=[{'id':'source.p1','from':0 if row['folio']==1 else 5,
                                         'to':5 if row['folio']==1 else 10,'textLength':5}]
            (root/'pages.jsonl').write_text('\n'.join(json.dumps(x) for x in rows)+'\n')
            result=module.audit(root,require_complete=True)
            self.assertEqual(result['characterCoverage']['rangeVerified'],4)
            rows[-1]['sourceFragments'][0]['from']=6
            (root/'pages.jsonl').write_text('\n'.join(json.dumps(x) for x in rows)+'\n')
            refused=module.audit(root)
            self.assertEqual(refused['state'],'BLOCKED')
            self.assertIn('source character gap/overlap',' '.join(refused['failedEvidence']))

    def test_review_warnings_are_not_automatic_print_approval(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);populate(root)
            lines=(root/'pages.jsonl').read_text().splitlines()
            row=json.loads(lines[0]);row['review']=['unusually-open-leaf-needs-editorial-judgment']
            lines[0]=json.dumps(row);(root/'pages.jsonl').write_text('\n'.join(lines)+'\n')
            result=module.audit(root,require_complete=True)
            self.assertEqual(result['state'],'INVENTORY_COMPLETE_REVIEW_REQUIRED')
            self.assertIn('review:unusually-open-leaf-needs-editorial-judgment',result['findings'])

if __name__=='__main__':unittest.main()
