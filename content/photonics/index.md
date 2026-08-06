---
title: Photonics
date: 2026-01-01
type: landing

sections:
  - block: markdown
    content:
      title: Photonics
      text: |
        The core of the instrument is an electro-optic up-converter. A
        whispering-gallery-mode resonator, diamond-turned from a nonlinear crystal,
        couples an incoming microwave or terahertz photon to an optical pump and
        emits an optical sideband. Because the output is at optical frequencies, it
        can be detected with quiet, compact, room-temperature photonics rather than
        the cryogenic receivers a conventional limb sounder needs.

        Our work covers resonator design and fabrication, coupling and noise
        temperature optimisation, and the engineering of a device that survives
        launch and operates unattended in the stratosphere.

        This area is led by Harald Schwefel and Mallika Suresh.
    design:
      columns: '1'

  - block: people
    content:
      title: Who works on this
      user_groups:
        - Photonics
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
        tag: photonics
    design:
      view: citation
      columns: '1'

  - block: collection
    content:
      title: News from this area
      count: 5
      filters:
        page_type: post
        tag: photonics
      order: desc
    design:
      view: card
      columns: '1'
---
