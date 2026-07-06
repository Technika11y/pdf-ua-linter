"""CLI: lint a PDF for PDF/UA conformance. Exit 1 on any error-severity finding."""
import argparse
import sys

from .rules import check, has_errors


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="pdf-ua-linter")
    parser.add_argument("pdf", help="path to a PDF file")
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = parser.parse_args(argv)

    from .extract import extract_facts  # lazy: only needs pypdf when a file is actually linted

    facts = extract_facts(args.pdf)
    findings = check(facts)

    if args.json:
        import json
        print(json.dumps({"file": args.pdf, "facts": facts, "findings": findings}, indent=2))
    else:
        for f in findings:
            cp = f" [{f['checkpoint']}]" if f.get("checkpoint") else ""
            print(f"{f['severity'].upper():5} {f['rule']}{cp}  {f['message']}", file=sys.stderr)
        if not findings:
            print("PASS — no PDF/UA errors from the implemented checks", file=sys.stderr)

    return 1 if has_errors(findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
