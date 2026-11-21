# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack
Static HTML/CSS/JS (user choice). No framework. Product data is generated from each folder's `data.txt` + `ficha.md` into a single data file by a small script. Deploy target: free static hosting (GitHub Pages / Netlify / Vercel), not yet decided.

## Users
Buyers in Mexico (prices in MXN pesos) looking for used music/audio gear: producers, bassists, guitarists, home-studio people. Mostly arriving from a shared link on their phone, browsing a short catalog and deciding whether to message the seller.

## Product Purpose
Bastians Flea Market is a personal one-person sale (bazar) of the owner's own used gear. Success = a visitor sees every item immediately, understands what it is, its price and condition, and contacts the seller.

## Positioning
A real person's shelf of gear, not a store: every item is the actual unit pictured in the owner's own space, with an honest condition note.

## Operating Context
- Catalog = one folder per product with photos (`*.jpeg`), `data.txt` (nombre, precio, estado, vendido) and `ficha.md` (5-row spec table + ≤140-char blurb).
- Owner edits `data.txt` to change price, condition, or mark sold; the site must reflect it after regeneration.
- Contact: WhatsApp button to +52 55 8809 9786 with a prefilled message per item, plus a message textbox delivered to the owner's email via Web3Forms (access key pending from the owner).
- No cart, no online payment.

## Capabilities and Constraints
- 10 items at launch; the catalog may grow or shrink.
- Home page shows the products directly; no landing/hero preamble.
- Each item: photos, name, price, condition (`estado`, may be empty until the owner fills it), 5-row spec sheet, short blurb, sold state.
- Undecided: hosting provider; Web3Forms access key.

## Brand Commitments
- Name: "Bastians Flea Market".
- User-pinned aesthetic: a rural Japanese dagashi-ya / curiosity shop (shelves, hand-written price tags) combined with a Teenage Engineering–style palette (warm grey, orange, white, black). Palette inspiration only; no TE logos or branding.
- Language: Spanish (Mexico).

## Evidence on Hand
- Real photos of each unit in its folder (taken in the owner's studio).
- Spec sheets in each `ficha.md`. Spec data for Tascam Model 12, Tascam US-2x2HR and Creative T40 was written from knowledge, not verified online.
- No testimonials, reviews or shipping/warranty policy exist; do not invent them.

## Product Principles
1. The goods are the page: products visible from the first viewport.
2. Honest over salesy: real photos, real condition, clear price.
3. Contacting the seller is one tap away from every item.
4. Easy for one person to maintain by editing text files.
