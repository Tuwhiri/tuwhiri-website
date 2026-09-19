---
title: People

# Profile pages are switched OFF by default here, and switched back ON
# individually by each person's stub in content/authors/<slug>/_index.md.
#
# The reason: `authors` is a taxonomy, so Hugo would otherwise build a page for
# every name that appears on a publication — including external co-authors who
# are not part of Tuwhiri. Those pages carried slugs like `anna-r.-petersen`
# and held nothing but one paper.
#
# With this cascade, only people listed in data/team.yaml get a page. Everyone
# else still appears in the citation, as plain text rather than a link.
#
# `list: always` keeps every author available to collections and filters, so
# publication listings are unaffected.
build:
  render: never
cascade:
  build:
    render: never
    list: always
---
