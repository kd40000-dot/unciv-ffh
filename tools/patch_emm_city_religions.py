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
        if (!city.emmPresentReligions.add(religionKey)) return false
        city.civ.gameInfo.changeEmmArmageddon(byKey[religionKey]!!.counterOnSpread)
        return true
    }

    /** Once-only holy-city identity and initial city religion presence. */
    fun foundAt(city: com.unciv.logic.city.City, religionKey: String): Boolean {
        if (religionKey !in byKey) return false
        val gameCities = city.civ.gameInfo.civilizations.flatMap { it.cities }
        val founded = city.civ.gameInfo.emmFoundedReligions
        if (religionKey in founded ||
            gameCities.any { religionKey in it.emmHolyCityReligions }) return false
        founded.add(religionKey)
        city.emmHolyCityReligions.add(religionKey)
        spreadToCity(city, religionKey)
        city.civ.gameInfo.changeEmmArmageddon(byKey[religionKey]!!.counterOnFound)
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
            // CvPlayer::foundReligion ranks cities by population and existing
            // religions; source random tie-breaking and settlements still pending.
            val city = civ.cities.maxByOrNull { candidate ->
                var score = (10 + candidate.population.population) /
                    (candidate.emmPresentReligions.size + 1)
                if (candidate.isCapital()) score /= 8
                score.coerceAtLeast(1)
            } ?: continue
            foundAt(city, religion.key)
        }
    }

'''
    e=e.replace(hook,method+hook)
    engine.write_text(e)
# Source-backed starting alignment for the 19 ported civilization/leader choices.
import json
leaders=json.loads(Path("docs/data/emm-leader-alignments.json").read_text())
assert leaders["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
values=leaders["selectedCivilizations"]
assert len(values)==19
records=(chr(44)+chr(10)).join("        "+json.dumps(k)+" to "+json.dumps(v["alignment"]) for k,v in sorted(values.items()))
engine=root/"core/src/com/unciv/logic/civilization/EmmReligions.kt"
e=engine.read_text()
if "fun initializeAlignment(" not in e:
    anchor="    fun changeAlignment(civ: Civilization, alignment: String): Boolean {"
    assert e.count(anchor)==1
    block='''    private val selectedLeaderAlignments = mapOf(
%s
    )

    /** Starting leader alignment, only once; never reset conversions on load. */
    fun initializeAlignment(civ: Civilization) {
        if (civ.emmAlignment != null) return
        civ.emmAlignment = selectedLeaderAlignments[civ.civName]
    }

''' % records
    engine.write_text(e.replace(anchor,block+anchor))
civ=root/"core/src/com/unciv/logic/civilization/Civilization.kt"
t=civ.read_text()
anchor='''fun setTransients():Unit = timeThis("Civilization.setTransients") {
'''
call="        EmmReligions.initializeAlignment(this)" + chr(10)
if "EmmReligions.initializeAlignment(this)" not in t:
    assert t.count(anchor)==1
    civ.write_text(t.replace(anchor,anchor+call,1))
game=root/"core/src/com/unciv/logic/GameInfo.kt"
g=game.read_text()
if "var emmFoundedReligions" not in g:
    anchor="    var turns = 0"
    assert g.count(anchor)==1
    g=g.replace(anchor,anchor+chr(10)+"    /** Global, persistent EMM founded religion slots, even if holy cities are razed. */"+chr(10)+"    var emmFoundedReligions = HashSet<String>()")
    anchor="        toReturn.turns = turns"
    assert g.count(anchor)==1
    g=g.replace(anchor,anchor+chr(10)+"        toReturn.emmFoundedReligions.addAll(emmFoundedReligions)")
    game.write_text(g)
print("Installed persisted multi-religion city presence and single holy-city founding API")
