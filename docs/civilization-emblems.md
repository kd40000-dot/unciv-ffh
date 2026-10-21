# Erebus civilization emblems — Phase 3.5

**Status:** 19 full-color user-provided civilization emblems installed and packed for Android; revised to circular-cropped, borderless presentation on October 21, 2026. Gameplay test of revised appearance pending.

## What was imported

The supplied `CivIcons.zip` contained 19 clearly labeled 64×64 RGBA WebP faction icons, including two nonstandard source filenames (`Bannorflag.webp` → `Bannor` and `ClanofEmbers.webp` → `Clan of Embers`). All 19 match the playable civilization names in `jsons/Nations.json` and are inventoried in [the source and filename ledger](data/erebus-civilization-emblems.json).

These are user-supplied FfH-looking faction emblems; their pixel-level correspondence to original EMM DDS files has not been independently established.

## Format and why NationPortraits

Unciv normally colors `NationIcons` with each faction's inner color; the submitted emblems are **already full-color squares**, so using them as `NationIcons` would tint them and spoil their appearance. Therefore these images are installed under `Images.Emblems/NationPortraits/<Nation>.png`, where Unciv displays portraits without icon tint.

Each source image is centered **without changing its 64×64 content** inside a transparent 96×96 RGBA PNG. There are 19 original-size source PNGs, a separate packed `emblems.png` page (512×512) and `emblems.atlas` with 19 `NationPortraits/<Nation>` keys. The root `Atlases.json` loads **both** `game` (existing, user-verified leader portraits) and `emblems` (these new icons), ensuring Android compatibility and no overwrite of the leader portrait page.

The verifier `python3 tools/verify_civilization_emblems.py` checks all 19 nation names, PNG formats/CRC/dimensions, both atlases and region names. GitHub Actions runs it.

## In-game QA

Update the GitHub mod on Android, then check the nation picker and diplomacy/first-contact screens. The icon backgrounds should retain their characteristic colors (red Calabim, blue Lanun, etc.) and should **not** all be tinted the same faction color or replaced by generic circles. Inspect a handful of different factions and confirm the existing leader portraits still appear.

A potential visual difference from vanilla Unciv is that color-preserving nation portraits have square symbols drawn over the usual circular nation background, rather than solid monochrome symbols. If this is undesirable, the alternative is deriving transparent monochrome `NationIcons` from the original flags, allowing Unciv's own inner/outer-color treatment.

Other gameplay mechanics and dialogue strings were not changed by this milestone.

## Circular emblem refinement — October 21, 2026

The initial import put each source rounded-square button and its gray border inside Unciv's circular symbol slot. The user reported that the double-framing looked poor and asked to remove the border and fill the circle. Several attempts to isolate fully transparent glyphs by color segmentation damaged the emblem details, so the selected correction instead **crops the 64×64 source button inward by five pixels on all sides, scales to a 96×96 square, and applies an antialiased circular transparency mask**. This drops the exterior square border and shadow while retaining the intact full-color design and background inside a circular silhouette. It is explicitly not a transparent glyph-only extraction.

All 19 `Images.Emblems/NationPortraits/*.png` assets and the separate `emblems.png` texture page were regenerated. The `emblems.atlas` coordinates and `Atlases.json` remain unchanged, as do `game.png`, `game.atlas`, the 19 leader portraits, and all game rules. Android appearance of this revision is pending user verification.
