"""Regression for 16 Nov source-pinned Fountain Press frontend maintenance lesson.

Policy verification only: this does not prove an actual site fix or device test.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
LINOTYPE = ROOT / '.codex/skills/linotype-estate-template'
PUBLISHER = ROOT / '.codex/skills/estate-publisher-deployment'

class BookshelfPublishedFrontendTests(unittest.TestCase):
    def test_existing_skills_own_the_procedure_and_link_reference(self):
        l = (LINOTYPE / 'SKILL.md').read_text()
        p = (PUBLISHER / 'SKILL.md').read_text()
        for term in ('deterministic CMS-like frontend',
                     'references/bookshelf-published-frontend.md',
                     '/estate/read/library/',
                     'hard-coded collection arrays',
                     'status-bearing admitted publication snapshot'):
            self.assertIn(term, l)
        self.assertIn('../linotype-estate-template/references/bookshelf-published-frontend.md', p)
        self.assertIn('legacy route that returns HTTP 200 with fewer published books', p)

    def test_source_authority_and_negative_navigation_regressions(self):
        text = (LINOTYPE / 'references/bookshelf-published-frontend.md').read_text()
        for term in ('54ac999f65d8d81a9c74aae7a173c343cd6dcab7',
                     'active-public', 'archived-public', 'staged/private',
                     'same source/release', 'top-level sibling',
                     'first/last controls', 'gallery count constants',
                     'visible horizontal continuation',
                     'stale hashed Reader module', 'source template incorrectly nested',
                     'different selected work in the two projections',
                     'one status-bearing', 'HTTP 200',
                     'physical iPad Safari/VoiceOver'):
            self.assertIn(term, text)
        self.assertIn('not permanent counts', text)
        self.assertIn('no new database', text)

    def test_repro_baseline_distinguished_from_future_fix(self):
        text = (LINOTYPE / 'references/bookshelf-published-frontend.md').read_text()
        for term in ('Essays **10**', 'First Readings **32**', 'Orange Dot **23**',
                     '**7** Essays', '**13** essay templates'):
            self.assertIn(term, text)
        self.assertIn('not permanent counts or evidence that the frontend repair has been performed', text)
        self.assertIn('No release is implied', (PUBLISHER / 'SKILL.md').read_text())

    def test_mandatory_preflight_is_required_not_an_optional_skill_tip(self):
        lino = (LINOTYPE / 'SKILL.md').read_text()
        estate = (PUBLISHER / 'SKILL.md').read_text()
        ref = (LINOTYPE / 'references/bookshelf-published-frontend.md').read_text()
        for text in (lino, estate, ref):
            self.assertIn('publication_closure.py', text)
            self.assertIn('/estate/essays/', text)
            self.assertIn('EstatePublisher', text)
        self.assertIn('MUST execute', lino)
        self.assertIn('not eligible for activation', estate)
        self.assertIn('refuse activation', estate)
        self.assertIn('PUBLICATION_CLOSURE_REFUSED', lino)
        self.assertIn('PUBLISHER PREFLIGHT BINDING NOT ESTABLISHED', estate)

    def test_stage_mismatch_must_not_be_accepted_as_live_success(self):
        estate = (PUBLISHER / 'SKILL.md').read_text()
        lino = (LINOTYPE / 'SKILL.md').read_text()
        self.assertIn('mandatory refusal', lino)
        self.assertIn('stale Essays index', estate)
        self.assertIn('source preflight', lino)
        self.assertIn('independently re-run', estate)
        self.assertIn('original Reader', estate)


if __name__ == '__main__':
    unittest.main()
