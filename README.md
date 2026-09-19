# Tuwhiri website

Source for the website of **Tuwhiri**, an MBIE Endeavour Programme (2025–2030)
led by the University of Otago: *Building critical capability for space-based
climate monitoring with next generation photonics.*

| | |
|---|---|
| Live site | `https://tuwhiri.netlify.app` — built from `main` |
| Draft site | `https://draft--tuwhiri.netlify.app` — built from `draft` |
| Repository | `https://github.com/Tuwhiri/tuwhiri-website` |
| Publications | Synced weekly from Zotero group `6627926` |

**If you are here to add a news item or edit a person, read
[CONTENT-GUIDE.md](CONTENT-GUIDE.md) instead.** This file is for whoever
maintains the machinery.

---

## 1. Stack

| Component | Version / notes |
|---|---|
| Hugo | **Extended**, ≥ 0.161.1. Pinned to 0.164.0 in `netlify.toml` |
| Theme | HugoBlox Kit — `github.com/HugoBlox/kit/modules/blox`, pinned in `go.mod` |
| Template origin | HugoBlox `academic-cv` |
| Go | Required — the theme is a Hugo Module |
| Node | 22. Tailwind CSS and Preact are compiled at build time |
| Package manager | **pnpm**, declared in `package.json` |
| Search index | `pagefind`, generated after Hugo runs |
| Host | Netlify |
| CI | GitHub Actions |

Three things bite newcomers:

- **Hugo must be Extended and ≥ 0.161.1.** Older versions fail with errors
  about jsx or undefined template functions that say nothing about the version.
- **`.npmrc` is load-bearing.** It contains one line, `node-linker=hoisted`.
  Without it pnpm creates `node_modules/.bin/tailwindcss` as a shell script,
  Hugo insists it be a Node script, and the build dies with
  `binary "tailwindcss" is not a Node.js script`.
- **Use pnpm, not npm.** `npm install` writes a competing lockfile and lets
  local builds drift from Netlify's.

### Local build

```bash
git clone https://github.com/Tuwhiri/tuwhiri-website.git
cd tuwhiri-website
git checkout draft
corepack enable      # once, ever
pnpm install         # once per branch
hugo server          # → http://localhost:1313
```

Site-wide search does not work under `hugo server`, because the pagefind index
is built separately. Use `pnpm run build` to test it.

---

## 2. Branch and deploy model

| Branch | Netlify context | URL | Who merges |
|---|---|---|---|
| `main` | production | `tuwhiri.netlify.app` | approver only, via PR |
| `draft` | branch deploy | `draft--tuwhiri.netlify.app` | anyone with write access |
| PR branches | deploy preview | auto-generated | — |

Work lands on `draft`; a pull request from `draft` into `main` publishes it.
`main` is protected and requires review from `CODEOWNERS`.

Draft and preview builds overwrite `robots.txt` with `Disallow: /`, so
unfinished pages are not indexed. **The draft site is unlisted, not private** —
anyone with the address can read it.

---

## 3. Content model

```
content/
  _index.md                  home page (landing, ~11 blocks)
  atmospheric-science/       ┐
  photonics/                 ├ research area landing pages
  engineering/               ┘
  outreach/                  outreach landing page
  people/index.md            People page — defines the group headings
  blog/<date-slug>/          news items
  events/<slug>/             events
  publications/<slug>/       GENERATED — do not hand-edit
  authors/<slug>/_index.md   stub pages only; see §5
data/
  team.yaml                  the roster — single source of truth for people
  authors/<slug>.yaml        GENERATED from team.yaml
  themes/tuwhiri.yaml        brand colours
  fonts/tuwhiri.yaml         brand typography
assets/
  media/authors/<slug>.jpg   staff photographs
  media/partners/            partner logos
  media/logo.svg, icon.svg   site logo and favicon (detected by filename)
  css/hbx/blocks/tuwhiri-brand/style.css    local CSS overrides
layouts/
  _partials/hbx/blocks/publication-filter/  custom block, see §6
```

### Research areas

The four tags `atmospheric-science`, `photonics`, `engineering` and `outreach`
are functional, not decorative. Each area page filters its news by tag, and each
person's area determines how their publications are tagged. A fifth tag,
`programme`, is a catch-all and filters nothing.

---

## 4. People

`data/team.yaml` is the single source of truth. Everything else is generated:

```bash
python3 scripts/make_people.py     # needs: pip install pyyaml
```

This writes `data/authors/<slug>.yaml` (the profile shown on the site) and
`content/authors/<slug>/_index.md` (a stub that exists only so the page is
built). It also deletes both for anyone removed from the roster.

Two fields deserve attention:

- **`family:`** is optional and only needed when the surname is not simply the
  last word — middle names, initials, compound surnames. Sorting is on the
  surname, so without it "Harald G. L. Schwefel" sorts under G.
- **`match:`** lists surname spellings used to recognise the person in Zotero
  author lists. Accents and hyphens are normalised automatically.

Photographs go in `assets/media/authors/<slug>.jpg`, matched by filename.

---

## 5. Why author pages are switched off by default

`content/authors/_index.md` carries a cascade setting `build.render: never` for
every author, and each roster member's stub switches theirs back on.

The reason: `authors` is a Hugo taxonomy, so without this, every external
co-author appearing on any publication gets their own page — pages like
`anna-r.-petersen` containing one paper. The cascade suppresses them; external
co-authors still appear in full in citations, as plain text rather than links.

If you delete the cascade, those pages return on the next Zotero sync.

---

## 6. Custom code — what is ours, and why

Everything here is **additive**. Nothing shadows a theme file, so a theme
upgrade cannot silently replace it.

| File | Purpose |
|---|---|
| `layouts/_partials/hbx/blocks/publication-filter/block.html` | Search / type / year filters on the publications page |
| `assets/css/hbx/blocks/tuwhiri-brand/style.css` | Two CSS overrides, see below |
| `data/themes/tuwhiri.yaml`, `data/fonts/tuwhiri.yaml` | Brand colours and typeface |
| `scripts/zotero_sync.py`, `scripts/make_people.py` | Content generation |

**`publication-filter`** is a new block, not an override — the theme has no
block by that name. The previous theme generation had a dedicated
`layouts/section/publication.html` with these controls; the current one dropped
it. The block renders the full list at build time and the script only hides and
shows, so it degrades to a plain list without JavaScript.

**`style.css`** fixes two things the theme gives no setting for:

1. The navigation drop-down rendered pale text on a white panel in light mode —
   a contrast ratio of 1.12:1, effectively invisible — because it inherits its
   colour from the header, and our header is dark. It now matches the header.
2. Partner logos were capped at 7rem wide, squashing anything wider than about
   2:1. Kea Aerospace (4.45:1) rendered at under half height. Cap raised to
   16rem.

### One known theme regression, currently unpatched

On a publication page, the author byline renders each name as a plain `<div>`
with no link, even for team members with profile pages. The previous theme
generation linked them, and the current theme still ships a partial that does
this correctly — `_partials/page_metadata_authors.html` — but `single.html` no
longer calls it, rendering the byline inline instead.

Team authors are still linked from the sidebar Authors panel and from the
publications listing, so nothing is unreachable.

Fixing it locally requires copying the theme's 352-line `single.html` into
`layouts/` and editing it, which was judged not worth the maintenance debt.
**The better fix is upstream**: report it at `github.com/HugoBlox/kit` — the ask
is that `single.html` use the existing `page_metadata_authors` partial.

---

## 7. Publications pipeline

Zotero group `6627926` → `.github/workflows/zotero-sync.yml` → `content/publications/`.

Runs Sundays 19:00 UTC (Monday morning NZ) and on demand from the Actions tab.
It writes only to the branch chosen in the `target_branch` input, default
`draft`. It never touches `main`.

The script:

- skips notes, attachments, and anything tagged `no-website` in Zotero;
- derives research-area tags **from the authors**, by matching surnames against
  `data/team.yaml` — a paper by Suresh and Kessenich gets both `photonics` and
  `atmospheric-science`;
- **does not** copy Zotero keyword tags. A shared library accumulates
  inconsistent keywords that would swamp the four functional tags. To allow
  specific ones, add them to `ALLOWED_ZOTERO_TAGS` in the script;
- deletes pages whose Zotero record has gone, identified by the `zotero_key`
  in their front matter. Hand-written publication pages are never touched.

Authentication: anonymous if the group library is world-readable, otherwise via
a `ZOTERO_API_KEY` repository secret.

**Never hand-edit `content/publications/`.** Fix the record in Zotero; the next
sync overwrites local changes.

---

## 8. Maintenance calendar

**Every few months** — check the Actions tab for failures. GitHub retires Node
versions periodically; the fix is to raise the version after `@` in
`.github/workflows/zotero-sync.yml`.

**Annually, or when something looks wrong** — theme upgrade. Bump the module in
`go.mod`, build locally, compare against the live site before merging. Check
whether the author-link regression in §6 has been fixed.

**Watch for** — a breaking HugoBlox migration. This project has already moved
once (Bootstrap → Tailwind generation) and the ecosystem is under active
development. Budget real time for the next one; the custom code in §6 is
deliberately small to make it survivable.

**Before 2030** — the programme ends. Decide whether the site is archived,
handed to a successor programme, or frozen. A static export or an institutional
host is the safer long-term home than a free Netlify site.

---

## 9. Known issues and unfinished business

These are live and worth attention:

1. **`.github/CODEOWNERS` still contains placeholder usernames**
   (`@harald-github-username` and so on). Until real GitHub usernames are
   filled in, review assignment on `main` does not work. **This is the most
   important item on this list.**

2. **Three leftover template workflows** in `.github/workflows/`:
   - `upgrade.yml` — upgrades HugoBlox automatically every Monday 05:00 UTC.
     An unattended theme upgrade on a site this customised is a poor idea.
     Recommend deleting, or restricting to `workflow_dispatch` only.
   - `publish.yaml` — deploys to GitHub Pages on every push to `main`,
     duplicating Netlify. Recommend deleting.
   - `import-publications.yml` — imports from a `publications.bib` that does
     not exist. Superseded by the Zotero sync. Recommend deleting.

3. **`.github/FUNDING.yml`** puts a "Sponsor" button on the repository pointing
   at the theme author. Delete it.

4. **Unused partner logo files** — `waikatoWhite.svg` and
   `Q-Bifrost_LogoWhite.svg` are light-on-dark variants, but the logos block
   uses one file for both colour modes and nothing references them. Either
   remove them or add per-mode support. Also `kea-aerospace.png` is referenced
   while `kea-aerospace.svg` exists — switching to the SVG will look sharper.

5. **Both EGU abstracts have Zotero item type "Report"** and so appear under
   Report in the publications type filter. Change the item type in Zotero to
   Conference Paper.

6. **`tuwhiri@otago.ac.nz`** is published as the contact address. Confirm it
   exists and forwards to the Programme Manager — enquiries to a non-existent
   address fail silently.

7. **Documentation left over from the build** — `ORDERING.md`,
   `DROPDOWN-FIX.md` and `HOWTO.md` were working notes, superseded by this file
   and `CONTENT-GUIDE.md`. `BRAND.md` is worth keeping.

---

## 10. Access and accounts

Whoever takes this on will need:

- **GitHub** — write access to `Tuwhiri/tuwhiri-website`, and admin if they are
  to manage branch protection.
- **Netlify** — access to the site. Confirm more than one person has it; a site
  owned by a single departing account is a real risk.
- **Zotero** — membership of group `6627926`, at least read.
- **Repository secrets** — `ZOTERO_API_KEY` if the library is not public.
  Secrets are write-only and cannot be read back; a lost key must be reissued.

Brand assets come from **Māui Studios**, who produced the identity. The colour
and type specification is in `BRAND.md`.
