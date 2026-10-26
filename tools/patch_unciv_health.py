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
nations=json.loads(Path('jsons/Nations.json').read_text())
expansive=sorted(n['name'] for n in nations if 'Expansive' in n.get('uniqueName','').split(', ') )
assert int(next(t['fields']['iHealth'] for t in source['groups']['traits']['entries'] if t['id']=='TRAIT_EXPANSIVE'))==3
expansive_set='setOf('+', '.join('"'+n+'"' for n in expansive)+')'
resource_names={r['name'] for r in json.loads(Path('jsons/TileResources.json').read_text())}
health_resources={}
for row in source['groups']['resources']['entries']:
    amount=int(row['fields'].get('iHealth','0'))
    if not amount:continue
    name=' '.join(x.capitalize() for x in row['id'].removeprefix('BONUS_').split('_'))
    if name=='Cow':name='Cattle'
    if name.startswith('Mana '):name=name[5:]+' Mana'
    if name in resource_names:health_resources[name]=amount
assert health_resources.get('Cattle')==1 and health_resources.get('Creation Mana')==1 and health_resources.get('Life Mana')==1
resource_map='mapOf('+', '.join(f'"{name}" to {amount}' for name,amount in sorted(health_resources.items()))+')'
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
            val expansiveHealth = if (city.civ.civName in EMM_EXPANSIVE_CIVS) 3 else 0
            val resourceHealth = EMM_RESOURCE_HEALTH.entries.sumOf { (name, value) ->
                if (city.civ.getResourceAmount(name) > 0) value else 0
            }
            val healthySources = 2 + buildingHealth + expansiveHealth + resourceHealth
            // Remove old temporary Food bonuses standing in for health buildings.
            // Only the health-enabled EMM ruleset gets this correction.
            val outdatedFoodProxy =
                (if ("Aqueduct" in built) 1 else 0) +
                (if ("Herbalist" in built) 1 else 0) +
                (if ("Infirmary" in built) 2 else 0)
            if (outdatedFoodProxy > 0)
                newFinalStatList.add("Replace health Food proxies", Stats(food = -outdatedFoodProxy.toFloat()))
            val netUnhealthy = (unhealthyPopulation - healthySources).coerceAtLeast(0)
            if (netUnhealthy > 0)
                newFinalStatList.add("Unhealthiness", Stats(food = -netUnhealthy.toFloat()))
        }'''
assert s.count(anchor)==1,'Pinned CityStats changed, refusing unsafe patch'
replacement=replacement.replace('EMM_HEALTH_MAP',health_map)
replacement=replacement.replace('EMM_EXPANSIVE_CIVS',expansive_set)
replacement=replacement.replace('EMM_RESOURCE_HEALTH',resource_map)
s=s.replace(anchor,replacement)
path.write_text(s)
print('Patched',path)
