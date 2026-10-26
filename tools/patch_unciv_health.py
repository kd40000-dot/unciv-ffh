#!/usr/bin/env python3
"""Patch pinned Unciv CityStats with initial EMM-style city-health food accounting.

This is an explicitly limited ENGINE prototype, not complete BtS/EMM health.
It activates only when the loaded ruleset has 'Herbalist' AND 'Infirmary'.
"""
from pathlib import Path
import sys
import json

root=Path(sys.argv[1] if len(sys.argv)>1 else 'upstream-unciv')
source=json.loads(Path('docs/data/emm-health-source.json').read_text())
assert source['commit']=='60b0ec3740083162aaab7bf8491761a54a65a610'
health={}
for row in source['groups']['buildings']['entries']:
    amount=int(row['fields'].get('iHealth','0'))
    if amount:
        name=' '.join(x.capitalize() for x in row['id'].removeprefix('BUILDING_').split('_'))
        health[name]=amount
assert health['Aqueduct']==2 and health['Herbalist']==1 and health['Infirmary']==3
health_map='mapOf('+', '.join(f'"{name}" to {amount}' for name,amount in sorted(health.items()))+')'
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
            // Building contributions are extracted from pinned EMM CIV4BuildingInfos.xml.
            // Base health 2 remains provisional pending handicap/terrain/feature mapping.
            val buildingHealth = EMM_HEALTH_MAP.entries.sumOf { (name, value) -> if (name in built) value else 0 }
            val healthySources = 2 + buildingHealth
            val netUnhealthy = (unhealthyPopulation - healthySources).coerceAtLeast(0)
            if (netUnhealthy > 0)
                newFinalStatList.add("Unhealthiness", Stats(food = -netUnhealthy.toFloat()))
        }'''
assert s.count(anchor)==1,'Pinned CityStats changed, refusing unsafe patch'
replacement=replacement.replace('EMM_HEALTH_MAP',health_map)
s=s.replace(anchor,replacement)
path.write_text(s)
print('Patched',path)
