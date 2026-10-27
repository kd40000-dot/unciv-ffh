#!/usr/bin/env python3
"""Persist EMM's explicit unit level and advance on purchased promotions.

EMM CvUnit::changeLevel(1) occurs upon choosing a genuine level-up
promotion, not simply because the unit has acquired free racial promotions.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
unit=root/"core/src/com/unciv/logic/map/mapunit/MapUnit.kt"
prom=root/"core/src/com/unciv/logic/map/mapunit/UnitPromotions.kt"
u=unit.read_text()
p=prom.read_text()
if "var emmLevel: Int = 1" not in u:
    anchor="    var health: Int = 100"
    assert u.count(anchor)==1
    u=u.replace(anchor,anchor+'''
    /** Serialized Civ IV level. Unlike Unciv promotions, free promotions do not raise it. */
    var emmLevel: Int = 1''')
    anchor="        newUnit.health = health"
    assert u.count(anchor)==1
    u=u.replace(anchor,anchor+"\n        newUnit.emmLevel = emmLevel")
    unit.write_text(u)
if "unit.emmLevel++" not in p:
    anchor='''                XP -= xpForNextPromotion()
                numberOfPromotions++'''
    assert p.count(anchor)==1
    # EMM grants one level for a purchased promotion; free racial/status
    # promotions must not inflate the level.
    p=p.replace(anchor,anchor+"\n                unit.emmLevel++")
    prom.write_text(p)
typed=root/"core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
t=typed.read_text()
anchor="level = unit.promotions.numberOfPromotions + 1,"
assert t.count(anchor)==1 or "level = unit.emmLevel," in t
if anchor in t:
    typed.write_text(t.replace(anchor,"level = unit.emmLevel,"))
print("Installed serialized EMM level on units, purchased promotions and copy/upgrade")
