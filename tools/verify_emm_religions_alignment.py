#!/usr/bin/env python3
"""Assertions on pinned EMM religion and alignment generator output."""
import json,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
doc=json.loads(Path("docs/data/emm-religions-alignment.json").read_text())
assert doc["sourceRevision"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
assert doc["alignments"]==["ALIGNMENT_GOOD","ALIGNMENT_NEUTRAL","ALIGNMENT_EVIL"]
religions=doc["religions"]
assert len(religions)==7 and len(set(x["key"] for x in religions))==7
assert all(x["alignment"] in doc["alignments"] for x in religions)
generated=(root/"core/src/com/unciv/logic/civilization/EmmReligions.kt").read_text()
for info in religions:
    assert info["key"] in generated
    assert info["tech"] in generated if info["tech"] else True
assert "fun adopt(civ: Civilization" in generated
assert "fun spreadToCity(" in generated
assert "fun foundAt(" in generated
assert "fun onTechnologyResearched(" in generated
assert "candidate.population.population" in generated
assert "candidate.emmPresentReligions.size + 1" in generated
assert "candidate.isCapital()" in generated
assert 'removePrefix("TECH")' in generated
assert "gameCities.any { religionKey in it.emmHolyCityReligions }" in generated
assert "fun changeAlignment(civ: Civilization" in generated
assert "fun initializeAlignment(civ: Civilization)" in generated
assert "selectedLeaderAlignments[civ.civName]" in generated
assert "order.indexOf(initial).coerceIn(lower, upper)" in generated
civ=(root/"core/src/com/unciv/logic/civilization/Civilization.kt").read_text()
assert "var emmAlignment: String? = null" in civ
assert "var emmStateReligion: String? = null" in civ
assert "toReturn.emmAlignment = emmAlignment" in civ
assert "EmmReligions.initializeAlignment(this)" in civ
assert "toReturn.emmStateReligion = emmStateReligion" in civ
city=(root/"core/src/com/unciv/logic/city/City.kt").read_text()
assert "toReturn.emmPresentReligions.addAll(emmPresentReligions)" in city
assert "toReturn.emmHolyCityReligions.addAll(emmHolyCityReligions)" in city
tech=(root/"core/src/com/unciv/logic/civilization/managers/TechManager.kt").read_text()
assert "EmmReligions.onTechnologyResearched(civInfo, techName)" in tech
leaders=json.loads(Path("docs/data/emm-leader-alignments.json").read_text())
assert len(leaders["selectedCivilizations"])==19
for name, info in leaders["selectedCivilizations"].items():
    assert name in generated
    assert info["alignment"] in doc["alignments"]
print("PASS: seven source religions and three alignments; persisted civilization clone fields")
