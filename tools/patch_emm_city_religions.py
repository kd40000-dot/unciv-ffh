#!/usr/bin/env python3
"""Persistent EMM city religion membership, holy city and basic spread/founding API."""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
engine=root/"core/src/com/unciv/logic/civilization/EmmReligions.kt"
s=engine.read_text()
if "fun spreadToCity(" not in s:
    anchor="    fun adopt(civ: Civilization, religionKey: String): Boolean {"
    assert s.count(anchor)==1
    s=s.replace(anchor,'''    /** Existing EMM health/event engine owns all world/city religion state. */
    private val gameNames = mapOf(
        "RELIGION_FELLOWSHIP_OF_LEAVES" to "Fellowship of Leaves",
        "RELIGION_THE_ORDER" to "The Order",
        "RELIGION_OCTOPUS_OVERLORDS" to "Octopus Overlords",
        "RELIGION_RUNES_OF_KILMORPH" to "Runes of Kilmorph",
        "RELIGION_THE_ASHEN_VEIL" to "The Ashen Veil",
        "RELIGION_THE_EMPYREAN" to "The Empyrean",
        "RELIGION_COUNCIL_OF_ESUS" to "Council of Esus"
    )

    /** Spread through the already integrated EMM clash/AC/city-state engine. */
    fun spreadToCity(city: com.unciv.logic.city.City, religionKey: String): Boolean {
        val name = gameNames[religionKey] ?: return false
        if (name in city.emmEstablishedReligions) return false
        city.civ.gameInfo.emmSpreadReligion(name, city)
        return name in city.emmEstablishedReligions
    }

    /** Preserve global founded slots even if the holy city is destroyed. */
    fun foundAt(city: com.unciv.logic.city.City, religionKey: String): Boolean {
        val name = gameNames[religionKey] ?: return false
        val game = city.civ.gameInfo
        if (name in game.emmFoundedReligions) return false
        game.emmFoundReligion(name, city)
        return name in game.emmFoundedReligions
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
                    (candidate.emmEstablishedReligions.size + 1)
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
print("Integrated EMM religion source catalog, founding, spread and alignment with existing health/event engine")
