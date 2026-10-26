#!/usr/bin/env python3
"""Validate the source-exact EMM Ancient starting rosters and special units."""
import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
source=load("docs/data/emm-civilizations.json")
nations={c["name"]:c for c in load("jsons/Nations.json")}
eras={e["name"]:e for e in load("jsons/Eras.json")}
units={u["name"]:u for u in load("jsons/Units.json")}
types={t["name"] for t in load("jsons/UnitTypes.json")}
promotions={p["name"]:p for p in load("jsons/UnitPromotions.json")}
original={u["id"]:u for u in load("docs/data/emm-unit-building-catalog.json")["units"]}
classes={"UNITCLASS_WARRIOR":"Warrior","UNITCLASS_SCOUT":"Scout","UNITCLASS_LUCIAN":"Lucian","UNITCLASS_LIGHTBRINGER":"Lightbringer"}
assert source["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
assert eras["Ancient era"]["startingSettlerCount"]==1
assert eras["Ancient era"]["startingMilitaryUnitCount"]==0
assert eras["Classical era"]["startingMilitaryUnitCount"]==2
assert eras["Medieval era"]["startingMilitaryUnitCount"]==3
def grant(name,n):
    return (f"Free [{name}] appears" if n==1 else f"[{n}] free [{name}] units appear")+" <if starting in the [Ancient era]>"
playable=[c for c in source["civilizations"] if c["playable"]]
assert len(playable)==19 and len(nations)==20
total=0
for civ in playable:
    classCounts=Counter()
    for entry in civ["startingUnits"]:classCounts[entry["id"]]+=entry["count"]
    assert classCounts.pop("UNITCLASS_SETTLER")==1,civ["name"]
    assert set(classCounts).issubset(classes),civ["name"]
    expected={grant(classes[cl],count) for cl,count in classCounts.items()}
    actual={text for text in nations[civ["name"]].get("uniques",[]) if text.startswith("Free [") or (" free [" in text and " units appear" in text)}
    assert expected==actual,(civ["name"],expected,actual)
    total+=sum(classCounts.values())
assert total==39,total
assert len(units)>=103 and "Disciple" in types
assert units["Disciple of the Ashen Veil"]["requiredTech"] == "Corruption of Spirit"
for name,civ,t in (("Lucian","Doviello","Sword"),("Lightbringer","Malakim","Disciple")):
    u=units[name];src=original["UNIT_"+name.upper()]
    assert u["uniqueTo"]==civ and u["unitType"]==t,(name,u)
    assert u["cost"]==src["cost"] and u["strength"]==src["attack"]
    assert u["movement"]==src["moves"] and "requiredTech" not in u
assert {"Unbuildable","Limited to [1] per Civilization","[+10]% Strength <vs cities>"}<=set(units["Lucian"]["uniques"])
assert "Sentry" in units["Lightbringer"]["promotions"]
assert "Disciple" in promotions["Sentry"]["unitTypes"]
for name,base,replacement in (("Calabim","Warrior","Bloodpet"),("Doviello","Warrior","Beastman"),("Clan of Embers","Scout","Goblin")):
    assert units[replacement]["uniqueTo"]==name and units[replacement]["replaces"]==base
print(f"OK: {len(playable)} EMM Ancient-era rosters, {total} nonsettler starting units and 2 EMM unit definitions.")
