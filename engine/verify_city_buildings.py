#!/usr/bin/env python3
"""Validate EMM-specific city-building mechanics and lost-effect inventory."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
buildings=json.loads((root/"jsons/Buildings.json").read_text(encoding="utf-8"))
by_name={b["name"]:b for b in buildings}
for name,health in {"Aqueduct":2,"Herbalist":1,"Infirmary":3,"Forge":-1}.items():
    assert by_name[name]["emmHealth"] == health
    assert by_name[name].get("food",0) == 0, f"{name}: health must not be raw food"
for name,crime in {"Courthouse":-10,"Market":5,"Gambling House":5,
                   "Inn":5,"Public Baths":5,"Tavern":5,
                   "Tavern Grigori":5,"Warrens":-5}.items():
    assert by_name[name]["emmCrime"] == crime
for name,rate in {"Herbalist":10,"Infirmary":25,"Inn":25}.items():
    assert by_name[name]["emmCityHealingPercent"] == rate
for name,resources in {"Herbalist":["Spices"],"Granary":["Wheat"],"Smokehouse":["Cattle","Sheep","Deer"],"Harbor":["Fish"]}.items():
    assert by_name[name]["emmHealthResourceBonuses"] == resources
assert by_name["Dungeon"]["emmCrime"] == -10
assert by_name["Dungeon"]["emmWarWearinessPercent"] == -25
overlay=(root/"engine/apply_overlay.py").read_text(encoding="utf-8")
assert "var emmHealth = 0" in overlay
assert "var emmHealthResourceBonuses = ArrayList<String>()" in overlay
assert "city.civ.getResourceAmount(resource) > 0" in overlay
assert "var emmCityHealingPercent = 0" in overlay
assert "healing = healing * (100 + healingPercent) / 100" in overlay
assert "populationUnhealth - buildingHealth" in overlay
assert "var emmCrime = 0" in overlay
assert "var emmWarWearinessPercent = 0" in overlay
assert "emmWarWearinessByEnemy" in overlay
assert 'newHappinessList["EMM War Weariness"] = -warUnhappiness' in overlay
assert "emmWarWearinessMultiplier" in overlay
assert "(score - 100).coerceAtLeast(0)" in overlay
assert "!attacker.getCivInfo().isBarbarian" in overlay
assert "attacker.unit.emmSummonTurnsLeft == 0" in overlay
units=json.loads((root/"jsons/Units.json").read_text(encoding="utf-8"))
units_by_name={u["name"]:u for u in units}
for name in ("Beastmaster","Lizardman Beastmaster","Myconid"):
    assert "Can only be built <in cities with a [Grove]>" in units_by_name[name].get("uniques",[]), name
for name in ("Tavern","Tavern Grigori"):
    assert by_name[name]["happiness"] == 1, name
print(f"EMM city buildings: {len(buildings)} examined, health conversion and crime/war metadata verified")
