"""PDF/UA (ISO 14289-1) conformance rules.

Expressed over a plain `facts` dict so the judgment is pure and unit-testable without a PDF
parser. Rule ids carry the matching Matterhorn Protocol checkpoint — the failure conditions PDF/UA
auditors actually cite.
"""
import re

# A deliberately loose BCP-47 shape check — enough to catch "english" / "EN_US", not a full parser.
_LANG_RE = re.compile(r"^[a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})*$")

# A title that's really a filename or an authoring-tool artifact, and non-descriptive alt text.
_FILENAME_RE = re.compile(r"\.(pdf|docx?|pptx?|xlsx?|pages)$", re.I)
_TOOL_TITLE_RE = re.compile(r"^microsoft (word|powerpoint|excel) - ", re.I)
_PLACEHOLDER_ALT = {"image", "picture", "figure", "graphic", "photo", "img", "spacer", "logo"}


def _looks_like_filename(title):
    t = title.strip()
    return bool(_FILENAME_RE.search(t) or _TOOL_TITLE_RE.match(t))


def _f(rule, severity, message, checkpoint=None):
    return {"rule": rule, "severity": severity, "message": message, "checkpoint": checkpoint}


def check(facts):
    """Return a list of findings from extracted document facts."""
    findings = []

    # Tagging — without a marked structure tree, assistive tech has nothing to read.
    if not facts.get("tagged"):
        findings.append(_f("pdfua-not-tagged", "error",
            "document is not tagged (no marked StructTreeRoot) — assistive tech has no structure",
            "01-005"))

    # Title — must exist AND be shown in the window title bar (DisplayDocTitle).
    title = facts.get("title")
    if not title or not str(title).strip():
        findings.append(_f("pdfua-no-title", "error",
            "document has no title in metadata", "06-003"))
    elif not facts.get("display_doc_title"):
        findings.append(_f("pdfua-title-not-displayed", "error",
            "ViewerPreferences /DisplayDocTitle is not true — the title won't show in the title bar",
            "07-001"))

    # Title should be a human-meaningful name, not a filename or authoring-tool artifact.
    if title and str(title).strip() and _looks_like_filename(str(title)):
        findings.append(_f("pdfua-title-is-filename", "warn",
            f'title "{title}" looks like a filename, not a descriptive document title', "06-004"))

    # Natural language — screen readers need it to choose pronunciation.
    lang = facts.get("lang")
    if not lang:
        findings.append(_f("pdfua-no-lang", "error",
            "no natural language set (/Lang) — a screen reader can't choose pronunciation",
            "11-001"))
    elif not _LANG_RE.match(str(lang)):
        findings.append(_f("pdfua-lang-malformed", "warn",
            f'/Lang "{lang}" is not a well-formed BCP-47 tag', "11-001"))

    # Figures — every figure needs a text alternative, and it must actually describe something.
    for i, fig in enumerate(facts.get("figures", [])):
        alt = fig.get("alt")
        page = fig.get("page")
        where = f" (page {page})" if page is not None else ""
        if not alt or not str(alt).strip():
            findings.append(_f("pdfua-figure-no-alt", "error",
                f"figure #{i + 1}{where} has no alternative text", "13-004"))
        elif str(alt).strip().lower() in _PLACEHOLDER_ALT:
            findings.append(_f("pdfua-figure-alt-placeholder", "warn",
                f'figure #{i + 1}{where} has non-descriptive alt text "{alt}"', "13-004"))

    return findings


def has_errors(findings):
    return any(x["severity"] == "error" for x in findings)
