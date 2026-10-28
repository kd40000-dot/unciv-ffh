#!/usr/bin/env python3
"""Persistent EMM city religion membership, holy city and basic spread/founding API."""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
city=root/"core/src/com/unciv/logic/city/City.kt"
s=city.read_text()
if "var emmPresentReligions" not in s:
    anchor="    var religion = CityReligionManager()"
    assert s.count(anchor)==1
    s=s.replace(anchor,anchor+'''
    /** Independently persisted EMM religions (multiple faiths can coexist). */
    var emmPresentReligions = HashSet<String>()
    /** Holy-city identities survive capture and changing state religion. */
    var emmHolyCityReligions = HashSet<String>()''')
    anchor="        toReturn.religion = religion.clone()"
    assert s.count(anchor)==1
    s=s.replace(anchor,anchor+'''
        toReturn.emmPresentReligions.addAll(emmPresentReligions)
        toReturn.emmHolyCityReligions.addAll(emmHolyCityReligions)''')
    city.write_text(s)
engine=root/"core/src/com/unciv/logic/civilization/EmmReligions.kt"
s=engine.read_text()
if "fun spreadToCity(" not in s:
    anchor="    fun adopt(civ: Civilization, religionKey: String): Boolean {"
    assert s.count(anchor)==1
    s=s.replace(anchor,'''    /** A source religion may coexist with others in the same city. */
    fun spreadToCity(city: com.unciv.logic.city.City, religionKey: String): Boolean {
        if (religionKey !in byKey) return false
        return city.emmPresentReligions.add(religionKey)
    }

    /** Once-only holy-city identity and initial city religion presence. */
    fun foundAt(city: com.unciv.logic.city.City, religionKey: String): Boolean {
        if (religionKey !in byKey) return false
        val gameCities = city.civ.gameInfo.civilizations.flatMap { it.cities }
        if (gameCities.any { religionKey in it.emmHolyCityReligions }) return false
        city.emmHolyCityReligions.add(religionKey)
        city.emmPresentReligions.add(religionKey)
        return true
    }

'''+anchor)
    engine.write_text(s)
tech=root/"core/src/com/unciv/logic/civilization/managers/TechManager.kt"
t=tech.read_text()
hook="        val isNewTech = techsResearched.add(techName)"
call="""        if (isNewTech)
            com.unciv.logic.civilization.EmmReligions.onTechnologyResearched(civInfo, techName)"""
if call not in t:
    assert t.count(hook)==1
    t=t.replace(hook,hook+"\n"+call)
    tech.write_text(t)
engine=root/"core/src/com/unciv/logic/civilization/EmmReligions.kt"
e=engine.read_text()
if "fun onTechnologyResearched(" not in e:
    hook="    fun spreadToCity("
    assert e.count(hook)==1
    method='''    /** EMM first-discovery holy-city trigger. A city-selection algorithm is pending. */
    fun onTechnologyResearched(civ: Civilization, techName: String) {
        fun canon(value: String) = value.uppercase()
            .replace(Regex("[^A-Z0-9]"), "").removePrefix("TECH")
        for (religion in source) {
            if (religion.tech == null || canon(religion.tech) != canon(techName)) continue
            val city = civ.cities.firstOrNull() ?: continue
            foundAt(city, religion.key)
        }
    }

'''
    e=e.replace(hook,method+hook)
    engine.write_text(e)
print("Installed persisted multi-religion city presence and single holy-city founding API")
