#!/usr/bin/env python3
"""Verify Body I Haste mod-only prototype and mana-node dependency."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def objects(path):
    return {x["name"]:x for x in json.loads((root/"jsons"/path).read_text(encoding="utf-8"))}
p=objects("UnitPromotions.json")
i=objects("TileImprovements.json")
r=objects("TileResources.json")
u=objects("Units.json")
assert r["Body Mana"]["resourceType"]=="Strategic"
assert "Provides [1] [Body Mana]" in i["Body Node"]["uniques"]
assert i["Body Node"]["techRequired"]=="Alteration"
assert p["Body I"]["unitTypes"]==["Magic"]
assert p["Body I"]["prerequisites"]==["Channeling I"]
assert "Only available <with [Body Mana]>" in p["Body I"]["uniques"]
assert "[This Unit] gains the [Hasted] status for [2] turn(s) <for all movement>" in p["Body I"]["uniques"]
assert p["Hasted"]["unitTypes"]==[]
assert "[+1] Movement" in p["Hasted"]["uniques"]
assert "Not shown on world screen" in p["Hasted"]["uniques"]
for name in ("Adept","Mage","Archmage"):
    assert u[name]["unitType"]=="Magic"
    assert "Channeling I" in u[name]["promotions"]
print("OK: Body I gate, Body Mana supply, self-cast Haste action, temporary Hasted +1 movement")
