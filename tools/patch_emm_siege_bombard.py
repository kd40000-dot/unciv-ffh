#!/usr/bin/env python3
"""Add player-callable city siege bombard action using source EMM bombard rates.

Scope: adjacent enemy cities. Super-Forts improvement bombard targeting, AI
selection and advanced tactical experience still require separate integration.
"""
from pathlib import Path
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
emm=Path(sys.argv[2] if len(sys.argv)>2 else "upstream-emm")
sha=subprocess.check_output(["git","-C",str(emm),"rev-parse","HEAD"],text=True).strip()
assert sha=="60b0ec3740083162aaab7bf8491761a54a65a610",sha
def name(tag): return tag.rsplit("}",1)[-1]
def fld(node,key):
    return next((child.text for child in node if name(child.tag)==key),None)
def normal(x): return re.sub(r"[^A-Z0-9]","",x.upper().removeprefix("UNIT_"))
xml=ET.parse(emm/"XML/Units/CIV4UnitInfos.xml").getroot()
source={}
for info in xml.iter():
    if name(info.tag)!="UnitInfo":continue
    typ=fld(info,"Type")
    rate=int(fld(info,"iBombardRate") or 0)
    if typ and rate>0 and typ.startswith("UNIT_"):source[typ]=rate
units=json.loads(Path("jsons/Units.json").read_text())
mapped={}
for unit in units:
    title=unit["name"]
    match=[key for key in source if normal(key)==normal(title)]
    assert len(match)<=1,(title,match)
    if match:mapped[title]=source[match[0]]
out=root/"core/src/com/unciv/logic/city/EmmSiegeBombard.kt"
out.parent.mkdir(parents=True,exist_ok=True)
rows=",\n".join("        %s to %d"%(json.dumps(k),v) for k,v in sorted(mapped.items()))
out.write_text('''package com.unciv.logic.city

import com.unciv.logic.map.mapunit.MapUnit
import com.unciv.models.UnitAction
import com.unciv.models.UnitActionType

/** Adjacent-city slice of EMM CvUnit::bombard() with source iBombardRate. */
object EmmSiegeBombard {
    private val sourceBombardRate = mapOf(
%s
    )

    /** Player and AI use identical legality and execution rules. */
    fun tryAutomatedBombard(unit: MapUnit): Boolean {
        val action = actions(unit).firstOrNull { it.action != null } ?: return false
        action.action?.invoke()
        return true
    }

    fun actions(unit: MapUnit): Sequence<UnitAction> {
        val rate = sourceBombardRate[unit.baseUnit.name] ?: return emptySequence()
        if (rate <= 0 || unit.attacksThisTurn > 0 || !unit.hasMovement()
            || unit.isEmbarked() || unit.isTransported)
            return emptySequence()
        val enemies = unit.getTile().getTilesInDistance(1)
            .filter { it.isCityCenter() }
            .mapNotNull { it.getCity() }
            .filter { it.civ != unit.civ && unit.civ.isAtWarWith(it.civ) }
            .filter { it.emmDefenseDamage < it.emmMaxDefenseDamage }
            .toList()
        return enemies.asSequence().map { target ->
            UnitAction(UnitActionType.Bombard, "Bombard " + target.name) {
                val total = EmmCityDefense.totalDefense(
                    EmmBuildingDefense.local(target),
                    EmmCityDefense.naturalDefenseForCulture(target.emmCultureLevel),
                    EmmBuildingDefense.empire(target),
                    EmmRangedDefense.forCity(target)
                )
                if (total <= 0 || !unit.hasMovement() || unit.attacksThisTurn > 0
                    || !unit.civ.isAtWarWith(target.civ)) return@UnitAction
                EmmCityDefense.bombard(target, rate, false, total)
                unit.attacksThisTurn += 1
                unit.useMovementPoints(1f)
            }
        }
    }
}
''' % rows)
actions=root/"core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt"
a=actions.read_text()
anchor="        yieldAll(UnitActionsUpgrade.getUpgradeActions(unit))"
injection="        yieldAll(com.unciv.logic.city.EmmSiegeBombard.actions(unit))\n\n"+anchor
if injection not in a:
    assert a.count(anchor)==1
    a=a.replace(anchor,injection)
    actions.write_text(a)
model=root/"core/src/com/unciv/models/UnitAction.kt"
m=model.read_text()
anchor='    Pillage("Pillage"),'
if '    Bombard("Bombard"),' not in m:
    assert m.count(anchor)==1
    model.write_text(m.replace(anchor,anchor+'\n    Bombard("Bombard"),'))
ui=root/"core/src/com/unciv/ui/screens/worldscreen/unit/actions/UiUnitAction.kt"
u=ui.read_text()
anchor='    Pillage(UnitActionType.Pillage, portrait("Pillage"), false, useFrequency = 65f),'
if '    Bombard(UnitActionType.Bombard' not in u:
    assert u.count(anchor)==1
    ui.write_text(u.replace(anchor,anchor+'\n    Bombard(UnitActionType.Bombard, portrait("Pillage"), false, useFrequency = 85f),'))
automation=root/"core/src/com/unciv/logic/automation/unit/UnitAutomation.kt"
auto=automation.read_text()
needle="        // if there is an attackable unit in the vicinity, attack!"
hook="""        // EMM: bombard enemy city defenses before conventional attacks.
        if (com.unciv.logic.city.EmmSiegeBombard.tryAutomatedBombard(unit)) return

"""
if hook not in auto:
    assert auto.count(needle)==1, "Pinned Unciv AI combat anchor moved"
    automation.write_text(auto.replace(needle,hook+needle))

print(f"Integrated adjacent city bombard action for {len(mapped)} of {len(source)} EMM bombard-rate units")
