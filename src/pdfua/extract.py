"""Pull PDF/UA-relevant facts out of a PDF with pypdf. Kept small on purpose — the judgment lives
in rules.py, this only reports what the file says. Requires: pypdf."""


def extract_facts(path):
    from pypdf import PdfReader  # lazy import so rules.py stays dependency-free

    reader = PdfReader(path)
    root = reader.trailer["/Root"]

    # tagged? — StructTreeRoot present and MarkInfo/Marked true
    marked = False
    mark_info = root.get("/MarkInfo")
    if mark_info is not None:
        marked = bool(mark_info.get("/Marked"))
    tagged = ("/StructTreeRoot" in root) and marked

    # title + whether it is shown in the title bar
    title = None
    if reader.metadata and reader.metadata.title:
        title = str(reader.metadata.title)
    view_prefs = root.get("/ViewerPreferences")
    display_doc_title = bool(view_prefs.get("/DisplayDocTitle")) if view_prefs is not None else False

    lang = str(root["/Lang"]) if "/Lang" in root else None

    return {
        "tagged": tagged,
        "title": title,
        "display_doc_title": display_doc_title,
        "lang": lang,
        "figures": _collect_figures(root),
        "pages": len(reader.pages),
    }


def _collect_figures(root):
    """Best-effort walk of the structure tree collecting /Figure elements and their /Alt."""
    figures = []
    struct = root.get("/StructTreeRoot")
    if struct is None:
        return figures

    def resolve(obj):
        return obj.get_object() if hasattr(obj, "get_object") else obj

    def walk(node, depth=0):
        if depth > 50:
            return
        node = resolve(node)
        if not hasattr(node, "get"):
            return
        if node.get("/S") == "/Figure":
            alt = node.get("/Alt")
            figures.append({"alt": str(alt) if alt is not None else None, "page": None})
        kids = node.get("/K")
        if kids is None:
            return
        for kid in (kids if isinstance(kids, list) else [kids]):
            kid = resolve(kid)
            if hasattr(kid, "get"):
                walk(kid, depth + 1)

    walk(struct)
    return figures
