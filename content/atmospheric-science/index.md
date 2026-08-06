---
title: Atmospheric Science
date: 2026-01-01
type: landing

sections:
  - block: markdown
    content:
      title: Atmospheric Science
      text: |
        Ozone in the Antarctic stratosphere shapes the jet streams that steer weather
        across Australasia. We are quantifying how much forecast skill New Zealand
        stands to lose when the Aura record ends, and using that to set hard numbers
        on what a replacement instrument must deliver.

        The work has four strands: establishing the link between ozone data quality
        and extreme-event forecasting, defining instrumental requirements for the
        photonics and engineering teams, retrieving atmospheric information from the
        instrument using the ARTS radiative transfer model, and identifying which
        further gases the same technique could measure.

        This area is led by Annika Seppälä.
    design:
      columns: '1'

  - block: people
    content:
      title: Who works on this
      user_groups:
        - Atmospheric Science
      sort_by: Params.last_name
      sort_ascending: true
    design:
      show_interests: false
      show_role: true
      show_organizations: true
      show_social: true

  - block: collection
    content:
      title: Publications in this area
      count: 0
      filters:
        folders:
          - publication
        tag: atmospheric-science
    design:
      view: citation
      columns: '1'

  - block: collection
    content:
      title: News from this area
      count: 5
      filters:
        page_type: post
        tag: atmospheric-science
      order: desc
    design:
      view: card
      columns: '1'
---
