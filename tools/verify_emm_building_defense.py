#!/usr/bin/env python3
"""Exercise EMM building-defense generator with a synthetic source fixture."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys

source = Path("tools/patch_emm_building_defense.py").read_text()
assert "iDefense" in source and "iAllCityDefense" in source
assert "getBuiltBuildings()" in source
assert "EmmBuildingDefense.local(city)" in source
assert "EmmBuildingDefense.empire(city)" in source
with TemporaryDirectory() as temp:
    home = Path(temp)
    upstream = home / "upstream"
    xml = home / "emm/XML/Buildings/CIV4BuildingInfos.xml"
    xml.parent.mkdir(parents=True)
    xml.write_text("""<Civ4BuildingInfos><BuildingInfos>
      <BuildingInfo><Type>BUILDING_PALACE</Type><iDefense>30</iDefense><iAllCityDefense>5</iAllCityDefense></BuildingInfo>
      <BuildingInfo><Type>BUILDING_EXAMPLE</Type><iDefense>0</iDefense><iAllCityDefense>0</iAllCityDefense></BuildingInfo>
    </BuildingInfos></Civ4BuildingInfos>""")
    subprocess.run(["git", "init", "-q", str(home / "emm")], check=True)
    subprocess.run(["git", "-C", str(home / "emm"), "add", "."], check=True)
    subprocess.run(["git", "-C", str(home / "emm"), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], check=True)
    rev = subprocess.check_output(["git", "-C", str(home / "emm"), "rev-parse", "HEAD"], text=True).strip()
    # Only the fixture copy permits its synthetic SHA; production enforces pinned EMM.
    fixture_script = home / "fixture.py"
    fixture_script.write_text(source.replace(
        "60b0ec3740083162aaab7bf8491761a54a65a610", rev
    ))
    typed = upstream / "core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
    typed.parent.mkdir(parents=True)
    typed.write_text("buildingDefense = city.emmBuildingDefense,\nownerDefense = city.emmOwnerDefense")
    for _ in range(2):
        subprocess.run([sys.executable, str(fixture_script), str(upstream), str(home / "emm")],
                       check=True)
    kotlin = (upstream / "core/src/com/unciv/logic/city/EmmBuildingDefense.kt").read_text()
    updated = typed.read_text()
    assert '"Palace" to (30 to 5)' in kotlin
    assert "getBuiltBuildings()" in kotlin
    assert "city.civ.cities.sumOf" in kotlin
    assert "EmmBuildingDefense.local(city)" in updated
    assert "EmmBuildingDefense.empire(city)" in updated
    assert "city.emmBuildingDefense" not in updated
print("PASS: building defense XML mapping, live integration and generator idempotence")
