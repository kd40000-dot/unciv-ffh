# EMM building-system audit — 2026-10-25

Branch: `checkpoint/emm-city-health-dungeon-2026-10-25`, experimental engine-backed mod; main playable branch not modified.

## Scope and known-source rules

The mod currently contains 81 building definitions. EMM source and FfH2 references distinguish **health**, **city healing**, **crime**, **war weariness**, training gates, trade, random events, and special magic from ordinary Food/Gold/Production yields. Flattening them into resources is incorrect.

Source reference for mechanics:
- EMM pinned source: https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610
- FfH2 building effects reference: https://fallfromheaven.fandom.com/wiki/Buildings
- Dungeon: https://fallfromheaven.fandom.com/wiki/Dungeon (Masonry, -10 Crime Rate, -25% War Weariness)
- EMM code `CvGameCoreDLL/CvCity.cpp` and `CvTeam.cpp` explain war weariness as a player/team combat-history statistic, not a simple flat Happiness bonus. Crime is chiefly a precondition for multiple random events.

## Implemented now (experimental EMM engine)

| Building(s) | Corrected effect | Current implementation |
|---|---|---|
| Aqueduct | +2 Health | engine-backed health, no unconditional Food |
| Herbalist | +1 Health, Spice bonus, 10% faster city healing | engine-backed health/resource/healing, no unconditional Food |
| Infirmary | +3 Health, 25% faster city healing | engine-backed health/healing, no unconditional Food |
| Forge | -1 Health | now contributes unhealthiness rather than food |
| Granary | +1 Health when Wheat available | resource-dependent health in addition to preserved food storage |
| Smokehouse | health bonuses from Cattle/Sheep/Deer in current resource roster | resource-dependent health plus preserved food storage |
| Harbor | +1 Health when Fish available | resource-dependent city health |
| Inn | units heal 25% faster in the city | built-unit native healing calculation |
| Tavern / Tavern Grigori | +1 Happiness | direct Happiness restored, crime contribution tracked |
| Grove | prerequisite for Beastmaster, Lizardman Beastmaster and Myconid | native `Can only be built <in cities with a [Grove]>` on affected units |

**Health caveat:** city health currently computes +/− building modifiers and available resource bonuses against a *provisional* population unhealth baseline `max(population-5,0)`. Only excess unhealth becomes extra Food consumption. This is a working baseline but NOT exact EMM: freshwater, forest, difficulty, leader, innate modifiers, pollution, Fallow and other health sources remain to be ported. Test in a separate save and do not merge to main yet.

## Dungeon, crime and war weariness

Dungeon now has source-backed `emmCrime:-10` and `emmWarWearinessPercent:-25`. We added corresponding fields to native `Building` and computed local `CityStats.emmCrimeModifier` and `CityStats.emmWarWearinessMultiplier`.

**These are not yet complete gameplay mechanics.** EMM random events must read the calculated Crime Rate and the full global/initial city Crime values; Unciv lacks the EMM random-event engine. Dungeon's war-weariness multiplier is calculated but cannot alter Happiness until EMM team war-exhaustion accrual, decay and per-city population anger are ported. Claiming Dungeon is fixed now would be misleading.

Other building Crime modifiers stored for future native event logic: Courthouse -10, Market +5, Gambling House +5, Inn +5, Public Baths +5, Tavern +5, Tavern Grigori +5, Warrens -5. Exact EMM source values and conditional modifiers require full audit before merging.

## Additional important missing systems

| Building or family | Original mechanic not yet implemented faithfully |
|---|---|
| Dungeon / Courthouse / Market / Public Baths / Taverns | Crime threshold and random-event triggers; world/city random crime baseline, event choices and outcome persistence |
| Dungeon and civic/Palace war modifiers | Per-enemy war weariness accumulation on combat; peacetime decay; 25% local reduction translated into unhappy citizens |
| Obsidian Gate | City-to-city teleport permissions, per-city-use budget, movement and relocation |
| Planar Gate | Armageddon-dependent gated unit spawn probabilities and source-building prerequisites |
| Grove and druid prerequisites | Remaining druid/Myconid variants and correct faction access |
| Tavern Grigori | Adventurer generation / specialists and trade bonuses |
| Infirmary | Grigori Medic unlock; original City Healing behavior needs in-game comparison |
| Harbor, Granary, Smokehouse and Herbalist | All original resource names and conditions; health from unavailable resources |
| Health in general | Real full FfH/EMM green/red health aggregation, terrain, fresh water, sanitation, missing buildings/resources, Fallow |
| Hall of Mirrors / Citadel of Light | Timed illusion spawning / automatic nearby damaging effects |
| Special civic, religion and race buildings | Native religion, alignment, faction restrictions, special promotion grants and world effects |

## Validation and manual tests

- `engine/verify_city_buildings.py` validates the fields, replacement of food proxies, Grove prerequisites and tavern happiness.
- Original pinned Unciv source anchors for `Building.kt`, `CityStats.kt` and `MapUnit.kt` were individually checked for unique match before overlay compilation. Full CI/Android build still requires confirmation.
- [ ] Compare a size-8 city with and without Aqueduct/Herbalist/Infirmary: unhealth-related extra Food consumption should fall, while building Food stays zero.
- [ ] At low population with spare health, the health buildings should not simply generate free Food.
- [ ] Give the civilization Spices/Wheat/Fish/Sheep, compare corresponding Herbalist/Granary/Harbor/Smokehouse conditional health effects.
- [ ] Damage a unit and heal in the city with/without Herbalist, Inn, Infirmary; confirm native healing multiplier.
- [ ] Confirm Forge can increase excess unhealth.
- [ ] Compare Tavern Happiness +1.
- [ ] Check Beastmaster/Lizardman Beastmaster/Myconid production is restricted before Grove and unlocked after.
- [ ] Dungeon Crime -10 and War Weariness -25 are **metadata-only in this checkpoint**. Do not report them as gameplay-tested until their dependent systems are implemented.
- [ ] Test save/load for city buildings and health values.

## Recommended implementation order

1. Full health aggregation / city UI, plus all health resources, traits and Fallow exemptions.
2. Native Crime Rate state, EMM source-defined random event prerequisites and player-choice outcomes; Dungeon becomes consequential.
3. War weariness combat accumulator + decay + CityStats unhappiness; apply Dungeon and other local modifiers.
4. City teleportation, Planar Gate, specialist and unit eligibility systems.
5. Re-audit all 81 buildings against pinned EMM source and playtest with the custom Android engine.
