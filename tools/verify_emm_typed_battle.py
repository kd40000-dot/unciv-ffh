#!/usr/bin/env python3
"""Fixture regression for typed battle attack and counterattack integration."""
from pathlib import Path
import subprocess
import sys
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    target=Path(tmp)/"core/src/com/unciv/logic/battle/BattleDamage.kt"
    target.parent.mkdir(parents=True)
    target.write_text('''object BattleDamage {
    /**
     * Includes attack modifiers
     */
    fun testAttack() {
        return max(1f, attacker.getAttackingStrength(defender) * attackModifier)
    }
    fun testDefense() {
        return max(1f, defender.getDefendingStrength(attacker) * defenceModifier)
    }
}
''')
    for _ in range(2):
        subprocess.run([sys.executable,"tools/patch_emm_typed_battle.py",tmp],check=True)
    kotlin=target.read_text()
    assert kotlin.count("private fun emmTypedStrengthMultiplier(")==1
    assert "emmTypedStrengthMultiplier(attacker, defender)" in kotlin
    assert "emmTypedStrengthMultiplier(defender, attacker)" in kotlin
    assert 'buildings.containsKey("Herbalist")' in kotlin
    assert "EmmTypedDamage.unitTypedComponents(own.unit)" in kotlin
    assert "EmmTypedDamage.resistedCombatStrength(" in kotlin
    assert "takeDamage(" not in kotlin
print("PASS: typed battle strength applies on attacker and defender, guarded, idempotent, no extra damage")
