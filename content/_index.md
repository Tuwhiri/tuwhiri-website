---
title: ''
summary: ''
date: 2026-01-01
type: landing

sections:
  - block: hero
    content:
      title: Tuwhiri
      text: |-
        **Building critical capability for space-based climate monitoring with
        next generation photonics.**

        An MBIE Endeavour Programme, 2025–2030, led by the University of Otago.
    design:
      background:
        gradient_mesh:
          enable: true

  - block: markdown
    content:
      title: We are losing key data on the atmosphere
      text: |-
        The 25-year record of atmospheric composition from NASA's EOS-Aura
        satellite ends when the spacecraft runs out of fuel. Aura's Microwave
        Limb Sounder is the only instrument that can measure ozone and related
        gases through the Antarctic polar winter, when the ozone hole forms. No
        replacement mission is planned, because conventional instruments of this
        kind are prohibitively expensive.

        Tuwhiri is developing a photonic radiometer small enough and cheap
        enough to fly on a CubeSat. It converts faint microwave and terahertz
        signals from the atmosphere into optical light, which can then be
        measured with ordinary photonics. Along the way we are establishing the
        atmospheric science, photonics and space engineering capability that
        Aotearoa New Zealand needs to keep that record going.
    design:
      columns: '1'

  - block: research-areas
    design:
      layout: cards
    content:
      title: Three research areas
      items:
        - name: Atmospheric Science
          description: What the data is for — how ozone drives extreme weather, what
            accuracy end users need, and what we can retrieve from the instrument.
          icon: hero/cloud
          url: /atmospheric-science/
        - name: Photonics
          description: The sensor itself — electro-optic up-conversion in
            whispering-gallery-mode resonators, from bench demonstration to
            flight-ready device.
          icon: hero/sparkles
          url: /photonics/
        - name: Space Systems Engineering
          description: Everything around the sensor — the payload, beam-steering
            antenna, thermal and vibration control, and the flight campaigns.
          icon: hero/rocket-launch
          url: /engineering/

  - block: collection
    id: news
    content:
      title: Latest news
      page_type: blog
      count: 4
      order: desc
    design:
      view: card

  - block: collection
    id: papers
    content:
      title: Recent publications
      count: 5
      filters:
        folders:
          - publications
    design:
      view: citation

  - block: cta-card
    content:
      title: Meet the team
      text: Tuwhiri brings together atmospheric scientists, photonics
        researchers and space systems engineers across New Zealand, Australia,
        Europe and the United States.
      button:
        text: See the people
        url: /people/
---
