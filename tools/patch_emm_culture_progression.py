#!/usr/bin/env python3
"""Track accumulated EMM city culture and advance natural defensive tiers."""
from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
data=json.loads(Path("docs/data/emm-culture-defense.json").read_text())["cultureDefenseLevels"]
defense=root/"core/src/com/unciv/logic/city/EmmCityDefense.kt"
city=root/"core/src/com/unciv/logic/city/City.kt"
exp=root/"core/src/com/unciv/logic/city/managers/CityExpansionManager.kt"
d=defense.read_text()
if "fun cultureLevelFor(" not in d:
    rows=",\n".join('        "%s" to mapOf(%s)' % (x["id"], ", ".join('"%s" to %d' % (k,v) for k,v in x["thresholds"].items())) for x in data)
    anchor="    fun naturalDefenseForCulture(level: String): Int ="
    assert d.count(anchor)==1
    addition='''    private val cultureThresholds = linkedMapOf(
%s
    )
    fun cultureLevelFor(totalCulture: Int, speed: String): String {
        val sourceSpeed = when (speed.uppercase()) {
            "MARATHON" -> "GAMESPEED_MARATHON"
            "EPIC" -> "GAMESPEED_EPIC"
            "QUICK" -> "GAMESPEED_QUICK"
            else -> "GAMESPEED_NORMAL"
        }
        return cultureThresholds.entries.lastOrNull { (_, tiers) ->
            totalCulture >= (tiers[sourceSpeed] ?: Int.MAX_VALUE)
        }?.key ?: "CULTURELEVEL_NONE"
    }

''' % rows
    d=d.replace(anchor,addition+anchor)
    defense.write_text(d)
c=city.read_text()
if "var emmTotalCulture: Int" not in c:
    anchor='    var emmCultureLevel: String = "CULTURELEVEL_NONE"'
    assert c.count(anchor)==1
    c=c.replace(anchor,anchor+"\n    var emmTotalCulture: Int = 0")
    anchor="        toReturn.emmCultureLevel = emmCultureLevel"
    assert c.count(anchor)==1
    c=c.replace(anchor,anchor+"\n        toReturn.emmTotalCulture = emmTotalCulture")
    city.write_text(c)
e=exp.read_text()
if "city.emmTotalCulture +=" not in e:
    anchor="        cultureStored += culture.toInt()"
    assert e.count(anchor)==1
    e=e.replace(anchor,anchor+'''
        // EMM keeps lifetime city culture, unlike the expendable Unciv tile-expansion bank.
        city.emmTotalCulture = (city.emmTotalCulture + culture.toInt()).coerceAtLeast(0)
        city.emmCultureLevel = com.unciv.logic.city.EmmCityDefense.cultureLevelFor(
            city.emmTotalCulture, city.civ.gameInfo.speed.name
        )''')
    exp.write_text(e)
print("Installed lifetime EMM culture accrual and speed-specific natural defense levels")
