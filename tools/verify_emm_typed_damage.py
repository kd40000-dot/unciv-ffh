#!/usr/bin/env python3
"""Static source tests for the EMM typed damage adapter."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys

source=json.loads(Path("docs/data/emm-typed-resistances.json").read_text())
resists=source["promotionResistances"]
assert len(resists)==34
assert resists["PROMOTION_DEMON"]["DAMAGE_DEATH"]==100
assert resists["PROMOTION_UNDEAD"]["DAMAGE_DEATH"]==100
assert resists["PROMOTION_ANGEL"]["DAMAGE_DEATH"]==50
assert resists["PROMOTION_MAGIC_RESISTANCE"]["DAMAGE_DEATH"]==20
assert resists["PROMOTION_STONESKIN"]["DAMAGE_DEATH"]==50
with TemporaryDirectory() as dirname:
    root=Path(dirname)
    (root/"core/src/com/unciv/logic/map/mapunit").mkdir(parents=True)
    subprocess.run([sys.executable,"tools/patch_emm_typed_damage.py",str(root)],check=True)
    kotlin=(root/"core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt").read_text()
    assert "object EmmTypedDamage" in kotlin
    assert "fun applyToUnit(" in kotlin
    assert "EmmCityDefense.defenseModifier(" in kotlin
    assert "occupied = city.isInResistance()" in kotlin
    assert "buildingDefense = city.getStrength().toInt()" in kotlin  # Before persistent-defense postpatch
    assert "typedResistance = resistance(unit.promotions.promotions, type)" in kotlin
    assert "if (amount > 0) unit.takeDamage(amount)" in kotlin
    assert "random.nextInt(initialDamage) + random.nextInt(initialDamage)" in kotlin
    assert "typedResistance.coerceIn(-100, 100)" in kotlin
    assert "cityDefense / 4" in kotlin
    assert '"Demon" to mapOf(' in kotlin
    assert '"DAMAGE_DEATH" to 100' in kotlin
print("PASS: 34 source-derived typed resistance records, kernel formula and generation")
print("NOTE: no-caster direct damage callers, source level/defense context and gameplay QA are separate.")
