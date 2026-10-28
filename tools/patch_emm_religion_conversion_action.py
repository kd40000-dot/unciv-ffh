#!/usr/bin/env python3
"""EMM in-game state religion action, reusing prior religion and alignment engine."""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
civ=root/"core/src/com/unciv/logic/civilization/Civilization.kt"
s=civ.read_text()
if "var emmReligionConversionTurn" not in s:
    anchor="    var emmStateReligion: String? = null"
    assert s.count(anchor)==1
    s=s.replace(anchor,anchor+"\n    var emmReligionConversionTurn: Int = 0")
    anchor="        toReturn.emmStateReligion = emmStateReligion"
    assert s.count(anchor)==1
    s=s.replace(anchor,anchor+"\n        toReturn.emmReligionConversionTurn = emmReligionConversionTurn")
    civ.write_text(s)
engine=root/"core/src/com/unciv/logic/civilization/EmmReligions.kt"
s=engine.read_text()
if "fun conversionActions(" not in s:
    anchor="    fun changeAlignment(civ: Civilization, alignment: String): Boolean {"
    assert s.count(anchor)==1
    helper='''    /** One-click state conversion in own religious city. Uses existing EMM city faith state. */
    fun conversionActions(unit: com.unciv.logic.map.mapunit.MapUnit):
            Sequence<com.unciv.models.UnitAction> {
        val civ = unit.civ
        if (civ.isBarbarian || civ.gameInfo.turns < civ.emmReligionConversionTurn)
            return emptySequence()
        val city = unit.getTile().takeIf { it.isCityCenter() }?.getCity()
            ?: return emptySequence()
        if (city.civ != civ) return emptySequence()
        return source.asSequence()
            .filter { gameNames[it.key] in city.emmEstablishedReligions }
            .filter { it.key != civ.emmStateReligion }
            .map { religion ->
                val name = gameNames[religion.key]!!
                com.unciv.models.UnitAction(
                    com.unciv.models.UnitActionType.EmmConvertReligion,
                    "Convert to " + name,
                    action = {
                        if (civ.gameInfo.turns >= civ.emmReligionConversionTurn
                            && name in city.emmEstablishedReligions
                            && civ.emmStateReligion != religion.key
                            && adopt(civ, religion.key)) {
                            civ.emmReligionConversionTurn = civ.gameInfo.turns + 10
                        }
                    }
                )
            }
    }

'''
    s=s.replace(anchor,helper+anchor)
    engine.write_text(s)
# Show in the ordinary unit actions, when stationed in a city following a faith.
actions=root/"core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt"
s=actions.read_text()
anchor="        yieldAll(UnitActionsUpgrade.getUpgradeActions(unit))"
line="        yieldAll(com.unciv.logic.civilization.EmmReligions.conversionActions(unit))\n\n"
if line not in s:
    assert s.count(anchor)==1
    actions.write_text(s.replace(anchor,line+anchor))
unit=root/"core/src/com/unciv/models/UnitAction.kt"
s=unit.read_text()
anchor='    Pillage("Pillage"),'
if '    EmmConvertReligion("Convert religion"),' not in s:
    assert s.count(anchor)==1
    unit.write_text(s.replace(anchor,anchor+'\n    EmmConvertReligion("Convert religion"),'))
ui=root/"core/src/com/unciv/ui/screens/worldscreen/unit/actions/UiUnitAction.kt"
s=ui.read_text()
anchor='    Pillage(UnitActionType.Pillage, portrait("Pillage"), false, useFrequency = 65f),'
if '    EmmConvertReligion(UnitActionType.EmmConvertReligion' not in s:
    assert s.count(anchor)==1
    ui.write_text(s.replace(anchor,anchor+'\n    EmmConvertReligion(UnitActionType.EmmConvertReligion, portrait("FoundReligion"), false, useFrequency = 82f),'))
print("Installed player conversion action for religions present in owned cities")
