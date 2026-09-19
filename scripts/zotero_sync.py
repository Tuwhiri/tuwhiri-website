#!/usr/bin/env python3
"""
Sync the Tuwhiri Zotero group library into Hugo publication pages.

    python3 scripts/zotero_sync.py            # write the files
    python3 scripts/zotero_sync.py --dry-run  # just show what would change

What it does
------------
1. Downloads every item from the Tuwhiri Zotero group library.
2. Skips notes, attachments and anything with the Zotero tag `no-website`.
3. Writes one page per publication to content/publication/<slug>/index.md
4. Tags each publication with a research area, worked out by matching the
   author surnames against data/team.yaml. A paper by Suresh and Sedlmeir
   gets tagged `photonics`; a paper by Kessenich gets `atmospheric-science`.
   A paper with authors from two areas gets both tags.

   Zotero's own keyword tags are deliberately not copied across. See
   ALLOWED_ZOTERO_TAGS below if you ever want particular ones through.
5. Deletes pages for items that have been removed from Zotero.

Pages it did not create are never touched, so you can still hand-write a
publication page if you ever need to.
"""

import argparse
import json
import os
import pathlib
import re
import sys
import unicodedata
import urllib.error
import urllib.request

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency. Run:  pip install pyyaml")

# --- Settings ---------------------------------------------------------------

GROUP_ID = "6627926"          # Tuwhiri Zotero group
PAGE_SIZE = 100
EXCLUDE_TAG = "no-website"    # add this tag in Zotero to hide an item

# Zotero keyword tags are NOT copied to the website. A shared reference library
# accumulates keywords from importers, publishers and personal habit -- "Q
# factor", "Whispering gallery modes", "Terahertz detectors" -- with no shared
# capitalisation or vocabulary. Mixing those into the site's tag list makes the
# tag index a jumble and buries the four tags that actually do work:
# atmospheric-science, photonics, engineering and outreach.
#
# Website tags are therefore derived from the AUTHORS alone, via data/team.yaml.
#
# To let specific Zotero keywords through, list them here, exactly as spelled in
# Zotero. Anything not listed is ignored. Example:
#     ALLOWED_ZOTERO_TAGS = {"ozone", "cubesat"}
ALLOWED_ZOTERO_TAGS = set()

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROSTER = ROOT / "data" / "team.yaml"
OUTDIR = ROOT / "content" / "publications"

# Zotero item type -> Hugo Blox publication type
TYPE_MAP = {
    "journalArticle": "article-journal",
    "conferencePaper": "paper-conference",
    "preprint": "paper",
    "report": "report",
    "book": "book",
    "bookSection": "chapter",
    "thesis": "thesis",
    "patent": "patent",
    "presentation": "manuscript",
    "manuscript": "manuscript",
    "dataset": "manuscript",
}

SKIP_TYPES = {"note", "attachment", "annotation"}

# Used to set the `peer_reviewed` flag the new schema supports.
PEER_REVIEWED_TYPES = {"journalArticle", "conferencePaper", "bookSection"}


# --- Helpers ----------------------------------------------------------------

def strip_accents(text):
    return "".join(c for c in unicodedata.normalize("NFD", text)
                   if unicodedata.category(c) != "Mn")


def slugify(text, maxlen=60):
    text = strip_accents(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:maxlen].strip("-")


def zotero_get(start):
    url = (f"https://api.zotero.org/groups/{GROUP_ID}/items/top"
           f"?format=json&limit={PAGE_SIZE}&start={start}")
    req = urllib.request.Request(url)
    req.add_header("Zotero-API-Version", "3")
    key = os.environ.get("ZOTERO_API_KEY", "").strip()
    if key:
        req.add_header("Zotero-API-Key", key)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_all():
    items, start = [], 0
    while True:
        batch = zotero_get(start)
        items.extend(batch)
        if len(batch) < PAGE_SIZE:
            return items
        start += PAGE_SIZE


def normalise_surname(text):
    """Lowercase, drop accents, treat hyphens as spaces, collapse whitespace.

    So 'García-Muñoz', 'Garcia Munoz' and 'García  Muñoz' all compare equal.
    """
    text = strip_accents(text).lower().replace("-", " ")
    return " ".join(text.split())


def load_roster():
    roster = yaml.safe_load(ROSTER.read_text(encoding="utf-8"))
    lookup = []
    for person in roster.get("people", []):
        for surname in person.get("match") or []:
            lookup.append((normalise_surname(surname),
                           person["slug"], person.get("area", "")))
    return lookup


def match_person(last_name, lookup):
    target = normalise_surname(last_name)
    for surname, slug, area in lookup:
        if target == surname:
            return slug, area
    return None, None


def creator_name(creator):
    if "name" in creator:                       # single-field name
        return creator["name"], creator["name"].split()[-1]
    first = creator.get("firstName", "").strip()
    last = creator.get("lastName", "").strip()
    return (f"{first} {last}".strip(), last)


def venue(data):
    for field in ("publicationTitle", "proceedingsTitle", "bookTitle",
                  "repository", "institution", "university", "publisher"):
        if data.get(field):
            return data[field]
    return ""


def venue_map(data):
    """Structured venue details, as the new schema expects.

    The old theme wanted one preformatted string; this generation wants
    separate fields so citation styles can format them properly.
    """
    name = venue(data)
    if not name:
        return None
    out = {"name": name}
    for src, dest in (("volume", "volume"), ("issue", "issue"),
                      ("pages", "pages")):
        if data.get(src):
            out[dest] = data[src]
    return out


def bibtex_entry(item, authors, key):
    data = item["data"]
    itype = data.get("itemType", "")
    btype = {"journalArticle": "article", "conferencePaper": "inproceedings",
             "book": "book", "bookSection": "incollection",
             "thesis": "phdthesis", "report": "techreport"}.get(itype, "misc")
    fields = {
        "title": data.get("title", ""),
        "author": " and ".join(authors),
        "year": (item.get("meta", {}).get("parsedDate", "") or "")[:4],
        "journal": venue(data),
        "volume": data.get("volume", ""),
        "number": data.get("issue", ""),
        "pages": data.get("pages", ""),
        "doi": data.get("DOI", ""),
        "url": data.get("url", ""),
    }
    lines = [f"@{btype}{{{key},"]
    for name, value in fields.items():
        if value:
            lines.append(f"  {name} = {{{value}}},")
    lines.append("}")
    return "\n".join(lines) + "\n"


# --- Page building ----------------------------------------------------------

def build_page(item, lookup):
    data = item["data"]
    if data.get("itemType") in SKIP_TYPES:
        return None
    ztags = [t.get("tag", "") for t in data.get("tags", [])]
    if EXCLUDE_TAG in ztags:
        return None

    title = (data.get("title") or "").strip()
    if not title:
        return None

    authors_display, author_refs, areas = [], [], []
    for creator in data.get("creators", []):
        if creator.get("creatorType") != "author":
            continue
        display, last = creator_name(creator)
        authors_display.append(display)
        slug, area = match_person(last, lookup)
        author_refs.append(slug if slug else display)
        if area and area not in areas:
            areas.append(area)

    parsed = item.get("meta", {}).get("parsedDate", "") or ""
    year = parsed[:4] if len(parsed) >= 4 else ""
    date = parsed if len(parsed) == 10 else (f"{year}-01-01" if year else "1970-01-01")

    first_last = ""
    for creator in data.get("creators", []):
        if creator.get("creatorType") == "author":
            first_last = creator_name(creator)[1]
            break
    slug = "-".join(x for x in [slugify(first_last, 20), year,
                                slugify(title, 40)] if x)

    # Research area tags come from the author matching above. Zotero keywords
    # are dropped unless explicitly allowed -- see ALLOWED_ZOTERO_TAGS.
    tags = sorted(set(areas)) + sorted(
        t for t in ztags if t != EXCLUDE_TAG and t in ALLOWED_ZOTERO_TAGS)

    fm = {
        "title": title,
        "authors": author_refs,
        "date": date,
        "publishDate": date,
        "publication_types": [TYPE_MAP.get(data.get("itemType"), "manuscript")],
        "publication": venue_map(data),
        "peer_reviewed": data.get("itemType") in PEER_REVIEWED_TYPES,
        "abstract": (data.get("abstractNote") or "").strip(),
        "summary": "",
        "tags": tags,
        "featured": False,
        "zotero_key": item["key"],          # marker: this page is auto-managed
    }

    # Identifiers and links use the current schema. The older top-level `doi`
    # and `url_source` keys still work but make Hugo print deprecation
    # warnings on every build.
    if data.get("DOI"):
        fm["hugoblox"] = {"ids": {"doi": data["DOI"]}}
    if data.get("url"):
        fm["links"] = [{"type": "source", "url": data["url"]}]

    fm = {k: v for k, v in fm.items() if v not in (None, "", [])}
    fm["featured"] = False

    body = ("<!-- This page is generated automatically from the Tuwhiri Zotero "
            "group library. Edits made here will be overwritten. Change the "
            "record in Zotero instead. -->\n")
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                           default_flow_style=False, width=10000)
    return slug, f"---\n{front}---\n\n{body}", \
        bibtex_entry(item, authors_display, slug)


# --- Main -------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    lookup = load_roster()
    print(f"Fetching Zotero group {GROUP_ID} ...")
    try:
        items = fetch_all()
    except urllib.error.HTTPError as err:
        if err.code == 403:
            sys.exit(
                "Zotero refused the request (HTTP 403).\n"
                "The group library is not readable without credentials.\n"
                "Either set Library Reading to 'Anyone' at\n"
                f"  https://www.zotero.org/groups/{GROUP_ID}/settings/library\n"
                "or create a read-only key at https://www.zotero.org/settings/keys\n"
                "and store it as a repository secret named ZOTERO_API_KEY."
            )
        if err.code == 404:
            sys.exit(f"Zotero has no group with id {GROUP_ID} (HTTP 404). "
                     "Check the GROUP_ID setting near the top of this script.")
        sys.exit(f"Zotero returned HTTP {err.code}: {err.reason}")
    except urllib.error.URLError as err:
        sys.exit(f"Could not reach Zotero: {err.reason}")

    print(f"  {len(items)} items retrieved from Zotero\n")
    if not items:
        print("=" * 68)
        print("THE ZOTERO GROUP LIBRARY IS EMPTY.")
        print("")
        print("Zotero answered correctly, but there are no references in the")
        print("group yet, so there is nothing to put on the website. This is")
        print("not a fault. Add references to the group library at")
        print(f"  https://www.zotero.org/groups/{GROUP_ID}")
        print("and run this again.")
        print("=" * 68)
        return

    OUTDIR.mkdir(parents=True, exist_ok=True)
    written, seen = 0, set()

    for item in items:
        built = build_page(item, lookup)
        if not built:
            continue
        slug, markdown, bib = built
        seen.add(slug)
        folder = OUTDIR / slug
        target = folder / "index.md"
        existing = target.read_text(encoding="utf-8") if target.exists() else ""
        if existing == markdown:
            continue
        print(f"  {'would write' if args.dry_run else 'writing'}  {slug}")
        if not args.dry_run:
            folder.mkdir(parents=True, exist_ok=True)
            target.write_text(markdown, encoding="utf-8")
            (folder / "cite.bib").write_text(bib, encoding="utf-8")
        written += 1

    # Remove pages whose Zotero record has gone, but only ones we created.
    removed = 0
    for folder in sorted(OUTDIR.iterdir()):
        if not folder.is_dir() or folder.name in seen:
            continue
        index = folder / "index.md"
        if index.exists() and "zotero_key:" in index.read_text(encoding="utf-8"):
            print(f"  {'would remove' if args.dry_run else 'removing'}  {folder.name}")
            if not args.dry_run:
                for child in folder.iterdir():
                    child.unlink()
                folder.rmdir()
            removed += 1

    print(f"\n{written} page(s) added or updated, {removed} removed.")


if __name__ == "__main__":
    main()
