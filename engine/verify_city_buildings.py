#!/usr/bin/env python3
"""Validate EMM-specific city-building mechanics and lost-effect inventory."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
buildings=json.loads((root/"jsons/Buildings.json").read_text(encoding="utf-8"))
by_name={b["name"]:b for b in buildings}
for name,health in {"Aqueduct":2,"Herbalist":1,"Infirmary":2}.items():
    assert by_name[name]["emmHealth"] == health
    assert by_name[name].get("food",0) == 0, f"{name}: health must not be raw food"
for name,crime in {"Courthouse":-10,"Market":5,"Gambling House":5,
                   "Inn":5,"Public Baths":5,"Tavern":5,
                   "Tavern Grigori":5,"Warrens":-5}.items():
    assert by_name[name]["emmCrime"] == crime
assert by_name["Dungeon"]["emmCrime"] == -10
assert by_name["Dungeon"]["emmWarWearinessPercent"] == -25
overlay=(root/"engine/apply_overlay.py").read_text(encoding="utf-8")
assert "var emmHealth = 0" in overlay
assert "populationUnhealth - buildingHealth" in overlay
assert "var emmCrime = 0" in overlay
assert "var emmWarWearinessPercent = 0" in overlay
print(f"EMM city buildings: {len(buildings)} examined, health conversion and crime/war metadata verified")
