#!/usr/bin/env python3
"""
One-off: bring existing publication pages up to the current schema.

    python3 fix_publication_schema.py

Run once from the top of the repository. After this, the updated
scripts/zotero_sync.py produces the new form for everything it writes, so this
script is never needed again.

What it changes:
    doi: 10.1234/x          ->  hugoblox: {ids: {doi: 10.1234/x}}
    url_source: https://... ->  links: [{type: source, url: https://...}]
and drops empty url_pdf / url_code / url_dataset / publication_short keys.

Both old forms still work; they just make Hugo print a deprecation warning on
every build.
"""
import pathlib, sys

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency. Run:  pip install pyyaml")

LEGACY = {"url_pdf": "pdf", "url_preprint": "preprint", "url_code": "code",
          "url_dataset": "dataset", "url_poster": "poster",
          "url_project": "project", "url_slides": "slides",
          "url_source": "source", "url_video": "video"}

root = pathlib.Path("content/publications")
if not root.exists():
    sys.exit("No content/publications folder here. Run from the repository root.")

count = 0
for path in sorted(root.glob("*/index.md")):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        continue
    _, head, body = text.split("---", 2)
    fm = yaml.safe_load(head) or {}
    changed = False

    if "doi" in fm and fm["doi"]:
        fm.setdefault("hugoblox", {}).setdefault("ids", {})["doi"] = fm.pop("doi")
        changed = True
    fm.pop("doi", None)

    for old, kind in LEGACY.items():
        value = fm.pop(old, None)
        if value:
            fm.setdefault("links", []).append({"type": kind, "url": value})
            changed = True

    if not fm.get("publication_short"):
        changed = fm.pop("publication_short", None) is not None or changed

    if changed:
        path.write_text(
            "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                                     width=10000) + "---" + body,
            encoding="utf-8")
        print(f"  updated {path.parent.name}")
        count += 1

print(f"\n{count} publication page(s) updated.")
