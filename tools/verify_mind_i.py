#!/usr/bin/env python3
"""Validate the city-centered Mind I Inspiration spell and its source-faithful science."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def objects(filename):
    return {x["name"]: x for x in json.loads((root/"jsons"/filename).read_text(encoding="utf-8"))}

promotions = objects("UnitPromotions.json")
units = objects("Units.json")
resources = objects("TileResources.json")
improvements = objects("TileImprovements.json")
spell = promotions["Mind I"]
status = promotions["Inspiration (Spell)"]
assert spell["unitTypes"] == ["Magic"]
assert spell["prerequisites"] == ["Channeling I"]
assert "Only available <with [Mind Mana]>" in spell["uniques"]
assert "[This Unit] gains the [Inspiration (Spell)] status for [2] turn(s) <for all movement> <with [Mind Mana]> <in [City center] tiles>" in spell["uniques"]
assert status["unitTypes"] == []
assert "Gain [2] [Science] <upon turn start> <in [City center] tiles> <with [Mind Mana]>" in status["uniques"]
assert "Not shown on world screen" in status["uniques"]
assert resources["Mind Mana"]["resourceType"] == "Strategic"
assert "Provides [1] [Mind Mana]" in improvements["Mind Node"]["uniques"]
assert improvements["Mind Node"]["techRequired"] == "Divination"
for unit in ["Adept", "Wizard", "Mage", "Archmage"]:
    assert units[unit]["unitType"] == "Magic"
    assert "Channeling I" in units[unit]["promotions"]
print("OK: Mind I is mana-gated, city-center-only, awards 2 Science at turn start for 2 turns, supports all arcane casters.")
