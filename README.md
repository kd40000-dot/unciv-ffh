# Erebus for Unciv (ExtraModMod adaptation)

An experimental **Unciv standalone base ruleset** adapting the fantasy strategy game **ExtraModMod Continued** (EMM; descended from Fall from Heaven II).

> **Status: prototype 0.2 (visual and civilization expansion).** Version 0.1a was confirmed playable on Android; the newly expanded graphics/units have passed Unciv's official `mod-ci` and GitHub Actions, but have **not yet had an in-game Android visual test**.

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

## First playable milestone: achieved

On 2026-10-20 the user confirmed that the mod **loads and is playable in Unciv**.
Both the static checks and official Unciv `mod-ci` validator passed on commit
`754f8d4`. This confirms basic installation, game loading and interaction,
not a complete mechanical or balance review.

**Rollback branch:** [`playable-0.1a`](https://github.com/kd40000-dot/unciv-ffh/tree/playable-0.1a) pins that user-tested commit. Do not rewrite or delete this branch.

## Next milestone: meaningful ExtraModMod gameplay

1. Audit the gameplay in a short 50–100 turn playthrough: expansion, research, combat, improvements and AI behavior.
2. Expand the EMM civilization-specific early units and buildings while preserving a startable game.
3. Prototype genuine player-activated magical abilities using supported Unciv unique actions. Keep existing passive bonuses as temporary placeholders only.
4. Introduce EMM monsters and lair/exploration interactions using supported Unciv mechanics.
5. Repeat the in-game smoke test before advancing the rollback point.

**Not yet verified:** all civilizations' full playthroughs, advanced unit upgrades, EMM spell fidelity, AI balance, religions, heroes and late-game systems.

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

## 0.2 graphics and civilization expansion

- Four illustrated leader portraits: **Valledia, Sabathiel, Arendel, Jonas**.
- Four nation emblems, **29 unit portraits/icons** and **37 2D unit sprite variants**, including several civilization-specific styles.
- Official packed `game.atlas`/`game.png` for Android (no on-device graphics compiling required).
- The prototype now contains **38 technologies and 29 units** including EMM's **Shaman, Wolf Rider, Lizardman, Ogre, Chanter, Flurry, Fyrdwell, and Crusader**.
- These are **noncanonical GPL-licensed Battle for Wesnoth visual stand-ins**, not original FFH2/EMM leaderheads or 3D models. [Art provenance](development/ARTWORK.md) and [credits](Credits.md).
- The Crusader temporarily has a technology gate instead of EMM's full religion condition; other systems remain adapted to Unciv's mechanics.

**Testing:** Update the mod in Unciv, restart the app if old textures persist, and start a new game with `unciv ffh` as the Base Ruleset (not Fantasia). Check the diplomacy portraits, new unit art on the map, construction menu art, and civilization-specific units. Report any missing graphics. The proven rollback is the `playable-0.1a` branch.
