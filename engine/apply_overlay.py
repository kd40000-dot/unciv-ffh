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
    # Independent Android application ID: keep upstream Unciv installed alongside the EMM test client.
    # Namespace is deliberately unchanged; Android manifest activities have fully-qualified class names.
    replace_once(root, "android/build.gradle.kts",
        '        applicationId = BuildConfig.identifier',
        '        applicationId = "com.unciv.emm"')
    destination = root / base / "logic/map/mapunit/actions/EmmSpellEngine.kt"
    if destination.exists():
        raise RuntimeError("EmmSpellEngine.kt already exists; overlay should not be applied twice")
    shutil.copy2(HERE/"overlay"/"EmmSpellEngine.kt", destination)
    print("EMM overlay applied: Haste, persisted 1-cast budget, unique/action/UI integration.")
    print("Source pin:", UPSTREAM)

if __name__ == "__main__":
    main()
