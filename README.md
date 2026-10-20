# Fall from Heaven II / ExtraModMod for Unciv

A **standalone Unciv base-ruleset mod** recreating Fall from Heaven II / ExtraModMod. This repository contains **only mod data and supporting development documents** — not a fork or rebuild of the Unciv game engine.

## Project status

**Fresh mod foundation (phase 0).** The ruleset defines Amurites and Bannor and a small shared starting-game scaffold. Their original distinctive buildings, units, religion, heroes, civics and spell mechanics are **not yet implemented**. This is not a faithful or feature-complete FFH2 release.

Development follows a **civilization-first** approach: inventory original EMM civilization definitions, implement their complete distinctive features (beginning with Amurites and Bannor), then add shared systems needed for those features. Gameplay features are checked against original EMM source and Unciv's documented supported JSON uniques, validated with official Unciv mod-ci, and playtested on Android.

## Installation and testing

Open Unciv → Mods → Download mod from URL → `https://github.com/kd40000-dot/unciv-ffh`. Choose the **unciv ffh** base ruleset when starting a new game. This foundation may still have gameplay omissions; CI checks its ruleset integrity only.

## Sources

- Original ExtraModMod implementation: https://github.com/bewlay/extramodmod
- Official Unciv modding instructions: https://github.com/yairm210/Unciv/blob/master/docs/Modders/Mods.md
- Official minimal base-ruleset template reference: https://github.com/yairm210/Unciv-minimal-base-ruleset

See `docs/ROADMAP.md` and `docs/MODDING_BOUNDARY.md` for development goals and mechanical scope.

## History

The former mod prototype and an untouched clone of Unciv are stored on archival branches for reference only. Neither is used as the new baseline. Previously generated leader portraits, art atlases and casting experiments have **not** been carried into the fresh ruleset.
