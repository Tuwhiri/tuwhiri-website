# How names are ordered, and a bug found while checking

## The rules

There are three different orderings on the site, and they work differently.

### 1. Group order on the People page

**Set by hand**, by the order you list them in `content/people/index.md`:

```yaml
      user_groups:
        - Programme Leadership
        - Atmospheric Science
        - Photonics
        - Space Systems Engineering
        - Engagement & Outreach
        - Advisory Board
        - Students
        - Alumni
```

Reorder that list and the page reorders. Delete a line and the group disappears
from the page — the people are still there, they just stop being shown under
that heading. A group with nobody in it is skipped.

Somebody in two groups appears in both. That is why Harald, Annika, Mika and
Randy each show up under Programme Leadership and again under their research
area.

### 2. Order within a group

**Alphabetical by surname**, from these two lines:

```yaml
      sort_by: name_family
      sort_ascending: true
```

The comparison is case-insensitive, and ties break on surname again, so the
result is stable between builds.

Other values `sort_by` accepts: `weight` (a number you assign, for a fully
manual order), `graduation_year`, `role`, or any other field in the author file.
`weight` and `graduation_year` sort numerically; everything else alphabetically.

A single group can override the rest. This is what Alumni are usually for:

```yaml
      user_groups:
        - Programme Leadership
        - Photonics
        - name: Alumni
          sort_by: graduation_year
          sort_ascending: false
```

If you ever want a hand-picked order — leadership by seniority rather than
alphabet, say — add `weight: 10`, `weight: 20` and so on to `data/team.yaml`,
then set `sort_by: weight` for that group. Leave gaps of ten so you can insert
someone later without renumbering.

### 3. Authors on a publication

**Exactly as Zotero has them**, which is to say as the journal printed them.
Never re-sorted — author order carries meaning in a paper. To change it, change
the record in Zotero.

---

## The bug

Sorting is on the **surname**, and the surname was being guessed as "everything
after the first word". That is right for *Mallika Suresh* and wrong for anyone
with a middle name or an initial.

Five of your 32 people were affected:

| Name | Was sorting under | Now sorts under |
|---|---|---|
| Harald G. L. Schwefel | **G** | Schwefel |
| H. Randy Pollock | **Randy** | Pollock |
| Hans Philipp Sültrop | **Philipp** | Sültrop |
| Luis Enrique García Muñoz | **Enrique** | García Muñoz |
| Gabriel Santamaría Botello | Santamaría | Santamaría Botello |

The last is a compound surname and was already correct; it is listed for
completeness.

This was easy to miss because it often looks right by accident. Under Programme
Leadership, "g. l. schwefel" happens to fall before "suresh", so the order
appeared correct while sorting on the wrong thing.

### The fix

`data/team.yaml` now accepts an optional `family:` line, used for sorting where
the guess would be wrong:

```yaml
  - slug: harald-schwefel
    name: Harald G. L. Schwefel
    family: Schwefel
```

Added for the five above. Everyone else is unchanged, and new people with
ordinary two-word names need nothing.

`make_people.py` also now records the middle name separately, so "G. L." is
kept rather than being silently folded into the surname.

**Add `family:` for any new person whose surname is not simply the last word** —
double-barrelled names, particles like *van der*, initials before the given
name. There is a note in the file explaining it.

### Verified

The Photonics group now reads: García Muñoz, Kjærgaard, Matsko, Santamaría
Botello, Schwefel. Correctly alphabetical. 108 pages, no errors or warnings.

## Applying

```bash
cp -r tuwhiri-ordering/. /path/to/your/tuwhiri-website/
python3 scripts/make_people.py
```
