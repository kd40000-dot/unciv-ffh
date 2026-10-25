#!/usr/bin/env python3
"""Static verification of initial persistent EMM event runtime."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
overlay=(root/"engine/apply_overlay.py").read_text(encoding="utf-8")
required=(
    "var emmEventLastTurn = HashMap<String, Int>()",
    "var emmEventCheckedTurn = -1",
    "if (city.emmEventCheckedTurn == turn) continue",
    "city.emmEventLastTurn[\"Crime Incident\"] = turn",
    "val crime = city.cityStats.emmCrimeModifier",
    "val incidentChance = (5 + crime).coerceIn(0, 30)",
    "turn - last >= 15",
    "civInfo.addGold(-10)",
)
for signature in required:
    assert signature in overlay, signature
assert overlay.count('        for (city in civInfo.cities) city.hasSoldBuildingThisTurn = false') == 1
print("Native event scheduling: persistent state, once-per-turn and crime trigger checks wired")
