#!/usr/bin/env python3
"""Check EMM source bombard-rate conversion and live UnitActions plumbing."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess,sys
s=Path("tools/patch_emm_siege_bombard.py").read_text()
assert "iBombardRate" in s and "EmmCityDefense.bombard(target, rate, false, total)" in s
with TemporaryDirectory() as temp:
    p=Path(temp)
    emm=p/"emm"
    xml=emm/"XML/Units/CIV4UnitInfos.xml"
    xml.parent.mkdir(parents=True)
    xml.write_text("""<Civ4UnitInfos xmlns="x-schema:CIV4UnitSchema.xml"><UnitInfos>
      <UnitInfo><Type>UNIT_WARRIOR</Type><iBombardRate>12</iBombardRate></UnitInfo>
      <UnitInfo><Type>UNIT_WORKER</Type><iBombardRate>0</iBombardRate></UnitInfo>
    </UnitInfos></Civ4UnitInfos>""")
    subprocess.run(["git","init","-q",str(emm)],check=True)
    subprocess.run(["git","-C",str(emm),"add","."],check=True)
    subprocess.run(["git","-C",str(emm),"-c","user.name=test",
                    "-c","user.email=test@example.invalid","commit","-qm","fixture"],check=True)
    sha=subprocess.check_output(["git","-C",str(emm),"rev-parse","HEAD"],text=True).strip()
    fixture=p/"fixture.py"
    fixture.write_text(s.replace("60b0ec3740083162aaab7bf8491761a54a65a610",sha))
    root=p/"engine"
    action=root/"core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt"
    action.parent.mkdir(parents=True)
    action.write_text("        yieldAll(UnitActionsUpgrade.getUpgradeActions(unit))")
    model=root/"core/src/com/unciv/models/UnitAction.kt"
    model.parent.mkdir(parents=True)
    model.write_text('    Pillage("Pillage"),')
    ui=root/"core/src/com/unciv/ui/screens/worldscreen/unit/actions/UiUnitAction.kt"
    ui.parent.mkdir(parents=True)
    ui.write_text('    Pillage(UnitActionType.Pillage, portrait("Pillage"), false, useFrequency = 65f),')
    automation=root/"core/src/com/unciv/logic/automation/unit/UnitAutomation.kt"
    automation.parent.mkdir(parents=True)
    automation.write_text("        // if there is an attackable unit in the vicinity, attack!")
    for _ in range(2):
        subprocess.run([sys.executable,str(fixture),str(root),str(emm)],check=True)
    generated=(root/"core/src/com/unciv/logic/city/EmmSiegeBombard.kt").read_text()
    assert '"Warrior" to 12' in generated
    assert "unit.attacksThisTurn += 1" in generated
    assert "unit.useMovementPoints(1f)" in generated
    assert "isAtWarWith(it.civ)" in generated
    assert action.read_text().count("EmmSiegeBombard.actions(unit)") == 1
    assert automation.read_text().count("EmmSiegeBombard.tryAutomatedBombard(unit)") == 1
    assert "fun tryAutomatedBombard(unit: MapUnit)" in generated
    assert "unit.isEmbarked() || unit.isTransported" in generated
    assert model.read_text().count('Bombard("Bombard")') == 1
    assert ui.read_text().count('Bombard(UnitActionType.Bombard') == 1
print("PASS: EMM bombard-rate data, player action and idempotent patching")
