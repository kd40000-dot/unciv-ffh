#!/usr/bin/env python3
"""Expose EMM holy-city religion state in city UI and remove silent founding failures."""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
# The original religion records are separate from the native Unciv religion UI.
# Show EMM city state explicitly, instead of making research appear to do nothing.
view=root/"core/src/com/unciv/view/CityView.kt"
v=view.read_text()
anchor="    @Readonly fun getEmmHealthInfo(): Pair<Int, Int>? = city.cityStats.emmHealthInfo"
assert v.count(anchor)==1
if "getEmmReligionCity()" not in v:
    view.write_text(v.replace(anchor,anchor+chr(10)+"    @Readonly fun getEmmReligionCity(): City = city"))
ui=root/"core/src/com/unciv/ui/screens/cityscreen/CityStatsTable.kt"
s=ui.read_text()
anchor='        lowerTable.add(unassignedPopLabel).row()'
block='''        // EMM's religious city state is separate from Unciv's vanilla religion manager.
        val emmCity = cityView.getEmmReligionCity()
        if (emmCity.civ.gameInfo.ruleset.buildings.containsKey("Herbalist")) {
            val names = emmCity.emmEstablishedReligions.sorted()
            if (names.isNotEmpty()) {
                lowerTable.add(("Religions: " + names.joinToString(", ")).toLabel(hideIcons = true)).row()
            }
            emmCity.emmHolyCityOf?.let { holy ->
                lowerTable.add(("Holy City: " + holy).toLabel(hideIcons = true)).row()
            }
            emmCity.civ.emmAlignment?.let { alignment ->
                lowerTable.add(("Alignment: " + alignment.removePrefix("ALIGNMENT_").lowercase().replaceFirstChar { it.uppercase() }).toLabel(hideIcons = true)).row()
            }
            emmCity.civ.emmStateReligion?.let { key ->
                lowerTable.add(("State Religion: " + com.unciv.logic.civilization.EmmReligions.displayName(key)).toLabel(hideIcons = true)).row()
            }
        }
'''
assert s.count(anchor)==1
if "Holy City: " not in s:ui.write_text(s.replace(anchor,block+anchor))
engine=root/"core/src/com/unciv/logic/civilization/EmmReligions.kt"
s=engine.read_text()
anchor="    fun spreadToCity("
assert s.count(anchor)==1
if "fun displayName(" not in s:
    s=s.replace(anchor,'''    fun displayName(key: String): String = gameNames[key] ?: key

'''+anchor)
    engine.write_text(s)
print("Added visible EMM city religion, holy city, alignment and state religion status")
