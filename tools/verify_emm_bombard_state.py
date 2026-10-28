#!/usr/bin/env python3
"""Idempotent fixture test for EMM defense damage and per-turn flags."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess,sys
with TemporaryDirectory() as temp:
    root=Path(temp)
    city=root/"core/src/com/unciv/logic/city/City.kt"
    city.parent.mkdir(parents=True)
    city.write_text("""class City {
    var emmDefenseDamage: Int = 0
    var emmMaxDefenseDamage: Int = 100
    fun clone(): City {
        val toReturn = City()
        toReturn.emmDefenseDamage = emmDefenseDamage
        return toReturn
    }
}
""")
    engine=root/"core/src/com/unciv/logic/city/EmmCityDefense.kt"
    engine.write_text("object EmmCityDefense {\n    fun totalDefense(buildingDefense: Int) = buildingDefense\n}\n")
    manager=root/"core/src/com/unciv/logic/city/managers/CityTurnManager.kt"
    manager.parent.mkdir(parents=True)
    manager.write_text('class CityTurnManager {\n        city.clearCaches()\n}\n')
    for _ in range(2):
        subprocess.run([sys.executable,"tools/patch_emm_bombard_state.py",temp],check=True)
    e=engine.read_text()
    result=city.read_text()
    turn=manager.read_text()
    assert result.count("var emmBombardedThisTurn") == 1
    assert result.count("toReturn.emmLastDefenseDamage") == 1
    assert "coerceIn(0, city.emmMaxDefenseDamage.coerceAtLeast(1))" in e
    assert "if (change > 0) city.emmBombardedThisTurn = true" in e
    assert "changeDefenseDamage(city, -(city.emmMaxDefenseDamage * change) / total)" in e
    assert "val effective = -(bombardRate * (100 - reduction).coerceAtLeast(0) / 100)" in e
    assert "if (!city.emmBombardedThisTurn)" in e
    assert turn.count("EmmCityDefense.startCityTurn") == 1
print("PASS: EMM persisted bombardment damage arithmetic and idempotent turn hook")
