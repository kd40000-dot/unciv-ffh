# Amurite Summons & Blaze — mechanics test 0.3

This follows [the working Magic Foundation 0.2](MAGIC_0.2.md). The user confirmed that 0.2 works in-game. All five approved unit portraits/map sprites and the prior 0.2 build remain preserved.

## Two new caster actions

### Death I — Raise Skeleton

- Reference: `bewlay/extramodmod/XML/Units/CIV4SpellInfos.xml`, `SPELL_RAISE_SKELETON`; `XML/Units/CIV4UnitInfos.xml`, `UNIT_SKELETON`.
- Unciv: `Free [Skeleton] appears <for all movement>` on **Death I**; caster summons one permanent Skeleton on a nearby legal tile.
- Skeleton: base strength 2, movement 1, unable to pillage; generated simple grayscale pixel sprite, deliberately separate from the five previously approved images.
- **Known deviation:** Native Unciv does not track which caster owns each summon for a dynamic one-per-Death-I-caster cap. This test provisionally limits the civilization to three living Skeletons, not the original caster-linked cap. The original graveyard triple-summon behavior and exact first-turn exhaustion need a future iteration.

### Fire I — Blaze

- Reference: `bewlay/extramodmod/XML/Units/CIV4SpellInfos.xml`, `SPELL_BLAZE`; `python/entrypoints/CvSpellInterface.py`, `reqBlaze`.
- Unciv: `Can instantly construct a [Smoke] improvement <for all movement>` on **Fire I**.
- Smoke should only be placeable on an unimproved **Forest or Jungle** tile beneath the caster. Smoke is meant to be created by Fire I units rather than Workers.
- **Known deviation:** Smoke is a **persistent 3-HP adjacent-enemy hazard** in this test. It does not become spreading Flames, consume Forest/Jungle or expire automatically as in ExtraModMod. The approximation is intentionally visible and tactical so we can verify the unit action and tile effects.

## How to test on Android

1. Start a **new game** as Amurites / Valledia with the new ZIP.
2. Verify the previously working Body I **Haste** still works.
3. Train a **Firebow** (requires Bowyers and an Archery Range), move him onto Forest/Jungle and check for **Create Smoke / Blaze** action. It should not appear on open Plains or Grassland.
4. Move an **Adept/Wizard** with **Fire I** onto Forest and check Blaze as well.
5. Find a **Raw Mana** tile and attune it to a **Death Node** with a Worker (Knowledge of the Ether).
6. Train an Adept at a Mage Guild and choose **Death I** once Death Mana is available.
7. Check the **Free Skeleton appears / Raise Skeleton** action. Verify a Skeleton spawns nearby, has strength 2/movement 1, persists after ending turns, and can be commanded next turn.
8. Attempt a fourth Skeleton and verify the three-living-skeleton limit. Killing/disbanding a skeleton should permit another.
9. Verify existing 0.2 save games are **not assumed compatible**. Save/reload a **new** 0.3 game with a Death Node, Smoke and Skeleton.

## Classification and implementation status

| Mechanic | Classification | Confidence |
| --- | --- | --- |
| Body I / self-Haste | Native Unciv approximation | User confirmed working in 0.2 |
| Death I / permanent Skeleton | Native Unciv approximation | Syntax checked; in-game behavior **not yet confirmed** |
| Fire I / Smoke | Native Unciv approximation | Syntax checked; in-game behavior **not yet confirmed** |
| Amurite starting Body, Fire, Mind Mana | Native global resource uniques | 0.2 included; individual node conversion needs testing |
| ExtraModMod dynamic summon cap | Blocked in current JSON-only design | Temporary flat 3-unit cap |
| Spreading Flames and decay | Blocked in current JSON-only design | Persistent Smoke hazard instead |

Do not label XML compatibility or a successful `mod-ci` run as proof of Android gameplay. No engine fork, no Kotlin changes.
