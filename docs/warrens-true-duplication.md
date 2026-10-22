# Warrens — true duplicate prototype (2026-10-22)

**Status:** Implemented in mod JSON and structurally validated, but **NOT tested in an actual Unciv game**. No engine source changes. Rollback: `checkpoint/pre-warrens-true-duplication-2026-10-22`.

## Source behavior (EMM Continued pinned commit)
`python/CvEventManager.py` has `onUnitBuilt`: if the city contains Warrens, the new unit is not a world/national unit, is not mechanical, and `unit.isAlive()`, it calls `pPlayer.initUnit(unit.getUnitType(), city.getX(), city.getY(), ...)` and then `city.applyBuildEffects(newUnit)`. Original Warrens also has +10% city maintenance (EMM feature notes and source XML).

Source: https://github.com/bewlay/extramodmod/blob/60b0ec3740083162aaab7bf8491761a54a65a610/python/CvEventManager.py

## Current JSON mechanism
- Removed the existing +100% Sword/Scout/Archery/Mounted production proxy from `jsons/Buildings.json` so it cannot stack with real duplication.
- Warrens (Clan of Embers only) grants a **unit-specific free 'Warrens Birth - NAME' promotion** to each eligible unit constructed in that city. There are 16 current eligible unit definitions. Generic unit replacements are excluded when there is a Clan variant, to prevent double triggers.
- Each `Warrens Birth` promotion has the native `SkipPromotion` unique (`Doing so will consume this opportunity to choose a Promotion`). Therefore the birth promotion is **not stored as a permanent promotion**, and does not use normal promotion XP. It immediately:
  1. Marks the parent with one-turn `Warrens Parent` status.
  2. Adds transient status markers for each qualifying existing XP building in the parent's city.
  3. Spawns exactly one unit of the matching named type using `Free [unit] appears`.
  4. Removes every transient marker from the parent, including the parent marker.
- `UnitTypes.json` has on-placement XP and racial promotion effects that fire **only while next to the marked parent**. Duplicate XP for each marker is +2, matching the **current mod's** production XP grants from Command Post, Training Yard, Hunting Lodge, Stable, Siege Workshop or Shipyard. Unciv's normal trained-unit path gives the original's XP *before* the birth event; the spawned duplicate bypasses that training path and collects marker bonuses via its placement trigger. Orc is added to Clan military-land duplicates, Mobility I to Clan Disciple duplicates.
- Ordinary preexisting promotions inherent to a unit's base definition are received naturally by the spawned copy.

The 16 mapped eligible unit definitions in this release: Archer, Axeman, Chariot, Longbowman, Settler, War Elephant, Warrior, Worker, Goblin, Shaman, Wolf Rider, Lizardman, Ogre, Lizardman Ranger, Lizardman Assassin, Mage. World/national units (e.g. Archmage, Beastmaster, Phalanx) are intentionally excluded. Siege devices, ships and nonliving faction units are intentionally excluded. Source-specific `isAlive`/mechanical flags are not fully represented in the current source inventory, so some eligibility remains provisional.

Native behavior verified by **source inspection**, not engine execution:
- `BaseUnit.construct` calls `addUnit` then `addConstructionBonuses`: https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unit/BaseUnit.kt
- `UnitPromotions.addPromotion` calls `doDirectPromotionEffects` and `SkipPromotion` prevents saving it: https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/map/mapunit/UnitPromotions.kt
- `UnitManager.placeUnitNearTile` runs UnitType instant effects on placement; free units are created without `addConstructionBonuses`: https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/civilization/managers/UnitManager.kt
- `UniqueTriggerActivation` implements XP gain, status markers and free-unit creation: https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/UniqueTriggerActivation.kt

## Edges to investigate before marking Warrens complete

1. **Spawn space / adjacency (high):** Unciv only allows one military unit on most tiles. It may place the duplicate away from the parent (if near-city tiles are crowded) or fail to place it at all; unlike Civ IV, the duplicate does not stack on the city tile. Our XP transfer depends on the spawned unit landing adjacent to its parent. If not adjacent, it may appear with 0 XP/without Orc.
2. **Purchased and hurried units (high):** `BaseUnit.construct` invokes `addConstructionBonuses` even for units constructed with `boughtWith != null`. Warrens may therefore duplicate bought units; check whether EMM `onUnitBuilt` includes source hurry production, and decide parity. Acquired gifts/other free units should not trigger building's training-only promotion, but test.
3. **Exact source eligibility (high):** EMM tests `isAlive()` and `isMechUnit()` dynamically. Current source catalog doesn't preserve every derived alive/mechanical state. Validate all 16 against EMM and consider promotions that change living status. Settlers and Workers are included deliberately: source exclusion does **not** say military only.
4. **Training effects beyond present XP buildings (medium):** Current +2 XP mirrored for six building categories. Other source effects, building replacements, civic/leader-based bonuses, special promotions, equipment and future training sources still require mapping and tests. Values are provisional as documented in `docs/ordinary-buildings-first-pass.md`. Check duplicates receive *all* relevant effects, including Orc and Clan Disciple Mobility I.
5. **Unit placement relative to cities (medium):** If original unit is placed on a tile outside the producing city's territory or into a neighbor city's plot, checks like `<in cities with a [Training Yard]>` could inspect wrong city.
6. **Repeatability / recursion / saves (high):** Verify exactly one duplicate per build, no duplicate spawns recursively, no permanent birth promotions/statuses, and that saves reload safely. Check multiple simultaneous completed cities and turns.
7. **Maintenance (high):** EMM imposes +10% city maintenance. Unciv has no source-equivalent building maintenance model in the current port; this modifier is still unimplemented (do not call Warrens source-complete).
8. **Over-cap / transformation (medium):** World/national caps are skipped for the birth map; confirm no copies of restricted units via replacements, upgrades or mod-added units. New units added later to `Units.json` must be classified and given birth mappings.
9. **Civilian duplication and strength impact (medium):** Test Worker/Settler, mounted, magic and Orc racial promotions, as well as mixed troop production. The effect intentionally includes living civilians per source code but could have large balance consequences.
10. **Version differences (medium):** Source inspection refers to upstream Unciv master. User's installed Unciv build could have different unique parsing, SkipPromotion behavior, spawn, or trigger timing. Test "Locate mod errors" before new game.

## Android acceptance matrix

| Scenario | Expected |
| --- | --- |
| Clan, no Warrens, build Warrior | 1 Warrior |
| Clan, Warrens, build Warrior | 2 Warriors (same named type) |
| Clan, Warrens and Training Yard, build Axeman | 2 Axemen, each 2 XP |
| Clan, Warrens and Command Post, build Warrior | 2 Warriors, each 2 XP |
| Clan, Warrens, Training Yard, Command Post, build Axeman | 2 Axemen, each 4 XP |
| Clan, Warrens and Hunting Lodge, build Lizardman | 2 Lizardmen, each 2 XP |
| Clan, Warrens, build Goblin | 2 Goblins and both have Orc |
| Clan, Warrens, build Worker or Settler | 2 equivalent civilians |
| Clan, Warrens, build capped national unit | only 1 unit |
| Other civ without Warrens, train regular units | no duplicate or leftover marker |
| Buy/upgrade/gift near a city with Warrens | check against EMM source behavior; should never recurse |
| Crowded city with blocked neighboring tiles | document spawn behavior and XP status |
| Save then reload | no replayed birth effects or leftover markers |

**Validation performed:** JSON parsed and consistency check passed: all 16 birth references point to valid unit names and corresponding promotion definitions, every promotion has a correct named free-unit effect and a scoped marker lifecycle, and all marker references in UnitTypes resolve. Actual Unciv mod-ci and gameplay tests have **not been run**.
