#!/usr/bin/env python3
"""Persist the independent EMM city defensive inputs, never alias City.strength.

EMM CvCity has separate building/natural/owner/ranged defense and bombardment
state. Those should not be inferred from Unciv's city combat strength.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
city=root/"core/src/com/unciv/logic/city/City.kt"
typed=root/"core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
c=city.read_text()
if "var emmBuildingDefense:" not in c:
    anchor="    var health = 200"
    assert c.count(anchor)==1
    c=c.replace(anchor,anchor+'''
    // EMM CvCity independent defense state; source mechanics will populate these.
    var emmBuildingDefense: Int = 0
    var emmNaturalDefense: Int = 0
    var emmOwnerDefense: Int = 0
    var emmRangedDefense: Int = 0
    var emmDefenseDamage: Int = 0
    var emmMaxDefenseDamage: Int = 100''')
    anchor="        toReturn.health = health"
    assert c.count(anchor)==1
    c=c.replace(anchor,anchor+'''
        toReturn.emmBuildingDefense = emmBuildingDefense
        toReturn.emmNaturalDefense = emmNaturalDefense
        toReturn.emmOwnerDefense = emmOwnerDefense
        toReturn.emmRangedDefense = emmRangedDefense
        toReturn.emmDefenseDamage = emmDefenseDamage
        toReturn.emmMaxDefenseDamage = emmMaxDefenseDamage''')
    city.write_text(c)
t=typed.read_text()
changes={
"buildingDefense = city.getStrength().toInt()":"buildingDefense = city.emmBuildingDefense",
"naturalDefense = 0":"naturalDefense = city.emmNaturalDefense",
"ownerDefense = 0":"ownerDefense = city.emmOwnerDefense",
"rangedDefense = 0":"rangedDefense = city.emmRangedDefense",
"defenseDamage = 0":"defenseDamage = city.emmDefenseDamage",
"maximumCityDefenseDamage = 100":"maximumCityDefenseDamage = city.emmMaxDefenseDamage.coerceAtLeast(1)"
}
for old,new in changes.items():
    if old in t: t=t.replace(old,new)
    else: assert new in t,old
t=t.replace('''            // These two runtime inputs are exact Unciv state (built defenses,
            // resistance). Civ IV culture/ranged/owner modifiers and bombardment
            // state still require their own EMM source integrations.''','''            // Independent persisted EMM city state: never confuse
            // Unciv's city combat strength with Civ IV building defense.''')
typed.write_text(t)
print("Connected persisted EMM city-defense fields to typed unit damage")
