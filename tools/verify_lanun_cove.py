#!/usr/bin/env python3
"""Check the first Lanun Pirate Cove against the pinned EMM spell and improvement source."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
source=load("docs/data/emm-lanun-pirate-coves.json")
unit_source=load("docs/data/emm-unit-building-catalog.json")
units=load("jsons/Units.json")
improvements=load("jsons/TileImprovements.json")
nations=load("jsons/Nations.json")
assert source["commit"]==unit_source["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
assert len(source["stages"])==3
assert [x["sourceId"] for x in source["stages"]]==[
    "IMPROVEMENT_PIRATE_COVE","IMPROVEMENT_PIRATE_HARBOR","IMPROVEMENT_PIRATE_PORT"]
assert [x["sourceYields"] for x in source["stages"]]==[[0,0,2],[1,1,3],[2,2,4]]
assert [x["upgradeTime"] for x in source["stages"]]==[10,20,0]
assert [x["defensePercent"] for x in source["stages"]]==[10,20,30]
assert [x["implemented"] for x in source["stages"]]==[True,True,True]
assert source["spell"]["sourceUnit"]=="UNIT_WORKBOAT"
assert source["spell"]["civilization"]=="CIVILIZATION_LANUN"
assert source["spell"]["creates"]=="IMPROVEMENT_PIRATE_COVE"
assert source["spell"]["consumesCaster"]
assert source["conversion"]["sourceCommerce"]==2
assert source["conversion"]["uncivGold"]==1 and source["conversion"]["uncivScience"]==1
byunit={u["name"]:u for u in units}
byimprovement={t["name"]:t for t in improvements}
workboat=byunit["Workboat"]
original=next(u for u in unit_source["units"] if u["id"]=="UNIT_WORKBOAT")
assert original["cost"]==workboat["cost"]==30
assert original["moves"]==workboat["movement"]==2
assert workboat["unitType"]=="Civilian Water" and workboat["requiredTech"]=="Fishing"
ability="Can instantly construct a [Pirate Cove] improvement <by consuming this unit> <for [Lanun] Civilizations>"
assert workboat.get("uniques",[]).count(ability)==1
assert len([u for u in units if any("construct a [Pirate Cove]" in v for v in u.get("uniques",[]))])==1
cove=byimprovement["Pirate Cove"]
assert cove["terrainsCanBeBuiltOn"]==["Coast"]
assert cove["uniqueTo"]=="Lanun" and cove["turnsToBuild"]==-1
assert cove.get("gold")==source["conversion"]["uncivGold"]==1
assert cove.get("science")==source["conversion"]["uncivScience"]==1
assert "production" not in cove and "food" not in cove
expected={
    "Can only be built on [your] tiles",
    "Can only be built on [unimproved] tiles",
    "Cannot be built on [resource] tiles",
    "Must be next to [Land]",
    "Gives a defensive bonus of [10]%",
    "Pillaging this improvement yields approximately [+10 Gold]",
}
assert set(cove.get("uniques",[]))==expected
assert "Lanun" in {n["name"] for n in nations}
# Native improvement actions are priced, consume their Workboat, and respect the
# target improvement's required technology and immediate-previous-stage filter.
tiers=[
    ("Pirate Harbor","Pirate Cove","Sailing",100,1,1,2,1,20),
    ("Pirate Port","Pirate Harbor","Optics",200,2,2,2,2,30)
]
for name,previous,tech,price,food,production,gold,science,defense in tiers:
    imp=byimprovement[name]
    assert imp["uniqueTo"]=="Lanun" and imp["terrainsCanBeBuiltOn"]==["Coast"]
    assert imp["techRequired"]==tech and imp["turnsToBuild"]==-1
    for field,expected_value in (("food",food),("production",production),("gold",gold),("science",science)):
        assert imp[field]==expected_value,(name,field)
    assert set(imp["uniques"]) == {
        "Can only be built on [your] tiles",
        "Cannot be built on [resource] tiles",
        "Must be next to [Land]",
        f"Can only be built on [{previous}] tiles",
        f"Gives a defensive bonus of [{defense}]%",
        "Pillaging this improvement yields approximately [+10 Gold]"
    },name
    action=f"Can instantly construct a [{name}] improvement <by consuming this unit> <costs [+{price} Gold] stats> <for [Lanun] Civilizations>"
    assert workboat["uniques"].count(action)==1,(name,action)
    assert not any(action in u.get("uniques",[]) for u in units if u["name"]!="Workboat")
assert len([u for u in workboat["uniques"] if "Can instantly construct a [Pirate" in u])==3
assert len(improvements)==44 and len(units)==103
print("OK: all 3 Lanun Cove upgrades verified: Workboat gold costs/consumption, Sailing/Optics gates, sequential existing-tile replacement, yields and defenses")
