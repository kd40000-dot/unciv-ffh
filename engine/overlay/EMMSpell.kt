package com.unciv.models.ruleset

/**
 * Ruleset-defined EMM spell. All fields have defaults for LibGDX JSON loading.
 *
 * Target: SELF | FRIENDLY | ENEMY
 * Effect: STATUS | DAMAGE | DAMAGE_STATUS | HEAL | SUMMON
 *
 * EMMSpell definitions live in the mod's jsons/EMMSpells.json rather than
 * requiring a new Kotlin branch for every FfH2 sphere spell.
 */
class EMMSpell {
    var name: String = ""
    var sourceId: String = ""
    var target: String = "SELF"
    var effect: String = "STATUS"
    var radius: Int = 0
    var status: String = ""
    var removeStatus: String = ""
    /** Status names explicitly eligible for multi-status removal. */
    var removeStatuses = ArrayList<String>()
    var duration: Int = 2
    var amount: Int = 0
    /** EMM damageLimit: maximum accumulated damage, measured from full health. */
    var damageLimit: Int = 100
    /** Civ IV damage category: COLD, DEATH, FIRE, HOLY, LIGHTNING, POISON, UNHOLY. */
    var damageType: String = ""
    var summonUnit: String = ""
    /** 0 means a permanent EMM unit, positive values expire automatically. */
    var summonDuration: Int = 0
    var livingOnly: Boolean = false
    /** Repair and similar spells accept a union of these unit types and name categories. */
    var eligibleUnitTypes = ArrayList<String>()
    var eligibleNameContains = ArrayList<String>()
    /** EMM bImmobileUnitCreate: summoned unit cannot move in its creation turn. */
    var immobileOnCreate: Boolean = false
    /** 0 is unlimited; otherwise prevents one caster maintaining excess summons. */
    var maxActivePerCaster: Int = 0
    var militaryOnly: Boolean = false
    var landOnly: Boolean = false
    var maxCastsPerTurn: Int = 1
}
