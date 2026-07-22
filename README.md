# PDF/UA Linter

> Lints PDFs for **PDF/UA (ISO 14289)** conformance — tags, title, language, figure alt text —
> with every rule mapped to the **Matterhorn Protocol** checkpoint an auditor would cite.
>
> Part of the **Technika11y** suite · *Root access for everyone.*

[![ci](https://github.com/technika11y/pdf-ua-linter/actions/workflows/ci.yml/badge.svg)](https://github.com/technika11y/pdf-ua-linter/actions/workflows/ci.yml)
![status](https://img.shields.io/badge/status-pre--alpha-orange)
![license](https://img.shields.io/badge/license-Apache--2.0-blue)
![python](https://img.shields.io/badge/python-3.10%2B-informational)

---

## Quick start

```bash
git clone https://github.com/technika11y/pdf-ua-linter && cd pdf-ua-linter
pip install pypdf
PYTHONPATH=src python3 -m pdfua.cli document.pdf   # point it at any PDF
```

## Status — read this first

**Pre-alpha (`v0.1.0a0`). Honest state of the code:**

| Capability | State |
|---|---|
| Rule: document is tagged (marked StructTreeRoot) — `01-005` | ✅ works, tested |
| Rule: title present — `06-003` | ✅ works, tested |
| Rule: title shown in title bar (DisplayDocTitle) — `07-001` | ✅ works, tested |
| Rule: natural language set + well-formed — `11-001` | ✅ works, tested |
| Rule: every figure has alt text — `13-004` | ✅ works, tested |
| Rule: title isn't a filename/authoring-tool artifact — `06-004` | ✅ works, tested |
| Rule: figure alt isn't a placeholder ("image", "logo", …) — `13-004` | ✅ works, tested |
| PDF fact extraction via pypdf | ⚠️ works, **not yet covered by automated tests** (needs a sample-PDF corpus) |
| Figure→page attribution, reading order, tables, contrast, artifacts | ❌ not built — [roadmap](#roadmap) |

The rules are the tested core. Extraction is real but honestly uncovered until there's a corpus of
known-good/known-bad PDFs to test against. This table is the honesty contract.

## Why it exists

PDF is where accessibility goes to be forgotten — a scanned image with no tags passes a glance and
fails every screen reader. The checks here are the ones that decide *pass or fail* in a real
PDF/UA audit: is it tagged, does it announce its title and language, does every image carry a text
alternative. The design splits **judgment** (pure rules, in `rules.py`) from **extraction** (pypdf,
in `extract.py`) so the rules are trivially testable and the parser can be hardened independently.

## Usage

```bash
pip install pypdf
PYTHONPATH=src python -m pdfua.cli document.pdf
PYTHONPATH=src python -m pdfua.cli document.pdf --json
```

```
ERROR pdfua-not-tagged [01-005]  document is not tagged (no marked StructTreeRoot) — assistive tech has no structure
ERROR pdfua-figure-no-alt [13-004]  figure #2 has no alternative text
```

Exit `1` on any error-severity finding — drops into CI to gate document publishing.

## Roadmap

- [ ] Sample-PDF corpus + extraction integration tests
- [ ] Attribute figures to page numbers (via `/Pg`)
- [ ] Reading-order and table-structure checks
- [ ] Colour-contrast and artifact checks
- [ ] SARIF output + the shared Technika11y CI gate

## License

[Apache-2.0](LICENSE). See [`SECURITY.md`](SECURITY.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

**Part of the [Technika11y](https://github.com/technika11y) suite** · [technika11y.github.io](https://technika11y.github.io/) · security, compliance, and accessibility as one discipline.
