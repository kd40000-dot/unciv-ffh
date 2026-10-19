# Erebus for Unciv (ExtraModMod adaptation)

An experimental **Unciv standalone base ruleset** adapting the fantasy strategy game **ExtraModMod Continued** (EMM; descended from Fall from Heaven II).

> **Status: prototype 0.1a / untested in Unciv.** This is development source, not a finished gameplay release.

## Goals

- Use EMM, not vanilla Fall from Heaven II, as the canonical gameplay reference.
- Preserve EMM civilizations, technology dependencies, flavorful magic, units, and distinctive gameplay wherever Unciv mechanics allow.
- Use the normal Unciv mod system for Android compatibility; avoid Unciv engine forks unless essential.
- Base the first playable test on Amurites, Bannor, Ljosalfar, and Clan of Embers.
- Keep exact EMM source values separate from gameplay approximations.

## Provenance

- EMM: https://github.com/bewlay/extramodmod, pinned reference commit `60b0ec3740083162aaab7bf8491761a54a65a610` (2026-04-19).
- Unciv base ruleset example: https://github.com/yairm210/Unciv-minimal-base-ruleset
- Fantasia reference for magic-related ruleset techniques: https://github.com/amfauzn/Fantasia

This project is an independent fan adaptation and is not affiliated with the original projects. Rights and licenses for artwork need review; no upstream art files are bundled by default.

## First milestone

1. Commit a basic standalone ruleset in `jsons/`.
2. Validate JSON and internal references.
3. Test loading and starting a game in Unciv on Android.
4. Iterate on mechanics based on actual in-game behavior.
5. Implement spells, monster/lair interactions, and unique civ mechanics incrementally.

**Not yet verified:** rendering, game creation, AI play, spell effects, and gameplay balance. We will record what has actually been tested rather than assume compatibility.

## Archive download compatibility

Unciv's GitHub ZIP importer requires recognized mod entries to outnumber
unrecognized entries at the archive root. All auxiliary project files live
under `development/` to keep the root valid. The validation workflow
checks this condition to prevent regression.

## Important: choose the right Base Ruleset

When setting up a game, select **unciv ffh** as the **Base Ruleset**
(not `Fantasia 3.2`). This mod is standalone rather than an expansion
for Fantasia. Do not select both in the same game. After updating the
mod via Unciv's mod manager, create a **new game** to test the current
ruleset.
