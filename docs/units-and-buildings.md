# Units and buildings — source-derived first conversion

EMM Continued source commit: [`60b0ec3740083162aaab7bf8491761a54a65a610`](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610).

## Coverage

| Category | Count |
| --- | ---: |
| Units inventoried | 356 |
| Building types inventoried | 189 |
| Units implemented in this slice | 47 |
| Buildings implemented, including the temporary shared Palace | 40 |
| Four-faction unique-unit replacements implemented | 14 |
| Buildings specific to the four factions implemented | 2 |

The [source inventory](data/emm-unit-building-catalog.json) contains the original IDs, costs, combat/defense strength, movement, tech requirements, class identities, resource/religion/civic restrictions, selected building yields and source class limits.

## Porting policy and fidelity

**Directly sourced:** original unit production costs, attack/defense base stats, movement points, building costs and tech prerequisites; actual unit classes and four-faction replacements; building yields where compatible.

**Unciv adaptations:** source `iCombat` becomes unit strength, with `iCombatDefense` represented using an integer-percent conditional defense bonus (rounding where needed). Civ IV archers are **not given a fabricated ranged attack**. Building `iDefense` is approximately divided by five to produce Unciv city strength; original raw values remain in the inventory. Commerce/yield modifiers use Unciv's native `percentStatBonus` property, and granary carryover uses its supported unique. Civ IV health, mana affinities, some building and resource gates, AI roles, collateral damage, summon duration, experience requirements, and spellcasting are not yet represented.

Units with required building classes use **Can only be built in cities with [Building]** where the prerequisite building is included. Source-defined national unit class caps use Unciv's per-civilization limit unique.

**Deferred:** unbuildable/summoned units, heroes, spell effects, religions, mana-dependent units, civic-dependent units, and world/national wonder systems. Unaffiliated but faction-gated content is not exposed globally.

**Temporary omissions:** Unit upgrading and obsolescence, city training conditions absent from Unciv, nation-specific palace powers, race-based promotion logic, and full economic effects. This conversion is not a complete FfH2 experience.

### Corrected early definitions

| Entry | Previous prototype | EMM-source-derived |
| --- | --- | --- |
| Warrior | Cost 40, movement 2, strength 6 | Cost 25, movement 1, strength 3 |
| Worker | Cost 70 | Cost 75 |
| Settler | Cost 110 | Cost 120 |
| Archer | Cost 65 | Cost 45 (Archery plus Archery Range prerequisite) |
| Adept | Cost 85, artificial ranged attack | Cost 90, melee strength 3, requires Mage Guild |
| Training Yard | Technology Crafting, cost 70 | Bronze Working, cost 100 |
| Elder Council | Ancient Chants, cost 65 | Mysticism, cost 60 |
| Warrens | Crafting, cost 80, arbitrary +2 Production | Masonry, cost 180; its unit-duplication ability still requires implementation |

Invented faction units/buildings from the previous slice have been removed; source-authentic replacements are used instead.

### Shared source unit aliases

The source assigns `UNIT_SWORDSMAN` to both the Amurites and Ljosalfar. Unciv's `uniqueTo` property accepts one civilization, so additional names are assigned to avoid collision:

- **Ljosalfar Swordsman** → original `UNIT_SWORDSMAN` for Ljosalfar

These aliases reference the same EMM source statistics.

## Source-defined disabled unit/building classes

The normal units or buildings listed below are explicitly prohibited for the stated factions, using Unciv's `Only available <for [non-[...]] Civilizations>` filter:

- Clan of Embers: Horse Archer (unit)
- Clan of Embers: Knight (unit)
- Clan of Embers: Alchemy Lab (building)
- Clan of Embers: Library (building)
- Clan of Embers: Mage Guild (building)
- Clan of Embers: Stable (building)
- Ljosalfar: Chariot (unit)
- Ljosalfar: Catapult (unit)
- Ljosalfar: Berserker (unit)
- Ljosalfar: Siege Workshop (building)

## Next implementation work

1. Complete the four civilizations' special traits and palace bonuses (the supported explicit `NONE` unit/building class prohibitions are now implemented).
2. Port supported promotions, upgrade chains and actual resource requirements.
3. Add religions, mana, spells, heroes and specialized construction conditions.
4. Address differences between Civ IV's health, happiness, city defense and Unciv's rules.

The CI workflow checks source-derived values and runs Unciv's official `mod-ci` validation. Full Android gameplay testing has not been performed.
