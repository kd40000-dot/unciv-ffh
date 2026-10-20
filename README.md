# Fall from Heaven II / ExtraModMod for Unciv

A **standalone Unciv base-ruleset mod** recreating Fall from Heaven II / ExtraModMod. This repository contains **only mod data and supporting development documents** — not a fork or rebuild of the Unciv game engine.

## Project status

**Fresh mod foundation (phase 0).** The ruleset defines Amurites and Bannor and a small shared starting-game scaffold. Their original distinctive units and art are being introduced in the Amurites first-playable slice; religions, civics, magic effects, full hero mechanics and unique buildings are **not yet implemented**. This is not a faithful or feature-complete FFH2 release.

Development follows a **civilization-first** approach: inventory original EMM civilization definitions, implement their complete distinctive features (beginning with Amurites and Bannor), then add shared systems needed for those features. Gameplay features are checked against original EMM source and Unciv's documented supported JSON uniques, validated with official Unciv mod-ci, and playtested on Android.

## Installation and testing

Open Unciv → Mods → Download mod from URL → `https://github.com/kd40000-dot/unciv-ffh`. Choose the **unciv ffh** base ruleset when starting a new game. This foundation may still have gameplay omissions; CI checks its ruleset integrity only.

## Sources

- Original ExtraModMod implementation: https://github.com/bewlay/extramodmod
- Official Unciv modding instructions: https://github.com/yairm210/Unciv/blob/master/docs/Modders/Mods.md
- Official minimal base-ruleset template reference: https://github.com/yairm210/Unciv-minimal-base-ruleset

See `docs/ROADMAP.md` and `docs/MODDING_BOUNDARY.md` for development goals and mechanical scope.

## History

The former mod prototype and an untouched clone of Unciv remain on archival branches for reference only. This standalone mod does **not** reuse their gameplay JSON or casting experiments. The user's **approved Valledia portrait** and the Amurite nation emblem have been selectively recovered from the archive; new Wizard, Firebow, and Govannon sprite concepts and their atlas are packaged using `development/tools/build_amurite_art.py`.

## Amurites roster (first playable slice)

Firebow (replaces Longbowman, Bowyers), Wizard (replaces Mage, Sorcery), and the unique Govannon hero (Arcane Lore, one per civilization) now have actual unit entries. Adept and Mage are their shared prerequisites. Original source: `bewlay/extramodmod/XML/Units/CIV4UnitInfos.xml` and civilization replacements in `XML/Civilizations/CIV4CivilizationInfos.xml`.

**Important limitations:** Fire/Channeling/Spellstaff currently preserve promotion identity but do not cast spells. Govannon does not yet teach spells. Unciv currently allows producing Wizards directly rather than enforcing the original level-gated Adept upgrade. A simplified tech path permits testing the roster before the full EMM tech tree is ported. No project-specific Android APK is needed. See `docs/AMURITES_STATUS.md` for precise status.

## Amurites 0.1 development preview

- Approved Valledia leader portrait and Amurite nation emblem.
- Distinct unit sprites and icons for Firebow, Govannon, and Wizard, registered in `game.atlas` for the FantasyHex and AbsoluteUnits tile sets.
- Original FFH2 0.30 Manual (user-supplied) is cross-referenced in [`docs/SOURCES.md`](docs/SOURCES.md). [`docs/AMURITES.md`](docs/AMURITES.md) records differences from the later ExtraModMod XML.
- Progress is held on the [`amurites-first-playable-01`](https://github.com/kd40000-dot/unciv-ffh/tree/amurites-first-playable-01) branch pending Android in-game acceptance testing; the working `main` baseline remains unchanged.
