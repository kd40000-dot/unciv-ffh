#!/usr/bin/env python3
"""Let existing saves found religions whose prerequisite technology was researched before the new EMM founding hook."""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
path=root/"core/src/com/unciv/logic/civilization/EmmReligions.kt"
s=path.read_text()
if "fun existingSaveFoundingActions(" not in s:
    anchor="    fun conversionActions("
    assert s.count(anchor)==1
    block='''    /** Recovery path for existing saves: research may predate EMM religion integration.
     * Explicit choice avoids silently awarding an already-discovered faith on load.
     */
    fun existingSaveFoundingActions(unit: com.unciv.logic.map.mapunit.MapUnit):
            Sequence<com.unciv.models.UnitAction> {
        val civ = unit.civ
        if (civ.isBarbarian || !civ.gameInfo.ruleset.buildings.containsKey("Herbalist"))
            return emptySequence()
        val city = unit.getTile().takeIf { it.isCityCenter() }?.getCity()
            ?: return emptySequence()
        if (city.civ != civ) return emptySequence()
        fun canon(value: String) = value.uppercase()
            .replace(Regex("[^A-Z0-9]"), "").removePrefix("TECH")
        return source.asSequence()
            .filter { religion -> religion.tech != null
                && civ.tech.techsResearched.any { canon(it) == canon(religion.tech) } }
            .filter { gameNames[it.key] !in civ.gameInfo.emmFoundedReligions }
            .map { religion ->
                val name = displayName(religion.key)
                com.unciv.models.UnitAction(
                    com.unciv.models.UnitActionType.EmmFoundResearchedReligion,
                    "Found " + name,
                    action = {
                        if (gameNames[religion.key] !in civ.gameInfo.emmFoundedReligions
                            && civ.tech.techsResearched.any { canon(it) == canon(religion.tech!!) }
                            && foundAt(city, religion.key)) {
                            civ.addNotification(name + " founded in [" + city.name + "]!",
                                NotificationCategory.General)
                        }
                    }
                )
            }
    }

'''
    path.write_text(s.replace(anchor,block+anchor))
actions=root/"core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt"
s=actions.read_text()
needle="        yieldAll(com.unciv.logic.civilization.EmmReligions.conversionActions(unit))"
addition="        yieldAll(com.unciv.logic.civilization.EmmReligions.existingSaveFoundingActions(unit))"
if addition not in s:
    assert s.count(needle)==1
    actions.write_text(s.replace(needle,needle+"\n"+addition))
enums=root/"core/src/com/unciv/models/UnitAction.kt"
s=enums.read_text()
needle='    EmmConvertReligion("Convert religion"),'
if '    EmmFoundResearchedReligion("Found religion"),' not in s:
    assert s.count(needle)==1
    enums.write_text(s.replace(needle,needle+'\n    EmmFoundResearchedReligion("Found religion"),'))
ui=root/"core/src/com/unciv/ui/screens/worldscreen/unit/actions/UiUnitAction.kt"
s=ui.read_text()
needle='    EmmConvertReligion(UnitActionType.EmmConvertReligion, portrait("FoundReligion"), false, useFrequency = 82f),'
if '    EmmFoundResearchedReligion(UnitActionType.EmmFoundResearchedReligion' not in s:
    assert s.count(needle)==1
    ui.write_text(s.replace(needle,needle+'\n    EmmFoundResearchedReligion(UnitActionType.EmmFoundResearchedReligion, portrait("FoundReligion"), false, useFrequency = 81f),'))
print("Installed explicit already-researched religion founding for existing save games")
