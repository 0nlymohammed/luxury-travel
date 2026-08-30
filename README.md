# LUXURY Travel & Tourism, website prototype (Phase 0, v11)

High-fidelity single-page design prototype for the LUXURY Travel and Tourism homepage. Follows the printed company profile (`COMPANY PROFILE LUXURY.pdf`). v5 replaces the hero with MOLTEN LETTERPRESS: the wordmark die-cut at monumental scale through the charcoal, filled with living molten gold rendered by a GLSL shader (Three.js fullscreen quad). Each letter pours in like a film title with a glowing liquid meniscus; the cursor acts as the gallery light (with an idle auto-orbit); scrolling out cools the gold toward charcoal. The Arabic toggle rebuilds the monument as an equal Arabic word (Cairo 900). The folio route line (BGW to ATH, km and heading) is COMPUTED from coordinates at runtime, never typed.

Live preview (private artifact): https://claude.ai/code/artifact/d87e6a9f-0ffc-4985-8ae2-c4511c9cef7b

## What is here

- `index.html` : the finished, self-contained page. Open directly in any browser. All photos inlined as data URIs (only Google Fonts load over the network).
- `luxury.template.html` : the editable source. Photos referenced as `{{IMG_name}}` tokens.
- `build.py` : inlines the JPEGs from `assets/` into the template and writes `index.html`. Run `python build.py` after editing.
- `assets/` : photos extracted from the profile PDF (wing_hi, window_sunset, window_bright, resort, coast_hi, worldmap, city_top, city_bottom).

## Design system (from the profile)

- Colors: camel-gold `#B19266`, gold-on-dark `#C6A97E`, gold text on white `#7D6240` (AA), charcoal `#202020` / `#282828`, white, paper `#F7F4EF`, slate wash `#EDF2F4`.
- Type (Google Fonts): Cormorant Garamond (wordmark, headlines, numerals), Archivo 800 (grotesque titles), IBM Plex Sans (body), Cairo (Arabic), IBM Plex Mono (coordinates, plate captions, data).
- Photo system: every image is a REAL photograph from the profile, treated one of two ways per the printed identity: full-bleed off a viewport edge, or matted in a white inset frame on a solid field. Gold duotone on dark bands only; the coast and resort stay natural (their color is the product). Mono plate captions throughout. Film-grain overlay on photographic surfaces only. No drawn objects, no mockups, no gradients, no shadows, zero border-radius.
- Bilingual: English default, Arabic RTL toggle (Cairo, mirrored layout, phone numbers and digits stay Latin).

## v11 highlights

- THE PLANE IS GONE, replaced by TWO client-selectable signatures built purely from light, pins, and geometry:
  1) LIVING ROUTES (default): every ~6s one route draws itself from Baghdad as a line of golden light; on arrival a gold map pin drops with a ripple, the destination label glows, and the folio ticker types the leg with runtime-computed distance and heading (BGW to IST, DXB, ATH, ...). Route light is masked so it never crosses the molten letters.
  2) GOLDEN EARTH (#globe in the URL, or the corner switch): a rotating particle Earth (real continents from land data) with route arcs rising off the sphere, behind the monument.
- A small MAP VIEW / GLOBE VIEW switch sits in the hero corner for side-by-side client review; remove it (and the hash check) once a winner is chosen.

## v10 highlights

- THE PLANE IS NOW A REAL 3D RENDER: a stylized gold-metal airliner modeled and rendered headlessly in Blender 5.2 (Cycles, transparent film, three-light studio, 3/4 aerial camera) via blender_plane.py; asset at assets/plane3d.png. Re-run the script against the portable Blender in C:/tmp/bl to iterate the model.
- The hero coordinates line (33.3152 N ...) removed.
- Blender MCP registered at user scope (uvx blender-mcp). To make it interactive later: install uv (winget install astral-sh.uv), open Blender, install/enable its MCP addon, then Claude sessions can drive Blender live.

## v9 highlights

- THE MAP IS NOW A REAL ATLAS: true continent coastlines stroked from Natural Earth geometry (land_polys.json) over the gold dot fill, with no dateline artifacts.
- THE TRAVEL SIGNATURE: a route network of real great circles from Baghdad to seven real destinations (ATH, IST, BEY, DXB, DOH, CDG, LHR), each with a labeled node; the plane cycles through the routes leg by leg.
- THE PLANE IS THE BRAND'S OWN: the swooshing jet cropped in high resolution from the official logo (assets/logo_plane.png), contrail fading naturally, flipping for westbound legs.
- The statement band photo replaced with the real wing-through-window photograph (the city sliver read as broken).
- Build now also needs land_polys.json and assets/logo_plane.png.

## v8 highlights

- A flat ivory-and-gold PLANE SILHOUETTE with a fading contrail now flies the Baghdad-to-Athens arc on the hero map, banking with the path (replaces the comet dot).
- Removed per client: the B2B section, the city-strip band above the footer, the three language chips in About, and the "Live render" chip.
- The statement band is no longer a pinned scroll scene: it is a simple full-bleed duotone photo with the tagline plate, gentle reveal only.

## v7 highlights

- FIXED the missing-photos bug for good: Chrome computes IntersectionObserver intersections AFTER an element's own clip-path, so a shade-hidden figure could never trigger its own reveal. Shades now clip the figure's children (the box stays observable), reveals also run from an always-on scroll sweep, and all entry states are armed only when JS is alive (body.anim), so content can never be blanked.
- The window-plates section is gone; in its place one full-bleed real photograph: an aircraft wing at golden hour ("Embraer 190 - Wing and winglet at sunset" by PierreSelim, CC BY-SA 3.0, Wikimedia Commons; credited in the footer).
- Partners section retitled to "Our Partners" / شركاؤنا; the 3-languages stat removed (stats band is now four).
- About copy rewritten short and warm; added <meta charset="utf-8"> so the standalone file renders Arabic correctly everywhere.

## v6 highlights

- ARABIC IS THE PRIMARY LANGUAGE: the site boots in Arabic (RTL), EN is the toggle. The hero monument boots as الفخامة.
- REAL BRAND LOGO in the nav, recovered from the abandoned old site (luxury-travel.net/assets/img/logo.png, trimmed and downscaled to assets/logo_nav.png).
- TRAVEL SIGNATURE: behind the monument, the REAL world drawn in gold dots (Natural Earth land data via the world-atlas package, decoded and sampled into land_dots.json), with the true Baghdad-to-Athens great circle dashed across it, a comet riding the arc, a pulsing beacon at Baghdad's true coordinates, and BGW/ATH labels. Distance and heading in the folio are computed at runtime (haversine + bearing).
- Arabic copy for core strengths, services headings, service 5 and 6 bodies, and all four B2B cells is now VERBATIM from the printed profile's Arabic pages.
- Instagram added to contact: instagram.com/luxury.travel.iq (from the old site).
- Build now also needs land_dots.json and assets/logo_nav.png (build.py handles .png assets).

## Molten hero (desktop)

- Three.js r128 inlined; the hero is one fullscreen quad + a GLSL molten-gold shader masked by a canvas-rendered type texture (R=glyph coverage, G=letter index, B=pour gradient).
- Letter-by-letter pour choreography; cursor-as-light with 6s idle auto-orbit; scroll-exit cooling; candle glints; die-cut edge hairline.
- Arabic mode renders the monument in Cairo 900; mask rebuilds on font load and on language toggle.
- Enabled on screens wider than 880px with WebGL and no reduced-motion preference; otherwise the real wing-photo split hero renders (also the reduced-motion and WebGL-fail fallback, which shows a single still frame where possible).
- vendor/plane_final.glb and GLTFLoader remain on disk for history but are no longer built into the page.

## Animation system ("scroll cinema", all vanilla JS/CSS)

- Hero load: cabin-shade photo reveal + gold "develop" fade, staggered masked line-rises, drawn BGW-ATH dashed arc with a plane rider that lands and detonates the ATH node, teletype coordinates with a double caret blink. Skippable on first scroll.
- Scroll: one-shot IO reveals with staggers; count-up stats; gold rules drawing from inline-start; CONFIRMED tags stamping once; curtain cuts at light-to-dark splices; window-shade reveals with duotone develop on every photo.
- Signature: the services flight-path spine draws with scroll, a plane-dot with trail rides the tip, and each waypoint ignites (square to gold diamond + one radar ring) as it passes. Fully reversible.
- Statement band: pinned 240vh scroll scene; the city photo zooms 1.25 to 1.0 while "We elevate your travel experience" resolves word by word.
- Ambient: twinkling map dots and a slow Ken Burns drift on matted plates. Everything gated behind prefers-reduced-motion (static final states).

## Notes and stand-ins

- The `LUXURY` wordmark is a typographic stand-in (Cormorant + plane glyph). Replace with the client's vector logo.
- Partner tiles are typeset names; swap in the 8 real partner logos.
- Secondary Arabic copy is a clean draft; proofread against the profile's own Arabic pages before launch.
- The "Every itinerary starts at a window" section uses the REAL window photographs from the profile cover. If the client still associates windows with the rejected mock, delete that one section block (`id="plates"`).

## Phase 1 (production), planned

Astro + Tailwind + TS, `/ar` (RTL, default) + `/en` routes, per-language JSON content, WebP/AVIF with srcset, Lighthouse 90+ mobile, JS < 150 KB, forms stubbed with backend TODO.
