#!/usr/bin/env python3
"""Pinned-source EMM building bombard-defense transformation regression."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess, sys
source = Path("tools/patch_emm_bombard_protection.py").read_text()
assert 'iBombardDefense' in source
assert 'EmmBombardProtection.forCity(city)' in source
with TemporaryDirectory() as folder:
    root=Path(folder)
    emm=root/"upstream-emm"
    xml=emm/"XML/Buildings/CIV4BuildingInfos.xml"
    xml.parent.mkdir(parents=True)
    xml.write_text("""<Civ4BuildingInfos xmlns="x-schema:CIV4BuildingsSchema.xml"><BuildingInfos>
      <BuildingInfo><Type>BUILDING_PALACE</Type><iBombardDefense>45</iBombardDefense></BuildingInfo>
      <BuildingInfo><Type>BUILDING_EXAMPLE</Type><iBombardDefense>0</iBombardDefense></BuildingInfo>
    </BuildingInfos></Civ4BuildingInfos>""")
    subprocess.run(["git","init","-q",str(emm)],check=True)
    subprocess.run(["git","-C",str(emm),"add","."],check=True)
    subprocess.run(["git","-C",str(emm),"-c","user.name=fixture",
                    "-c","user.email=fixture@example.invalid",
                    "commit","-qm","fixture"],check=True)
    rev=subprocess.check_output(["git","-C",str(emm),"rev-parse","HEAD"],text=True).strip()
    fixture=root/"fixture.py"
    fixture.write_text(source.replace("60b0ec3740083162aaab7bf8491761a54a65a610",rev))
    upstream=root/"upstream-unciv"
    city=upstream/"core/src/com/unciv/logic/city/EmmCityDefense.kt"
    city.parent.mkdir(parents=True)
    city.write_text("""object EmmCityDefense {
    fun bombard(city: City, bombardRate: Int, buildingBombardDefense: Int,
                ignoreBuildingDefense: Boolean, total: Int) {
        val reduction = if (ignoreBuildingDefense) 0 else buildingBombardDefense
    }
}
""")
    for _ in range(2):
        subprocess.run([sys.executable,str(fixture),str(upstream),str(emm)],check=True)
    generated=(city.parent/"EmmBombardProtection.kt").read_text()
    assert '"Palace" to 45' in generated
    assert "getBuiltBuildings()" in generated
    assert "EmmBombardProtection.forCity(city)" in city.read_text()
    assert city.read_text().count("EmmBombardProtection.forCity(city)") == 1
print("PASS: namespace-aware EMM building bombard defense mapping and idempotence")
