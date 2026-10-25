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

    # Courage boosts natural per-turn healing of the actual recipient,
    # not the original temporary caster's entire adjacent healing aura.
    replace_once(root, base+"logic/map/mapunit/MapUnit.kt",
        '        else -> healingAmountForTile(getTile(), noTerrainDamage = true)',
        '''        else -> healingAmountForTile(getTile(), noTerrainDamage = true).let { amount ->
            if (amount > 0 && hasStatus("Courage (Spell)")) amount + 10 else amount
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
