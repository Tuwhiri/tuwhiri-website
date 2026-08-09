# Partner logo files

Eight files go in this folder. The names must match exactly — they are written
into `content/_index.md` and nothing detects them automatically.

## Affiliated partners

| Filename | Organisation |
|---|---|
| `otago.svg` | University of Otago |
| `dodd-walls.svg` | Dodd-Walls Centre |
| `waikato.svg` | University of Waikato |
| `paihau-robinson.svg` | Paihau–Robinson Research Institute |

## Industry partners

| Filename | Organisation |
|---|---|
| `kea-aerospace.svg` | Kea Aerospace |
| `quantifi.svg` | Quantifi Photonics |
| `shamrock.svg` | Shamrock Industries |
| `q-bifrost.svg` | Q-Bifrost |

## What to ask for

**SVG wherever possible.** Logos are line art and stay sharp at any size. PNG
works — use about 600 pixels wide on a transparent background — but change the
extension in `content/_index.md` to match.

**Transparent background**, not white. A white rectangle looks wrong on the pale
blue page and badly wrong in dark mode.

**The horizontal version** where an organisation offers one. Logos here sit in a
row and are constrained by height, so a tall stacked mark ends up tiny.

**Colours will be shown unaltered.** The block would normally grey logos out
until you hover over them; that has been turned off, because most institutions
require their mark shown in approved colours, and Otago's brand rules say so
explicitly.

## Two things to sort out before the site goes public

**Permission.** Displaying an organisation's logo generally needs their
agreement, and most universities have a form or a brand contact. Otago and the
Dodd-Walls Centre will have specific requirements about clear space and minimum
size. Worth an email each rather than an assumption.

**Two URLs are blank.** `content/_index.md` has empty `url:` values for Shamrock
Industries and Q-Bifrost, since I did not have them. Fill them in, or the logos
render without a link, which is fine but less useful.

## Dark mode

If a logo is dark ink on transparent, it will disappear against the Te Pō
background in dark mode. If that happens, ask for a reversed (white or light)
version and tell me — the block needs a small change to swap them, the same way
the site logo already does.
