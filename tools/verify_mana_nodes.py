#!/usr/bin/env python3
"""Audit first playable EMM mana-node slice against pinned source definitions."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

ledger=load("docs/data/emm-mana-nodes.json")
resources={r["name"]:r for r in load("jsons/TileResources.json")}
improvements={r["name"]:r for r in load("jsons/TileImprovements.json")}
units={r["name"]:r for r in load("jsons/Units.json")}
techs={t["name"] for c in load("jsons/Techs.json") for t in c["techs"]}
assert ledger["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
assert len(ledger["spheres"])==21
assert len({s["name"] for s in ledger["spheres"]})==21
raw=resources["Raw Mana"]
assert raw["resourceType"]=="Bonus"
assert "Hill" in raw["terrainsCanBeFoundOn"]
assert len(raw["improvedBy"])==21
assert not any("Raw Mana" in x for x in units["Adept"].get("promotions",[]))
adept=units["Adept"]
for sphere in ledger["spheres"]:
    name,tech=sphere["name"],sphere["tech"]
    assert tech in techs
    resource=resources[f"{name} Mana"]
    assert resource["resourceType"]=="Strategic"
    assert resource["terrainsCanBeFoundOn"]==[]
    assert "Doesn't generate naturally" in resource["uniques"]
    improvement=improvements[f"{name} Node"]
    assert improvement["techRequired"]==tech
    assert improvement["turnsToBuild"]==17
    assert improvement["terrainsCanBeBuiltOn"]==[]
    assert set(improvement["uniques"])=={
        "Can only be built to improve a resource",
        "Can only be built on [Raw Mana] tiles",
        "Can only be built on [your] tiles",
        f"Provides [1] [{name} Mana]",
    }
    assert "Can only be built on [unimproved] tiles" not in improvement["uniques"]  # enables direct 17-turn node-to-node replacement
    assert improvement["name"] in raw["improvedBy"]
    for caster_name in ("Adept", "Wizard", "Mage", "Archmage"):
        assert f"Can build [{name} Node] improvements on tiles" in units[caster_name]["uniques"]
for caster_name in ("Adept", "Wizard", "Mage", "Archmage"):
    caster=units[caster_name]
    assert caster["unitType"]=="Magic"
    assert len([u for u in caster["uniques"] if u.startswith("Can build [") and u.endswith(" Node] improvements on tiles")])==21
assert [name for name in resources if name.endswith(" Mana") and name!="Raw Mana"]==[
    f'{s["name"]} Mana' for s in ledger["spheres"]]
assert all(not any("Can build ["+s["name"]+" Node]" in u for u in units["Workboat"]["uniques"])
           for s in ledger["spheres"])
print("OK: 21 EMM sphere prerequisites, Raw Mana placement, 21 retunable nodes, strategic resource outputs and Adept build abilities")
