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
assert [x["implemented"] for x in source["stages"]]==[True,False,False]
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
assert "Pirate Harbor" not in byimprovement and "Pirate Port" not in byimprovement
assert len(improvements)==21 and len(units)==102
print("OK: Lanun Workboat can create one source-derived, nation-locked Pirate Cove; 3 stage source ledgers preserved; unsupported upgrades deferred")
