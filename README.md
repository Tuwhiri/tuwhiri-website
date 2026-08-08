# Tuwhiri website 

Source for the Tuwhiri programme website.
Built with Hugo and the Hugo Blox Research Group template, hosted on Netlify.

| | |
|---|---|
| Live site | https://o4o.netlify.app (built from `main`) |
| Draft site | https://draft--o4o.netlify.app (built from `draft`) |
| Publications | Synced weekly from the Tuwhiri Zotero group (id 6627926) |

**Start here: [HOWTO.md](HOWTO.md)** — full setup and day-to-day instructions,
written for someone who has not made a website before.

## In one paragraph

Everyone works on the `draft` branch, which is published to the draft site
within a minute of any change. When the draft looks right, open a pull request
from `draft` into `main`; Harald, Annika or Mika approves it, and it goes live.
Publications are not edited here at all — they come from the Zotero group
library, and the research area tags are worked out automatically by matching
author surnames against `data/team.yaml`.
