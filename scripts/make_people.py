#!/usr/bin/env python3
"""
Generate content/authors/<slug>/_index.md for every person in data/team.yaml.

Run from the repository root:

    python3 scripts/make_people.py

Safe to re-run. It only rewrites the YAML front matter (the part between the
--- markers). Anything you have typed BELOW the front matter -- i.e. a person's
biography -- is preserved. Avatars are never touched.

To add a photo for someone, drop a file called avatar.jpg (or avatar.png) into
their folder, e.g. content/authors/harald-schwefel/avatar.jpg
"""

import pathlib
import sys

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency. Run:  pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROSTER = ROOT / "data" / "team.yaml"
AUTHORS = ROOT / "content" / "authors"


def split_existing(path):
    """Return the body text (below the front matter) of an existing file."""
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip("\n")
    return ""


def build_front_matter(person):
    name = person["name"]
    bits = name.split()
    first_name = bits[0]
    last_name = bits[-1]

    social = []
    if person.get("email"):
        social.append({"icon": "envelope", "icon_pack": "fas",
                       "link": "mailto:" + person["email"]})
    if person.get("orcid"):
        social.append({"icon": "orcid", "icon_pack": "ai",
                       "link": "https://orcid.org/" + person["orcid"]})

    fm = {
        "title": name,
        "first_name": first_name,
        "last_name": last_name,
        "superuser": False,
        "role": person.get("role", ""),
        "organizations": [{"name": person.get("org", ""), "url": ""}],
        "bio": "",
        "social": social,
        "user_groups": person.get("groups", []),
    }
    if person.get("area"):
        fm["research_area"] = person["area"]
    return fm


def main():
    if not ROSTER.exists():
        sys.exit(f"Cannot find {ROSTER}. Run this from the repository root.")

    roster = yaml.safe_load(ROSTER.read_text(encoding="utf-8"))
    people = roster.get("people", [])
    AUTHORS.mkdir(parents=True, exist_ok=True)

    for person in people:
        folder = AUTHORS / person["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "_index.md"

        body = split_existing(path)
        if not body.strip():
            body = (
                f"<!-- Write {person['name']}'s biography here, in plain "
                "sentences. Delete this comment line first. -->\n"
            )

        fm = yaml.safe_dump(build_front_matter(person),
                            sort_keys=False, allow_unicode=True,
                            default_flow_style=False)
        path.write_text(f"---\n{fm}---\n\n{body}", encoding="utf-8")
        print(f"  wrote {path.relative_to(ROOT)}")

    print(f"\nDone. {len(people)} people written to content/authors/")
    print("Remember to add avatar.jpg files where you have photos.")


if __name__ == "__main__":
    main()
