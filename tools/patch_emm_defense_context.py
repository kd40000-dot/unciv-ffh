#!/usr/bin/env python3
"""Replace Unciv-strength approximation with original EMM unit defense and typed components.
Run after patch_emm_typed_damage.py.
"""
from pathlib import Path
import json
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
target=root/"core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
s=target.read_text()
if "emmSourceBaseDefense" in s:
    print("EMM defense mapping already present")
    sys.exit(0)
defense=json.loads(Path("docs/data/emm-unit-defense.json").read_text())
combat=json.loads(Path("docs/data/emm-typed-combat-strength.json").read_text())
assert defense["sourceCommit"]==combat["sourceCommit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
def fmt_int_map(d):
    return ",\n".join(f'        "{k}" to {v}' for k,v in sorted(d.items()))
def fmt_type_map(d):
    return ",\n".join('        "%s" to mapOf(%s)' % (k, ", ".join('"%s" to %d' % (t,v) for t,v in sorted(a.items()))) for k,a in sorted(d.items()))
defs='''    // Original EMM Civ4 XML defense/typed combat values.
    private val emmSourceBaseDefense = mapOf(
%s
    )
    private val emmSourceUnitCombat = mapOf(
%s
    )
    private val emmSourcePromotionCombat = mapOf(
%s
    )
    private fun emmUnitKey(name: String): String =
        "UNIT_" + name.uppercase().replace(" ", "_").replace("-", "_")

    /**
     * EMM CvUnit::maxCombatStr: typed offensive components are reduced
     * by the opponent's resistance to each damage type.
     * The base component is unaffected by typed resistance.
     */
    @yairm210.purity.annotations.Readonly
    fun resistedCombatStrength(
        ordinaryStrength: Int,
        typedComponents: Map<String, Int>,
        targetPromotions: Set<String>
    ): Int {
        var scaled = ordinaryStrength * 100
        for ((type, component) in typedComponents) {
            val resist = resistance(targetPromotions, type)
            scaled -= component * resist
        }
        return (scaled / 100).coerceAtLeast(0)
    }

    @yairm210.purity.annotations.Readonly
    fun unitTypedComponents(unit: MapUnit): Map<String, Int> {
        val output = mutableMapOf<String, Int>()
        fun include(parts: Map<String, Int>) {
            for ((type, value) in parts) output[type] = (output[type] ?: 0) + value
        }
        include(emmSourceUnitCombat[emmUnitKey(unit.baseUnit.name)].orEmpty())
        for (held in unit.promotions.promotions) {
            val key = "PROMOTION_" + held.uppercase().replace(" ", "_").replace("-", "_")
            include(emmSourcePromotionCombat[key].orEmpty())
        }
        return output
    }

    private fun sourceDefense(unit: MapUnit): Int {
        val key = emmUnitKey(unit.baseUnit.name)
        val base = emmSourceBaseDefense[key] ?: unit.baseUnit.strength
        // CivUnit::baseCombatStrDefense includes all typed combat components.
        val sourceTypes = emmSourceUnitCombat[key].orEmpty().values.sum()
        val promotionTypes = unit.promotions.promotions.sumOf { held ->
            val key = "PROMOTION_" + held.uppercase().replace(" ", "_").replace("-", "_")
            emmSourcePromotionCombat[key].orEmpty().values.sum()
        }
        return (base + sourceTypes + promotionTypes).coerceAtLeast(0)
    }

''' % (fmt_int_map(defense["unitBaseDefense"]),fmt_type_map(combat["unitCombat"]),fmt_type_map(combat["promotionCombat"]))
anchor="    fun applyToUnit(\n"
assert s.count(anchor)==1
s=s.replace(anchor,defs+anchor)
s=s.replace("val effectiveBaseDefense = unit.baseUnit.strength.coerceAtLeast(0)","val effectiveBaseDefense = sourceDefense(unit)")
target.write_text(s)
print("Installed source EMM defensive base values and typed combat contributions")
