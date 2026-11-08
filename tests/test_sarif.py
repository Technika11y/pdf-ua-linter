import unittest

from pdfua.sarif import to_sarif


def f(rule="pdfua-not-tagged", severity="error", message="m", checkpoint="01-005"):
    return {"rule": rule, "severity": severity, "message": message, "checkpoint": checkpoint}


class SarifTests(unittest.TestCase):
    def test_envelope_is_sarif_210(self):
        s = to_sarif([f()], "a.pdf")
        self.assertEqual(s["version"], "2.1.0")
        self.assertIn("sarif-2.1.0", s["$schema"])
        self.assertEqual(s["runs"][0]["tool"]["driver"]["name"], "pdf-ua-linter")

    def test_level_mapping(self):
        s = to_sarif([f(severity="error"), f(rule="x", severity="warn"), f(rule="y", severity="info")])
        self.assertEqual([r["level"] for r in s["runs"][0]["results"]], ["error", "warning", "note"])

    def test_rules_deduped_and_carry_the_matterhorn_checkpoint(self):
        rules = to_sarif([f(), f()])["runs"][0]["tool"]["driver"]["rules"]
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["properties"]["matterhornCheckpoint"], "01-005")
        self.assertIn("matterhorn", rules[0]["helpUri"].lower())

    def test_target_pdf_is_the_artifact(self):
        s = to_sarif([f()], "reports/q3.pdf")
        uri = s["runs"][0]["results"][0]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
        self.assertEqual(uri, "reports/q3.pdf")


if __name__ == "__main__":
    unittest.main()
