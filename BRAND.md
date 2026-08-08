# Applying the Tuwhiri brand to the website

Implements *Tuwhiri Light Branding Document v1.0* (Māui Studios).

## What is in place

Two new files define the look, and one existing file points at them:

| File | What it holds |
|---|---|
| `data/themes/tuwhiri.yaml` | The three brand colours and how they map to light and dark mode |
| `data/fonts/tuwhiri.yaml` | The typeface settings |
| `config/_default/params.yaml` | Two lines changed, selecting the packs above |

Both the colours and the fonts are now standard theme packs, so switching back
to the stock look is a matter of changing `pack: "tuwhiri"` to
`pack: "default"`. Nothing is hard-coded.

## Colours

| Brand name | Hex | Where it appears |
|---|---|---|
| Ātea, Orbital Light | `#EAF3FB` | Page background in light mode; text in dark mode |
| Te Pō, Deep Space Indigo | `#19134A` | Body text in light mode; page background in dark mode. Header and footer in both |
| Tohu, Signal Magenta | `#ED2884` | Links, buttons, headings, accents, in both modes |

Light mode is Ātea-led, as on pages 1.D and 3.D of the brand document. Dark mode
is Te Pō-led, as on 1.F, 1.G and 3.A. Magenta is the accent throughout, which is
what the document means by "used selectively for highlights, calls to action,
key discoveries".

### Contrast, and one thing to be careful about

Body text is Te Pō on Ātea, or the reverse. That is 15.17:1 — far above the
4.5:1 that accessibility guidelines require, and comfortably AAA.

Magenta is a different matter. At full strength it reaches only 3.57:1 on the
light background. That is fine for headings, buttons and large text, where the
requirement is 3:1, but it fails for paragraphs.

The theme handles this automatically. It generates a 50–950 scale from each
brand colour and picks a darker step for links, reaching 5.23:1 in light mode
and 9.33:1 in dark. Full-strength magenta still appears on buttons and headings
where it belongs.

**What this means for you:** never set body text in magenta by hand. Use it for
emphasis, which is what the brand document says as well. If someone asks for a
magenta paragraph, the answer is that it would not be readable for a
significant number of people, and the university will have an accessibility
standard that forbids it.

## Typeface

The brand specifies Helvetica Bold and Helvetica Regular. Helvetica cannot be
used on a website: it is licensed, no web font service carries it, and it is
installed only on Apple computers, so Windows and Android visitors would
silently see something else.

The site uses **Arimo**, which is metrically identical to Helvetica — every
character occupies exactly the same width, so spacing and line breaks match what
the designer sees. It is open licensed and served from Google Fonts, so every
visitor sees the same thing.

Print material from the studio should still use real Helvetica. Side by side the
two are near enough indistinguishable.

If you would rather have no web fonts at all, change both `heading` and `body`
in `data/fonts/tuwhiri.yaml` to `system-sans`. Slightly faster, but the site
then looks different on each operating system.

## Still to do: the logo

The theme is styled, but the wordmark is not in place yet. Ask Māui Studios for
**SVG** versions — vector, so they stay sharp at any size, and a fraction of the
file size of PNG. Specifically:

1. **Wordmark on transparent background**, both the magenta and the light
   version, for the navigation bar. Roughly 1.A and 1.B.
2. **A square icon**, the ozone-molecule-and-magnifying-glass mark alone, for
   the browser tab. Also a 512×512 PNG, which some platforms still require.
3. **A wide version** for social media previews, 1200×630, of the sort shown
   at 1.G.

Put them in `assets/media/brand/` and set them in `params.yaml` under the
branding section.

## One question the brand document does not settle

The document spells the name both ways. The cover, the introduction and the
logo read **Tuwhiri**, without a macron. The colour descriptions on page 2
read **Tūwhiri**, with one.

These are different words in te reo Māori, and the site currently uses the
unmacronised form throughout — page titles, metadata, the repository name and
the web address. Worth settling with Māui Studios and with whoever advised on
the name before the site goes public, because changing it afterwards means
changing the domain as well.

If it should be Tūwhiri, the places to change are `hugoblox.branding.name` in
`params.yaml`, the wording on the home page, and every heading that spells it
out.
