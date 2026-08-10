# Fixing the unreadable Research drop-down

## What was wrong

You were right, and it was a real fault in the brand theme I built.

The theme's own stylesheet gives the navigation drop-down a **white panel** in
light mode, and sets a text colour only for dark mode. In light mode the links
inherit their colour from the header.

With the stock theme that causes no trouble, because its header is pale with
dark text. Our header is Te Pō indigo with Ātea text — which is what the brand
document asks for — so the links inherited Ātea and rendered pale blue on white.

| | Contrast |
|---|---|
| Before: Ātea on white | **1.12:1** — invisible |
| After: Ātea on Te Pō | **15.17:1** — passes AAA |
| Hover: light magenta on Te Pō | **9.33:1** — passes AAA |

## The fix

Rather than forcing dark text onto a white panel, the drop-down now matches the
header it falls from: Te Pō background, Ātea text. That is both readable and
closer to the brand document, where the navigation reads as one dark band.

## How to apply it

Copy the folder over your repository, as before:

```bash
cp -r tuwhiri-dropdown-fix/. /path/to/your/tuwhiri-website/
```

It adds one file:

```
assets/css/hbx/blocks/tuwhiri-brand/style.css
```

Nothing to configure. The theme compiles every
`assets/css/hbx/blocks/<name>/style.css` into the site stylesheet automatically.

## One thing to know if you edit it later

**The path and filename matter.** The theme scans for
`assets/css/hbx/blocks/**/style.css`. A file placed directly in
`assets/css/hbx/blocks/` — or named anything other than `style.css` — is
silently ignored, with no warning. I lost a build to exactly that.

This is now the right place for any future styling tweak of your own.

## Worth checking while you are there

The same inheritance issue could affect anything else that sits on a white
panel inside the header. Have a look at the search box and the mobile menu when
it is open. If either shows pale text on white, tell me and I will extend this
file.
