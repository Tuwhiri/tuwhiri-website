#!/usr/bin/env python3
"""
Generate data/authors/<slug>.yaml for every person in data/team.yaml.

    python3 scripts/make_people.py

Safe to re-run. Each author file is rebuilt from the roster, so lasting changes
belong in data/team.yaml, not in the generated files.

The exception is `bio`: a biography written into an author file by hand is kept.

Photographs go in assets/media/authors/<slug>.jpg, matched by filename. This
script never touches them.
"""

import pathlib
import sys

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency. Run:  pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROSTER = ROOT / "data" / "team.yaml"
AUTHORS = ROOT / "data" / "authors"


def existing_bio(path):
    """Keep any biography already written into the author file."""
    if not path.exists():
        return ""
    try:
        current = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return ""
    return (current.get("bio") or "").strip()


def build(person):
    name = person["name"]
    parts = name.split()

    links = []
    if person.get("email"):
        links.append({"icon": "at-symbol",
                      "url": "mailto:" + person["email"],
                      "label": "Email"})
    if person.get("orcid"):
        links.append({"icon": "academicons/orcid",
                      "url": "https://orcid.org/" + person["orcid"],
                      "label": "ORCID"})

    profile = {
        "schema": "hugoblox/author/v1",
        "slug": person["slug"],
        "name": {
            "display": name,
            "given": parts[0],
            "family": " ".join(parts[1:]) if len(parts) > 1 else parts[0],
        },
        "role": person.get("role", ""),
        "bio": "",
        "affiliations": ([{"name": person["org"]}] if person.get("org") else []),
        "links": links,
        "user_groups": person.get("groups", []),
    }
    if person.get("area"):
        profile["research_area"] = person["area"]
    return profile


def main():
    if not ROSTER.exists():
        sys.exit(f"Cannot find {ROSTER}. Run this from the repository root.")

    roster = yaml.safe_load(ROSTER.read_text(encoding="utf-8"))
    people = roster.get("people", [])
    AUTHORS.mkdir(parents=True, exist_ok=True)

    written = set()
    for person in people:
        path = AUTHORS / f"{person['slug']}.yaml"
        profile = build(person)
        profile["bio"] = existing_bio(path)
        path.write_text(
            yaml.safe_dump(profile, sort_keys=False, allow_unicode=True,
                           default_flow_style=False),
            encoding="utf-8")
        written.add(path.name)

    strays = [p.name for p in AUTHORS.glob("*.yaml") if p.name not in written]
    if strays:
        print("These author files are not in data/team.yaml. Delete them by "
              "hand if the person has left the programme:")
        for name in sorted(strays):
            print(f"  data/authors/{name}")
        print()

    print(f"Done. {len(people)} people written to data/authors/")
    print("Photographs go in assets/media/authors/<slug>.jpg")


if __name__ == "__main__":
    main()
