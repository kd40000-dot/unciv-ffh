#!/usr/bin/env python3
"""Static checks for the Spirit I Courage prototype; not a gameplay test."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
def load(name):
    return {item["name"]: item for item in json.loads((root/"jsons"/name).read_text(encoding="utf-8"))}
p = load("UnitPromotions.json")
r = load("TileResources.json")
i = load("TileImprovements.json")
u = load("Units.json")
assert p["Spirit I"]["prerequisites"] == ["Channeling I"]
assert p["Spirit I"]["unitTypes"] == ["Magic"]
assert "Only available <with [Spirit Mana]>" in p["Spirit I"]["uniques"]
assert "[This Unit] gains the [Courage (Spell)] status for [2] turn(s) <for all movement>" in p["Spirit I"]["uniques"]
assert "All adjacent units heal [10] HP when healing" in p["Courage (Spell)"]["uniques"]
assert "Not shown on world screen" in p["Courage (Spell)"]["uniques"]
assert r["Spirit Mana"]["resourceType"] == "Strategic"
assert "Provides [1] [Spirit Mana]" in i["Spirit Node"]["uniques"]
assert i["Spirit Node"]["techRequired"] == "Divination"
for n in ("Adept", "Mage", "Wizard", "Archmage"):
    assert u[n]["unitType"] == "Magic"
    assert "Channeling I" in u[n]["promotions"]
print("PASS: Spirit I source prereqs, mana, spell status, caster roster")
