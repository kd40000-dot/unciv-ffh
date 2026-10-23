#!/usr/bin/env python3
"""Validate the Fire I -> Blaze -> Smoke prototype against current mod JSON."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def objs(f):
    return {obj["name"]:obj for obj in json.loads((root/"jsons"/f).read_text())}
resources=objs("TileResources.json")
promotions=objs("UnitPromotions.json")
improvements=objs("TileImprovements.json")
units=objs("Units.json")
assert resources["Fire Mana"]["resourceType"] == "Strategic"
assert "Provides [1] [Fire Mana]" in improvements["Fire Node"]["uniques"]
fire=promotions["Fire I"]
assert fire["unitTypes"]==["Magic"]
assert fire["prerequisites"]==["Channeling I"]
assert "Only available <with [Fire Mana]>" in fire["uniques"]
assert "Can instantly construct a [Smoke] improvement <for all movement> <with [Fire Mana]>" in fire["uniques"]
smoke=improvements["Smoke"]
assert smoke["terrainsCanBeBuiltOn"]==["Forest","Jungle"]
assert smoke["turnsToBuild"] == -1
assert "Can only be built on [unimproved] tiles" in smoke["uniques"]
assert "Can only be built on [your] tiles" in smoke["uniques"]
assert "Adjacent enemy units ending their turn take [5] damage" in smoke["uniques"]
for name in ("Adept","Mage","Archmage"):
    assert units[name]["unitType"]=="Magic"
    assert "Channeling I" in units[name]["promotions"]
assert not any("Smoke" in u for name,unit in units.items() for u in unit.get("uniques",[]))
print("OK: Fire I mana-gated, Channeling I prerequisite, Smoke construction and danger verified.")
