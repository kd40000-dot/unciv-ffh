#!/usr/bin/env python3
"""Generate EMM building bombard resistance from pinned source XML.

CvCity::getBuildingBombardDefense sums each built building's
CvBuildingInfo::getBombardDefenseModifier. Kept distinct from city-strength
and from the ordinary building defensive percentage.
"""
from pathlib import Path
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-unciv")
emm = Path(sys.argv[2] if len(sys.argv) > 2 else "upstream-emm")
revision = subprocess.check_output(["git", "-C", str(emm), "rev-parse", "HEAD"], text=True).strip()
assert revision == "60b0ec3740083162aaab7bf8491761a54a65a610", revision
def tag(element):
    return element.tag.rsplit("}", 1)[-1]
def field(entry, name, default=None):
    return next((child.text for child in entry if tag(child) == name), default)
def normal(name):
    return re.sub(r"[^A-Z0-9]", "", name.upper().removeprefix("BUILDING_"))
entries = ET.parse(emm / "XML/Buildings/CIV4BuildingInfos.xml").getroot()
bonuses = {}
for entry in entries.iter():
    if tag(entry) != "BuildingInfo":
        continue
    key = field(entry, "Type")
    value = int(field(entry, "iBombardDefense", "0") or 0)
    if key and value:
        bonuses[key] = value
assert bonuses, "Pinned XML contains no bombard defense values"
imported = json.loads(Path("jsons/Buildings.json").read_text())
mapped = {}
for building in imported:
    names = [building["name"], building.get("replaces") or ""]
    matches = [key for key in bonuses if any(normal(key) == normal(name) for name in names if name)]
    assert len(matches) <= 1, (building["name"], matches)
    if matches:
        mapped[building["name"]] = bonuses[matches[0]]
destination = root / "core/src/com/unciv/logic/city/EmmBombardProtection.kt"
destination.parent.mkdir(parents=True, exist_ok=True)
lines = ",\n".join(f'        {json.dumps(k)} to {v}' for k,v in sorted(mapped.items()))
content = '''package com.unciv.logic.city

/** Sum of original EMM iBombardDefense from current city buildings.
 * CvCity::m_iBuildingBombardDefense is recomputed from owned buildings
 * so sold, captured and removed structures cannot leave stale state.
 */
object EmmBombardProtection {
    private val sourceBonuses = mapOf(
%s
    )
    fun forCity(city: City): Int =
        city.cityConstructions.getBuiltBuildings().sumOf {
            sourceBonuses[it.name] ?: 0
        }
}
''' % lines
if not destination.exists() or destination.read_text() != content:
    destination.write_text(content)
defense = root / "core/src/com/unciv/logic/city/EmmCityDefense.kt"
s = defense.read_text()
old = '''fun bombard(city: City, bombardRate: Int, buildingBombardDefense: Int,
                ignoreBuildingDefense: Boolean, total: Int) {
        val reduction = if (ignoreBuildingDefense) 0 else buildingBombardDefense'''
new = '''fun bombard(city: City, bombardRate: Int,
                ignoreBuildingDefense: Boolean, total: Int) {
        val reduction = if (ignoreBuildingDefense) 0 else EmmBombardProtection.forCity(city)'''
if old in s:
    s = s.replace(old, new)
else:
    assert new in s, "Cannot find original EMM bombard kernel signature"
defense.write_text(s)
print(f"Mapped {len(mapped)} of {len(bonuses)} source bombard-defense buildings")
