#!/usr/bin/env python3
"""Populate EMM natural city defense from its seven XML culture-level tiers."""
from pathlib import Path
import json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
data=json.loads(Path("docs/data/emm-culture-defense.json").read_text())
assert data["sourceCommit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
levels=data["cultureDefenseLevels"]
assert len(levels)==7
city=root/"core/src/com/unciv/logic/city/City.kt"
defense=root/"core/src/com/unciv/logic/city/EmmCityDefense.kt"
c=city.read_text()
if "var emmCultureLevel: String" not in c:
    a="    var emmNaturalDefense: Int = 0"
    assert c.count(a)==1
    c=c.replace(a,a+'''
    var emmCultureLevel: String = "CULTURELEVEL_NONE"''')
    a="        toReturn.emmNaturalDefense = emmNaturalDefense"
    assert c.count(a)==1
    c=c.replace(a,a+"\n        toReturn.emmCultureLevel = emmCultureLevel")
    city.write_text(c)
d=defense.read_text()
if "fun naturalDefenseForCulture" not in d:
    a="object EmmCityDefense {"
    assert d.count(a)==1
    rows="\n".join('        "%s" to %s,' %(x["id"],x["defense"]) for x in levels)
    d=d.replace(a,a+'''
    private val sourceCultureDefense = mapOf(
'''+rows+'''
    )
    fun naturalDefenseForCulture(level: String): Int =
        sourceCultureDefense[level] ?: 0
''')
    defense.write_text(d)
typed=root/"core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
t=typed.read_text()
a="naturalDefense = city.emmNaturalDefense"
b="naturalDefense = com.unciv.logic.city.EmmCityDefense.naturalDefenseForCulture(city.emmCultureLevel)"
if a in t: t=t.replace(a,b)
else: assert b in t
typed.write_text(t)
print("Installed pinned seven-level culture-defense mapping and persisted city culture tier")
