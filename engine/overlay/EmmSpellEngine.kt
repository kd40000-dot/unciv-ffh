package com.unciv.logic.map.mapunit.actions

import com.unciv.logic.map.mapunit.MapUnit

/**
 * First EMM-specific spell executor.
 *
 * This class intentionally lives in the engine fork, not the JSON mod: native Unciv uniques
 * cannot apply promotion effects to *other* individual units selected at cast time.
 *
 * SOURCE: bewlay/extramodmod, CIV4SpellInfos.xml SPELL_HASTE, PROMOTION_HASTED.
 * Haste affects living friendly land units in the caster's stack, gives +1 movement,
 * removes Slow, and the promotion expires with 100% chance at its next eligible tick.
 *
 * HEX ADAPTATION: Unciv permits one military unit per tile rather than Civ IV's stacks,
 * so "friendly living stack members" becomes caster + adjacent friendly land units (radius 1).
 *
 * The base game already serializes statusMap and decrements statuses in UnitTurnManager.startTurn.
 * Two stored turns keep the buff through the next friendly turn before expiration.
 */
object EmmSpellEngine {
    private val hasteUnitTypes = setOf("Sword", "Archery", "Scout", "Mounted", "Magic")
    private val notLivingNames = listOf("Golem", "Elemental", "Skeleton", "Spectre", "Wraith", "Lich",
        "Pyre Zombie", "Djinn", "Mistform")

    private fun canReceiveHaste(target: MapUnit, caster: MapUnit): Boolean {
        if (target.isDestroyed || target.civ != caster.civ) return false
        if (!target.isMilitary() || target.isEmbarked()) return false
        if (target.baseUnit.unitType !in hasteUnitTypes) return false
        if ("Undead" in target.promotions.promotions) return false
        if (notLivingNames.any { target.baseUnit.name.contains(it, ignoreCase = true) }) return false
        return true
    }

    private fun hasteTargets(caster: MapUnit): List<MapUnit> {
        val tile = caster.getTile()
        val nearbyTiles = sequenceOf(tile) + tile.neighbors.asSequence()
        return nearbyTiles.flatMap { it.getUnits() }
            .filter { canReceiveHaste(it, caster) }
            .distinctBy { it.id }
            .toList()
    }

    /** All restrictions enforced here, not merely when deciding whether to show a button. */
    fun canCast(caster: MapUnit, spell: String): Boolean {
        if (caster.isDestroyed || !caster.hasMovement() || caster.emmSpellsCastThisTurn >= 1) return false
        return when (spell) {
            "Haste" -> hasteTargets(caster).any { !it.hasStatus("Hasted") || it.hasStatus("Slowed") }
            else -> false // An unsupported spell is deliberately unavailable, not a silent no-op.
        }
    }

    fun cast(caster: MapUnit, spell: String) {
        if (!canCast(caster, spell)) return
        when (spell) {
            "Haste" -> {
                // Source removes PROMOTION_SLOW from eligible units when HASTE is cast.
                // Unciv's corresponding unit state is a status. Does not confuse
                // the old caster-wide "Slow (Spell)" damage proxy with actual Slowed.
                for (target in hasteTargets(caster)) {
                    target.removeStatus("Slowed")
                    target.setStatus("Hasted", 2)
                }
            }
            else -> return
        }
        caster.emmSpellsCastThisTurn++
        caster.useMovementPoints(caster.currentMovement)
    }
}
