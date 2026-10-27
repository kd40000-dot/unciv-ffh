#!/usr/bin/env python3
"""Regression cases for the pinned EMM CvCity defense formula."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess,sys
with TemporaryDirectory() as temp:
    subprocess.run([sys.executable,"tools/patch_emm_city_defense.py",temp],check=True)
    subprocess.run([sys.executable,"tools/patch_emm_city_defense.py",temp],check=True)
    code=(Path(temp)/"core/src/com/unciv/logic/city/EmmCityDefense.kt").read_text()
    assert "if (occupied) return 0" in code
    assert "naturalDefense + ownerDefense + rangedDefense" in code
    assert "maximumCityDefenseDamage - defenseDamage" in code
    assert "if (ignoreBuilding) 0 else buildingDefense" in code
def defense(b,n,o,r,damage,maxdamage,occupation=False,ignore=False):
    if occupation:return 0
    total=(0 if ignore else b)+n+o+r
    return total*(maxdamage-damage)//maxdamage
assert defense(25,20,10,5,0,100)==60
assert defense(25,20,10,5,50,100)==30
assert defense(25,20,10,5,0,100,True)==0
assert defense(25,20,10,5,0,100,False,True)==35
print("PASS: source city defense formula, occupancy and bombardment arithmetic")
