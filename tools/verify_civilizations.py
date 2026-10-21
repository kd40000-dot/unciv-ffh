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

# Source-faithful faction upgrade chains, including faction-specific class bans.
# EMM upgrades point to *classes*: resolve to their ordinary Unciv unit names so
# native civilization replacement resolution can select the correct faction unit.
progression = data("docs/data/emm-promotions-upgrades-resources.json")
source_by_id = {u["id"]: u for u in progression["unitProgression"]}
base_by_class = {}
for u in units:
    if u.get("uniqueTo"):
        continue
    source_id = "UNIT_" + u["name"].upper().replace(" ", "_")
    if source_id not in source_by_id:
        continue
    unit_class = source_by_id[source_id]["classId"]
    assert unit_class not in base_by_class, (unit_class, u["name"])
    base_by_class[unit_class] = u["name"]
forbidden = {(b["civ"], b["name"]) for b in catalog["classProhibitions"] if b["type"] == "unit"}
added_routes = 0
unimplemented_routes = 0
prohibited_routes = 0
for item in catalog["addedUnits"]:
    source = source_by_id[item["sourceId"]]
    expected = []
    for target_class in source["upgrades"]:
        if target_class not in base_by_class:
            unimplemented_routes += 1
            continue
        target_name = base_by_class[target_class]
        if (item["civilization"], target_name) in forbidden:
            prohibited_routes += 1
            continue
        expected.append(target_name)
    unit = byUnit[item["name"]]
    actual = ([unit["upgradesTo"]] if unit.get("upgradesTo") else [])
    actual += [u[len("Can upgrade to ["):-1] for u in unit.get("uniques", [])
               if u.startswith("Can upgrade to [") and u.endswith("]")]
    assert actual == expected, (item["name"], actual, expected)
    added_routes += len(expected)
assert added_routes == 63 and unimplemented_routes == 14 and prohibited_routes == 1

print("OK: 19 normal EMM civilizations, 2 special event civilizations deferred,",len(catalog["addedUnits"]),"faction units,",len(catalog["addedBuildings"]),"faction buildings; city names and colors exact;",added_routes,"faction upgrade routes verified")
