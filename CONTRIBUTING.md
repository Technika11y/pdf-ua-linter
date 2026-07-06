# Contributing

## Ground rules

- **Honesty contract:** the README status table must always match the code; a capability PR
  updates that table in the same change. Extraction stays marked "uncovered" until it has tests.
- **License:** contributions accepted under [Apache-2.0](LICENSE).
- **Sign-off (DCO):** commit with `git commit -s`.
- **Cite the checkpoint:** every rule carries its Matterhorn Protocol id. New rules must too — a
  finding a user can't trace to a standard is noise.

## Dev loop

```bash
PYTHONPATH=src python -m unittest discover -s tests -v   # rules only; no pypdf needed
pip install pypdf
PYTHONPATH=src python -m pdfua.cli some.pdf
```

## Design conventions

- `rules.py` is **pure** (facts in, findings out) — no pypdf, no I/O. That's what keeps it tested.
- `extract.py` owns all pypdf contact. Keep it dumb: report what the file says, judge nothing.
- Prefer checks that map to a real PDF/UA pass/fail criterion over stylistic preferences.
