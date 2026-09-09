#!/usr/bin/env python3
"""
Export every piece of editable prose on the site into one file.

    python3 scripts/export_content.py            # writes CONTENT.md
    python3 scripts/export_content.py out.md     # or somewhere else

The point is to let someone edit all the site's wording in a single document
rather than hunting through folders. The companion script,
`import_content.py`, reads the edited file back and applies the changes.

WHAT IS INCLUDED
    - the home page and the four section landing pages
    - every news item
    - every event
    - each person's one-line role and biography

WHAT IS NOT, and why
    - publications: they come from the Zotero group library and are overwritten
      on every sync. Edit the record in Zotero instead.
    - navigation labels, colours, layout: these are configuration, not prose.
    - people's names, affiliations and group membership: these live in
      data/team.yaml, which drives sorting and publication tagging.

Each entry carries an `id:` line. That is how the importer finds its way home,
so it must not be edited.
"""

import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency. Run:  pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULE = "=" * 78

LANDING = [
    ("content/_index.md", "Home page"),
    ("content/atmospheric-science/index.md", "Atmospheric Science page"),
    ("content/photonics/index.md", "Photonics page"),
    ("content/engineering/index.md", "Space Systems Engineering page"),
    ("content/outreach/index.md", "Outreach page"),
    ("content/people/index.md", "People page"),
]


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)


def field(name, value, width=13):
    return f"{(name + ':').ljust(width)}{value}"


COUNTER = {"n": 0}
ENTRIES = []
PART = {"name": "PART 1 — THE PAGES"}


def block(out, entry_id, kind, fields, body=None, body_label="Body"):
    COUNTER["n"] += 1
    ENTRIES.append({"n": COUNTER["n"], "id": entry_id, "kind": kind,
                    "fields": list(fields), "body": body,
                    "body_label": body_label, "part": PART["name"]})
    out.append("")
    out.append(RULE)
    out.append(f"[{COUNTER['n']}]  {kind}")
    out.append(f"id: {entry_id}")
    out.append(RULE)
    out.append("")
    for k, v in fields:
        out.append(field(k, v))
    if body is not None:
        out.append("")
        out.append(f"{body_label}:")
        out.append("")
        out.append(body.rstrip())
    out.append("")


def export_landing(out):
    out.append("")
    out.append("#" * 78)
    PART["name"] = "PART 1 — THE PAGES"
    out.append("# PART 1 — THE PAGES")
    out.append("#" * 78)

    for rel, label in LANDING:
        path = ROOT / rel
        if not path.exists():
            continue
        fm, _ = front_matter(path)
        for i, sec in enumerate(fm.get("sections") or []):
            content = sec.get("content") or {}
            kind = sec.get("block", "?")
            base = f"{rel}::sections[{i}]"

            # Headings and prose
            for key, human in (("title", "Heading"),
                               ("subtitle", "Subheading"),
                               ("text", None)):
                val = content.get(key)
                if not val or not str(val).strip():
                    continue
                if key == "text":
                    block(out, f"{base}.content.text",
                          f"{label} — {kind} block, body text",
                          [], str(val), "Text")
                else:
                    block(out, f"{base}.content.{key}",
                          f"{label} — {kind} block, {human.lower()}",
                          [(human, str(val).strip())])

            # Card lists: research areas, partner logos
            for j, item in enumerate(content.get("items") or []):
                if not isinstance(item, dict):
                    continue
                name = item.get("name") or item.get("title") or ""
                desc = item.get("description") or item.get("text") or ""
                if not (name or desc):
                    continue
                block(out, f"{base}.content.items[{j}]",
                      f"{label} — {kind} card",
                      [("Name", str(name).strip())],
                      str(desc).strip(), "Description")

            # Call-to-action button
            btn = content.get("button")
            if isinstance(btn, dict) and btn.get("text"):
                block(out, f"{base}.content.button.text",
                      f"{label} — button label",
                      [("Label", str(btn["text"]).strip())])

            # Contact block's note to prospective students
            pros = content.get("prospective")
            if isinstance(pros, dict):
                if pros.get("title"):
                    block(out, f"{base}.content.prospective.title",
                          f"{label} — prospective students, heading",
                          [("Heading", str(pros["title"]).strip())])
                if pros.get("text"):
                    block(out, f"{base}.content.prospective.text",
                          f"{label} — prospective students, text",
                          [], str(pros["text"]).strip(), "Text")


def export_folder(out, folder, part_title, kind_label, date_fields):
    items = sorted([d for d in (ROOT / "content" / folder).iterdir()
                    if d.is_dir() and (d / "index.md").exists()], reverse=True)
    out.append("")
    out.append("#" * 78)
    PART["name"] = part_title
    out.append(f"# {part_title}")
    out.append("#" * 78)

    for d in items:
        fm, body = front_matter(d / "index.md")
        fields = [("Title", str(fm.get("title", "")).strip())]
        if "summary" in fm:
            fields.append(("Summary", str(fm.get("summary", "")).strip()))
        for f in date_fields:
            if f in fm:
                fields.append((f.replace("_", " ").title(), str(fm[f])))
        for f in ("location",):
            if f in fm:
                fields.append((f.title(), str(fm[f])))
        fields.append(("Authors", ", ".join(fm.get("authors") or [])))
        fields.append(("Tags", ", ".join(fm.get("tags") or [])))
        if "featured" in fm:
            fields.append(("Featured", "yes" if fm["featured"] else "no"))

        block(out, f"content/{folder}/{d.name}",
              f"{kind_label}: {fm.get('title','')}",
              fields, body, "Body")


def export_people(out):
    roster = yaml.safe_load((ROOT / "data" / "team.yaml").read_text())["people"]
    out.append("")
    out.append("#" * 78)
    PART["name"] = "PART 4 — PEOPLE: ROLE AND BIOGRAPHY"
    out.append("# PART 4 — PEOPLE: ROLE AND BIOGRAPHY")
    out.append("#" * 78)
    out.append("")
    out.append("Only the role line and the biography are editable here. Names,")
    out.append("affiliations and group membership live in data/team.yaml,")
    out.append("because they also drive sorting and publication tagging.")
    out.append("")
    out.append("Biographies are all empty at present. Anything written here")
    out.append("appears on the person's profile page.")

    for p in roster:
        slug = p["slug"]
        bio_path = ROOT / "data" / "authors" / f"{slug}.yaml"
        bio = ""
        if bio_path.exists():
            bio = (yaml.safe_load(bio_path.read_text()) or {}).get("bio", "") or ""
        block(out, f"person/{slug}",
              f"Person: {p['name']}",
              [("Name", p["name"]),
               ("Affiliation", p.get("org", "")),
               ("Role", p.get("role", ""))],
              bio.strip() or "(none yet)", "Biography")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_docx = "--docx" in sys.argv
    default = "CONTENT.docx" if as_docx else "CONTENT.md"
    dest = ROOT / (args[0] if args else default)

    out = []
    out.append("# Tuwhiri website — all editable text")
    out.append("")
    out.append("Everything on the site that is words rather than machinery, in")
    out.append("one file, for the first launch.")
    out.append("")
    out.append("## How to use this")
    out.append("")
    out.append("Edit the text freely. Rewrite, shorten, delete a whole entry,")
    out.append("add notes in square brackets — whatever is useful. Then hand the")
    out.append("file back and the changes will be applied to the website.")
    out.append("")
    out.append("**The only rule: leave every `id:` line exactly as it is.**")
    out.append("That line is how each piece of text finds its way back to the")
    out.append("right place. Everything else is yours.")
    out.append("")
    out.append("To delete an item entirely, write DELETE on the line after its")
    out.append("`id:` line rather than removing the block.")
    out.append("")
    out.append("The number in square brackets is only there so you can point at")
    out.append("an entry in an email — \"see 47\". It carries no other meaning.")
    out.append("")
    out.append("Formatting in the body text: `**bold**`, `*italic*`,")
    out.append("`[link text](https://address)`, and `## ` at the start of a line")
    out.append("for a subheading. A blank line starts a new paragraph.")
    out.append("")
    out.append("## What is not here")
    out.append("")
    out.append("- **Publications** come from the Zotero group and are rewritten")
    out.append("  automatically. Correct them in Zotero.")
    out.append("- **Names, affiliations, advisory board membership** live in")
    out.append("  data/team.yaml, because they drive sorting and tagging too.")
    out.append("- **Menus, colours and layout** are configuration, not wording.")

    export_landing(out)
    export_folder(out, "blog", "PART 2 — NEWS ITEMS", "News item",
                  ["date"])
    export_folder(out, "events", "PART 3 — EVENTS", "Event",
                  ["event_start", "event_end", "date"])
    export_people(out)

    out.append("")
    out.append(RULE)
    out.append("END")
    out.append(RULE)

    if as_docx:
        sys.path.insert(0, str(ROOT / "scripts"))
        from content_docx import write_docx
        intro = [l for l in out[:out.index("") if "" in out else 30]] if False else []
        # the introduction is everything before the first part header
        first = next(i for i, l in enumerate(out) if l.startswith("#" * 20))
        intro = [l for l in out[1:first] if l.strip()]
        write_docx(ENTRIES, intro, dest)
    else:
        dest.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote {dest.relative_to(ROOT)}")
    print(f"  {COUNTER['n']} editable entries")


if __name__ == "__main__":
    main()
