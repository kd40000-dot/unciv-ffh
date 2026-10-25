# EMM sprite redraw — artwork acceptance gate

The previous scripted placeholders are **rejected**, not an acceptable artistic solution. This branch deliberately does **not** recolor Amurite poses, run the polygon sprite generator, or approve anything based solely on valid PNG files.

## Protected artwork
Do not edit original approved Amurite sprites or any Worker or Settler PNGs.

## Required for each redraw
1. **Art style and quality:** original character illustration with Amurite reference quality, faceless polygonal cel-shading, consistent dark outline weight, credible anatomy and appropriately layered clothing. Recoloring an existing character or using a blocky geometric figure is **not acceptable**.
2. **Civ and race:** a meaningful design tied to that civilization (Bannor crusaders, Balseraphs eerie carnival, Clan orcs, Calabim vampires, dwarven Khazad/Luchuirp, etc.) and using recognizable nation colors. A color shift without character redesign **does not count**.
3. **Technical:** 512×512 true RGBA PNG with transparent exterior and interior negative spaces and no clipping or stray matte pixels.

A replacement must be independently reviewed and tagged `styleQuality: pass`, `themeColors: pass`, `reviewed: true`, and have a valid `replacement` PNG path in `art/REDRAW_QA.json`. `python art/validate_redraw_qa.py` validates accepted entries and file properties; **it does not assess subjective art quality**.

## Queue
`art/REDRAW_QA.json` lists every affected generated unit and keeps an explicit rejected/awaiting/accepted state. The existing placeholder manifest is retained for rollback and tracking.

The old generative drawing scripts remain in the inherited history but **must not be used to claim visual parity**. No PNG is accepted purely because a GitHub Actions job succeeded.

## Current work status
This checkpoint sets up the audit and quality gate only. It contains **no newly accepted image redraws**. The old images remain available as explicitly rejected placeholders until actual illustrations pass human/visual review.
