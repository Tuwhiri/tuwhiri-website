#!/usr/bin/env python3
"""
Read an edited CONTENT.md back and apply the changes to the site.

    python3 scripts/import_content.py --dry-run     # show what would change
    python3 scripts/import_content.py               # apply it

Companion to `export_content.py`. It finds each entry by its `id:` line, so
those must survive editing intact; everything else in the file can be rewritten
freely.

WHAT IT WILL DO
    - update headings, body text, card names and descriptions on the pages
    - update any field of a news item or event, including its body
    - update a person's role and biography
    - delete an item, if DELETE appears on the line after its `id:`

WHAT IT WILL NOT DO
    - create new items. Adding a news item is a separate step; ask, and it will
      be created with the right filename and front matter.
    - touch publications, which come from Zotero.
    - change names, affiliations or group membership, which live in
      data/team.yaml.

Always run --dry-run first, and check `git diff` before committing.
"""

import argparse
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency. Run:  pip install pyyaml")

# The landing pages carry explanatory comments that PyYAML would silently
# discard on re-serialising. ruamel round-trips them.
try:
    from ruamel.yaml import YAML
    _RT = YAML()
    _RT.preserve_quotes = True
    _RT.width = 100000
    _RT.indent(mapping=2, sequence=4, offset=2)
except ImportError:
    _RT = None

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULE_RE = re.compile(r"^={20,}\s*$")


# --- reading the edited file ------------------------------------------------

def parse(path):
    """Split the file into entries keyed by id. Accepts .md or .docx."""
    if str(path).lower().endswith(".docx"):
        sys.path.insert(0, str(ROOT / "scripts"))
        from content_docx import read_docx, has_tracked_changes
        if has_tracked_changes(path):
            print("!" * 74)
            print("This document still contains tracked changes that have not")
            print("been accepted.")
            print()
            print("The importer reads it as though every change were accepted,")
            print("so the result should be right — but what it read may not be")
            print("what the last reviewer saw. Accept all changes in Word first:")
            print("    Review -> Accept -> Accept All Changes")
            print("then re-run this. Continuing anyway.")
            print("!" * 74)
            print()
        lines = read_docx(path)
    else:
        lines = path.read_text(encoding="utf-8").splitlines()
    entries, current = [], None

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("id: "):
            entry_id = line[4:].split("<-")[0].strip()
            # the block header rule sits directly below
            start = i + 2 if i + 1 < len(lines) and RULE_RE.match(lines[i + 1]) else i + 1
            current = {"id": entry_id, "start": start, "lines": []}
            entries.append(current)
            i = start
            continue
        if current is not None:
            # the next entry's "[n] Heading" line closes this one; decorative
            # rules and part headers are ignored in both formats
            if re.match(r"^\[\d+\]\s", line.strip()):
                current = None
            elif re.match(r"^#\s+PART\b", line.strip()) or line.strip() == "END":
                current = None
            elif RULE_RE.match(line) or re.match(r"^#{20,}\s*$", line):
                pass
            else:
                current["lines"].append(line)
        i += 1

    for e in entries:
        e["fields"], e["body"] = split_entry(e["lines"])
    return entries


def split_entry(lines):
    """Separate `Name: value` fields from the free-text body."""
    fields, body, in_body = {}, [], False
    body_labels = ("Body:", "Text:", "Description:", "Biography:")

    for line in lines:
        if not in_body and line.strip() in body_labels:
            in_body = True
            continue
        if in_body:
            body.append(line)
            continue
        m = re.match(r"^([A-Z][A-Za-z ]{1,20}):\s{1,}(.*)$", line)
        if m:
            fields[m.group(1).strip().lower()] = m.group(2).strip()

    return fields, "\n".join(body).strip("\n")


# --- applying to the site ---------------------------------------------------

def same_text(a, b):
    """Compare prose ignoring how it happens to be wrapped.

    The source files are hard-wrapped at about 78 characters; text coming back
    from Word is one line per paragraph. Markdown renders both identically, so
    a difference in wrapping alone is not an edit and should not rewrite the
    file or show up in the diff.
    """
    def norm(s):
        # A heading is its own block whether or not a blank line follows it,
        # so put one there before comparing.
        s = re.sub(r"(?m)^(\s*#{1,6}\s.*)$", r"\n\1\n", (s or ""))
        paras = re.split(r"\n\s*\n", s.strip())
        return [" ".join(p.split()) for p in paras if p.strip()]
    return norm(a) == norm(b)


def read_page(path, roundtrip=False):
    """Read front matter and body. With roundtrip=True, comments are kept."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if roundtrip and _RT is not None:
        import io
        return _RT.load(io.StringIO(m.group(1))), m.group(2)
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)


def write_page(path, fm, body, roundtrip=False):
    if roundtrip and _RT is not None:
        import io
        buf = io.StringIO()
        _RT.dump(fm, buf)
        dumped = buf.getvalue()
    else:
        dumped = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                                default_flow_style=False, width=100000)
    path.write_text(f"---\n{dumped}---\n{body}", encoding="utf-8")


def get_by_path(fm, dotted):
    """Read the current value at a dotted path, or None."""
    node = fm
    for key, arr in [(k, i) for k, i in
                     re.findall(r"([A-Za-z_]+)(?:\[(\d+)\])?", dotted) if k]:
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
        if arr != "":
            if not isinstance(node, list) or int(arr) >= len(node):
                return None
            node = node[int(arr)]
    return node


def set_by_path(fm, dotted, value):
    """Set e.g. sections[2].content.items[0].description on the front matter."""
    node = fm
    parts = re.findall(r"([A-Za-z_]+)(?:\[(\d+)\])?", dotted)
    parts = [(k, i) for k, i in parts if k]
    for idx, (key, arr) in enumerate(parts):
        last = idx == len(parts) - 1
        if last and arr == "":
            node[key] = value
            return True
        nxt = node.get(key) if isinstance(node, dict) else None
        if arr != "":
            if not isinstance(nxt, list) or int(arr) >= len(nxt):
                return False
            nxt = nxt[int(arr)]
        if last:
            return False
        node = nxt
        if node is None:
            return False
    return False


def apply_entry(entry, changes, dry):
    eid = entry["id"]
    body = entry["body"].strip()
    deleted = body.upper().startswith("DELETE") or \
        entry["fields"].get("delete", "").lower() in ("yes", "true")

    # ---- a page fragment -------------------------------------------------
    if "::" in eid:
        rel, dotted = eid.split("::", 1)
        path = ROOT / rel
        if not path.exists():
            changes.append(("MISSING", eid, "file not found"))
            return
        fm, page_body = read_page(path, roundtrip=True)

        if re.search(r"items\[\d+\]$", dotted):
            # card: Name is a field, the body is the description
            name_new = entry["fields"].get("name", "")
            before = (str(get_by_path(fm, dotted + ".name") or ""),
                      str(get_by_path(fm, dotted + ".description") or ""))
            if not set_by_path(fm, dotted + ".name", name_new):
                set_by_path(fm, dotted + ".title", name_new)
            set_by_path(fm, dotted + ".description", body)
            if before[0].strip() != name_new.strip() or not same_text(before[1], body):
                if not dry:
                    write_page(path, fm, page_body, roundtrip=True)
                changes.append(("card", eid, name_new))
            return

        if body:
            new = body
        else:
            key = dotted.rsplit(".", 1)[-1]
            label = {"title": "heading", "subtitle": "subheading",
                     "text": "label"}.get(key, key)
            new = entry["fields"].get(label) or entry["fields"].get(key) \
                or next(iter(entry["fields"].values()), "")

        before = get_by_path(fm, dotted)
        if set_by_path(fm, dotted, new):
            if not same_text(str(before or ""), str(new or "")):
                if not dry:
                    write_page(path, fm, page_body, roundtrip=True)
                changes.append(("page", eid, (new or "")[:58].replace("\n", " ")))
        else:
            changes.append(("FAILED", eid, "could not locate that field"))
        return

    # ---- a person --------------------------------------------------------
    if eid.startswith("person/"):
        slug = eid.split("/", 1)[1]
        f = ROOT / "data" / "authors" / f"{slug}.yaml"
        if not f.exists():
            changes.append(("MISSING", eid, "no such person"))
            return
        data = yaml.safe_load(f.read_text()) or {}
        bio = "" if body.lower().startswith("(none") else body
        role = entry["fields"].get("role", data.get("role", ""))
        if not same_text(data.get("bio", ""), bio) or data.get("role", "") != role:
            data["bio"], data["role"] = bio, role
            if not dry:
                f.write_text(yaml.safe_dump(data, sort_keys=False,
                                            allow_unicode=True), encoding="utf-8")
            changes.append(("person", eid, role))
            changes.append(("NOTE", eid,
                            "role also lives in data/team.yaml — update it there too"))
        return

    # ---- a news item or event -------------------------------------------
    path = ROOT / eid / "index.md"
    if not path.exists():
        changes.append(("MISSING", eid, "file not found"))
        return

    if deleted:
        if not dry:
            for child in (ROOT / eid).iterdir():
                child.unlink()
            (ROOT / eid).rmdir()
        changes.append(("DELETED", eid, ""))
        return

    fm, before_body = read_page(path)
    before_fm = yaml.safe_load(yaml.safe_dump(fm))   # deep copy for comparison
    f = entry["fields"]
    mapping = {
        "title": "title", "summary": "summary", "date": "date",
        "event start": "event_start", "event end": "event_end",
        "location": "location",
    }
    for human, key in mapping.items():
        if human in f and f[human]:
            new_val = f[human]
            if str(fm.get(key, "")) != new_val:
                fm[key] = new_val
    if "authors" in f:
        fm["authors"] = [a.strip() for a in f["authors"].split(",") if a.strip()]
    if "tags" in f:
        fm["tags"] = [t.strip() for t in f["tags"].split(",") if t.strip()]
    if "featured" in f:
        fm["featured"] = f["featured"].strip().lower() in ("yes", "true")

    if fm != before_fm or not same_text(before_body, body):
        dumped = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                                default_flow_style=False, width=100000)
        if not dry:
            path.write_text(f"---\n{dumped}---\n\n{body}\n", encoding="utf-8")
        changes.append(("item", eid, str(fm.get("title", ""))[:58]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", default="CONTENT.md")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = ROOT / args.file
    if not src.exists():
        sys.exit(f"Cannot find {args.file}")

    entries = parse(src)
    print(f"Read {len(entries)} entries from {args.file}\n")

    changes = []
    for e in entries:
        apply_entry(e, changes, args.dry_run)

    problems = [c for c in changes if c[0] in ("FAILED", "MISSING")]
    for kind, eid, note in changes:
        mark = "!" if kind in ("FAILED", "MISSING") else " "
        print(f" {mark} {kind:8} {eid[:60]:62} {note}")

    print(f"\n{len(changes) - len(problems)} change(s)"
          + (" — dry run, nothing written" if args.dry_run else " applied"))
    if problems:
        print(f"{len(problems)} problem(s) above, marked !")
    if not args.dry_run:
        print("\nCheck `git diff` before committing.")


if __name__ == "__main__":
    main()
