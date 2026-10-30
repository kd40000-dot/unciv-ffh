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
techs=json.loads(Path("jsons/Techs.json").read_text())
imported={t["name"].upper().replace(" ","").replace("-","") for col in techs for t in col.get("techs",[])}
for info in religions:
    assert info["tech"].removeprefix("TECH_").replace("_","").upper() in imported, info["tech"]
generated=(root/"core/src/com/unciv/logic/civilization/EmmReligions.kt").read_text()
for info in religions:
    assert info["key"] in generated
    assert info["tech"] in generated if info["tech"] else True
assert "fun adopt(civ: Civilization" in generated
assert "fun conversionActions(" in generated
assert "emmReligionConversionTurn" in generated
assert "city.emmEstablishedReligions" in generated
assert "fun spreadToCity(" in generated
assert "fun foundAt(" in generated
assert "fun onTechnologyResearched(" in generated
assert "founded in [" in generated
assert "has already been founded." in generated
assert "fun displayName(key: String)" in generated
assert "candidate.population.population" in generated
assert "candidate.emmEstablishedReligions.size + 1" in generated
assert "candidate.isCapital()" in generated
assert 'removePrefix("TECH")' in generated
assert "game.emmFoundedReligions" in generated
assert "city.civ.gameInfo.emmSpreadReligion(name, city)" in generated
assert "game.emmFoundReligion(name, city)" in generated
assert "RELIGION_THE_ASHEN_VEIL" in generated
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
assert "toReturn.emmReligionConversionTurn = emmReligionConversionTurn" in civ
city=(root/"core/src/com/unciv/logic/city/City.kt").read_text()
assert "toReturn.emmEstablishedReligions.addAll(emmEstablishedReligions)" in city
assert "toReturn.emmHolyCityOf = emmHolyCityOf" in city
tech=(root/"core/src/com/unciv/logic/civilization/managers/TechManager.kt").read_text()
assert "EmmReligions.onTechnologyResearched(civInfo, techName)" in tech
leaders=json.loads(Path("docs/data/emm-leader-alignments.json").read_text())
assert len(leaders["selectedCivilizations"])==19
for name, info in leaders["selectedCivilizations"].items():
    assert name in generated
    assert info["alignment"] in doc["alignments"]
game=(root/"core/src/com/unciv/logic/GameInfo.kt").read_text()
assert "var emmFoundedReligions = hashSetOf<String>()" in game
assert "toReturn.emmFoundedReligions.addAll(emmFoundedReligions)" in game
actions=(root/"core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt").read_text()
assert "EmmReligions.conversionActions(unit)" in actions
ui=(root/"core/src/com/unciv/ui/screens/worldscreen/unit/actions/UiUnitAction.kt").read_text()
assert "EmmConvertReligion(UnitActionType.EmmConvertReligion" in ui
city_ui=(root/"core/src/com/unciv/ui/screens/cityscreen/CityStatsTable.kt").read_text()
assert "Religions: " in city_ui and "Holy City: " in city_ui
assert "Alignment: " in city_ui and "State Religion: " in city_ui
assert "getEmmReligionCity()" in (root/"core/src/com/unciv/view/CityView.kt").read_text()
print("PASS: seven source religions and three alignments; persisted civilization clone fields")
