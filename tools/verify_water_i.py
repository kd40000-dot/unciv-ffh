#!/usr/bin/env python3
"""Check Water I's real Spring terraforming and smoke removal actions."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def items(name): return {o["name"]:o for o in json.loads((root/"jsons"/name).read_text(encoding="utf-8"))}
promotions=items("UnitPromotions.json")
improvements=items("TileImprovements.json")
resources=items("TileResources.json")
units=items("Units.json")
terrains=items("Terrains.json")
water=promotions["Water I"]
assert water["unitTypes"]==["Magic"]
assert water["prerequisites"]==["Channeling I"]
assert "Only available <with [Water Mana]>" in water["uniques"]
terraform="Turn this tile into a [Plains] tile <for all movement> <with [Water Mana]> <in [Desert] tiles> <in [your] tiles> <in [unimproved] tiles> <in tiles without [Flood plains]>"
extinguish="Remove [Smoke] improvements from this tile <for all movement> <with [Water Mana]> <in [Smoke] tiles> <in [your] tiles>"
assert terraform in water["uniques"]
assert extinguish in water["uniques"]
assert "Plains" in terrains and "Desert" in terrains and "Flood plains" in terrains
assert resources["Water Mana"]["resourceType"]=="Strategic"
assert "Provides [1] [Water Mana]" in improvements["Water Node"]["uniques"]
assert improvements["Water Node"]["techRequired"]=="Elementalism"
assert "Smoke" in improvements
for name in ["Adept","Wizard","Mage","Archmage"]:
    assert units[name]["unitType"]=="Magic"
    assert "Channeling I" in units[name]["promotions"]
print("OK: Water I mana gate, Desert to Plains restrictions, direct Smoke removal, and all arcane casters.")
