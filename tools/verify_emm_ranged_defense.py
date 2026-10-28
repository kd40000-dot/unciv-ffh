#!/usr/bin/env python3
"""Source-fixture regression for EMM improvement-based ranged defense."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess, sys
import xml.etree.ElementTree as ET

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
if len(sys.argv) > 1:
    improvement_xml = Path(sys.argv[1]) / "XML/Terrain/CIV4ImprovementInfos.xml"
    tree = ET.parse(improvement_xml).getroot()
    def local(tag):
        return tag.rsplit("}", 1)[-1]
    def get(entry, name):
        return next((child.text for child in entry if local(child.tag) == name), None)
    records = {}
    for entry in tree.iter():
        if local(entry.tag) != "ImprovementInfo":
            continue
        key = get(entry, "Type")
        rng = int(get(entry, "iRange") or 0)
        bonus = int(get(entry, "iRangeDefenseModifier") or 0)
        if key and bonus:
            records[key.removeprefix("IMPROVEMENT_").replace("_", " ").title()] = (rng, bonus)
    assert records == expected, (records, expected)
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
