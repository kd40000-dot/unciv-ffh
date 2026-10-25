#!/usr/bin/env python3
"""Apply the initial EMM native spell overlay to a PINNED checkout of upstream Unciv.

This is deliberately a fail-closed patcher: if upstream changes move an anchor we refuse
to generate a partially-patched APK. Run 'python3 engine/apply_overlay.py /path/to/Unciv'.
"""
import argparse
import pathlib
import shutil

UPSTREAM = "b5c4bccd2b038f49183338811dc30efec81cb105"
HERE = pathlib.Path(__file__).resolve().parent

def replace_once(root, filename, before, after):
    path = root / filename
    original = path.read_text(encoding="utf-8")
    if original.count(before) != 1:
        raise RuntimeError(f"{filename}: expected exactly one anchor, found {original.count(before)}: {before[:90]!r}")
    path.write_text(original.replace(before, after, 1), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("unciv", type=pathlib.Path)
    args = parser.parse_args()
    root = args.unciv.resolve()
    if not (root / "core" / "build.gradle.kts").exists():
        parser.error("path must be an Unciv source checkout root")
    # Preserve a reproducible pin, including for local builds outside Actions.
    import subprocess
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    if sha != UPSTREAM:
        parser.error(f"expected pinned Unciv {UPSTREAM}, got {sha}. Explicitly rebase the overlay to change the pin.")

    base = "core/src/com/unciv/"
    replace_once(root, base+"models/ruleset/unique/UniqueType.kt",
        '    CanTransform("Can transform to [unit]", UniqueTarget.UnitAction,',
        '    EmmSpell("Can cast EMM spell [comment]", UniqueTarget.UnitAction),\n    CanTransform("Can transform to [unit]", UniqueTarget.UnitAction,')
    replace_once(root, base+"models/UnitAction.kt",
        '    Transform("Transform"),',
        '    EmmSpell("Cast EMM spell"),\n    Transform("Transform"),')
    replace_once(root, base+"ui/screens/worldscreen/unit/actions/UiUnitAction.kt",
        '    Transform(UnitActionType.Transform, portrait("Transform"), uncivSound = UncivSound.Upgrade, useFrequency = 70f),',
        '    EmmSpell(UnitActionType.EmmSpell, portrait("Promote"), useFrequency = 78f),\n    Transform(UnitActionType.Transform, portrait("Transform"), uncivSound = UncivSound.Upgrade, useFrequency = 70f),')
    replace_once(root, base+"logic/map/mapunit/actions/UnitActions.kt",
        '        UnitActionType.Transform to UnitActionsFromUniques::getTransformActions,',
        '        UnitActionType.EmmSpell to UnitActionsFromUniques::getEmmSpellActions,\n        UnitActionType.Transform to UnitActionsFromUniques::getTransformActions,')
    replace_once(root, base+"logic/map/mapunit/actions/UnitActionsFromUniques.kt",
        'object UnitActionsFromUniques {',
        '''object UnitActionsFromUniques {

    /** Only registered EMM engine spells are executable; unsupported names return disabled buttons. */
    internal fun getEmmSpellActions(unit: MapUnit, tile: Tile): Sequence<UnitAction> =
        unit.getMatchingUniques(UniqueType.EmmSpell).map { unique ->
            val spell = unique.params[0]
            UnitAction(
                UnitActionType.EmmSpell,
                title = "Cast [$spell]",
                associatedUnique = unique,
                action = { EmmSpellEngine.cast(unit, spell) }
                    .takeIf { EmmSpellEngine.canCast(unit, spell) }
            )
        }
''')
    replace_once(root, base+"logic/map/mapunit/MapUnit.kt",
        '    var attacksThisTurn = 0\n    var promotions = UnitPromotions()',
        '''    var attacksThisTurn = 0
    /** Persisted EMM spell budget; reset only at unit start-of-turn. */
    var emmSpellsCastThisTurn = 0
    var promotions = UnitPromotions()''')
    replace_once(root, base+"logic/map/mapunit/UnitTurnManager.kt",
        '        unit.attacksThisTurn = 0\n        unit.due = true',
        '        unit.attacksThisTurn = 0\n        unit.emmSpellsCastThisTurn = 0\n        unit.due = true')

    # Engine ruleset extension: load the mod's EMMSpells.json with ordinary
    # Unciv ruleset merge semantics, including base rulesets and combined mods.
    replace_once(root, base+"models/ruleset/Ruleset.kt",
        '    val unitPromotions = LinkedHashMap<String, Promotion>()',
        '    val unitPromotions = LinkedHashMap<String, Promotion>()\n    val emmSpells = LinkedHashMap<String, EMMSpell>()')
    replace_once(root, base+"models/ruleset/Ruleset.kt",
        '        unitPromotions.putAll(ruleset.unitPromotions)',
        '        unitPromotions.putAll(ruleset.unitPromotions)\n        emmSpells.putAll(ruleset.emmSpells)')
    replace_once(root, base+"models/ruleset/Ruleset.kt",
        '        if (promotionsFile.exists()) unitPromotions += createHashmap(json().fromJsonFile(Array<Promotion>::class.java, promotionsFile))',
        '''        if (promotionsFile.exists()) unitPromotions += createHashmap(json().fromJsonFile(Array<Promotion>::class.java, promotionsFile))

        val emmSpellsFile = folderHandle.child("EMMSpells.json")
        if (emmSpellsFile.exists())
            for (spell in json().fromJsonFile(Array<EMMSpell>::class.java, emmSpellsFile))
                emmSpells[spell.name] = spell''')

    # Summoned-unit expiration and links live on each unit and survive save/load.
    replace_once(root, base+"logic/map/mapunit/MapUnit.kt",
        '    var emmSpellsCastThisTurn = 0',
        '''    var emmSpellsCastThisTurn = 0
    /** 0 = ordinary/permanent unit; positive counts down at owner's start turn. */
    var emmSummonTurnsLeft = 0
    /** Persistent summoner ID (used by later caster-death and summon-limit rules). */
    var emmSummonerId = -1''')
    replace_once(root, base+"logic/map/mapunit/MapUnit.kt",
        '        toReturn.abilityToTimesUsed = HashMap(abilityToTimesUsed)',
        '''        toReturn.abilityToTimesUsed = HashMap(abilityToTimesUsed)
        toReturn.emmSpellsCastThisTurn = emmSpellsCastThisTurn
        toReturn.emmSummonTurnsLeft = emmSummonTurnsLeft
        toReturn.emmSummonerId = emmSummonerId''')
    replace_once(root, base+"logic/map/mapunit/UnitTurnManager.kt",
        '    fun startTurn():Unit = timeThis("UnitTurnManager.startTurn") {\n        unit.movement.clearPathfindingCache()',
        '''    fun startTurn():Unit = timeThis("UnitTurnManager.startTurn") {
        if (unit.emmSummonTurnsLeft > 0) {
            unit.emmSummonTurnsLeft--
            if (unit.emmSummonTurnsLeft == 0) {
                unit.destroy()
                return@timeThis
            }
        }
        unit.movement.clearPathfindingCache()''')

    # Save event cooldowns on the city, rather than using transient UI state.
    replace_once(root, base+"logic/city/City.kt",
        '    var turnAcquired = 0',
        '''    var turnAcquired = 0
    /** EMM event cooldown, keyed by event name. Persisted across saves. */
    var emmEventLastTurn = HashMap<String, Int>()''')
    # Source-inspired FfH/EMM war weariness. The original tracks a score
    # per opposing team and applies per-city percentage reductions.
    replace_once(root, base+"logic/civilization/Civilization.kt",
        '    var civID = ""\\n\\n    var tech = TechManager()',
        '''    var civID = ""
    /** Scaled by 100, keyed by enemy civilization ID, saved with the game. */
    var emmWarWearinessByEnemy = HashMap<String, Int>()

    var tech = TechManager()''')
    replace_once(root, base+"logic/battle/Battle.kt",
        '        val damageDealt = takeDamage(attacker, defender) + extraRangedAttackDamage',
        '''        val damageDealt = takeDamage(attacker, defender) + extraRangedAttackDamage
        // Civ IV war weariness is gained by casualties, not elapsed war turns.
        // Unciv has no culture-weighted plot-ownership shares; ownership is
        // a provisional binary proxy for that original calculation.
        if (attacker is MapUnitCombatant && defender is MapUnitCombatant &&
            !attacker.getCivInfo().isBarbarian && !defender.getCivInfo().isBarbarian &&
            attacker.unit.emmSummonTurnsLeft == 0 && defender.unit.emmSummonTurnsLeft == 0 &&
            attacker.getCivInfo().isAtWarWith(defender.getCivInfo())) {
            val attackingCiv = attacker.getCivInfo()
            val defendingCiv = defender.getCivInfo()
            val plotOwner = attackedTile.getOwner()
            if (attacker.isDefeated() && !defender.isDefeated()) {
                if (plotOwner != attackingCiv)
                    attackingCiv.emmWarWearinessByEnemy[defendingCiv.civID] =
                        (attackingCiv.emmWarWearinessByEnemy[defendingCiv.civID] ?: 0) + 300
                if (plotOwner != defendingCiv)
                    defendingCiv.emmWarWearinessByEnemy[attackingCiv.civID] =
                        (defendingCiv.emmWarWearinessByEnemy[attackingCiv.civID] ?: 0) + 100
            } else if (defender.isDefeated() && !attacker.isDefeated()) {
                if (plotOwner != defendingCiv)
                    defendingCiv.emmWarWearinessByEnemy[attackingCiv.civID] =
                        (defendingCiv.emmWarWearinessByEnemy[attackingCiv.civID] ?: 0) + 200
                if (plotOwner != attackingCiv)
                    attackingCiv.emmWarWearinessByEnemy[defendingCiv.civID] =
                        (attackingCiv.emmWarWearinessByEnemy[defendingCiv.civID] ?: 0) + 200
            }
        }''')
    replace_once(root, base+"logic/civilization/managers/TurnManager.kt",
        '        for (city in civInfo.cities) city.hasSoldBuildingThisTurn = false',
        '''        // Original Civ IV: flat -1 WW point per turn and 99% in peace.
        // Scores are stored in hundredths of a point for territory weighting.
        for ((enemyId, score) in civInfo.emmWarWearinessByEnemy.toMap()) {
            val enemy = civInfo.gameInfo.civilizations.firstOrNull { it.civID == enemyId }
            val afterDecay = (score - 100).coerceAtLeast(0)
            civInfo.emmWarWearinessByEnemy[enemyId] =
                if (enemy != null && civInfo.isAtWarWith(enemy))
                    afterDecay
                else (afterDecay * 99) / 100
        }

        for (city in civInfo.cities) {
            city.hasSoldBuildingThisTurn = false
            val crime = city.cityStats.emmCrimeModifier
            val turn = civInfo.gameInfo.turns
            // Temporary source-mapped prototype: Dungeon supplies a persistent
            // negative crime modifier, reducing incident risk. Incidents do not
            // overwrite city buildings or launch without a legitimate city.
            val incidentChance = (5 + crime).coerceIn(0, 30)
            val last = city.emmEventLastTurn["Crime Incident"] ?: -1000
            if (city.population.population >= 3 && turn - last >= 15 &&
                kotlin.random.Random.nextInt(100) < incidentChance) {
                city.emmEventLastTurn["Crime Incident"] = turn
                // Automatic consequence while interactive Civ IV event choices
                // are not ported: the city pays an upkeep loss.
                civInfo.addGold(-10)
            }
        }''')
    replace_once(root, base+"logic/city/CityStats.kt",
        "        // we don\u0027t want to modify the existing happiness list because that leads",
        '''        // EMM city-specific war weariness. The Dungeon provides a -25%
        // local multiplier on the unrest generated by combat losses.
        val activeWeariness = civInfo.emmWarWearinessByEnemy
            .filter { (enemyId, _) ->
                val enemy = civInfo.gameInfo.civilizations.firstOrNull { it.civID == enemyId }
                enemy != null && civInfo.isAtWarWith(enemy)
            }.values.sum()
        val warUnhappiness = city.population.population.toFloat() *
            (activeWeariness / 100f) / 200f * emmWarWearinessMultiplier
        if (warUnhappiness > 0f)
            newHappinessList["EMM War Weariness"] = -warUnhappiness

        // we don't want to modify the existing happiness list because that leads''')

    # EMM city health is distinct from unconditional food yields. Store
    # building modifiers as data and apply net unhealth to food consumption.
    replace_once(root, base+"models/ruleset/Building.kt",
        '    var maintenance = 0',
        '''    var maintenance = 0
    /** EMM health modifier; interpreted by CityStats, not as direct food. */
    var emmHealth = 0
    /** +1 health for each available resource in this list. */
    var emmHealthResourceBonuses = ArrayList<String>()
    /** Additional percentage of unit healing while inside the city. */
    var emmCityHealingPercent = 0
    /** EMM crime-rate modifier; pending crime-event integration. */
    var emmCrime = 0
    /** EMM war-weariness modifier; pending war weariness integration. */
    var emmWarWearinessPercent = 0''')
    replace_once(root, base+"logic/city/CityStats.kt",
        'class CityStats(val city: City) {',
        '''class CityStats(val city: City) {
    /** EMM building-driven crime modifier. Event gating remains pending. */
    val emmCrimeModifier: Int
        get() = city.cityConstructions.builtBuildings.sumOf { name ->
            city.civ.gameInfo.ruleset.buildings[name]?.emmCrime ?: 0
        }

    /** Local multiplicative war-weariness modifier. Currently calculated,
     * but will only have an effect when EMM weariness is ported. */
    val emmWarWearinessMultiplier: Float
        get() = (100 + city.cityConstructions.builtBuildings.sumOf { name ->
            city.civ.gameInfo.ruleset.buildings[name]?.emmWarWearinessPercent ?: 0
        }).coerceAtLeast(0) / 100f
''')
    replace_once(root, base+"logic/city/CityStats.kt",
        '        return foodEaten\\n    }',
        '''        // EMM health prototype: population creates unhealth; public
        // sanitation buildings counter it. Do not add their health directly
        // to city food yield. Natural health/resource components are still
        // pending source-accurate EMM porting.
        val buildingHealth = city.cityConstructions.builtBuildings.sumOf { buildingName ->
            val building = city.civ.gameInfo.ruleset.buildings[buildingName]
            (building?.emmHealth ?: 0) +
                (building?.emmHealthResourceBonuses?.count { resource ->
                    city.civ.getResourceAmount(resource) > 0
                } ?: 0)
        }
        val populationUnhealth = (city.population.population - 5).coerceAtLeast(0)
        foodEaten += (populationUnhealth - buildingHealth).coerceAtLeast(0)
        return foodEaten
    }''')

    # Building-based EMM healing works for troops in the city center.
    # Terrain damage must continue to apply after the healing bonus.
    replace_once(root, base+"logic/map/mapunit/MapUnit.kt",
        '        if (noTerrainDamage) return healing\\n        healing -= getDamageFromTerrain(tile)',
        '''        if (tile.isCityCenter()) {
            val healingCity = tile.getCity()
            if (healingCity != null && isAlly(healingCity.civ)) {
                val healingPercent = healingCity.cityConstructions.builtBuildings.sumOf { name ->
                    healingCity.civ.gameInfo.ruleset.buildings[name]?.emmCityHealingPercent ?: 0
                }
                healing = healing * (100 + healingPercent) / 100
            }
        }
        if (noTerrainDamage) return healing
        healing -= getDamageFromTerrain(tile)''')

    # Courage boosts natural per-turn healing of the actual recipient,
    # not the original temporary caster's entire adjacent healing aura.
    replace_once(root, base+"logic/map/mapunit/MapUnit.kt",
        '        else -> healingAmountForTile(getTile(), noTerrainDamage = true)',
        '''        else -> healingAmountForTile(getTile(), noTerrainDamage = true).let { amount ->
            when {
                amount <= 0 -> 0
                hasStatus("Withered (Spell)") -> (amount - 20).coerceAtLeast(0)
                hasStatus("Courage (Spell)") -> amount + 10
                else -> amount
            }
        }''')

    # EMM uses permanent/condition-removable promotions for several spells.
    # Negative UnitStatus.turnsLeft is a persistent status, not an expired one.
    replace_once(root, base+"logic/map/mapunit/UnitTurnManager.kt",
        '''        for (status in unit.statusMap.values.toList()){
            status.turnsLeft--
            if (status.turnsLeft <= 0) unit.removeStatus(status.name)
        }''',
        '''        for (status in unit.statusMap.values.toList()){
            if (status.turnsLeft < 0) continue // EMM: until dispelled / specific removal event.
            status.turnsLeft--
            if (status.turnsLeft <= 0) unit.removeStatus(status.name)
        }''')

    # EMM regeneration has bRemovedWhenHealed=1: it persists until completely healed.
    replace_once(root, base+"logic/map/mapunit/MapUnit.kt",
        '''        if (health > 100) health = 100
        cache.updateUniques()
    }

    fun takeDamage(amount: Int) {''',
        '''        if (health > 100) health = 100
        if (health >= 100 && hasStatus("Regeneration (Spell)"))
            removeStatus("Regeneration (Spell)")
        cache.updateUniques()
    }

    fun takeDamage(amount: Int) {''')
    # Source Stoneskin bRemovedByCombat; taking combat damage is a subset
    # of combat events. We explicitly document this remaining discrepancy.
    replace_once(root, base+"logic/map/mapunit/MapUnit.kt",
        '''    fun takeDamage(amount: Int) {
        health -= amount''',
        '''    fun takeDamage(amount: Int) {
        if (amount > 0 && hasStatus("Stoneskin (Spell)"))
            removeStatus("Stoneskin (Spell)")
        health -= amount''')

    spellModel = root / base / "models/ruleset/EMMSpell.kt"
    if spellModel.exists():
        raise RuntimeError("EMMSpell.kt already exists; overlay should not be applied twice")
    shutil.copy2(HERE/"overlay"/"EMMSpell.kt", spellModel)

    # Public SDK channel on CI currently exposes API 36; upstream has compileSdk 37.
    # Use API 36 for this prototype and remove this compatibility shim when API 37 is available.
    replace_once(root, "android/build.gradle.kts",
        '    compileSdk = 37',
        '    compileSdk = 36')
    # Independent Android application ID: keep upstream Unciv installed alongside the EMM test client.
    # Namespace is deliberately unchanged; Android manifest activities have fully-qualified class names.
    replace_once(root, "android/build.gradle.kts",
        '        applicationId = BuildConfig.identifier',
        '        applicationId = "com.unciv.emm"')
    destination = root / base / "logic/map/mapunit/actions/EmmSpellEngine.kt"
    if destination.exists():
        raise RuntimeError("EmmSpellEngine.kt already exists; overlay should not be applied twice")
    shutil.copy2(HERE/"overlay"/"EmmSpellEngine.kt", destination)
    print("EMM overlay applied: data-driven EMM spell executor, statuses, direct damage, summoned lifetimes.")
    print("Source pin:", UPSTREAM)

if __name__ == "__main__":
    main()
