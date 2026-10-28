#!/usr/bin/env python3
"""Regression contract for EMM epidemic post-patcher on a generated Kotlin fixture."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys

upstream = Path("tools/patch_emm_epidemic_damage.py")
assert upstream.is_file()
source = upstream.read_text()
assert "damageLivingUnits(game)" in source
with TemporaryDirectory() as folder:
    root = Path(folder)
    kt = root / "core/src/com/unciv/logic/city/EmmArmageddonEvents.kt"
    kt.parent.mkdir(parents=True)
    kt.write_text("""package com.unciv.logic.city
import com.unciv.logic.GameInfo
object EmmArmageddonEvents {
    fun fireBlight(game: GameInfo) {
        for (civ in game.civilizations) for (city in civ.cities) {
            city.cityStats.update()
        }
    }
    fun firePestilence(game: GameInfo) {
        for (civ in game.civilizations) for (city in civ.cities) {
            EmmCityEpidemics.pestilence(city, random, goodBuildingHealth)
            city.cityStats.update()
        }
    }
}
""")
    for _ in range(2):
        subprocess.run([sys.executable, str(upstream), str(root)], check=True)
    result = kt.read_text()
    assert result.count('damageLivingUnits(game, "Blight")') == 1
    assert result.count('damageLivingUnits(game, "Pestilence")') == 1
    assert '"EMM.Epidemic." + event' in result
    assert result.count("private fun damageLivingUnits(game: GameInfo, event: String)") == 1
    assert "EmmTypedDamage.applyToUnit(" in result
    assert 'type = "DAMAGE_DEATH"' in result
    assert "unit.takeDamage(25)" not in result
    assert "private fun isEmmLiving(" in result
    assert "unit.baseUnit.name in emmMechanizedUnits" in result
    assert "unit.promotions.promotions.count { it in emmNotAlivePromotions }" in result
    assert "if (!isEmmLiving(unit)) continue" in result
    assert "unit.baseUnit.isWaterUnit()" not in result
    assert result.count("city.cityStats.update()") == 2
print("PASS: Blight and Pestilence engine hook injection and idempotence")
print("NOTE: this tests source transformation, not Kotlin compilation or typed Death resistance")
