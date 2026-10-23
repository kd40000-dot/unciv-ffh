#!/usr/bin/env python3
"""Verify Nature I -> Treetop Tactics mana, forestry and combat effect."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def obj(f): return {x["name"]:x for x in json.loads((root/"jsons"/f).read_text())}
promos=obj("UnitPromotions.json")
resources=obj("TileResources.json")
improvements=obj("TileImprovements.json")
units=obj("Units.json")
terrain=obj("Terrains.json")
spell=promos["Nature I"]
assert spell["unitTypes"]==["Magic"]
assert spell["prerequisites"]==["Channeling I"]
assert "Only available <with [Nature Mana]>" in spell["uniques"]
assert "[This Unit] gains the [Treetop Tactics] status for [2] turn(s) <for all movement> <with [Nature Mana]> <in [Forest] tiles>" in spell["uniques"]
status=promos["Treetop Tactics"]
assert status["unitTypes"]==[]
assert "[+10]% Strength <when fighting in [Forest] tiles>" in status["uniques"]
assert "Not shown on world screen" in status["uniques"]
assert terrain["Forest"]["type"]=="TerrainFeature"
assert resources["Nature Mana"]["resourceType"]=="Strategic"
assert "Provides [1] [Nature Mana]" in improvements["Nature Node"]["uniques"]
assert improvements["Nature Node"]["techRequired"]=="Alteration"
for name in ("Adept","Wizard","Mage","Archmage"):
    assert units[name]["unitType"]=="Magic"
    assert "Channeling I" in units[name]["promotions"]
print("OK: Nature I Treetop Tactics forest trigger, mana gate, +10% combat buff, expiring status and all casters")
