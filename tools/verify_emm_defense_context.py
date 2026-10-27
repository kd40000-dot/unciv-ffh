#!/usr/bin/env python3
"""Static/fixture checks for pinned EMM base defense and typed combat components."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

base=json.loads(Path("docs/data/emm-unit-defense.json").read_text())
typed=json.loads(Path("docs/data/emm-typed-combat-strength.json").read_text())
assert len(base["unitBaseDefense"])==299
assert len(typed["unitCombat"])==96
assert len(typed["promotionCombat"])==14
assert base["unitBaseDefense"]["UNIT_PYRE_ZOMBIE"]==3
assert base["unitBaseDefense"]["UNIT_MUD_GOLEM"]==2
assert typed["unitCombat"]["UNIT_ANGEL"]["DAMAGE_HOLY"]==1
with tempfile.TemporaryDirectory() as temp:
    directory=Path(temp)/"core/src/com/unciv/logic/map/mapunit"
    directory.mkdir(parents=True)
    subprocess.run([sys.executable,"tools/patch_emm_typed_damage.py",temp],check=True)
    for _ in range(2):
        subprocess.run([sys.executable,"tools/patch_emm_defense_context.py",temp],check=True)
    kotlin=(directory/"EmmTypedDamage.kt").read_text()
    assert kotlin.count("private fun sourceDefense(unit: MapUnit)") == 1
    assert "val effectiveBaseDefense = sourceDefense(unit)" in kotlin
    assert "fun resistedCombatStrength(" in kotlin
    assert "scaled -= component * resist" in kotlin
    assert "fun unitTypedComponents(unit: MapUnit)" in kotlin
    assert "emmSourcePromotionCombat[key].orEmpty().values.sum()" in kotlin
    assert '"UNIT_MUD_GOLEM" to 2' in kotlin
    assert '"UNIT_ANGEL" to mapOf("DAMAGE_HOLY" to 1)' in kotlin
print("PASS: 299 EMM base-defense unit values, 96 unit and 14 promotion typed components; idempotent generation")
