---
title: ''
summary: ''
date: 2026-01-01
type: landing

sections:
  # The wordmark comes first, with nothing above it.
  #
  # The hero draws its text before its image, so the only way to get the logo
  # at the very top is to give the hero no title and no text. The tagline then
  # follows in the markdown block below.
  #
  # `layout: stacked` is required: the default `centered` layout does not
  # render an image at all.
  - block: hero
    content:
      media:
        src: hero-logo.svg
        dark_src: hero-logo-dark.svg
        alt: Tuwhiri
    design:
      size: "compact"
      css_style: "padding: 10px 0;"
      layout: stacked
      background:
        gradient_mesh:
          enable: true

  - block: markdown
    content:
      title: Building critical capability for space-based climate monitoring with next generation photonics.
      subtitle: An MBIE Endeavour Programme, 2025–2030, led by the University of Otago.
      text: |-
        ##### An MBIE Endeavour Programme, 2025–2030, led by the University of Otago.

        The 25-year record of atmospheric composition from NASA's EOS-Aura satellite is coming to an end. Aura's Microwave Limb Sounder is the only instrument that can measure ozone and related gases through the Antarctic polar winter, when the ozone hole forms, and it is about to run out of fuel. No replacement mission has been funded, because conventional instruments of this kind are prohibitively expensive.

        Tuwhiri is developing a photonic radiometer small enough and cheap enough to fly on a CubeSat. It converts faint microwave and terahertz signals from the atmosphere into optical light, which can then be measured with ordinary photonics. Along the way we are establishing the atmospheric science, photonics and space engineering capability that Aotearoa New Zealand needs to keep that record going.
    design:
      text_color_light: true
      background:
        gradient_mesh:
      columns: '1'

  - block: research-areas
    design:
      layout: cards
    content:
      title: Three research areas
      items:
        - name: Atmospheric Science
          description: What the data is for — how ozone drives extreme weather, what accuracy end users need, and what we can retrieve from the instrument.
          icon: hero/cloud
          url: /atmospheric-science/
        - name: Photonics
          description: The sensor itself — electro-optic up-conversion in whispering-gallery-mode resonators, from bench demonstration to flight-ready device.
          icon: hero/sparkles
          url: /photonics/
        - name: Space Systems Engineering
          description: Everything around the sensor — the payload, beam-steering antenna, thermal and vibration control, and the flight campaigns.
          icon: hero/rocket-launch
          url: /engineering/

  # ====
  # Outreach and engagement. Deliberately a separate block from the three
  # research areas above, so it does not read as a fourth one.
  # ====
  - block: markdown
    content:
      title: Outreach and engagement
      text: |-
        Building the instrument is only part of the work. Tuwhiri also builds the people, partnerships and public understanding that a long-term climate monitoring capability depends on.

        Working with community groups and organisations, we bring atmospheric science and photonics to life for the wider public, as well as inspire school students, with a particular focus on pathways into science for Māori and Pacific learners. Alongside this, we work with New Zealand industry on the manufacturing, commercialisation and deployment of the instrument, so that what we develop here can be built and sold here.

        [Read more about outreach and engagement →](/outreach/)
    design:
      columns: '1'
      background:
        gradient_mesh:
          enable: true


  - block: collection
    id: news
    content:
      title: Latest news
      page_type: blog
      count: 3
      order: desc
      filters:
        folders:
          - blog
    design:
      view: date-title-summary
  # ====
  # View Options
  # card, citation, date-title-summary, article-grid, slides-gallery
  # ====

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


  # ====
  # Partner logos, in two groups. The logos block has no built-in grouping,
  # so each group is its own block with its own heading.
  #
  # Image paths are relative to assets/media/, so `partners/otago.svg` means
  # assets/media/partners/otago.svg. See assets/media/partners/README.md for
  # what to obtain and how to name it.
  #
  # THE KEY MUST BE `items:`, NOT `logos:`. The block's own documentation says
  # `logos:`, and the names do appear either way -- but the image paths are
  # only resolved for `items:`, so with `logos:` you get a row of captions and
  # no pictures. This cost an afternoon; do not "correct" it back.
  # ====
  - block: logos
    id: partners
    content:
      title: Affiliated partners
      items:
        - name: University of Otago
          image: partners/otago.svg
          url: https://www.otago.ac.nz
          description: Host institution
        - name: Dodd-Walls Centre
          image: partners/dodd-walls.svg
          url: https://www.doddwalls.ac.nz
          description: Centre of Research Excellence for Photonic and Quantum Technologies
        - name: University of Waikato
          image: partners/waikato.svg
          url: https://www.waikato.ac.nz
          description: Atmospheric science
        - name: Paihau–Robinson Research Institute
          image: partners/victoria.svg
          url: https://www.wgtn.ac.nz/robinson
          description: Space systems engineering, Victoria University of Wellington
    design:
      size: "compact"
      layout: grid
      logo_style: color   # `grayscale` is the default; see note below
      logo_size: lg
      css_style: "padding: 10px 0;"
      background:
        gradient:
          type: linear

  - block: logos
    content:
      title: Industry partners
      items:
        - name: Kea Aerospace
          image: partners/kea-aerospace.svg
          url: https://www.keaaerospace.com
          description: Stratospheric flight platforms
        - name: Quantifi Photonics
          image: partners/quantifi.svg
          url: https://quantifiphotonics.com
          description: Instrument commercialisation
        - name: Shamrock Industries
          image: partners/shamrock.png
          url: ''
          description: Manufacture and deployment
        - name: Q-Bifrost
          image: partners/Q-Bifrost_Logo.svg
          url: ''
          description: Industry partner
    design:
      size: "compact"
      layout: grid
      logo_style: color
      logo_size: lg
      css_style: "padding: 10px 0;"
      background:
        gradient_mesh:
          type: linear
          enable: true


  - block: cta-card
    content:
      title: Meet the team
      text: Tuwhiri brings together atmospheric scientists, photonics researchers and space systems engineers across New Zealand, Australia, Europe and the United States.
      button:
        text: See the people
        url: /people/

  # ====
  # Contact. All general enquiries go to the Programme Manager.
  #
  # The address below is a shared programme inbox rather than a personal one,
  # so nothing here needs changing when the role turns over.
  #
  # BEFORE THIS PAGE GOES PUBLIC: confirm that tuwhiri@otago.ac.nz actually
  # exists and forwards to Carla. Until it does, enquiries will bounce and
  # nobody will know.
  # ====
  - block: contact-info
    id: contact
    content:
      title: Contact
      subtitle: Enquiries about Tuwhiri are welcome. Dr Carla Meledandri, our Programme Manager, is the first point of contact and will route anything technical to the right person.
      email: tuwhiri@otago.ac.nz
      visit_title: Where we are
      address:
        lines:
          - Tuwhiri Programme
          - Department of Physics
          - University of Otago
          - PO Box 56
          - Dunedin 9054
          - New Zealand
      connect_title: For media and outreach
      prospective:
        title: Students and prospective researchers
        text: Tuwhiri supports doctoral and masters students across atmospheric science, photonics and space systems engineering. Get in touch if you would like to work on this.
        button:
          text: Meet the team
          url: /people/
      show_form: false
---
