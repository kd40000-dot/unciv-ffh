# Typed EMM damage integration status — 2026-10-27

Pinned source: `bewlay/extramodmod@60b0ec3740083162aaab7bf8491761a54a65a610`, `CvGameCoreDLL/CvUnit.cpp` (`CvUnit::doDamage`, `CvUnit::getDamageTypeResist`) and `python/entrypoints/CvRandomEventInterface.py`.

## Connected runtime damage

- The Blight and Pestilence callbacks use `EmmTypedDamage.applyToUnit` with `DAMAGE_DEATH`, base damage 25 and total damage limit 100, after source-derived living classification.
- The adapter sums current promotion resistances using 34 XML resistance records and clamps to [-100, 100].
- The source direct-damage kernel rolls two random numbers in [0, damage), applies resistance and the remaining damage cap, then modifies actual unit HP by calling `MapUnit.takeDamage`.
- EMM also adds 2× defensive combat strength, 2× unit level and one quarter of current city defenses to the resistance total; the Unciv adapter currently approximates these as base unit strength, 1 + earned promotion count, and zero city defense. This is **not yet exact damage parity**.
- Typed damage is not applied automatically to all vanilla Unciv attacks. Generic combat, spell damage, promotion-applied poison and feature/terrain damage have different EMM triggers and must be connected individually to avoid duplicate damage or changing vanilla combat by accident.

## Remaining source integration

1. Port effective `baseCombatStrDefense()`, actual EMM level semantics and plot-city defense so the direct-damage adapter can operate without approximations.
2. Extract unit and promotion `DamageTypeCombats`; EMM uses their portions in effective melee combat strength after defender typed resistances, not as a second direct-damage roll.
3. Port damaging spells from `CIV4SpellInfos.xml` and `CvSpellInterface.py`, distinguishing per-target damage type, source damage caps and caster spell-damage modifiers.
4. Port promotion-driven combat infection/poison and post-combat effects, including target survival and target's Poison resistance.
5. Port hazardous-plot and feature damage through a distinct environmental dispatcher, preserving movement/turn trigger semantics.
6. Confirm Android engine compilation and run static regressions. In-game verification is deliberately postponed until health is substantially complete.

No fidelity percentage was increased for this partial integration.

## 2026-10-27 live city context checkpoint

The typed damage adapter now calls `EmmCityDefense.defenseModifier` when a
unit stands in its owner's city center. Its `occupied` input is the live
`City.isInResistance()` state. The current built-defense input is
`City.getStrength().toInt()`, which is an **Unciv city-strength value** and
not a proven equivalent of EMM's `CvCity::getBuildingDefense()`.

Thus this wiring eliminates the unconditional zero-city-defense placeholder
for many city garrisons, but it is **not** a faithful full city-defense port.
EMM's natural culture-level defense, civilization modifiers, range defense,
bombardment damage, and building-defense XML data have not yet been mapped
into actual city state. These remain mandatory before source-parity claims.

All live state integration is guarded by tile city-center and city owner,
and occupation yields zero via the source formula.

## 2026-10-27 — Remove invalid Unciv city-strength proxy

The earlier direct-damage adapter used `city.getStrength().toInt()` as EMM
`CvCity::getBuildingDefense()`. These values are conceptually different.
That proxy has been removed. `City` now persists six independent fields:
`emmBuildingDefense`, `emmNaturalDefense`, `emmOwnerDefense`,
`emmRangedDefense`, `emmDefenseDamage`, and `emmMaxDefenseDamage`.
They survive city cloning and feed `EmmCityDefense.defenseModifier`.

All defense components currently initialize to zero (except maximum damage
100) until the source-specific building/culture/owner/range/bombardment
systems update them. Consequently, this change corrects model boundaries
and save state but **does not yet yield full EMM city defense in play**.
