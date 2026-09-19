#!/usr/bin/env python3
"""
Word support for the content round-trip.

`export_content.py --docx` writes CONTENT.docx through this module, and
`import_content.py CONTENT.docx` reads it back through it.

WHY WORD
Several people can review at once with track changes, which a markdown file
cannot do.

THE ONE RULE
Accept all tracked changes before importing. The importer reads the document as
if every change were accepted, so it will do the right thing either way, but it
warns loudly when it finds unaccepted marks — because what it read may not be
what the last reviewer saw on screen.

WHAT SURVIVES THE ROUND TRIP
    Word bold          <->  **bold**
    Word italic        <->  *italic*
    Word hyperlink     <->  [text](https://address)
    Heading 3          <->  ## subheading in the body

Word comments are ignored. They are not part of the text, so a note left in a
comment will not reach the website — put instructions in an email instead.
"""

import re
import sys

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

ID_STYLE = "TuwhiriId"
FIELD_LABELS = ("Title", "Summary", "Heading", "Subheading", "Name", "Label",
                "Date", "Event Start", "Event End", "Location", "Authors",
                "Tags", "Featured", "Role", "Affiliation")
BODY_LABELS = ("Body:", "Text:", "Description:", "Biography:")


# --------------------------------------------------------------------------
# Inline markdown  <->  Word runs
# --------------------------------------------------------------------------

INLINE = re.compile(r"(\*\*.+?\*\*|(?<!\*)\*[^*]+?\*(?!\*)|\[[^\]]+?\]\([^)]+?\))")


def add_markdown_runs(paragraph, text):
    """Render a line of simple markdown into formatted Word runs."""
    for piece in INLINE.split(text):
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**"):
            paragraph.add_run(piece[2:-2]).bold = True
        elif piece.startswith("*") and piece.endswith("*"):
            paragraph.add_run(piece[1:-1]).italic = True
        elif piece.startswith("["):
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", piece)
            add_hyperlink(paragraph, m.group(1), m.group(2))
        else:
            paragraph.add_run(piece)


def add_hyperlink(paragraph, text, url):
    """python-docx has no hyperlink helper; build the element by hand."""
    from docx.oxml.shared import OxmlElement, qn
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    style = OxmlElement("w:rStyle")
    style.set(qn("w:val"), "Hyperlink")
    props.append(style)
    run.append(props)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def runs_to_markdown(paragraph):
    """Read a paragraph back as markdown, honouring accepted tracked changes.

    python-docx only sees runs that are direct children of the paragraph, so
    text someone inserted with track changes on — which sits inside <w:ins> —
    would be invisible to it. We walk the XML instead, which is why an
    unaccepted document still imports correctly.
    """
    out = []
    for node in paragraph._p.iter():
        tag = node.tag

        if tag == f"{W}delText":
            continue                      # deleted text: treat as gone

        if tag == f"{W}t":
            # skip if this run sits inside a deletion
            parent = node.getparent()
            if parent is not None and parent.getparent() is not None and \
                    parent.getparent().tag == f"{W}del":
                continue
            text = node.text or ""
            bold = italic = False
            rpr = parent.find(f"{W}rPr") if parent is not None else None
            if rpr is not None:
                b = rpr.find(f"{W}b")
                i = rpr.find(f"{W}i")
                bold = b is not None and b.get(f"{W}val") not in ("0", "false")
                italic = i is not None and i.get(f"{W}val") not in ("0", "false")
            stripped = text.strip()
            if stripped:
                lead = text[:len(text) - len(text.lstrip())]
                trail = text[len(text.rstrip()):]
                if bold:
                    text = f"{lead}**{stripped}**{trail}"
                elif italic:
                    text = f"{lead}*{stripped}*{trail}"
            out.append(text)

    return "".join(out)


def normalise_link(url):
    """Undo the relative-path rewriting some editors apply.

    LibreOffice turns a root-relative link like /blog/x/ into ../blog/x/ when
    it saves. Every internal link on this site is root-relative, so anything
    that is not an absolute URL is restored to a single leading slash.
    """
    if re.match(r"^[a-z][a-z0-9+.\-]*:", url, re.I) or url.startswith("#"):
        return url
    return "/" + re.sub(r"^(?:\.\.?/)+", "", url).lstrip("/")


def paragraph_hyperlinks(paragraph, doc_part):
    """Return [(text, url)] for hyperlinks in a paragraph."""
    links = []
    for link in paragraph._p.iter(f"{W}hyperlink"):
        rid = link.get(f"{R}id")
        if not rid:
            continue
        try:
            url = doc_part.rels[rid].target_ref
        except KeyError:
            continue
        text = "".join(t.text or "" for t in link.iter(f"{W}t"))
        if text:
            links.append((text, normalise_link(url)))
    return links


# --------------------------------------------------------------------------
# Splitting markdown into Word-shaped blocks
# --------------------------------------------------------------------------

def split_blocks(body):
    """Yield (kind, level, text) blocks from a markdown body.

    A heading is its own block even when the next line follows immediately with
    no blank line between, which is how the landing pages are written. Wrapped
    lines within a paragraph are joined with a space -- a Word run must never
    contain a newline, because Word ignores it and the text runs together.
    """
    blocks, buf = [], []

    def flush():
        if buf:
            blocks.append(("para", 0, " ".join(" ".join(buf).split())))
            buf.clear()

    for raw in (body or "").split("\n"):
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        if line.lstrip().startswith("#"):
            flush()
            stripped = line.lstrip()
            level = len(stripped) - len(stripped.lstrip("#"))
            blocks.append(("heading", level, stripped.lstrip("# ").strip()))
            continue
        if re.match(r"^\s*[-*]\s+", line):
            flush()
            blocks.append(("bullet", 0, re.sub(r"^\s*[-*]\s+", "", line)))
            continue
        buf.append(line.strip())
    flush()
    return blocks


# --------------------------------------------------------------------------
# Writing
# --------------------------------------------------------------------------

def write_docx(entries, intro_lines, path):
    try:
        import docx
        from docx.shared import Pt, Cm, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except ImportError:
        sys.exit("Missing dependency. Run:  pip install python-docx")

    doc = docx.Document()

    # A4, not Letter — python-docx defaults to Letter.
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.left_margin = section.right_margin = Cm(2.5)
        section.top_margin = section.bottom_margin = Cm(2.2)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)

    # A quiet style for the id lines, so they read as machinery not prose.
    if ID_STYLE not in [s.name for s in doc.styles]:
        from docx.enum.style import WD_STYLE_TYPE
        st = doc.styles.add_style(ID_STYLE, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = doc.styles["Normal"]
        st.font.name = "Consolas"
        st.font.size = Pt(7.5)
        st.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        st.paragraph_format.space_after = Pt(10)

    doc.add_heading("Tuwhiri website — all editable text", 0)

    for line in intro_lines:
        if line.startswith("## "):
            doc.add_heading(line[3:], 2)
        elif line.strip():
            p = doc.add_paragraph()
            add_markdown_runs(p, line)

    p = doc.add_paragraph()
    r = p.add_run("Before importing, accept all tracked changes: "
                  "Review \u2192 Accept \u2192 Accept All Changes.")
    r.bold = True

    current_part = None
    for e in entries:
        if e["part"] != current_part:
            current_part = e["part"]
            doc.add_page_break()
            doc.add_heading(current_part, 1)

        doc.add_heading(f"[{e['n']}]  {e['kind']}", 2)

        idp = doc.add_paragraph(f"id: {e['id']}", style=ID_STYLE)
        idp.alignment = WD_ALIGN_PARAGRAPH.LEFT

        for label, value in e["fields"]:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(f"{label}: ")
            run.bold = True
            add_markdown_runs(p, str(value))

        if e.get("body") is not None:
            p = doc.add_paragraph()
            p.add_run(f"{e['body_label']}:").bold = True
            p.paragraph_format.space_after = Pt(2)
            for kind, level, text in split_blocks(e["body"]):
                if kind == "heading":
                    doc.add_heading(text, min(level + 3, 9))
                elif kind == "bullet":
                    para = doc.add_paragraph(style="List Bullet")
                    add_markdown_runs(para, text)
                else:
                    para = doc.add_paragraph()
                    add_markdown_runs(para, text)

    doc.save(str(path))


# --------------------------------------------------------------------------
# Reading
# --------------------------------------------------------------------------

def has_tracked_changes(path):
    """True if the document still carries unaccepted insertions or deletions."""
    import zipfile
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    return ("<w:ins " in xml) or ("<w:del " in xml)


def read_docx(path):
    """Flatten a CONTENT.docx into the same lines the markdown parser expects."""
    try:
        import docx
    except ImportError:
        sys.exit("Missing dependency. Run:  pip install python-docx")

    doc = docx.Document(str(path))
    lines = []

    for para in doc.paragraphs:
        style = (para.style.name or "")
        text = runs_to_markdown(para)

        # Restore hyperlinks as markdown; they live outside ordinary runs.
        for link_text, url in paragraph_hyperlinks(para, doc.part):
            if link_text in text:
                text = text.replace(link_text, f"[{link_text}]({url})", 1)
            else:
                text = (text + f" [{link_text}]({url})").strip()

        text = text.rstrip()

        # Field labels are bold in the document, so they come back as
        # "**Title:** value". Unwrap them to plain "Title: value".
        m = re.match(r"^\*\*([A-Z][A-Za-z ]{1,20}):\*\*\s*(.*)$", text)
        if m and m.group(1) in FIELD_LABELS:
            text = f"{m.group(1)}: {m.group(2)}"
        else:
            m2 = re.match(r"^\*\*(Body|Text|Description|Biography):\*\*\s*$", text)
            if m2:
                text = f"{m2.group(1)}:"

        if style == ID_STYLE or text.startswith("id: "):
            lines.append(text if text.startswith("id: ") else f"id: {text}")
            continue

        if style.startswith("List Bullet"):
            lines.append(f"- {text}")
            continue

        m3 = re.match(r"^Heading (\d)$", style)
        if m3 and int(m3.group(1)) >= 4:
            level = int(m3.group(1)) - 3
            lines.append("")
            lines.append("#" * level + " " + text)
            lines.append("")
            continue

        if style.startswith("Heading 1") or style == "Title":
            continue                                   # part headers, decorative

        if style.startswith("Heading 2"):
            lines.append(text)                         # "[47]  News item: ..."
            continue

        lines.append(text)
        if text.strip() and not is_field_line(text) and text.strip() not in BODY_LABELS:
            lines.append("")                           # paragraph break

    return lines


def is_field_line(text):
    m = re.match(r"^([A-Z][A-Za-z ]{1,20}):\s", text)
    return bool(m and m.group(1) in FIELD_LABELS)
