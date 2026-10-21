#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def data(p):return json.loads((root/p).read_text(encoding="utf8"))
catalog=data("docs/data/emm-civilizations.json")
nations=data("jsons/Nations.json");units=data("jsons/Units.json");buildings=data("jsons/Buildings.json")
promotionNames={p["name"] for p in data("jsons/UnitPromotions.json")}
techNames={t["sourceId"]:t["name"] for t in data("docs/data/emm-technologies.json")["technologies"] if t["researchCost"]>0 and not t["disabled"]}
byNation={n["name"]:n for n in nations};byUnit={u["name"]:u for u in units};byBuilding={b["name"]:b for b in buildings}
assert catalog["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610" and len(catalog["civilizations"])==21
assert len(byNation)==20 and "Barbarians" in byNation
assert {x["id"] for x in catalog["civilizations"] if not x["playable"]}=={"CIVILIZATION_INFERNAL","CIVILIZATION_MERCURIANS"}
for original in catalog["civilizations"]:
    if not original["playable"]:
        assert original["name"] not in byNation
        continue
    n=byNation[original["name"]]
    assert n["cities"]==original["cityNames"]
    assert n["outerColor"]==original["colors"]["outer"]
    assert n["innerColor"]==original["colors"]["inner"]
    assert original["chosenLeader"] in {l["id"] for l in original["leaders"]}
    for t in original["startingTech"]:
        if t in techNames:assert "Starts with ["+techNames[t]+"]" in n.get("uniques",[]),(n["name"],t)
    race={"PROMOTION_ORC":"Orc","PROMOTION_ELF":"Elf","PROMOTION_DWARF":"Dwarf","PROMOTION_DARK_ELF":"Dark Elf"}.get(original["race"])
    if race:
        assert race in promotionNames
        assert any("receive the ["+race+"] promotion" in u for u in n.get("uniques",[]))
for x in catalog["addedUnits"]:
    u=byUnit[x["name"]]
    assert u["uniqueTo"]==x["civilization"] and u["replaces"]==x["replaces"] and u["replaces"] in byUnit
for x in catalog["addedBuildings"]:
    b=byBuilding[x["name"]]
    assert b["uniqueTo"]==x["civilization"] and b["replaces"]==x["replaces"] and b["replaces"] in byBuilding
# Every source prohibition implemented in the ruleset must remain active.
for ban in catalog["classProhibitions"]:
    target=byUnit[ban["name"]] if ban["type"]=="unit" else byBuilding[ban["name"]]
    effect="Only available <for [non-["+ban["civ"]+"]] Civilizations>"
    assert effect in target.get("uniques",[]),(ban["civ"],ban["name"])
# Ensure every mapped selected-leader trait remains present and tied to its selected leader.
for selection in catalog["leaderSelections"]:
    nation=byNation[selection["civilization"]]
    for trait in selection["implementedTraits"]:
        assert trait in selection["traits"],(nation["name"],trait)
    if "TRAIT_CHARISMATIC" in selection["traits"]:
        assert "[-25]% XP required for promotions" in nation.get("uniques",[]),nation["name"]
    if "TRAIT_CREATIVE" in selection["traits"]:
        assert "[+2 Culture] [in all cities]" in nation.get("uniques",[]),nation["name"]
print("OK: 19 normal EMM civilizations, 2 special event civilizations deferred,",len(catalog["addedUnits"]),"faction units,",len(catalog["addedBuildings"]),"faction buildings; city names and colors exact")
