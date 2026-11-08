"""SARIF 2.1.0 output, so PDF/UA findings become real GitHub code-scanning alerts.

Each rule carries its Matterhorn checkpoint as a property, so an auditor reading the
Security tab can still trace a finding to the standard it came from.
"""
_LEVEL = {"error": "error", "warn": "warning", "info": "note"}
_MATTERHORN = "https://pdfa.org/resource/the-matterhorn-protocol/"


def to_sarif(findings, target="document.pdf"):
    rules, seen = [], set()
    for f in findings:
        rid = f["rule"]
        if rid in seen:
            continue
        seen.add(rid)
        desc = {"id": rid, "shortDescription": {"text": rid.replace("-", " ")}}
        if f.get("checkpoint"):
            desc["properties"] = {"matterhornCheckpoint": f["checkpoint"]}
            desc["helpUri"] = _MATTERHORN
        rules.append(desc)

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {
                "name": "pdf-ua-linter",
                "informationUri": "https://github.com/technika11y/pdf-ua-linter",
                "rules": rules,
            }},
            "results": [{
                "ruleId": f["rule"],
                "level": _LEVEL.get(f["severity"], "note"),
                "message": {"text": f["message"]},
                "locations": [{"physicalLocation": {"artifactLocation": {"uri": target}}}],
            } for f in findings],
        }],
    }
