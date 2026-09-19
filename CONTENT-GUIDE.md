# Looking after the Tuwhiri website

This is for whoever keeps the website's content up to date. It assumes you have
never used GitHub, never written code, and would rather not start now.

You do not need to install anything. Everything here happens in a web browser.

Allow twenty minutes to read this once. After that, posting a news item takes
about five minutes.

---

## Part 1. How the site works, in one page

There are two copies of the website.

| | Address | What it is |
|---|---|---|
| **Draft** | `draft--tuwhiri.netlify.app` | The working version. Rough edges fine. |
| **Live** | `tuwhiri.netlify.app` | What the public sees. |

You always edit the draft. When the draft looks right, someone with approval
rights publishes it to the live site.

The useful comparison is a manuscript. The draft is the shared document everyone
types into. The live site is the published version. Moving one to the other is a
deliberate act that somebody signs off — exactly like submitting a paper.

**Nothing you do can break the live site.** That is the point of the
arrangement. The worst that happens on the draft is that the draft looks wrong
for a few minutes.

Changes appear on the draft site about a minute after you save them. Not
instantly — if you refresh and nothing has changed, wait and refresh again.

### What you need

A free GitHub account, and someone to add you to the Tuwhiri repository. Ask
the Programme Manager. Once that is done, everything is at:

`https://github.com/Tuwhiri/tuwhiri-website`

---

## Part 2. The one thing that goes wrong

**Always check you are on the `draft` branch before editing.**

Above the list of files there is a button showing a branch name. If it says
`main`, click it and choose `draft`. If it already says `draft`, carry on.

Editing on `main` will fail at the end, after you have typed everything, with a
message about permissions. Annoying, and entirely avoidable.

---

## Part 3. Posting a news item

1. Go to the repository and **switch to `draft`**.
2. Click **Add file** → **Create new file**.
3. In the filename box, type this, including the slashes:

   ```
   content/blog/2026-09-14-balloon-flight-from-lauder/index.md
   ```

   Typing a `/` creates a folder as you go. Use the date, then a few words
   describing the item. Lower case, hyphens instead of spaces, no punctuation
   and no accented characters in the folder name.

4. Paste this into the big box and edit it:

   ```
   ---
   title: "First balloon flight from Lauder"
   summary: "One sentence describing the item. This appears in listings."
   date: 2026-09-14
   authors:
     - annika-seppala
   tags:
     - engineering
   featured: false
   ---

   Write the article here, in ordinary paragraphs. Leave a blank line
   between paragraphs.

   ## A subheading looks like this

   You can make text **bold** or *italic*, and add
   [a link like this](https://example.org).
   ```

5. Scroll down, type a short note saying what you did, and click
   **Commit changes**.

6. Wait a minute, then look at `draft--tuwhiri.netlify.app/blog/`.

### The block at the top

The part between the two `---` lines is the label on the item. It is fussy about
spacing — keep the indentation exactly as shown, and never use the Tab key.

| Line | What to put |
|---|---|
| `title` | The headline, in quotation marks |
| `summary` | One sentence. Shows in listings and link previews |
| `date` | `YYYY-MM-DD`. Controls the ordering |
| `authors` | Folder names, not display names — see below |
| `tags` | Which research area, see below |
| `featured` | `true` puts it on the home page. Use sparingly |

### Author names

These must be the person's **slug**, not their display name:
`annika-seppala`, not `Annika Seppälä`. To find someone's slug, open the
`data/authors/` folder and look at the filenames.

Get it wrong and the name simply does not appear. There is no error.

### Tags

Use one or more of these five, spelled exactly:

- `atmospheric-science`
- `photonics`
- `engineering`
- `outreach`
- `programme` — for anything that spans the whole programme

The first four are not decoration: an item tagged `photonics` also appears on
the Photonics page. `programme` does not filter anything; it is for items that
belong to no single area.

### Adding a photograph

Put an image called `featured.jpg` in the same folder as the item.

Open the item's folder, click **Add file** → **Upload files**, drag the image
in, commit. Nothing to configure — it is found by its name.

Resize it to about 1600 pixels wide first. A folder of photographs straight
from a phone will slow every future build, permanently.

**Only use photographs you have the right to use.** Your own, the University's,
or ones you have been given permission for. An image found through a web search
almost certainly belongs to somebody, and a public university website is a poor
place to find that out.

---

## Part 4. Editing people

### Changing someone's details

Everyone has a file at `data/authors/<their-slug>.yaml`. Open it, click the
pencil icon, edit, commit — on `draft`.

The `bio:` line is their biography. The rest are structured fields; keep the
indentation exactly as it is.

### Adding a photograph of someone

Upload it to `assets/media/authors/`, named to match their slug —
`harald-schwefel.jpg`. About 800 pixels square is plenty.

### Adding or removing someone

This one is different, and there is a reason.

`data/team.yaml` is the master list. It controls the People page **and** how
publications are sorted into research areas. Editing `data/authors/` alone is
not enough — that folder is generated from `data/team.yaml`.

So: add or remove the person in `data/team.yaml`, copying the shape of an
existing entry, and then **ask whoever maintains the site to run the update
script**. It is one command and takes them a few seconds.

If you skip that step, the person will not appear.

### Changing the order people appear in

Within each heading, people are listed alphabetically by surname. To change the
headings themselves, or their order, edit the list in
`content/people/index.md`. The headings there must match the `groups:` values
in `data/team.yaml` exactly, including capital letters and the `&` in
`Engagement & Outreach`.

---

## Part 5. Publications — do not edit these

Publications come from the programme's **Zotero group library** and are
rewritten automatically every Monday morning.

- **To add a paper**: put it in the Zotero group. That is all.
- **To correct a title, author or date**: fix it in Zotero, not on the website.
  Anything you change on the website is overwritten at the next sync.
- **To hide something**: give it the tag `no-website` in Zotero.

Research areas are worked out from the authors. A paper by two members of the
photonics team is tagged `photonics` automatically; nobody has to remember.

If a paper appears in the main list but not on its research area page, the
author is missing from `data/team.yaml`, or their surname is spelled
differently in Zotero.

---

## Part 6. Adding an event

Same as a news item, but in `content/events/` and with different fields:

```
---
title: "Tuwhiri annual meeting"
summary: "One sentence."
event_start: '2027-02-10T09:00:00+13:00'
event_end: '2027-02-11T17:00:00+13:00'
location: University of Otago
authors:
  - carla-meledandri
tags:
  - programme
---

Details here.
```

The `+13:00` is New Zealand time. Use `+12:00` between April and September,
when daylight saving is not in effect.

---

## Part 7. Publishing to the live site

When the draft looks right:

1. On the repository, click the **Pull requests** tab → **New pull request**.
2. Set **base: main** on the left and **compare: draft** on the right.
   Getting these the wrong way round is the usual mistake — base is the
   destination.
3. Click **Create pull request** and give it a title, such as
   `Publish September news`.
4. GitHub asks the approvers to review it. Netlify posts a link in the comments
   showing exactly what the change looks like.
5. Once someone approves, click **Merge pull request**.

Two minutes later it is live.

**You cannot approve your own pull request** — GitHub does not allow it. If you
opened it, someone else must approve.

Do this in batches, perhaps fortnightly, rather than one item at a time.

---

## Part 8. When something goes wrong

**My change has not appeared.**
Check you were on `draft`. Then wait another minute — builds take about that
long. Then refresh with Ctrl+Shift+R (Cmd+Shift+R on a Mac), which forces the
browser to fetch a fresh copy.

**The page has gone blank, or looks broken.**
Almost always the block at the top of the file. Look for a stray Tab character,
a missing `---`, or a line that has lost its indentation.

Every file has a **History** button. Open the last version that worked, and
restore it. Nothing is ever lost — that is what this system is for.

**A person is not showing on the People page.**
Their `groups:` value in `data/team.yaml` does not match a heading in
`content/people/index.md`, or they were added to `data/authors/` without going
through `data/team.yaml`.

**A news item is not on its research area page.**
Check the tag is spelled exactly as in Part 3 — `atmospheric-science`, not
`Atmospheric Science`.

**Something else.**
Take a screenshot and ask whoever maintains the site. It is almost certainly a
five-minute fix, and asking is much faster than experimenting.

---

## Part 9. A short checklist for each item

- [ ] On the `draft` branch
- [ ] Folder name is lower case, hyphenated, dated
- [ ] `date` is `YYYY-MM-DD`
- [ ] `authors` are slugs, not display names
- [ ] `tags` are from the list of five
- [ ] Photograph is one you have the right to use, and resized
- [ ] Checked it on the draft site before asking for it to be published

---

## Where to ask

The Programme Manager holds the list of who does what. For anything involving
the machinery rather than the words — a script to run, a build that failed, a
theme upgrade — that is a job for whoever maintains the site, and `README.md`
in this repository is written for them.
