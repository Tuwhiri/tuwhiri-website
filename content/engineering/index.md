---
title: Space Systems Engineering
date: 2026-01-01
type: landing

sections:
  - block: markdown
    content:
      title: Space Systems Engineering
      text: |
        Turning a laboratory instrument into a flight payload means solving the
        problems that surround the sensor: mass, power and volume budgets, vibration
        isolation, thermal control, pointing knowledge, and data handling.

        A particular challenge is the collection antenna, which must be steerable
        while still directing radiation into the coupling waveguide. Our approach
        uses a cascaded pair of independently rotating prisms as a beam-steering
        mechanism.

        The payload will be demonstrated on balloon flights from Lauder and
        Antarctica, and on a Kea Aerospace Kea Atmos Mk2 stratospheric aircraft.

        This area is led by Randy Pollock.
    design:
      columns: '1'

  - block: people
    content:
      title: Who works on this
      user_groups:
        - Space Systems Engineering
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
        tag: engineering
    design:
      view: citation
      columns: '1'

  - block: collection
    content:
      title: News from this area
      count: 5
      filters:
        page_type: post
        tag: engineering
      order: desc
    design:
      view: card
      columns: '1'
---
