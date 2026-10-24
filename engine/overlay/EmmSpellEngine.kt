package com.unciv.logic.map.mapunit.actions

import com.unciv.logic.map.mapunit.MapUnit
import com.unciv.models.ruleset.EMMSpell
import com.unciv.models.ruleset.unique.UniqueType
import kotlin.math.min
import kotlin.math.max

/**
 * EMM spell executor shared by ruleset-defined spells.
 *
 * The caster's action advertises a spell via the native "Can cast EMM spell [name]"
 * unique. The actual effect and selection rules are loaded from EMMSpells.json.
 *
 * NOTE: Civ IV stacks cannot map exactly to Unciv one-military-unit hexes. For
 * stack-targeting spells, radius 1 selects friendlies in the caster's hex and
 * the immediately adjacent hexes. This is an explicit gameplay adaptation.
 */
object EmmSpellEngine {
    private val landMilitaryTypes = setOf("Sword", "Archery", "Scout", "Mounted", "Magic")
    private val notLivingNames = listOf(
        "Golem", "Elemental", "Skeleton", "Spectre", "Wraith", "Lich",
        "Pyre Zombie", "Djinn", "Mistform"
    )

    private fun definition(caster: MapUnit, name: String): EMMSpell? =
        caster.civ.gameInfo.ruleset.emmSpells[name]

    private fun isLiving(unit: MapUnit): Boolean =
        "Undead" !in unit.promotions.promotions &&
        "Construct" !in unit.promotions.promotions &&
        notLivingNames.none { unit.baseUnit.name.contains(it, ignoreCase = true) }

    private fun matchesTarget(caster: MapUnit, other: MapUnit, spell: EMMSpell): Boolean {
        if (other.isDestroyed) return false
        when (spell.target) {
            "SELF" -> if (other !== caster) return false
            "FRIENDLY" -> if (other.civ != caster.civ) return false
            "ENEMY" -> if (!caster.civ.isAtWarWith(other.civ)) return false
            else -> return false
        }
        if (spell.eligibleUnitTypes.isNotEmpty() || spell.eligibleNameContains.isNotEmpty()) {
            val typeMatch = other.baseUnit.unitType in spell.eligibleUnitTypes
            val nameMatch = spell.eligibleNameContains.any {
                other.baseUnit.name.contains(it, ignoreCase = true)
            }
            if (!typeMatch && !nameMatch) return false
        }
        if (spell.militaryOnly && !other.isMilitary()) return false
        if (spell.landOnly && (other.baseUnit.unitType !in landMilitaryTypes || other.isEmbarked())) return false
        if (spell.livingOnly && !isLiving(other)) return false
        return true
    }

    private fun targets(caster: MapUnit, spell: EMMSpell): List<MapUnit> {
        if (spell.target == "SELF") return listOf(caster).filter { matchesTarget(caster, it, spell) }
        return caster.getTile().getTilesInDistance(spell.radius)
            .flatMap { it.getUnits() }
            .filter { matchesTarget(caster, it, spell) }
            .distinctBy { it.id }
            .toList()
    }

    private fun damageAllowed(target: MapUnit, spell: EMMSpell): Int {
        // FfH2 iDamageLimit caps TOTAL accrued damage, not damage dealt per cast.
        val remainingAllowed = spell.damageLimit - (100 - target.health)
        return max(0, min(spell.amount, remainingAllowed))
    }

    private fun wouldChange(target: MapUnit, spell: EMMSpell): Boolean =
        when (spell.effect) {
            "STATUS" -> (!target.hasStatus(spell.status) ||
                (spell.removeStatus.isNotEmpty() && target.hasStatus(spell.removeStatus)))
            "DAMAGE" -> damageAllowed(target, spell) > 0
            "HEAL" -> target.health < 100 && spell.amount > 0
            else -> false
        }

    /** Rechecked at execution time: an available UI action may become stale. */
    fun canCast(caster: MapUnit, name: String): Boolean {
        if (caster.isDestroyed || !caster.hasMovement()) return false
        val spell = definition(caster, name) ?: return false
        if (spell.name.isBlank() || spell.sourceId.isBlank()) return false
        if (caster.emmSpellsCastThisTurn >= spell.maxCastsPerTurn) return false
        // Do not allow direct calls to bypass the real learned promotion/unique.
        if (caster.getMatchingUniques(UniqueType.EmmSpell).none { it.params[0] == name }) return false
        return when (spell.effect) {
            "SUMMON" -> spell.summonUnit.isNotEmpty() &&
                caster.civ.gameInfo.ruleset.units.containsKey(spell.summonUnit) &&
                (spell.maxActivePerCaster <= 0 ||
                 caster.civ.units.getCivUnits().count {
                     it.name == spell.summonUnit && it.emmSummonerId == caster.id
                 } < spell.maxActivePerCaster)
            "STATUS", "DAMAGE", "HEAL" -> targets(caster, spell).any { wouldChange(it, spell) }
            else -> false
        }
    }

    /**
     * Cast once, applying independent effects per target and consuming movement
     * only after a real state change. Old vanilla self-cast proxy actions are
     * removed from the corresponding promotions in the EMM engine ruleset.
     */
    fun cast(caster: MapUnit, name: String) {
        if (!canCast(caster, name)) return
        val spell = definition(caster, name) ?: return
        var applied = false
        if (spell.effect == "SUMMON") {
            val summoned = caster.civ.units.placeUnitNearTile(caster.getTile().position, spell.summonUnit)
            if (summoned != null) {
                summoned.emmSummonerId = caster.id
                summoned.emmSummonTurnsLeft = spell.summonDuration
                if (spell.immobileOnCreate) summoned.currentMovement = 0f
                applied = true
            }
        } else {
            // Snapshot targets before effects: kills can remove units from tiles.
            for (target in targets(caster, spell)) {
                if (!wouldChange(target, spell)) continue
                when (spell.effect) {
                    "STATUS" -> {
                        if (spell.removeStatus.isNotEmpty()) target.removeStatus(spell.removeStatus)
                        target.setStatus(spell.status, spell.duration)
                    }
                    "DAMAGE" -> target.takeDamage(damageAllowed(target, spell))
                    "HEAL" -> target.healBy(spell.amount)
                }
                applied = true
            }
        }
        if (!applied) return
        caster.emmSpellsCastThisTurn++
        caster.useMovementPoints(caster.currentMovement)
    }
}
