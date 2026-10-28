#!/usr/bin/env python3
"""Wire EMM CvPlot::getRangeDefense(getTeam(), 3, false, true) into city damage.

Values transcribed from pinned XML/Terrain/CIV4ImprovementInfos.xml.
Exact source rules: only same-team, unoccupied-by-enemy improvement plots;
center excluded; range applies separately to dx and dy; maximum, not sum.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream-unciv")
file = root / "core/src/com/unciv/logic/city/EmmRangedDefense.kt"
file.parent.mkdir(parents=True, exist_ok=True)
kotlin = '''package com.unciv.logic.city

import kotlin.math.abs

/** CvPlot::getRangeDefense, EMM pinned commit 60b0ec37.
 * bFinal=false, bExcludeCenter=true and iRange=3.
 */
object EmmRangedDefense {
    private val improvements = mapOf(
        "Castle" to (2 to 10),
        "Citadel" to (3 to 15),
        "Fort" to (1 to 5),
        "Goblin Fort" to (1 to 5),
        "Odios Prison" to (3 to 25),
        "Pirate Harbor" to (1 to 5),
        "Pirate Port" to (2 to 10)
    )

    fun forCity(city: City): Int {
        val center = city.getCenterTile()
        var maximum = 0
        // A radius of six covers the EMM 7x7 grid's farthest axial
        // coordinate; filter by the exact two per-axis source checks below.
        for (plot in center.getTilesInDistance(6)) {
            val dx = abs(plot.position.x - center.position.x)
            val dy = abs(plot.position.y - center.position.y)
            if (dx == 0 && dy == 0) continue
            if (dx > 3 || dy > 3) continue
            if (plot.getOwner() != city.civ) continue
            if (plot.improvementIsPillaged) continue
            val values = improvements[plot.improvement] ?: continue
            if (dx > values.first || dy > values.first) continue
            if (plot.getUnits().any { city.civ.isAtWarWith(it.civ) }) continue
            if (values.second > maximum) maximum = values.second
        }
        return maximum
    }
}
'''
if not file.exists() or file.read_text() != kotlin:
    file.write_text(kotlin)
typed = root / "core/src/com/unciv/logic/map/mapunit/EmmTypedDamage.kt"
s = typed.read_text()
old = "rangedDefense = city.emmRangedDefense"
new = "rangedDefense = com.unciv.logic.city.EmmRangedDefense.forCity(city)"
if old in s:
    s = s.replace(old, new)
else:
    assert new in s, "Missing ranged-defense insertion anchor"
typed.write_text(s)
print("Integrated source-range EMM improvement defense in city typed damage")
