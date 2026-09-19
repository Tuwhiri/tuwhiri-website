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
PAGES = ROOT / "content" / "authors"


def existing_bio(path):
    """Keep any biography already written into the author file."""
    if not path.exists():
        return ""
    try:
        current = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return ""
    return (current.get("bio") or "").strip()


def split_name(person):
    """Work out given / middle / family from the roster entry.

    The naive rule -- first word is the given name, everything else is the
    family name -- gets middle names and initials wrong, and the family name is
    what the People page sorts on. "Harald G. L. Schwefel" would sort under G,
    and "H. Randy Pollock" under R.

    So the roster may state it explicitly:

        - name: Harald G. L. Schwefel
          family: Schwefel          # optional, overrides the guess
          given: Harald             # optional

    Where `family` is given, everything between it and the given name is
    treated as a middle name. Where it is not, we fall back to the old rule,
    which is right for the ordinary two-word case.
    """
    name = person["name"]
    parts = name.split()
    given = person.get("given") or parts[0]
    family = person.get("family")
    if not family:
        family = " ".join(parts[1:]) if len(parts) > 1 else parts[0]
    middle = name
    for piece in (given, family):
        middle = middle.replace(piece, "", 1)
    middle = " ".join(middle.split())
    return given, middle, family


def build(person):
    name = person["name"]
    parts = name.split()

    given, middle, family = split_name(person)
    name_block = {"display": name, "given": given, "family": family}
    if middle:
        name_block["middle"] = middle

    links = []
    if person.get("email"):
        links.append({"icon": "at-symbol",
                      "url": "mailto:" + person["email"],
                      "label": "Email"})
    if person.get("orcid"):
        links.append({"icon": "academicons/orcid",
                      "url": "https://orcid.org/" + person["orcid"],
                      "label": "ORCID"})

    # Optional profile links. Each is a plain field in data/team.yaml, so it
    # survives the next run of this script -- anything added by hand to
    # data/authors/<slug>.yaml is overwritten, because `links` is rebuilt here.
    for field, icon, label in (
        ("linkedin",   "brands/linkedin",           "LinkedIn"),
        ("scholar",    "academicons/google-scholar", "Google Scholar"),
        ("researchgate", "academicons/researchgate", "ResearchGate"),
        ("github",     "brands/github",             "GitHub"),
        ("website",    "hero/globe-alt",            "Website"),
    ):
        value = (person.get(field) or "").strip()
        if not value:
            continue
        url = value if value.startswith(("http://", "https://")) else "https://" + value
        links.append({"icon": icon, "url": url, "label": label})

    profile = {
        "schema": "hugoblox/author/v1",
        "slug": person["slug"],
        "name": name_block,
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

        # Every person also needs a stub page, or their profile does not exist.
        #
        # Profile pages are taxonomy pages, and Hugo only builds one for an
        # author who appears on some publication or news item. Without this
        # stub, anyone with nothing published yet -- students, the programme
        # manager, most of the advisory board -- would be linked to from the
        # People page but land on a 404.
        stub_dir = PAGES / person["slug"]
        stub_dir.mkdir(parents=True, exist_ok=True)
        stub = stub_dir / "_index.md"

        # An existing stub may predate the render setting, in which case the
        # profile page silently stops being built. Repair it rather than
        # leaving it: add the build block, keep everything else.
        if stub.exists() and "render: always" not in stub.read_text(encoding="utf-8"):
            existing = stub.read_text(encoding="utf-8")
            if existing.startswith("---"):
                _, front, rest = existing.split("---", 2)
                stub.write_text(
                    "---" + front.rstrip("\n") +
                    "\nbuild:\n  render: always\n  list: always\n---" + rest,
                    encoding="utf-8")
                print(f"  repaired content/authors/{person['slug']}/_index.md")

        if not stub.exists():
            stub.write_text(
                "---\n"
                f"title: {person['name']}\n"
                "# This file switches the profile page ON for this person.\n"
                "# content/authors/_index.md switches every author page OFF by\n"
                "# default, so that external co-authors from Zotero do not get\n"
                "# pages of their own. Removing this file hides the profile.\n"
                "#\n"
                "# The details shown come from data/authors/"
                f"{person['slug']}.yaml\n"
                "build:\n"
                "  render: always\n"
                "  list: always\n"
                "---\n",
                encoding="utf-8")

    # Remove data and stub pages for anyone no longer in the roster, so that
    # deleting a person from data/team.yaml is enough to remove them from the
    # site. Without this they linger: the profile file stays behind and their
    # page keeps being published.
    slugs = {person["slug"] for person in people}
    removed = []
    for path in sorted(AUTHORS.glob("*.yaml")):
        if path.name not in written:
            path.unlink()
            removed.append(f"data/authors/{path.name}")
    for folder in sorted(PAGES.iterdir()) if PAGES.exists() else []:
        if folder.is_dir() and folder.name not in slugs:
            for child in folder.iterdir():
                child.unlink()
            folder.rmdir()
            removed.append(f"content/authors/{folder.name}/")
    if removed:
        print("Removed, no longer in data/team.yaml:")
        for name in removed:
            print(f"  {name}")
        print()

    print(f"Done. {len(people)} people written to data/authors/,")
    print(f"      and {len(people)} profile pages under content/authors/.")
    print("Photographs go in assets/media/authors/<slug>.jpg")


if __name__ == "__main__":
    main()
