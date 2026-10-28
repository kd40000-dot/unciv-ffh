#!/usr/bin/env python3
"""Generate live EMM building and empire-wide city defense from pinned building XML.

Requires an EMM source checkout at the pinned revision as argv[2].
Runs after the existing city-state and culture patches.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-unciv")
emm = Path(sys.argv[2] if len(sys.argv) > 2 else "upstream-emm")
xml = emm / "XML/Buildings/CIV4BuildingInfos.xml"
assert xml.is_file(), f"Missing pinned EMM building XML: {xml}"
definitions = ET.parse(xml).getroot()
records = {}
def tag_name(element):
    return element.tag.rsplit("}", 1)[-1]

def field(entry, name, default=None):
    return next((child.text for child in entry if tag_name(child) == name), default)

for entry in definitions.iter():
    if tag_name(entry) != "BuildingInfo":
        continue
    key = field(entry, "Type")
    if not key or not key.startswith("BUILDING_"):
        continue
    local = int(field(entry, "iDefense", "0"))
    empire = int(field(entry, "iAllCityDefense", "0"))
    if local or empire:
        records[key] = (local, empire)
if not records:
    entries = [entry for entry in definitions.iter() if tag_name(entry) == "BuildingInfo"]
    print("EMM XML diagnostics:", "bytes=", xml.stat().st_size,
          "entries=", len(entries), "root=", definitions.tag,
          "first=", ET.tostring(entries[0], encoding="unicode")[:1200] if entries else "none",
          flush=True)
    raise AssertionError("No EMM building defenses parsed; inspect upstream XML format")

# Explicitly verify the source version, not just an arbitrary checkout.
# A CI checkout supplies the pinned commit; local executions can use .git.
import subprocess
rev = subprocess.run(["git", "-C", str(emm), "rev-parse", "HEAD"],
                     capture_output=True, text=True, check=True).stdout.strip()
assert rev == "60b0ec3740083162aaab7bf8491761a54a65a610", rev

def normalize(value):
    return re.sub(r"[^A-Z0-9]", "", value.upper().removeprefix("BUILDING_"))
# Identify imported buildings by their actual JSON names, not by a guessed
# correspondence to Unciv cityStrength (a different mechanic).
mod_buildings = json.loads(Path("jsons/Buildings.json").read_text())
mapped = {}
unmapped = []
for building in mod_buildings:
    name = building["name"]
    candidates = [name, building.get("replaces") or ""]
    matches = [k for k in records if any(normalize(k) == normalize(n) for n in candidates if n)]
    if len(matches) == 1:
        mapped[name] = records[matches[0]]
    elif len(matches) > 1:
        raise AssertionError(f"Ambiguous source defense: {name} -> {matches}")
for key in records:
    if not any(normalize(key) == normalize(name) for name in mapped):
        unmapped.append(key)

out = root / "core/src/com/unciv/logic/city/EmmBuildingDefense.kt"
out.parent.mkdir(parents=True, exist_ok=True)
rows = ",\n".join(
    '        "%s" to (%d to %d)' % (name.replace('\\', '\\\\').replace('"', '\\"'), local, empire)
    for name, (local, empire) in sorted(mapped.items()))
out.write_text('''package com.unciv.logic.city

/** EMM CvCity::changeBuildingDefense and CvPlayer::getCityDefenseModifier,
 * generated from pinned CIV4BuildingInfos.xml; local plus empire-wide defense.
 */
object EmmBuildingDefense {
    private val values = mapOf(
%s
    )
    fun local(city: City): Int =
        city.cityConstructions.getBuiltBuildings().sumOf { values[it.name]?.first ?: 0 }
    fun empire(city: City): Int =
        city.civ.cities.sumOf { ownedCity ->
            ownedCity.cityConstructions.getBuiltBuildings().sumOf {
                values[it.name]?.second ?: 0
            }
        }
}
''' % rows)
typed = root / "core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
s = typed.read_text()
# Recalculate from built-building state at every damage event so construction,
# sale, loss, capture, and save reload are reflected without stale caches.
replacements = {
    "buildingDefense = city.emmBuildingDefense":
        "buildingDefense = com.unciv.logic.city.EmmBuildingDefense.local(city)",
    "ownerDefense = city.emmOwnerDefense":
        "ownerDefense = com.unciv.logic.city.EmmBuildingDefense.empire(city)"
}
for before, after in replacements.items():
    if before in s:
        s = s.replace(before, after)
    else:
        assert after in s, f"Missing typed-damage anchor: {before}"
typed.write_text(s)
print(f"Integrated {len(mapped)} imported building defenses from {len(records)} source entries")
print(f"Source defense buildings without an imported matching name: {len(unmapped)}")
