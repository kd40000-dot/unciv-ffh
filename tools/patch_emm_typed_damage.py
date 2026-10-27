#!/usr/bin/env python3
"""Install reusable source-derived typed resistance and direct-damage math.

EMM CvUnit.cpp doDamage uses two random rolls, defense, level, city defense,
and promotion resistances. Callers pass defense/level/city stats until their
exact EMM adapters are introduced. No unit gameplay tests are claimed.
"""
from pathlib import Path
import json
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
source=json.loads(Path("docs/data/emm-typed-resistances.json").read_text())
assert source["sourceCommit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
records=source["promotionResistances"]
lines=[]
for name,types in sorted(records.items()):
    label=" ".join(w.capitalize() for w in name.removeprefix("PROMOTION_").split("_"))
    entries=", ".join(f'"{t}" to {v}' for t,v in sorted(types.items()))
    lines.append(f'        "{label}" to mapOf({entries})')
file=root/"core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
file.write_text("""package com.unciv.logic.map.mapunit

import kotlin.random.Random

/**
 * EMM CvUnit::doDamage, no-caster typed direct damage.
 * Resistance contributions are additive before clipping to [-100,100].
 * Engine callers must supply EMM defense strength, level and city defense.
 */
object EmmTypedDamage {
    private val sourcePromotionResistances = mapOf(
%s
    )

    fun resistance(promotions: Set<String>, type: String): Int =
        promotions.sumOf { sourcePromotionResistances[it]?.get(type) ?: 0 }
            .coerceIn(-100, 100)

    /**
     * Apply source-typed direct damage to a real Unciv unit.
     * In EMM, level is XP-derived and defense is baseCombatStrDefense().
     * Current Unciv adapter uses base strength and earned promotion count;
     * city defense remains zero until the full EMM city-defense adapter.
     */
    fun applyToUnit(
        unit: MapUnit,
        type: String,
        initialDamage: Int,
        damageLimit: Int,
        random: Random
    ): Int {
        val amount = rollDamage(
            initialDamage = initialDamage,
            previousDamage = 100 - unit.health,
            damageLimit = damageLimit,
            defenseStrength = unit.baseUnit.strength,
            level = 1 + unit.promotions.numberOfPromotions,
            cityDefense = 0,
            typedResistance = resistance(unit.promotions.promotions, type),
            random = random
        )
        if (amount > 0) unit.takeDamage(amount)
        return amount
    }

    fun rollDamage(
        initialDamage: Int,
        previousDamage: Int,
        damageLimit: Int,
        defenseStrength: Int,
        level: Int,
        cityDefense: Int,
        typedResistance: Int,
        random: Random
    ): Int {
        require(initialDamage > 0)
        val effectiveResist = defenseStrength * 2 + level * 2 +
            cityDefense / 4 + typedResistance.coerceIn(-100, 100)
        if (effectiveResist >= 100) return 0
        val rolled = random.nextInt(initialDamage) + random.nextInt(initialDamage)
        val amount = rolled * (100 - effectiveResist) / 100
        return amount.coerceAtLeast(0).coerceAtMost((damageLimit - previousDamage).coerceAtLeast(0))
    }
}
""" % (",\n".join(lines)))
print(f"Created EMM typed damage/resistance kernel using {len(records)} promotion definitions")
