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
feature_names={r['name'] for r in json.loads(Path('jsons/Terrains.json').read_text())}
feature_health={}
for row in source['groups']['features']['entries']:
    amount=int(row['fields'].get('iHealthPercent','0'))
    name=' '.join(x.capitalize() for x in row['id'].removeprefix('FEATURE_').split('_'))
    if name=='Flood Plains':name='Flood plains'
    if name in feature_names and amount:feature_health[name]=amount
assert feature_health['Forest']==50 and feature_health['Jungle']==-25 and feature_health['Flood Plains']==-40 if 'Flood Plains' in feature_health else feature_health.get('Flood plains')==-40
feature_map='mapOf('+', '.join(f'"{name}" to {amount}' for name,amount in sorted(feature_health.items()))+')'
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
difficultyBonuses = {entry['id'].removeprefix('HANDICAP_').capitalize():int(entry['fields']['iHealthBonus']) for entry in source['groups']['handicaps']['entries'] if 'iHealthBonus' in entry['fields']}
assert difficultyBonuses['Settler']==4 and difficultyBonuses['Chieftain']==3 and difficultyBonuses['Prince']==2
handicap_map='mapOf('+', '.join(f'"{name}" to {amount}' for name,amount in sorted(difficultyBonuses.items()))+')'
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
            // Difficulty health is read from pinned EMM CIV4HandicapInfo.xml.
            val handicapHealth = EMM_DIFFICULTY_HEALTH[city.civ.gameInfo.difficulty] ?: 2
            val buildingHealth = EMM_HEALTH_MAP.entries.sumOf { (name, value) -> if (name in built) value else 0 }
            val expansiveHealth = if (city.civ.civName in EMM_EXPANSIVE_CIVS) 3 else 0
            val resourceHealth = EMM_RESOURCE_HEALTH.entries.sumOf { (name, value) ->
                if (city.civ.getResourceAmount(name) > 0) value else 0
            }
            val freshwaterHealth = if (city.getCenterTile().isAdjacentTo("Fresh Water")) 2 else 0
            val featureEffects = city.getCenterTile().getTilesInDistance(2)
                .flatMap { tile -> tile.terrainFeatures.map { EMM_FEATURE_HEALTH[it] ?: 0 } }
                .toList()
            val featureHealth = featureEffects.sumOf { it.coerceAtLeast(0) } / 100
            val featureUnhealth = featureEffects.sumOf { (-it).coerceAtLeast(0) } / 100
            val healthySources = handicapHealth + buildingHealth + expansiveHealth + resourceHealth + freshwaterHealth + featureHealth
            val netUnhealthy = (unhealthyPopulation + featureUnhealth - healthySources).coerceAtLeast(0)
            if (netUnhealthy > 0)
                newFinalStatList.add("Unhealthiness", Stats(food = -netUnhealthy.toFloat()))
        }'''
assert s.count(anchor)==1,'Pinned CityStats changed, refusing unsafe patch'
replacement=replacement.replace('EMM_HEALTH_MAP',health_map)
replacement=replacement.replace('EMM_DIFFICULTY_HEALTH',handicap_map)
replacement=replacement.replace('EMM_EXPANSIVE_CIVS',expansive_set)
replacement=replacement.replace('EMM_RESOURCE_HEALTH',resource_map)
replacement=replacement.replace('EMM_FEATURE_HEALTH',feature_map)
s=s.replace(anchor,replacement)
# Shared city health state is recalculated alongside Food penalties.
field='    var currentCityStats: Stats = Stats()'
assert s.count(field)==1
s=s.replace(field, '''    var emmHealthInfo: Pair<Int, Int>? = null // (healthy, unhealthy) for city UI
    var emmHealthBreakdown: Map<String, Int> = emptyMap()
'''+field)
s=s.replace('        val foodEaten = calcFoodEaten()', '''        emmHealthInfo = null
        emmHealthBreakdown = emptyMap()
        val foodEaten = calcFoodEaten()''', 1)
s=s.replace('            val netUnhealthy = (unhealthyPopulation + featureUnhealth - healthySources).coerceAtLeast(0)', '''            val totalUnhealthy = unhealthyPopulation + featureUnhealth
            emmHealthInfo = healthySources to totalUnhealthy
            emmHealthBreakdown = linkedMapOf(
                "Difficulty health" to handicapHealth,
                "Buildings" to buildingHealth,
                "Expansive trait" to expansiveHealth,
                "Connected resources" to resourceHealth,
                "Fresh water" to freshwaterHealth,
                "Forests and features (healthy)" to featureHealth,
                "Population" to -unhealthyPopulation,
                "Unhealthy features" to -featureUnhealth
            )
            val netUnhealthy = (totalUnhealthy - healthySources).coerceAtLeast(0)''')
path.write_text(s)
# Expose the read-only health figures on CityView for both city widgets.
view=root/'core/src/com/unciv/view/CityView.kt'
v=view.read_text()
needle='    @Readonly fun getCurrentCityStats(): Stats = city.cityStats.currentCityStats'
assert v.count(needle)==1
v=v.replace(needle,needle+'\n    @Readonly fun getEmmHealthInfo(): Pair<Int, Int>? = city.cityStats.emmHealthInfo\n    @Readonly fun getEmmHealthBreakdown(): Map<String, Int> = city.cityStats.emmHealthBreakdown')
view.write_text(v)
# Show city health at all population sizes, not only during starvation.
ui=root/'core/src/com/unciv/ui/screens/cityscreen/CityStatsTable.kt'
u=ui.read_text()
needle='        lowerTable.add(unassignedPopLabel).row()'
assert u.count(needle)==1
u=u.replace(needle, '''        cityView.getEmmHealthInfo()?.let { (healthy, unhealthy) ->
            val net = healthy - unhealthy
            val status = if (net >= 0) Color.FOREST else Color.SCARLET
            val healthLabel = "Health: $healthy / $unhealthy (net ${if (net >= 0) "+" else ""}$net)".toLabel(status, hideIcons = true)
            lowerTable.add(Table().apply {\n                add(ImageGetter.getExternalImage("Icons/EMMHealth.png")).size(20f).padRight(5f)\n                add(healthLabel)\n            }).row()
        }
'''+needle)
ui.write_text(u)
# Add breakdown to the detailed Stats popup, preceding existing stat tables.
pop=root/'core/src/com/unciv/ui/screens/cityscreen/DetailedStatsPopup.kt'
d=pop.read_text()
needle='        totalTable.add("Base values".toLabel().apply { setAlignment(Align.center) })'
assert d.count(needle)==1
d=d.replace(needle,'''        cityView.getEmmHealthInfo()?.let { (healthy, unhealthy) ->
            val net = healthy - unhealthy
            totalTable.add("City health: $healthy healthy / $unhealthy unhealthy (net ${if (net >= 0) "+" else ""}$net)".toLabel(if (net >= 0) Color.GREEN else Color.SCARLET))
                .colspan(columnCount).left().row()
            totalTable.add("Population unhealthiness and buildings, resources, terrain, traits and freshwater health are included.".toLabel())
                .colspan(columnCount).left().row()
            for ((source, value) in cityView.getEmmHealthBreakdown()) {
                if (value == 0) continue
                val sign = if (value > 0) "+" else ""
                totalTable.add(("    $source: $sign$value").toLabel())
                    .colspan(columnCount).left().row()
            }
            totalTable.addSeparator(colSpan = columnCount)
        }
'''+needle)
pop.write_text(d)
print('Patched city health status in CityStats, CityView, city screen, Stats popup')
print('Patched',path)

# Display health-building bonuses with the same icon, instead of prose.
info=root/'core/src/com/unciv/ui/screens/cityscreen/ConstructionInfoTable.kt'
c=info.read_text()
anchor='''            if (cityConstructions.isBuilt(construction.name)) {'''
assert c.count(anchor)==1
code='''            if (construction is Building && cityView.getEmmHealthInfo() != null) {
                val health = when (construction.name) {
                    "Herbalist" -> 1
                    "Aqueduct" -> 2
                    "Infirmary" -> 3
                    else -> 0
                }
                if (health > 0) {
                    row()
                    add(Table().apply {
                        add(ImageGetter.getExternalImage("Icons/EMMHealth.png")).size(20f).padRight(5f)
                        add("+$health".toLabel(Color.FOREST))
                    }).colspan(2).left().row()
                }
            }
'''
# toLabel extension is included for concise value text.
c=c.replace('import com.unciv.ui.components.extensions.toTextButton','import com.unciv.ui.components.extensions.toLabel\nimport com.unciv.ui.components.extensions.toTextButton')
c=c.replace(anchor,code+anchor)
info.write_text(c)
