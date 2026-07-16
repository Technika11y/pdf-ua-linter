import unittest

from pdfua.rules import check, has_errors

# A fully PDF/UA-conformant set of facts, per the implemented checks.
GOOD = {
    "tagged": True,
    "title": "Quarterly Report",
    "display_doc_title": True,
    "lang": "en-US",
    "figures": [{"alt": "Bar chart of revenue by quarter", "page": 2}],
    "pages": 3,
}


class RulesTests(unittest.TestCase):
    def test_conformant_facts_pass(self):
        self.assertFalse(has_errors(check(GOOD)))

    def test_untagged_is_error(self):
        self.assertTrue(any(f["rule"] == "pdfua-not-tagged" for f in check(dict(GOOD, tagged=False))))

    def test_missing_title_is_error(self):
        self.assertTrue(any(f["rule"] == "pdfua-no-title" for f in check(dict(GOOD, title=None))))

    def test_title_present_but_not_displayed_is_error(self):
        findings = check(dict(GOOD, display_doc_title=False))
        self.assertTrue(any(f["rule"] == "pdfua-title-not-displayed" for f in findings))

    def test_missing_lang_is_error(self):
        self.assertTrue(any(f["rule"] == "pdfua-no-lang" for f in check(dict(GOOD, lang=None))))

    def test_malformed_lang_warns(self):
        self.assertIn("pdfua-lang-malformed", [f["rule"] for f in check(dict(GOOD, lang="english"))])

    def test_figure_without_alt_is_error(self):
        findings = check(dict(GOOD, figures=[{"alt": None, "page": 1}]))
        self.assertTrue(any(f["rule"] == "pdfua-figure-no-alt" for f in findings))

    def test_figure_with_whitespace_alt_is_error(self):
        findings = check(dict(GOOD, figures=[{"alt": "   ", "page": 1}]))
        self.assertTrue(any(f["rule"] == "pdfua-figure-no-alt" for f in findings))

    def test_checkpoints_are_attached(self):
        f = next(x for x in check(dict(GOOD, tagged=False)) if x["rule"] == "pdfua-not-tagged")
        self.assertEqual(f["checkpoint"], "01-005")

    def test_title_that_is_a_filename_warns(self):
        self.assertIn("pdfua-title-is-filename", [f["rule"] for f in check(dict(GOOD, title="Report.pdf"))])

    def test_authoring_tool_title_warns(self):
        self.assertIn("pdfua-title-is-filename", [f["rule"] for f in check(dict(GOOD, title="Microsoft Word - draft"))])

    def test_descriptive_title_is_not_flagged(self):
        self.assertNotIn("pdfua-title-is-filename", [f["rule"] for f in check(GOOD)])

    def test_placeholder_figure_alt_warns(self):
        facts = dict(GOOD, figures=[{"alt": "image", "page": 1}])
        self.assertIn("pdfua-figure-alt-placeholder", [f["rule"] for f in check(facts)])

    def test_descriptive_figure_alt_not_flagged(self):
        self.assertNotIn("pdfua-figure-alt-placeholder", [f["rule"] for f in check(GOOD)])


if __name__ == "__main__":
    unittest.main()
