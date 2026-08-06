# Tuwhiri website — how to build it and how to run it

This guide assumes you have never made a website before. It explains what each
piece is for, not just which button to press. Work through Part 1 to Part 7 in
order; after that the parts are independent.

Allow about two hours for the first setup. Once it is done, publishing a news
item takes about three minutes.

---

## Part 0. How the whole thing works

There are three services, and each does one job.

**GitHub** stores the text. Think of it as a shared folder with a complete,
permanent history of every change and who made it. Nothing is ever really
deleted. This is where the website's content lives, as ordinary text files.

**Netlify** turns the text into a website. Every time anything changes on
GitHub, Netlify notices within a few seconds, rebuilds all the pages, and puts
them online. You never upload a website; you change the text and the website
follows.

**Zotero** holds the publication list. A script reads your group library once a
week and writes a page for each paper.

The tool that does the actual page-building is called **Hugo**. You will
probably never interact with it directly. It runs on Netlify's computers.

### The two versions of the site

You asked for a draft version and a live version. This is done with two
**branches**. A branch is a parallel copy of all the files.

| Branch | What it is | Address | Who can change it |
|---|---|---|---|
| `draft` | The working version. Rough edges allowed. | `https://draft--o4o.netlify.app` | Anyone on the team |
| `main` | The live, public website. | `https://o4o.netlify.app` | Only after Harald, Annika or Mika approves |

The useful analogy is a manuscript. `draft` is the shared Overleaf document
everyone types into. `main` is the published version. Moving work from `draft`
to `main` is a deliberate act that someone signs off, exactly like submitting.

The draft site also tells search engines not to index it, so a half-finished
page will not turn up in Google.

---

## Part 1. Accounts you need

1. **GitHub** — everyone who will edit the site needs a free account at
   github.com. Ask each person for their **username** (the name in their
   profile address, `github.com/username`). You will need Harald's, Annika's
   and Mika's in Part 6.

2. **Netlify** — one account for the programme, at netlify.com. Sign up using
   the "Sign up with GitHub" button; this saves connecting them later. Only one
   or two people need this.

3. **Zotero** — already done. The group is
   `https://www.zotero.org/groups/6627926/tuwhiri`.

A note on who should own things: create the GitHub repository under an
**organisation** rather than a personal account, and add at least two people as
owners. If it lives in one person's personal account and that person leaves,
recovering it is unpleasant. On GitHub: your avatar (top right) → *Your
organizations* → *New organization* → the free plan is fine.

---

## Part 2. Create the repository

A "repository" (everyone says *repo*) is one project's folder on GitHub.

1. Go to `https://github.com/HugoBlox/theme-research-group`
2. Click the green **Use this template** button, then **Create a new
   repository**.
3. Owner: your new organisation. Repository name: `tuwhiri-website`.
4. Choose **Public**. The site's content will be public anyway, and public
   repositories get unlimited free build minutes.
5. Click **Create repository**.

You now have your own complete copy of the Research Group template.

---

## Part 3. Add the Tuwhiri files and remove the examples

The scaffold provided alongside this guide contains everything specific to
Tuwhiri. You need to put those files into your repository and delete the
template's demonstration content.

### 3a. Upload the Tuwhiri files

Unzip the scaffold somewhere on your computer. Then in your repository on
GitHub:

1. Click **Add file** → **Upload files**.
2. Drag the *contents* of the unzipped folder into the browser window — that
   is, drag `content`, `config`, `data`, `scripts`, `static`, `.github`,
   `netlify.toml` and `HOWTO.md`, not the folder that contains them.
3. Wait for the upload to finish. Under *Commit changes*, type
   `Add Tuwhiri content and configuration`.
4. Click **Commit changes**.

> **If the `.github` folder does not upload.** Some browsers hide folders whose
> name starts with a dot. If that happens, create those two files by hand:
> **Add file** → **Create new file**, type `.github/CODEOWNERS` as the filename,
> paste the contents, commit. Repeat for
> `.github/workflows/zotero-sync.yml`.

### 3b. Delete the template's example content

These folders contain a fictional research group and must go. To delete a
folder on GitHub, open it, click the file inside, then the **⋯** menu at the
top right of the file view → **Delete file** → **Commit changes**.

Delete all of these:

```
content/admin/                          (an old content editor we replace)
content/authors/admin/                  (a made-up professor)
content/authors/吳恩達/                  (another made-up person)
content/post/20-12-01-wowchemy-prize/
content/post/20-12-02-ICML-best-paper/
content/publication/conference-paper/
content/publication/journal-article/
content/publication/preprint/
content/tour/
```

`content/admin/` matters: it installs an editor that relies on a login service
Netlify has retired. Leaving it in place will produce a broken page.

---

## Part 4. Create the draft branch

1. On the repository's main page, click the branch selector — a button showing
   **main** with a small branch symbol, just above the file list.
2. Type `draft` into the box.
3. Click **Create branch: draft from main**.

That is the entire step. You now have two identical branches that will start to
diverge as people work.

---

## Part 5. Connect Netlify

1. Log in to netlify.com.
2. **Add new site** → **Import an existing project** → **GitHub**.
3. Authorise Netlify when asked, then pick `tuwhiri-website` from the list.
4. Netlify will show build settings. It reads them from the `netlify.toml` file
   you uploaded, so leave everything as it is. Confirm that *Branch to deploy*
   is `main`.
5. Click **Deploy**.

The first build takes three to five minutes, because Netlify has to download
Hugo and its components. Later builds take under a minute.

### 5a. Set the site name

Netlify gives every site a random name like `chipper-marzipan-a1b2c3`. Change
it: **Site configuration** → **General** → **Site details** → **Change site
name** → enter `o4o`.

Your live site is now at `https://o4o.netlify.app`.

### 5b. Turn on the draft site and pull request previews

This is the step that makes the two-version arrangement work.

1. **Site configuration** → **Build & deploy** → **Branches and deploy
   contexts**.
2. Under *Branch deploys*, choose **Let me add individual branches** and enter
   `draft`.
3. Make sure *Deploy Previews* is enabled.
4. Save.

Netlify will build the draft branch immediately. It appears at:

```
https://draft--o4o.netlify.app
```

Note the **two** hyphens between `draft` and `o4o`. That is Netlify's format,
not a typo.

*Deploy Previews* means that when someone proposes a change, Netlify builds a
temporary private website showing exactly what that change looks like, and
posts the address as a comment. Reviewers can look at the actual page rather
than reading raw text. This is the single most useful feature for a team of
non-technical editors.

> **A caution about privacy.** The draft site is not indexed by search engines,
> but anyone who knows the address can open it. It is unlisted, not secret. Do
> not put unpublished results, personal information or anything under embargo
> on it. Netlify's password protection is a paid feature; check the current
> pricing if you decide you need it.

---

## Part 6. Lock down the live site

Right now anyone with access could change the live site directly. Fix that.

### 6a. Fill in the approvers

Open `.github/CODEOWNERS` in your repository, click the pencil icon, and
replace the three placeholders with real GitHub usernames:

```
*   @harald-username @annika-username @mika-username
```

Keep the `*` and the spacing. The `@` is required. Commit the change.

### 6b. Require approval before anything goes live

1. In the repository: **Settings** → **Branches** (in the left sidebar).
2. **Add branch protection rule** (on newer GitHub this may be called *Add
   ruleset*; the options are the same).
3. Branch name pattern: `main`
4. Tick:
   - **Require a pull request before merging**
   - **Require approvals** — set to **1**
   - **Require review from Code Owners**
5. Save.

From now on nobody, including the person who set this up, can change the live
site without one of the three named people approving. Work still flows freely
on `draft`.

### 6c. Give the team access

**Settings** → **Collaborators and teams** → **Add people**. Give everyone the
**Write** role. Write access sounds alarming but is correct: it lets people
edit `draft` freely, and Part 6b prevents them from touching `main` unilaterally.

---

## Part 7. The everyday workflow

### Writing a news item

1. Go to your repository and **switch to the `draft` branch** using the branch
   selector. This matters. If you are on `main` you will be blocked at the end.
2. **Add file** → **Create new file**.
3. In the filename box type the path, including the slashes:

   ```
   content/post/2026-03-14-first-balloon-flight/index.md
   ```

   Typing a `/` creates a folder. Use the date and a few descriptive words.
   Lower case, hyphens instead of spaces, no punctuation.

4. Paste this into the large box and edit it:

   ```markdown
   ---
   title: "First balloon flight from Lauder"
   summary: "A one-sentence description that appears in listings."
   date: 2026-03-14
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
   [a link](https://example.org).
   ```

   The block between the two `---` lines is the label on the article. The
   `authors` entries must be folder names from `content/authors/` —
   `annika-seppala`, not `Annika Seppälä`. The `tags` entry decides which
   research area page the item also appears on: use `atmospheric-science`,
   `photonics`, `engineering`, `outreach` or `programme`.

5. Scroll down, type a short description of what you did, and click **Commit
   changes**.

6. Wait about a minute, then look at `https://draft--o4o.netlify.app/post/`.

### Adding a photograph to a news item

Put an image called `featured.jpg` in the same folder as the `index.md`. On
GitHub: open the folder, **Add file** → **Upload files**, drag the image in,
commit. Resize it to roughly 1200 pixels wide first; a 6 MB photo from a phone
will make the page slow.

### Editing a person's profile

Each person has a folder under `content/authors/`. Open
`content/authors/harald-schwefel/_index.md`, click the pencil, edit, commit —
on the `draft` branch.

The text below the second `---` is their biography. The lines above it are
structured fields; keep the indentation exactly as it is, because the spacing
carries meaning.

To add a portrait, upload `avatar.jpg` into the same folder.

### Adding a new person

Two steps:

1. Add them to `data/team.yaml`, copying the shape of an existing entry. This
   is what tags their publications correctly.
2. Create `content/authors/their-slug/_index.md`. The quickest way is to open
   an existing person's file, copy all of it, create the new file, paste, and
   edit.

If you are comfortable running a command, `python3 scripts/make_people.py` does
step 2 automatically from step 1.

### Publishing: moving draft to live

When the draft site looks right:

1. On the repository, click the **Pull requests** tab → **New pull request**.
2. Set **base: main** on the left and **compare: draft** on the right. Getting
   these the wrong way round is the usual mistake — base is the destination.
3. Click **Create pull request**. Give it a title such as
   `Publish March news and updated profiles`.
4. GitHub automatically requests a review from Harald, Annika and Mika. Netlify
   posts a preview link in the comments.
5. One of them clicks **Files changed** → **Review changes** → **Approve**.
6. Anyone then clicks **Merge pull request**.

Two minutes later it is live on `https://o4o.netlify.app`.

Do this in batches — perhaps fortnightly — rather than one item at a time.

---

## Part 8. Publications from Zotero

### How it works

A script reads the Zotero group library and writes one page per publication. It
works out the research area from the **authors**: it compares each author's
surname against `data/team.yaml`, and applies the area of everyone it
recognises. A paper by Suresh and Sedlmeir is tagged `photonics`; a paper by
Kessenich is tagged `atmospheric-science`; a paper by both gets both tags and
appears on both area pages.

This is why `data/team.yaml` matters. If someone is missing from it, their
papers will appear in the main publication list but not on any area page.

### 8a. Make the library readable

Simplest option, if the group's contents are not sensitive: go to the group's
**Settings** → **Library Settings** on zotero.org and set *Library Reading* to
**Anyone**. Nothing further is needed.

If you would rather keep it private:

1. Go to `https://www.zotero.org/settings/keys` → **Create new private key**.
2. Tick read access to group libraries. Save and copy the key.
3. In your GitHub repository: **Settings** → **Secrets and variables** →
   **Actions** → **New repository secret**. Name it exactly `ZOTERO_API_KEY`
   and paste the key as the value.

A GitHub secret is write-only — once saved, nobody can read it back, including
you. That is intended.

### 8b. Run it for the first time

1. Go to the **Actions** tab in your repository.
2. If prompted, click the button enabling workflows.
3. Click **Sync publications from Zotero** in the left sidebar.
4. Click **Run workflow** → select the `draft` branch → **Run workflow**.

It takes under a minute. Refresh, click the run, and read the log if anything
went wrong. Then check `https://draft--o4o.netlify.app/publication/`.

After this it runs itself every Monday morning, always onto `draft`. New papers
reach the public site only when someone promotes draft to main, which gives you
the pre-publication review your IP arrangements require.

### 8c. Day-to-day use

- **To add a paper**: put it in the Zotero group. That is all.
- **To hide one**: give it the Zotero tag `no-website`.
- **To correct a title or author**: fix it in Zotero, not on the website. The
  website is overwritten from Zotero every week.
- **Decide the inclusion rule** and write it in the group description, so
  everyone applies the same test. A workable one: *anything that acknowledges
  the Endeavour contract, plus anything by a Tuwhiri member that directly
  advances a programme deliverable.*

---

## Part 9. Optional — the web editor

Parts 1 to 8 give a working site editable through GitHub's website. Some people
find GitHub's interface unfriendly. The scaffold includes a form-based editor
at `/admin/`, which presents news items and profiles as ordinary web forms.

It needs one extra piece of setup: a small authentication service, because
GitHub will not let a web page write to a repository without one. Netlify's own
version of this was retired in 2025.

Set it up when the rest is working, not before:

1. Edit `static/admin/config.yml` and change `repo:` to your real
   `organisation/repository`.
2. Follow the current authentication instructions at
   `https://github.com/sveltia/sveltia-cms`. This involves registering a GitHub
   OAuth application and deploying a small proxy. Budget an hour.

The editor writes only to `draft`, so it cannot alter the live site.

*Honest assessment: for a team of researchers who mostly all have GitHub
accounts, the editor is a convenience rather than a necessity. Try Part 7's
workflow for a month first and see whether anyone actually asks for it.*

---

## Part 10. Optional — previewing on your own computer

Useful if you are making larger changes and do not want a trail of commits.

Install **Hugo Extended** (the extended version specifically) and **Go**, then:

```bash
git clone https://github.com/YOUR-ORG/tuwhiri-website.git
cd tuwhiri-website
git checkout draft
hugo server
```

Open `http://localhost:1313`. Pages refresh as you save. Press `Ctrl+C` to
stop.

---

## Part 11. When something goes wrong

**A change does not appear on the site.**
Check you committed to the branch you meant. Then look at Netlify → **Deploys**.
A red entry means the build failed; click it to read the log.

**The build failed and the log mentions YAML or unmarshal.**
Almost always indentation. In these files, spaces at the start of a line carry
meaning, and tab characters are forbidden. Compare your file with a working one
line by line. Use the *History* button on the file to see the last good
version.

**A person does not appear on the People page.**
Their `user_groups` must match a heading in `content/people/index.md` exactly,
including capitals and the `&` in `Engagement & Outreach`.

**A publication is on the main list but not on its area page.**
The author is not in `data/team.yaml`, or their surname is spelled differently
in Zotero. Add the Zotero spelling to that person's `match:` list.

**Someone with a compound or accented surname is not matched.**
Accents and hyphens are handled automatically, but add the spelling as it
appears in Zotero to their `match:` list to be certain.

**I have broken something and want to go back.**
Every file has a *History* button. Open the last good version, click the ⋯
menu, and restore it. Nothing is ever lost.

---

## Part 12. Before you make it public

- [ ] MBIE Endeavour funding acknowledgement — required wording, correct place
- [ ] University of Otago branding approval and any required logo lock-ups
- [ ] Partner logos: Otago, Paihau–Robinson, NIWA/NZIES, Kea Aerospace,
      Adelaide, JPL, Otago Museum
- [ ] Written consent from every person shown, for their photo and biography
- [ ] Clearance for JPL/NASA and FMI members to be listed — their institutions
      often require it
- [ ] Privacy statement, and a decision on whether to use analytics at all
- [ ] Accessibility check — Otago will have a standard you must meet
- [ ] Contact page: which address, and who monitors it
- [ ] Whether `o4o.netlify.app` is the permanent address or a placeholder

---

## Where each file lives

| Path | What it does |
|---|---|
| `content/_index.md` | The homepage |
| `content/atmospheric-science/index.md` | Atmospheric Science area page |
| `content/photonics/index.md` | Photonics area page |
| `content/engineering/index.md` | Space Systems Engineering area page |
| `content/people/index.md` | The People page, and its list of headings |
| `content/authors/<name>/_index.md` | One person's profile |
| `content/post/<date-title>/index.md` | One news item |
| `content/publication/` | Written automatically from Zotero — do not edit |
| `data/team.yaml` | The roster. Drives people and publication tagging |
| `config/_default/menus.yaml` | The navigation bar |
| `config/_default/params.yaml` | Colours, fonts, footer, analytics |
| `config/_default/hugo.yaml` | Site name and address |
| `netlify.toml` | Build settings. Rarely needs changing |
| `.github/CODEOWNERS` | Who must approve changes to the live site |
| `.github/workflows/zotero-sync.yml` | The weekly Zotero update |
| `scripts/zotero_sync.py` | The script that reads Zotero |
| `scripts/make_people.py` | Creates profiles from `data/team.yaml` |
| `static/admin/` | The optional web editor |
