#!/usr/bin/env python3
"""Apply EMM typed combat-strength resistance in regular Unciv battle ratios.

Deliberately preserve Unciv's other battle modifiers until their EMM equivalents
are implemented. Guard by the same Herbalist feature flag as the health engine.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
path=root/"core/src/com/unciv/logic/battle/BattleDamage.kt"
s=path.read_text()
if "private fun emmTypedStrengthMultiplier(" in s:
    print("EMM typed battle strength already installed")
    sys.exit(0)
anchor='''    /**
     * Includes attack modifiers
     */'''
helper='''    /**
     * EMM CvUnit::maxCombatStr reduces each typed combat component according
     * to the opposing unit's resistance. Apply that relative change to the
     * strength already calculated by Unciv to preserve existing non-EMM
     * modifiers until the complete CvUnit combat pipeline is ported.
     * This never applies a separate HP damage roll.
     */
    @yairm210.purity.annotations.Readonly
    private fun emmTypedStrengthMultiplier(own: ICombatant, enemy: ICombatant): Float {
        if (own !is MapUnitCombatant || enemy !is MapUnitCombatant) return 1f
        if (!own.getCivInfo().gameInfo.ruleset.buildings.containsKey("Herbalist")) return 1f
        val components = com.unciv.logic.map.mapunit.EmmTypedDamage.unitTypedComponents(own.unit)
        if (components.isEmpty()) return 1f
        val base = own.unit.baseUnit.strength.coerceAtLeast(1)
        val original = base + components.values.sum()
        if (original <= 0) return 1f
        val typed = com.unciv.logic.map.mapunit.EmmTypedDamage.resistedCombatStrength(
            original, components, enemy.unit.promotions.promotions
        )
        return (typed.toFloat() / original).coerceAtLeast(0f)
    }

'''
assert s.count(anchor)==1
s=s.replace(anchor,helper+anchor)
a='return max(1f, attacker.getAttackingStrength(defender) * attackModifier)'
b='return max(1f, attacker.getAttackingStrength(defender) * attackModifier * emmTypedStrengthMultiplier(attacker, defender))'
assert s.count(a)==1
s=s.replace(a,b)
a='return max(1f, defender.getDefendingStrength(attacker) * defenceModifier)'
b='return max(1f, defender.getDefendingStrength(attacker) * defenceModifier * emmTypedStrengthMultiplier(defender, attacker))'
assert s.count(a)==1
s=s.replace(a,b)
path.write_text(s)
print("Installed EMM typed strengths in both attacking and defending battle ratios")
