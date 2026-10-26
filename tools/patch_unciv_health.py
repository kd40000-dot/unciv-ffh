#!/usr/bin/env python3
"""Patch pinned Unciv CityStats with initial EMM-style city-health food accounting.

This is an explicitly limited ENGINE prototype, not complete BtS/EMM health.
It activates only when the loaded ruleset has 'Herbalist' AND 'Infirmary'.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'upstream-unciv')
path=root/'core/src/com/unciv/logic/city/CityStats.kt'
s=path.read_text()
anchor='''        val foodEaten = calcFoodEaten()
        newFinalStatList["Population"]!!.food -= foodEaten'''
replacement='''        val foodEaten = calcFoodEaten()
        newFinalStatList["Population"]!!.food -= foodEaten

        // EMM/FfH2 health prototype: unlike food-yield stand-ins, net unhealthiness
        // reduces food directly, after population consumption and before growth.
        // This ruleset guard keeps ordinary Unciv games completely unaffected.
        if (city.getRuleset().buildings.containsKey("Herbalist") &&
            city.getRuleset().buildings.containsKey("Infirmary")) {
            val unhealthyPopulation = city.population.population
            val built = city.cityConstructions.builtBuildings
            // Provisional baseline and structure mapping, subject to original EMM XML audit.
            val healthySources = 2 +
                (if ("Aqueduct" in built) 2 else 0) +
                (if ("Herbalist" in built) 2 else 0) +
                (if ("Infirmary" in built) 3 else 0)
            val netUnhealthy = (unhealthyPopulation - healthySources).coerceAtLeast(0)
            if (netUnhealthy > 0)
                newFinalStatList.add("Unhealthiness", Stats(food = -netUnhealthy.toFloat()))
        }'''
assert s.count(anchor)==1,'Pinned CityStats changed, refusing unsafe patch'
s=s.replace(anchor,replacement)
path.write_text(s)
print('Patched',path)
