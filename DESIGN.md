---
name: Bastians Flea Market
description: A provincial dagashi-ya seen straight on, lettered in a warm grey, orange, black and white palette.
colors:
  aluminium-ground: "#cdcac2"
  aluminium-highlight: "#e1ded7"
  aluminium-recess: "#b3afa6"
  bay-back: "#bebab1"
  sumi-ink: "#151514"
  ink-soft: "#47453f"
  price-paper: "#f6f5f2"
  signal-orange: "#ff5a1f"
  marker-orange: "#c43d0b"
  error-rust: "#a8240a"
typography:
  display:
    fontFamily: "Dela Gothic One, Zen Kaku Gothic New, system-ui, sans-serif"
    fontSize: "clamp(20px, 4.6vw, 64px)"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "0.01em"
  headline:
    fontFamily: "Dela Gothic One, Zen Kaku Gothic New, system-ui, sans-serif"
    fontSize: "clamp(26px, 4vw, 48px)"
    fontWeight: 400
    lineHeight: 1.1
  title:
    fontFamily: "Dela Gothic One, Zen Kaku Gothic New, system-ui, sans-serif"
    fontSize: "clamp(24px, 2.6vw, 36px)"
    fontWeight: 400
    lineHeight: 1.12
  price:
    fontFamily: "Yusei Magic, Zen Kaku Gothic New, system-ui, sans-serif"
    fontSize: "30px"
    fontWeight: 400
    lineHeight: 1.1
    fontFeature: "tnum"
  body:
    fontFamily: "Zen Kaku Gothic New, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Zen Kaku Gothic New, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    letterSpacing: "0.12em"
rounded:
  none: "0px"
  field: "4px"
  button: "6px"
  round: "50%"
spacing:
  gutter: "clamp(16px, 3vw, 32px)"
  upright: "12px"
  sign: "60px"
  rail: "18px"
components:
  button-whatsapp:
    backgroundColor: "{colors.signal-orange}"
    textColor: "{colors.sumi-ink}"
    rounded: "{rounded.button}"
    padding: "12px 22px"
    height: "52px"
  button-whatsapp-hover:
    backgroundColor: "{colors.sumi-ink}"
    textColor: "{colors.signal-orange}"
  button-ink:
    backgroundColor: "{colors.sumi-ink}"
    textColor: "{colors.price-paper}"
    rounded: "{rounded.button}"
    padding: "12px 22px"
    height: "52px"
  button-ink-hover:
    backgroundColor: "{colors.signal-orange}"
    textColor: "{colors.sumi-ink}"
  button-paper:
    backgroundColor: "{colors.price-paper}"
    textColor: "{colors.sumi-ink}"
    rounded: "{rounded.button}"
    padding: "12px 22px"
    height: "52px"
  price-strip:
    backgroundColor: "{colors.price-paper}"
    textColor: "{colors.sumi-ink}"
    rounded: "{rounded.none}"
    padding: "14px 14px 10px"
  shelf-sign:
    backgroundColor: "{colors.sumi-ink}"
    textColor: "{colors.price-paper}"
    width: "{spacing.sign}"
  drawer-price:
    backgroundColor: "{colors.signal-orange}"
    textColor: "{colors.sumi-ink}"
    typography: "{typography.price}"
    padding: "4px 16px 6px"
  field-input:
    backgroundColor: "#ffffff"
    textColor: "{colors.sumi-ink}"
    rounded: "{rounded.field}"
    padding: "11px 12px"
---

# Design System: Bastians Flea Market

## Overview

**Creative North Star: "The Provincial Dagashi-ya"**

The page is a small Japanese curiosity shop seen straight on. A black noren hangs over the door; behind it stands a black-framed cabinet of shelves, each bay a recessed grey back panel with an orange-edged board running across it. Every item is a real, uncropped photo standing on that board, and a white paper price strip, pinned through the top and lettered in orange marker, hangs off the board edge at a slight tilt. Nothing is a card; everything is furniture.

The palette is borrowed from Teenage Engineering hardware (warm aluminium grey, signal orange, black, white) and applied as shop materials: aluminium for the ground, black lacquer for uprights, signs and noren, orange for the board edges and stamps, paper for strips and the drawer body. Density is shop-like: items sit at their own aspect ratio and width, not in equal cells. Detail lives in a drawer that slides out from under the shelf, not on a separate page.

Motion is physical and sparse: the noren sways once on load, price strips swing on hover, the drawer pulls out with a long exponential ease-out.

**Key Characteristics:**
- Black cabinet frame (12px uprights) around grey bays with an orange shelf board.
- Hanging paper price strips, pinned, tilted per item, prices in Yusei Magic marker.
- Vertical single-kanji shelf-end signs in Dela Gothic One with a Spanish label.
- Orange hanko 売約済 stamped over sold items.
- Detail drawer opens inline under the shelf; no modal, no separate product page.
- Real photos at native aspect ratio; never cropped into uniform tiles on the shelf.

## Colors

Warm aluminium neutrals carry the shop body; black and paper carry signage; one signal orange marks boards, stamps and the primary action.

### Primary
- **Signal Orange** (signal-orange): the shelf board front edge, the noren mon, the drawer pull, the drawer price plaque, the hanko ring, and the WhatsApp button. It is a surface and stroke color, not a text color on light grounds.
- **Marker Orange** (marker-orange): the orange that must read as text on paper: prices on strips, hanko lettering, sold notices, the caret.

### Neutral
- **Aluminium Ground** (aluminium-ground): page body.
- **Aluminium Highlight** (aluminium-highlight): the top surface of each shelf board.
- **Aluminium Recess** (aluminium-recess): drawer face, close bar, photo and thumbnail placeholders, sold price plaque.
- **Bay Back** (bay-back): back panel of each shelf bay, with a 40px top shade (rgb 0 0 0 / 0.12 fading out) where the board above casts shadow.
- **Sumi Ink** (sumi-ink): text, cabinet uprights, noren cloth, shelf signs, footer counter board, focus rings.
- **Ink Soft** (ink-soft): secondary text, spec labels, condition notes, currency suffixes.
- **Price Paper** (price-paper): price strips, drawer body, text on black.
- **Error Rust** (error-rust): invalid field border and error status on light grounds (a lighter #ff9a76 stands in on the black counter).

### Named Rules
**The Shop Materials Rule.** Every color is a material in the shop: aluminium, lacquer, paper, orange paint. A new surface picks the material it would be made of, not a new tint.

**The Two Oranges Rule.** Signal orange fills and strokes; marker orange is the only orange used for text on paper or grey. Orange text on black may use signal orange (noren kanji, shelf labels).

## Typography

**Display Font:** Dela Gothic One (with Zen Kaku Gothic New, system-ui)
**Marker Font:** Yusei Magic (with Zen Kaku Gothic New), prices only
**Body Font:** Zen Kaku Gothic New 400/700 (with system-ui)

**Character:** Heavy shop signage over a plain Japanese gothic, with a felt-marker hand reserved for the number that matters. All fonts are self-hosted; the Japanese display subset covers kana and kanji for signs and stamps.

### Hierarchy
- **Display** (Dela Gothic One, clamp 20px to 64px, line-height 1, uppercase): the noren words only.
- **Headline** (Dela Gothic One, clamp 26px to 48px, 1.1): the counter board title; the placard lead uses the same face at clamp 19px to 28px, 1.3, balanced.
- **Title** (Dela Gothic One, clamp 24px to 36px, 1.12): item name in the drawer.
- **Price** (Yusei Magic, 30px on strips, 23px on phones, 38px on the drawer plaque, tabular numerals): prices only, with a small bold body-font "MXN" suffix.
- **Body** (Zen Kaku Gothic New 400, 16px, 1.55): running text; blurbs at 18px/1.5 capped at 46ch, condition at 52ch.
- **Label** (Zen Kaku Gothic New 700, 11px to 13px, 0.12em to 0.2em tracking, uppercase): spec-table keys, the condition key, shelf-sign Spanish labels, hanko Spanish line. Labels always name the value beside them.

### Named Rules
**The Marker Is For Money Rule.** Yusei Magic sets prices and nothing else.

**The Sign Kanji Rule.** Shelf-end signs carry one kanji each (弾 作 録 聴), vertical, Dela Gothic One. Drop okurigana: at sign scale く reads as an arrow.

## Layout

A single cabinet, max 1280px, centered inside a fluid gutter (clamp 16px to 32px). Each shelf is a two-column grid: a black sign column (60px; 44px under 760px) and a bay. Cabinet uprights are 12px black borders on top and right (8px on phones); the last shelf closes the bottom. At 1180px and up the cabinet splits into two columns of shelves, and a wide shelf spans both with larger items (250px portrait, 330px landscape instead of 210px / 272px).

Each row is a three-track grid (items, an 18px board, tags) with items on a subgrid so photos sit on the board and strips hang below it. Under 760px each shelf becomes a stack of boards holding two items each at about half the bay width, with 12px spacers; nothing scrolls sideways. On wider screens a board that outgrows its bay may scroll horizontally with proximity snap. The drawer spans the full row beneath the shelf; its body is photo gallery and sheet side by side, stacking to one column on phones.

## Elevation & Depth

Depth is physical, not abstract: soft drop shadows stand in for real objects resting on or hanging from the shelf. There is no ambient card elevation and no hover-lift on surfaces other than items.

### Shadow Vocabulary
- **Board** (`box-shadow: 0 10px 16px -8px rgb(0 0 0 / 0.45)`): under each shelf board.
- **Standing item** (`box-shadow: 0 2px 0 rgb(0 0 0 / 0.25), 0 12px 20px -12px rgb(0 0 0 / 0.5)`): the photo resting on the board; deepens to `0 22px 26px -14px` when lifted 6px on hover or open.
- **Hanging strip** (`box-shadow: 0 1px 0 rgb(0 0 0 / 0.15), 0 8px 12px -6px rgb(0 0 0 / 0.4)`): price strips.
- **Cloth** (`box-shadow: 0 14px 22px -14px rgb(0 0 0 / 0.55)`): noren panels.

### Named Rules
**The Gravity Rule.** A shadow falls downward from something that rests or hangs. Nothing floats.

## Shapes

Square by default: uprights, boards, signs, noren panels, strips, the drawer, and photos have no radius. Circles are reserved for the mon, the strip pin, and the hanko. Only interactive controls soften: buttons (6px) and fields and the mini hanko (4px). Tags rotate per item through a fixed tilt sequence (-2.2, 1.4, -0.8, 2, -1.6, 0.9, -2.6, 1.8 deg); the drawer price plaque sits at -1.5deg and the hanko at -14deg.

## Components

### Buttons
- **Shape:** gently softened rectangle (6px), 2px ink border, 52px minimum height, bold 17px body type, inline SVG icon at 1.25em.
- **WhatsApp (primary):** signal orange with ink text; hover inverts to ink with orange text. Always the first action in a drawer.
- **Ink:** ink with paper text; hover goes orange with ink text. Form submit on light grounds.
- **Paper:** paper with paper border; hover goes orange. Form submit on the black counter.
- **Active:** nudges down 2px. Disabled: 0.55 opacity.

### Price Strip (signature)
Paper strip, 132px minimum width, hung -10px into the board, pinned by a 7px ink dot, rotated by its item's tilt from the top center. Model name 15px bold, price in marker orange Yusei Magic, condition 12px ink soft. On hover it swings (+5deg, -2.5deg, settle) over 0.9s. Sold: price struck through 2px.

### Shelf Sign
Black column, vertical writing mode: one kanji at 30px over a 12px uppercase Spanish label in signal orange.

### Hanko
108px circle (150px in the drawer), 4px signal-orange ring over 86% paper, rotated -14deg, 売約済 in Dela Gothic One over a tracked Spanish line. Sold photos go 85% grayscale. The mini hanko is its inline cousin in running text.

### Drawer
Opens under its shelf by animating grid rows 0fr to 1fr over 0.7s on the exponential ease-out. A grey face with an orange pull bar tops it; a paper body holds gallery (68px square thumbs, selected thumb gets an ink border and orange ring) and sheet (title, orange price plaque, condition, blurb, five-row spec table with hairline rules, actions, message form); a full-width grey close bar ends it.

### Inputs / Fields
- **Style:** white field, 2px ink border, 4px radius, 16px text, bold 13px label above.
- **Focus:** 3px signal-orange ring replaces the outline.
- **Error:** error-rust border with a faint rust ring. On the black counter, borders go paper.

### Navigation
None. The noren is the header and the shelves are the navigation.

## Do's and Don'ts

### Do:
- **Do** frame every new display surface as shop furniture: black uprights, grey bay, orange-edged board.
- **Do** show each item's real photo at its native aspect ratio standing on the board.
- **Do** hang prices on paper strips in Yusei Magic, marker orange, with tabular numerals.
- **Do** mark sold goods with the orange 売約済 hanko and a struck-through price, and hide purchase actions.
- **Do** keep WhatsApp as the first, orange action wherever an item can be contacted about.
- **Do** use the exponential ease-out (cubic-bezier(0.16, 1, 0.3, 1)) for physical motion, and drop sway and swing under reduced motion.

### Don't:
- **Don't** put items in equal rounded cards or a uniform crop grid.
- **Don't** set orange text on aluminium or paper in signal orange; use marker orange.
- **Don't** use Yusei Magic for anything but prices.
- **Don't** round structural surfaces; radius belongs to controls only.
- **Don't** add Teenage Engineering logos or branding; the palette is inspiration only.
- **Don't** make shelves scroll sideways on phones; stack boards of two items each.
