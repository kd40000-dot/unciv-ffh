#!/usr/bin/env python3
"""EMM city defense bombardment state and turn recovery postpatch.

Authoritative operations: CvCity::changeDefenseDamage, changeDefenseModifier,
CvCity::doTurn, CvUnit::bombard. Installs callable engine API (bombard attack
binding to full unit actions is a separate step).
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
city=root/"core/src/com/unciv/logic/city/City.kt"
turn=root/"core/src/com/unciv/logic/city/managers/CityTurnManager.kt"
kernel=root/"core/src/com/unciv/logic/city/EmmCityDefense.kt"
c=city.read_text()
if "var emmBombardedThisTurn" not in c:
    a="    var emmDefenseDamage: Int = 0"
    assert c.count(a)==1
    c=c.replace(a,a+'''
    // CvCity::isBombarded, blocks recovery during a bombardment turn.
    var emmBombardedThisTurn: Boolean = false
    var emmLastDefenseDamage: Int = 0''')
    a="        toReturn.emmDefenseDamage = emmDefenseDamage"
    assert c.count(a)==1
    c=c.replace(a,a+'''
        toReturn.emmBombardedThisTurn = emmBombardedThisTurn
        toReturn.emmLastDefenseDamage = emmLastDefenseDamage''')
    city.write_text(c)
k=kernel.read_text()
if "fun changeDefenseDamage(city: City," not in k:
    anchor="    fun totalDefense("
    assert k.count(anchor)==1
    addition='''    /** CvCity::changeDefenseDamage clamps the persisted value. */
    fun changeDefenseDamage(city: City, change: Int) {
        if (change == 0) return
        city.emmDefenseDamage = (city.emmDefenseDamage + change)
            .coerceIn(0, city.emmMaxDefenseDamage.coerceAtLeast(1))
        if (change > 0) city.emmBombardedThisTurn = true
    }

    /** CvCity::changeDefenseModifier: truncating integer arithmetic. */
    fun changeDefenseModifier(city: City, change: Int, total: Int) {
        if (change == 0 || total <= 0) return
        changeDefenseDamage(city, -(city.emmMaxDefenseDamage * change) / total)
    }

    /** CvUnit::bombard: source rate reduced by building bombard defense. */
    fun bombard(city: City, bombardRate: Int, buildingBombardDefense: Int,
                ignoreBuildingDefense: Boolean, total: Int) {
        val reduction = if (ignoreBuildingDefense) 0 else buildingBombardDefense
        val effective = -(bombardRate * (100 - reduction).coerceAtLeast(0) / 100)
        changeDefenseModifier(city, effective, total)
    }

    /** CvCity::doTurn: repair only if no bombard occurred since last turn. */
    fun startCityTurn(city: City, healRate: Int) {
        if (!city.emmBombardedThisTurn)
            changeDefenseDamage(city, -healRate.coerceAtLeast(0))
        city.emmLastDefenseDamage = city.emmDefenseDamage
        city.emmBombardedThisTurn = false
    }

'''
    k=k.replace(anchor,addition+anchor)
    kernel.write_text(k)
t=turn.read_text()
if "EmmCityDefense.startCityTurn" not in t:
    # Civ IV base GlobalDefines.xml CITY_DEFENSE_DAMAGE_HEAL_RATE = 5;
    # EMM does not override the key in its GlobalDefinesAlt.xml.
    anchor='''        city.clearCaches()'''
    assert t.count(anchor)>=1
    t=t.replace(anchor,'''        com.unciv.logic.city.EmmCityDefense.startCityTurn(city, 5)
'''+anchor,1)
    turn.write_text(t)
print("Installed persisted EMM bombardment state and live turn hook (default Civ IV heal rate 5)")
