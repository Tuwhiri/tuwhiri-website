---
# The homepage. Leave `title` empty so the site name is used.
title:
date: 2026-01-01
type: landing

sections:
  - block: hero
    content:
      title: |
        Tuwhiri
      text: |
        <br>

        **Building critical capability for space-based climate monitoring with next generation photonics.**

        An MBIE Endeavour Programme, 2025–2030, led by the University of Otago.

  - block: markdown
    content:
      title: We are losing key data on the atmosphere
      text: |
        The 25-year record of atmospheric composition from NASA's EOS-Aura satellite
        ends when the spacecraft runs out of fuel. Aura's Microwave Limb Sounder is
        the only instrument that can measure ozone and related gases through the
        Antarctic polar winter, when the ozone hole forms. No replacement mission is
        planned, because conventional instruments of this kind are prohibitively
        expensive.

        Tuwhiri is developing a photonic radiometer small enough and cheap enough to
        fly on a CubeSat. It converts faint microwave and terahertz signals from the
        atmosphere into optical light, which can then be measured with ordinary
        photonics. Along the way we are establishing the atmospheric science,
        photonics and space engineering capability that Aotearoa New Zealand needs
        to keep that record going.
    design:
      columns: '1'

  - block: markdown
    content:
      title: Three research areas
      text: |
        **[Atmospheric Science →](./atmospheric-science/)**
        What the data is for: how ozone drives extreme weather, what accuracy
        end users actually need, and what we can retrieve from the instrument.

        **[Photonics →](./photonics/)**
        The sensor itself: electro-optic up-conversion in whispering-gallery-mode
        resonators, and the path from a laboratory demonstration to a flight-ready device.

        **[Space Systems Engineering →](./engineering/)**
        Everything around the sensor: the payload, the beam-steering antenna,
        thermal and vibration control, and the balloon and aircraft flights.
    design:
      columns: '1'

  - block: collection
    content:
      title: Latest news
      count: 4
      filters:
        page_type: post
      order: desc
      page_type: post
    design:
      view: card
      columns: '1'

  - block: collection
    content:
      title: Recent publications
      count: 5
      filters:
        folders:
          - publication
    design:
      view: citation
      columns: '1'

  - block: markdown
    content:
      text: |
        {{% cta cta_link="./people/" cta_text="Meet the team →" %}}
    design:
      columns: '1'
---
