#!/usr/bin/env python3
"""Validate EMM-inspired Enchantment I and deliberately localized aura proxy."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def load(path):
    return {x["name"]:x for x in json.loads((root/"jsons"/path).read_text(encoding="utf-8"))}
p=load("UnitPromotions.json")
r=load("TileResources.json")
imp=load("TileImprovements.json")
u=load("Units.json")
t=load("UnitTypes.json")
assert r["Enchantment Mana"]["resourceType"]=="Strategic"
assert imp["Enchantment Node"]["techRequired"]=="Alteration"
assert "Provides [1] [Enchantment Mana]" in imp["Enchantment Node"]["uniques"]
spell=p["Enchantment I"]
assert spell["unitTypes"]==["Magic"]
assert spell["prerequisites"]==["Channeling I"]
assert "Only available <with [Enchantment Mana]>" in spell["uniques"]
assert "[This Unit] gains the [Enchanted Blade Aura] status for [2] turn(s) <for all movement>" in spell["uniques"]
aura=p["Enchanted Blade Aura"]
assert aura["unitTypes"]==[]
assert "[20]% Strength bonus for [Sword] units within [1] tiles" in aura["uniques"]
assert "Not shown on world screen" in aura["uniques"]
assert t["Sword"]["movementType"]=="Land"
for name in ("Adept","Wizard","Mage","Archmage"):
    assert u[name]["unitType"]=="Magic"
    assert "Channeling I" in u[name]["promotions"]
print("OK: Enchantment I mana gating, 2-turn self-cast aura, +20% nearby Sword Strength, 4 casters")
