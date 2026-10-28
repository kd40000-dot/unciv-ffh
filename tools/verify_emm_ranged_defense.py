#!/usr/bin/env python3
"""Source-fixture regression for EMM improvement-based ranged defense."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess, sys

source = Path("tools/patch_emm_ranged_defense.py").read_text()
expected = {
    "Castle": (2, 10),
    "Citadel": (3, 15),
    "Fort": (1, 5),
    "Goblin Fort": (1, 5),
    "Odios Prison": (3, 25),
    "Pirate Harbor": (1, 5),
    "Pirate Port": (2, 10),
}
for name, values in expected.items():
    assert f'"{name}" to ({values[0]} to {values[1]})' in source
with TemporaryDirectory() as temp:
    root = Path(temp)
    kt = root / "core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
    kt.parent.mkdir(parents=True)
    kt.write_text("rangedDefense = city.emmRangedDefense")
    for _ in range(2):
        subprocess.run([sys.executable, "tools/patch_emm_ranged_defense.py", temp], check=True)
    result = (root / "core/src/com/unciv/logic/city/EmmRangedDefense.kt").read_text()
    assert "for (plot in center.getTilesInDistance(6))" in result
    assert "dx > 3 || dy > 3" in result
    assert "dx > values.first || dy > values.first" in result
    assert "plot.getOwner() != city.civ" in result
    assert "plot.improvementIsPillaged" in result
    assert "city.civ.isAtWarWith(it.civ)" in result
    assert "values.second > maximum" in result
    assert "EmmRangedDefense.forCity(city)" in kt.read_text()
print("PASS: seven pinned ranged defenses and generated Kotlin integration")
