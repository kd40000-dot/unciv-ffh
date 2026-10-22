# Warrens — training XP parity design (investigation 2026-10-22)

**Status:** Source-code supported **design**, not yet implemented or gameplay-validated. No engine edits proposed. This is a prerequisite for the method-1 Warrens duplication experiment. The currently committed Warrens remains a +100% unit Production workaround.

## Original EMM behavior
Pinned EMM commit `60b0ec3740083162aaab7bf8491761a54a65a610`, `python/CvEventManager.py` in `onUnitBuilt`: after checks for Warrens, non-world/non-national, non-mechanical and alive, `newUnit = pPlayer.initUnit(unit.getUnitType(), city.getX(), city.getY(), ...)` followed by `city.applyBuildEffects(newUnit)`. This last call is **essential**: the twin receives the city's training effects, including XP and free promotions. `mainFolder/emm_features.txt` also confirms +10% maintenance.

## Verified native Unciv primitives
Current upstream master `yairm210/Unciv` (must confirm release/version):
1. `BaseUnit.construct` calls `civInfo.units.addUnit`, then `addConstructionBonuses`, which computes starting XP by summing city `UnitStartingExperience` uniques and **sets** `unit.promotions.XP = XP`. It then grants `All newly-trained ... receive promotion` effects.
2. `UnitPromotions.addPromotion` records the new promotion then executes its immediate `doDirectPromotionEffects` in listed order.
3. `UniqueTriggerActivation.OneTimeFreeUnit` calls `civInfo.units.addUnit` to create the twin, which **does not invoke `BaseUnit.addConstructionBonuses`**.
4. `UnitManager.placeUnitNearTile` executes eligible `UnitType` / `Unit` instant triggerables upon placing a unit, including a spawned twin.
5. `UniqueTriggerActivation.OneTimeUnitGainXP` implements `[This Unit] gains [amount] XP` as `unit.promotions.XP += ...`.
6. `UniqueType` includes `[This Unit] gains the [promotion] status for [N] turn(s)`, `[This Unit] loses the [promotion] status`, and `when adjacent to a [mapUnitFilter] unit`. `MapUnit.matchesSingleFilter` recognizes a status/promotion name. `Conditionals` implements the adjacent-unit check for friendly units.
7. Units do not expose unit-trigger actions unless the effect includes a `UnitActionModifier`, so an immediate XP-on-placement effect with no such modifier should not create a repeatable XP button.

Source:
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unit/BaseUnit.kt
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/map/mapunit/UnitPromotions.kt
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/UniqueTriggerActivation.kt
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/civilization/managers/UnitManager.kt
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/Conditionals.kt

## Proposed high-fidelity XP bridge: scoped status markers
At the instant a **trained** original unit receives its type-specific Warrens Birth promotion:

1. The promotion applies short-lived status marker(s) to the original only if the **original's city** supplies the relevant XP bonuses (e.g. `Warrens XP: Sword Training` if Training Yard present; `Warrens XP: Command` if Command Post present).
2. Its next immediate effect is `Free [Original unit name] appears`.
3. The twin's one-time creation effects (on the appropriate UnitType or unit definition) detect a **friendly adjacent unit** carrying each marker. For each marker, award the appropriate XP: e.g. `[This Unit] gains [2] XP <when adjacent to a [Warrens XP: Sword Training] unit>`.
4. After that free unit returns, the original's promotion immediately removes all temporary status markers and optionally removes the one-time Birth promotion. The tags therefore cannot affect upgrades or purchases later in the turn.
5. The original's XP remains computed by Unciv's normal `UnitStartingExperience`; the twin receives matching numeric bonuses via markers. No duplicate production bonuses should remain.

### Illustrative sequence — **schematic**, not ready-to-paste tested uniques

```text
Promotion Warrens Birth - Warrior:
  [This Unit] gains the [Warrens Sword Training] status for [1] turn(s) <in cities with a [Training Yard]>
  [This Unit] gains the [Warrens Command Training] status for [1] turn(s) <in cities with a [Command Post]>
  Free [Warrior] appears
  [This Unit] loses the [Warrens Sword Training] status
  [This Unit] loses the [Warrens Command Training] status

UnitTypes/Sword (instant upon unit placement, no unit action modifier):
  [This Unit] gains [2] XP <when adjacent to a [Warrens Sword Training] unit>
  [This Unit] gains [2] XP <when adjacent to a [Warrens Command Training] unit>
```

The promotion granting birth is itself given **only by Warrens on unit training**, not by a general acquisition trigger. Thus only this brief synchronous spawn window supplies an adjacent marker. The twin does not receive training-only birth promotions and therefore cannot recurse. Bonus condition evaluation on the **original** (in its city) is more robust than evaluating the twin's tile if the twin is forced outside the city border.

**This is contingent** on the spawn being **adjacent** to its original, unique execution order remaining deterministic, immediate status removal working, and a real Android/Unciv test. When stacking/tile congestion pushes the free unit farther away, the twin can miss the XP markers. This is a remaining parity risk. Do not claim source-exact XP until tested for crowded cities.

## Simpler fallback: unconditional acquired-unit XP mirroring
Place `[This Unit] gains [2] XP <in cities with a [Warrens]> <in cities with a [Training Yard]>` on UnitTypes/Sword, plus corresponding effects for Command Post, Hunting Lodge, Stable etc. These are instant on unit creation, so a spawned twin gets XP and an original trained unit's XP will subsequently be set to the regular total.

**However**, unrelated acquisitions/upgrades in a Warrens city can also get XP. Reject this as the *final* method unless scoped marker variant fails and limitations are acceptable. Do **not** place one triggered XP unique on every city building: civilization-wide gain triggers scan all built buildings and could multiply XP across cities.

## Current mod XP sources to mirror
`jsons/Buildings.json`: Command Post +2 Military; Training Yard +2 Sword; Hunting Lodge +2 Scout; Stable +2 Mounted; Siege Workshop +2 Siege; Shipyard +2 Melee Water; Arena +2 Sword; Sculptors Studio +2 Sword (the last two replace Training Yard but are faction-external to Clan). These are themselves provisional gameplay proxies, not EMM original source-verified XP values.

**Further parity:** `Nations.json` currently grants Orc to newly-trained Clan military land units and Mobility I to some newly-trained Clan Disciple units. Twins will **also miss these**, unless the same spawn-window marker mechanism replicates free promotions. This must be in the test/implementation checklist, alongside weapon equipment and any future source-specific training effects.

## Test matrix / release gate
- Warrens only: original 0 XP, twin 0 XP.
- Warrens + Training Yard: Sword originals and twins 2 / 2.
- Warrens + Command Post: military originals and twins 2 / 2.
- Warrens + both: Sword originals and twins 4 / 4.
- Warrens + Hunting Lodge: Scout originals and twins 2 / 2.
- No Warrens: one unit, normal XP, no leaked statuses.
- Purchase, free spawn, gift, upgrade near a Warrens city: **no** extra XP caused by this mechanism.
- Multiple cities each with Warrens and different XP sources: strictly local XP, no cross-city stacking.
- Inspect both units' Orc / other starting promotions separately, not just XP.
- Cluttered city center and all neighboring military slots blocked: detect spawn failure or lack of adjacency; prevent marking as fully faithful.
- Remove current +100% unit Production proxy upon adopting working actual duplication.

This design does **not** yet resolve the exact source-wide training effects and cannot be marked as implemented until loaded, tested, and EMM parity checked.
