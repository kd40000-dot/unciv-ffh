#!/usr/bin/env python3
"""Install EMM's exact city-defense arithmetic as a reusable Kotlin kernel.

Source: pinned CvCity.cpp getTotalDefense/getDefenseModifier.
Integrating each city source (culture, ranged defenses, bombardment) remains
separate from the verified arithmetic itself.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else "upstream-unciv")
path=root/"core/src/com/unciv/logic/city/EmmCityDefense.kt"
path.parent.mkdir(parents=True,exist_ok=True)
text='''package com.unciv.logic.city

/** Port of CvCity::getTotalDefense / getDefenseModifier from pinned EMM. */
object EmmCityDefense {
    fun totalDefense(
        buildingDefense: Int,
        naturalDefense: Int,
        ownerDefense: Int,
        rangedDefense: Int,
        ignoreBuilding: Boolean = false
    ): Int = (if (ignoreBuilding) 0 else buildingDefense) +
        naturalDefense + ownerDefense + rangedDefense

    fun defenseModifier(
        buildingDefense: Int,
        naturalDefense: Int,
        ownerDefense: Int,
        rangedDefense: Int,
        defenseDamage: Int,
        maximumCityDefenseDamage: Int,
        occupied: Boolean,
        ignoreBuilding: Boolean = false
    ): Int {
        require(maximumCityDefenseDamage > 0)
        if (occupied) return 0
        val total = totalDefense(buildingDefense, naturalDefense,
            ownerDefense, rangedDefense, ignoreBuilding)
        return total * (maximumCityDefenseDamage - defenseDamage) /
            maximumCityDefenseDamage
    }
}
'''
if path.exists() and path.read_text()==text:
    print("EMM city-defense formula already present")
else:
    path.write_text(text)
    print("Installed EMM city-defense formula")
