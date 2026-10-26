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
global_health={}
area_health={}
no_population_unhealth=[]
for row in source['groups']['buildings']['entries']:
    name=' '.join(part.capitalize() for part in row['id'].removeprefix('BUILDING_').split('_'))
    if name.startswith('Palace '): name=name.removeprefix('Palace ')+' Palace'
    area_amount=int(row['fields'].get('iAreaHealth','0'))
    if area_amount: area_health[name]=area_amount
    global_amount=int(row['fields'].get('iGlobalHealth','0'))
    if global_amount: global_health[name]=global_amount
    if row['fields'].get('bNoUnhealthyPopulation')=='1':no_population_unhealth.append(name)
assert global_health.get('Kuriotates Palace')==1
assert area_health.get('Aquae Sucellus')==1
assert 'Demonic Citizens' in no_population_unhealth
area_health_map='mapOf('+', '.join(f'"{name}" to {amount}' for name,amount in sorted(area_health.items()))+')'
global_health_map='mapOf('+', '.join(f'"{name}" to {amount}' for name,amount in sorted(global_health.items()))+')'
no_unhealth_set='setOf('+', '.join('"'+n+'"' for n in no_population_unhealth)+')'
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
            val built = city.cityConstructions.builtBuildings
            val exemptPopulation = EMM_NO_UNHEALTHY_POPULATION.any { it in built }
            val unhealthyPopulation = if (exemptPopulation) 0 else city.population.population
            // Building contributions are extracted from pinned EMM CIV4BuildingInfos.xml.
            // Difficulty health is read from pinned EMM CIV4HandicapInfo.xml.
            val handicapHealth = EMM_DIFFICULTY_HEALTH[city.civ.gameInfo.difficulty] ?: 2
            val buildingHealth = EMM_HEALTH_MAP.entries.sumOf { (name, value) -> if (name in built) value.coerceAtLeast(0) else 0 }
            val buildingUnhealth = EMM_HEALTH_MAP.entries.sumOf { (name, value) -> if (name in built) (-value).coerceAtLeast(0) else 0 }
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
            val globalHealth = EMM_GLOBAL_HEALTH.entries.sumOf { (name, value) ->
                if (city.civ.cities.any { name in it.cityConstructions.builtBuildings }) value else 0
            }
            val currentContinent = city.getCenterTile().getContinent()
            val areaHealth = EMM_AREA_HEALTH.entries.sumOf { (name, value) ->
                if (currentContinent >= 0 && city.civ.cities.any {
                    it.getCenterTile().getContinent() == currentContinent && name in it.cityConstructions.builtBuildings
                }) value else 0
            }
            val healthySources = handicapHealth + buildingHealth + globalHealth + areaHealth + expansiveHealth + resourceHealth + freshwaterHealth + featureHealth
            val netUnhealthy = (unhealthyPopulation + featureUnhealth - healthySources).coerceAtLeast(0)
            if (netUnhealthy > 0)
                newFinalStatList.add("Unhealthiness", Stats(food = -netUnhealthy.toFloat()))
        }'''
assert s.count(anchor)==1,'Pinned CityStats changed, refusing unsafe patch'
replacement=replacement.replace('EMM_HEALTH_MAP',health_map)
replacement=replacement.replace('EMM_GLOBAL_HEALTH',global_health_map)
replacement=replacement.replace('EMM_AREA_HEALTH',area_health_map)
replacement=replacement.replace('EMM_NO_UNHEALTHY_POPULATION',no_unhealth_set)
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
s=s.replace('            val netUnhealthy = (unhealthyPopulation + featureUnhealth - healthySources).coerceAtLeast(0)', '''            val totalUnhealthy = unhealthyPopulation + featureUnhealth + buildingUnhealth + city.emmDiseaseHealthCounter
            emmHealthInfo = healthySources to totalUnhealthy
            emmHealthBreakdown = linkedMapOf(
                "Difficulty health" to handicapHealth,
                "Healthy buildings" to buildingHealth,
                "Unhealthy buildings" to -buildingUnhealth,
                "Plague and Blight" to -city.emmDiseaseHealthCounter,
                "Empire-wide buildings" to globalHealth,
                "Continent buildings" to areaHealth,
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
                val health = EMM_CONSTRUCTION_HEALTH[construction.name] ?: 0
                if (health != 0) {
                    row()
                    add(Table().apply {
                        add(ImageGetter.getExternalImage("Icons/EMMHealth.png")).size(20f).padRight(5f)
                        add("${if (health > 0) "+" else ""}$health".toLabel(if (health > 0) Color.FOREST else Color.SCARLET))
                    }).colspan(2).left().row()
                }
            }
'''
# toLabel extension is included for concise value text.
c=c.replace('import com.unciv.ui.components.extensions.toTextButton','import com.unciv.ui.components.extensions.toLabel\nimport com.unciv.ui.components.extensions.toTextButton')
c=c.replace(anchor,code.replace('EMM_CONSTRUCTION_HEALTH',health_map)+anchor)
info.write_text(c)


# Preserve city-level effects in saves and copied game states.
cityfile=root/'core/src/com/unciv/logic/city/City.kt'
v=cityfile.read_text()
needle='    var health = 200'
assert v.count(needle)==1
v=v.replace(needle, needle+'''
    /** EMM Blight/Pestilence excess unhealthiness (not city combat health). Serialized. */
    var emmDiseaseHealthCounter = 0
''')
needle='        toReturn.health = health'
assert v.count(needle)==1
v=v.replace(needle,needle+'\n        toReturn.emmDiseaseHealthCounter = emmDiseaseHealthCounter')
cityfile.write_text(v)

# Health effects are ticked once each city turn. Event application must be invoked
# by the Armageddon event system, not randomly improvised as normal city disease.
turn=root/'core/src/com/unciv/logic/city/managers/CityTurnManager.kt'
t=turn.read_text()
needle='        city.clearCaches()'
assert t.count(needle)>=1
t=t.replace(needle,'''        city.clearCaches()
        // Existing Civ IV temporary sickness steadily clears; retain a persistent
        // numerical counter across save/load. Other disease sources will add to it.
        if (city.emmDiseaseHealthCounter > 0)
            city.emmDiseaseHealthCounter -= 1
''', 1)
turn.write_text(t)

# Source-aligned Armageddon event application API. The global AC threshold,
# once ported, must call these methods once at the appropriate event threshold.
event=root/'core/src/com/unciv/logic/city/EmmCityEpidemics.kt'
event.write_text('''package com.unciv.logic.city

import kotlin.math.max

/** Per-city disease effects; global Armageddon event dispatch is tracked separately. */
object EmmCityEpidemics {
    /**
     * EMM CvRandomEventInterface.doArmageddonBlight:
     * random(15) + population + bad feature health - good feature health
     * - total *good building* health. Infernal cities are excluded.
     *
     * Caller supplies source random draw in 0..14, preserving global RNG policy.
     * Creature damage (25 death-type, capped at 100 in EMM) is handled separately.
     */
    fun blight(city: City, random15: Int, badFeatureHealth: Int,
               goodFeatureHealth: Int, goodBuildingHealth: Int) {
        require(random15 in 0..14)
        if (city.civ.civName == "Infernal") return
        val amount = random15 + city.population.population + badFeatureHealth -
                goodFeatureHealth - goodBuildingHealth
        if (amount > 0)
            city.emmDiseaseHealthCounter += amount
    }

    /**
     * EMM CvRandomEventInterface.doArmageddonPestilence:
     * random(9) + floor(population / 4) - good building health.
     * Unlike Blight, the original source adds the signed result.
     */
    fun pestilence(city: City, random9: Int, goodBuildingHealth: Int) {
        require(random9 in 0..8)
        if (city.civ.civName == "Infernal") return
        val amount = random9 + city.population.population / 4 - goodBuildingHealth
        city.emmDiseaseHealthCounter = max(0, city.emmDiseaseHealthCounter + amount)
    }
}
''')
print('Patched persisted city epidemic counter and event source formulas')


# Complete disease/plague healing modifiers from EMM PromotionInfos on the
# pinned Unciv healing path; these are separate from their strength modifiers.
unit=root/'core/src/com/unciv/logic/map/mapunit/MapUnit.kt'
u=unit.read_text()
begin=u.index('fun healingAmountForTile(')
end=u.index('    // Only military land units',begin)
section=u[begin:end]
needle='        if (noTerrainDamage) return healing'
assert section.count(needle)==1
section=section.replace(needle,'''        if (civ.gameInfo.ruleset.buildings.containsKey("Herbalist")) {
            if (promotions.getPromotions().any { it.name == "Diseased" }) healing -= 10
            if (promotions.getPromotions().any { it.name == "Plagued" }) healing -= 20
        }
        if (noTerrainDamage) return healing''')
u=u[:begin]+section+u[end:]
unit.write_text(u)
print('Installed EMM Diseased/Plagued healing modifiers (-10/-20)')


# Diseased promotion has PromotionCombatApply=PROMOTION_DISEASED in EMM.
# Apply on surviving targets after damage, blocked by source immunity.
battle=root/'core/src/com/unciv/logic/battle/Battle.kt'
b=battle.read_text()
anchor='''        // Exploring units surviving an attack should "wake up"'''
assert b.count(anchor)==1
code='''        // EMM: Diseased transmits through combat to eligible living targets.
        // This is NOT a plague spell: Plagued does not have PromotionCombatApply.
        if (attacker is MapUnitCombatant && defender is MapUnitCombatant &&
            !attacker.isDefeated() && !defender.isDefeated() &&
            attacker.unit.civ.gameInfo.ruleset.unitPromotions.containsKey("Diseased") &&
            "Diseased" in attacker.unit.promotions.promotions &&
            "Immune to Disease" !in defender.unit.promotions.promotions &&
            "Diseased" !in defender.unit.promotions.promotions &&
            "Plagued" !in defender.unit.promotions.promotions) {
            defender.unit.promotions.addPromotion("Diseased", isFree = true)
        }

'''
b=b.replace(anchor,code+anchor)
battle.write_text(b)
print('Added EMM Diseased combat infection with immunity guard')

# EMM PromotionImmune1/2 must apply to all promotion-granting routes,
# not only the explicit combat-infection path.
promo=root/'core/src/com/unciv/logic/map/mapunit/UnitPromotions.kt'
p=promo.read_text()
needle='''        if (promotions.contains(promotionName)) return
        val ruleset = unit.civ.gameInfo.ruleset'''
assert p.count(needle)==1
p=p.replace(needle,'''        if (promotions.contains(promotionName)) return
        // EMM immune-disease blocks both disease promotions from ANY source.
        if (unit.civ.gameInfo.ruleset.buildings.containsKey("Herbalist") &&
            promotionName in listOf("Diseased", "Plagued") &&
            "Immune to Disease" in promotions) return
        val ruleset = unit.civ.gameInfo.ruleset''')
needle='''        unit.updateUniques()

        // Since some units get promotions upon construction'''
assert p.count(needle)==1
p=p.replace(needle,'''        // Granting EMM immunity also cures any existing disease.
        if (promotionName == "Immune to Disease" &&
            unit.civ.gameInfo.ruleset.buildings.containsKey("Herbalist")) {
            removePromotion("Diseased")
            removePromotion("Plagued")
        }
        unit.updateUniques()

        // Since some units get promotions upon construction''')
promo.write_text(p)
print('Implemented global EMM disease-promotion immunity')

# First playable Cure Disease action. EMM SPELL_CURE_DISEASE requires Medic II;
# cures friendly sick units co-located with the caster. Fine-grained source
# target selection still requires spell XML audit.
actiontype=root/'core/src/com/unciv/models/UnitAction.kt'
a=actiontype.read_text()
needle='    Skip("Skip turn"),'
assert a.count(needle)==1
a=a.replace(needle,'    EmmCureDisease("Cure Disease"),\n'+needle)
actiontype.write_text(a)

actions=root/'core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt'
a=actions.read_text()
needle='''        addSkipAction(unit)'''
assert a.count(needle)==1
a=a.replace(needle,'''        if (unit.civ.gameInfo.ruleset.buildings.containsKey("Herbalist") &&
            "Medic II" in unit.promotions.promotions) {
            val targets = unit.getTile().getUnits().filter { it.civ == unit.civ &&
                ("Diseased" in it.promotions.promotions || "Plagued" in it.promotions.promotions) }.toList()
            if (targets.isNotEmpty()) {
                yield(UnitAction(UnitActionType.EmmCureDisease, action = if (unit.hasMovement()) ({
                    for (target in targets) {
                        target.promotions.removePromotion("Diseased")
                        target.promotions.removePromotion("Plagued")
                    }
                    unit.useMovementPoints(1f)
                }) else null))
            }
        }

'''+needle)
actions.write_text(a)
print('Added playable Medic II Cure Disease unit action')

# Start the full-engine Armageddon Counter integration. Its value and event state
# are serialized; future EMM spell/civic/city triggers must call changeEmmArmageddon.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
anchor='class GameInfo : '
# Insert into class body after the opening brace, not in GameInfoPreview.
start=g.index('class GameInfo :')
opening=g.index('{',start)
g=g[:opening+1]+'''
    /** EMM world Armageddon Counter, 0..100, saved with the game. */
    var emmArmageddonCounter = 0
    var emmBlightTriggered = false
    var emmPestilenceTriggered = false

    fun changeEmmArmageddon(delta: Int) {
        if (!ruleset.buildings.containsKey("Herbalist")) return
        val prior = emmArmageddonCounter
        emmArmageddonCounter = (prior + delta).coerceIn(0, 100)
        if (prior < 30 && emmArmageddonCounter >= 30 && !emmBlightTriggered) {
            emmBlightTriggered = true
            com.unciv.logic.city.EmmArmageddonEvents.fireBlight(this)
        }
        if (prior < 35 && emmArmageddonCounter >= 35 && !emmPestilenceTriggered) {
            emmPestilenceTriggered = true
            com.unciv.logic.city.EmmArmageddonEvents.firePestilence(this)
        }
    }
'''+g[opening+1:]
gamefile.write_text(g)

dispatcher=root/'core/src/com/unciv/logic/city/EmmArmageddonEvents.kt'
dispatcher.write_text('''package com.unciv.logic.city

import com.unciv.logic.GameInfo

/**
 * EMM Armageddon threshold dispatcher. This deliberately does not invent AC
 * generation: changing the counter must be hooked to source-accurate actions.
 */
object EmmArmageddonEvents {
    fun fireBlight(game: GameInfo) {
        for (civ in game.civilizations) for (city in civ.cities) {
            val breakdown = city.cityStats.emmHealthBreakdown
            val random = city.state.stateBasedRandom("EMM.Blighter." + game.turns).nextInt(15)
            EmmCityEpidemics.blight(
                city, random,
                -(breakdown["Unhealthy features"] ?: 0),
                breakdown["Forests and features (healthy)"] ?: 0,
                breakdown["Healthy buildings"] ?: 0
            )
            city.cityStats.update()
        }
    }

    fun firePestilence(game: GameInfo) {
        for (civ in game.civilizations) for (city in civ.cities) {
            val random = city.state.stateBasedRandom("EMM.Pestilence." + game.turns).nextInt(9)
            val goodBuildingHealth = city.cityStats.emmHealthBreakdown["Healthy buildings"] ?: 0
            EmmCityEpidemics.pestilence(city, random, goodBuildingHealth)
            city.cityStats.update()
        }
    }
}
''')
print('Installed serialized Armageddon threshold state and Blight/Pestilence dispatcher')

# Expose an explicit developer-console path to test AC without fabricating
# EMM's still-unported AC-generating world events.
console=root/'core/src/com/unciv/ui/screens/devconsole/ConsoleGameCommands.kt'
v=console.read_text()
needle='''        "setdifficulty" to ConsoleAction'''
assert v.count(needle)==1
v=v.replace(needle,'''        "emm-armageddon" to ConsoleAction("game emm-armageddon <delta>") { console, params ->
            val delta = params[0].toInt()
            if (!console.gameInfo.ruleset.buildings.containsKey("Herbalist"))
                throw ConsoleErrorException("EMM mod not active")
            console.gameInfo.changeEmmArmageddon(delta)
            DevConsoleResponse.OK
        },

'''+needle)
console.write_text(v)
print('Added game emm-armageddon <delta> test command for world-event acceptance')

# Surface the real saved AC on the city screen, avoiding a hidden invisible
# world system. Keep it alongside the existing city health display.
ui=root/'core/src/com/unciv/ui/screens/cityscreen/CityStatsTable.kt'
u=ui.read_text()
needle='''        cityView.getEmmHealthInfo()?.let { (healthy, unhealthy) ->'''
assert u.count(needle)==1
u=u.replace(needle,'''        if (cityView.getEmmHealthInfo() != null) {
            val ac = cityView.getState().gameInfo?.emmArmageddonCounter ?: 0
            lowerTable.add(("Armageddon: $ac / 100").toLabel(
                if (ac >= 35) Color.SCARLET else if (ac >= 30) Color.ORANGE else Color.LIGHT_GRAY,
                hideIcons = true
            )).row()
        }
'''+needle)
ui.write_text(u)


# Source EMM: founding the Ashen Veil gives +5 AC; first founding of
# Octopus Overlords gives +3; each distinct Ashen Veil city spread gives +1.
# Keep these independent of vanilla Unciv's very different faith/prophet flow.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='    var emmPestilenceTriggered = false'
assert g.count(needle)==1
g=g.replace(needle,needle+'''
    /** EMM religions first founded anywhere in this world. Serialized. */
    var emmFoundedReligions = hashSetOf<String>()

    fun emmFoundReligion(name: String, city: com.unciv.logic.city.City) {
        if (!ruleset.buildings.containsKey("Herbalist")) return
        if (!emmFoundedReligions.add(name)) return
        if (name == "The Ashen Veil") changeEmmArmageddon(5)
        if (name == "Octopus Overlords") changeEmmArmageddon(3)
        emmSpreadReligion(name, city)
    }

    fun emmSpreadReligion(name: String, city: com.unciv.logic.city.City) {
        if (!ruleset.buildings.containsKey("Herbalist")) return
        if (!city.emmEstablishedReligions.add(name)) return
        if (name == "The Ashen Veil") changeEmmArmageddon(1)
    }
''')
gamefile.write_text(g)

cityfile=root/'core/src/com/unciv/logic/city/City.kt'
c=cityfile.read_text()
needle='    var emmDiseaseHealthCounter = 0'
assert c.count(needle)==1
c=c.replace(needle,needle+'''
    /** Once-per-city EMM religious spread accounting, preserved in saves. */
    var emmEstablishedReligions = hashSetOf<String>()
''')
needle='        toReturn.emmDiseaseHealthCounter = emmDiseaseHealthCounter'
assert c.count(needle)==1
c=c.replace(needle,needle+'\n        toReturn.emmEstablishedReligions.addAll(emmEstablishedReligions)')
cityfile.write_text(c)

# Source EMM: researching a religion's tech founds it for the first player
# before later players receive the respective missionary instead.
tech=root/'core/src/com/unciv/logic/civilization/managers/TechManager.kt'
t=tech.read_text()
needle='''        val isNewTech = techsResearched.add(techName)'''
assert t.count(needle)==1
t=t.replace(needle,needle+'''
        if (isNewTech && civInfo.cities.isNotEmpty() &&
            civInfo.gameInfo.ruleset.buildings.containsKey("Herbalist")) {
            when (techName) {
                "Corruption of Spirit" -> civInfo.gameInfo.emmFoundReligion("The Ashen Veil", civInfo.cities.first())
                "Message from the Deep" -> civInfo.gameInfo.emmFoundReligion("Octopus Overlords", civInfo.cities.first())
            }
        }
''')
tech.write_text(t)
print('Wired EMM religion founding by technology and distinct-city religion spread AC changes')


# Make the original Ashen Veil spread source accessible during ordinary play.
actiontype=root/'core/src/com/unciv/models/UnitAction.kt'
a=actiontype.read_text()
needle='    EmmCureDisease("Cure Disease"),'
assert a.count(needle)==1
a=a.replace(needle,needle+'\n    EmmSpreadAshenVeil("Spread the Ashen Veil"),')
actiontype.write_text(a)

actions=root/'core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt'
a=actions.read_text()
needle='''        addSkipAction(unit)'''
assert a.count(needle)==1
a=a.replace(needle,'''        if (unit.name == "Disciple of the Ashen Veil" &&
            unit.civ.gameInfo.ruleset.buildings.containsKey("Herbalist")) {
            val city = unit.getTile().getCity()
            if (unit.getTile().isCityCenter() && city != null &&
                "The Ashen Veil" !in city.emmEstablishedReligions &&
                "The Ashen Veil" in unit.civ.gameInfo.emmFoundedReligions) {
                yield(UnitAction(UnitActionType.EmmSpreadAshenVeil,
                    action = if (unit.hasMovement()) ({
                        unit.civ.gameInfo.emmSpreadReligion("The Ashen Veil", city)
                        unit.destroy()
                    }) else null))
            }
        }
'''+needle)
actions.write_text(a)
print('Wired gameplay missionary action into source-backed +1/city AC progress')


# EMM CvEventManager.onImprovementDestroyed: destruction of a Necrototem
# decrements AC by two. Unciv pillage/destruction must fire this effect only
# for a genuinely removed improvement (not merely damaged/temporarily pillaged).
pillage=root/'core/src/com/unciv/logic/map/mapunit/actions/UnitActionsPillage.kt'
v=pillage.read_text()
needle='''                    tile.removeImprovement()
                }'''
assert v.count(needle)==1
v=v.replace(needle,'''                    if (pillagedImprovement == "Necrototem" &&
                        unit.civ.gameInfo.ruleset.buildings.containsKey("Herbalist"))
                        unit.civ.gameInfo.changeEmmArmageddon(-2)
                    tile.removeImprovement()
                }''')
pillage.write_text(v)
print('Linked EMM Necrototem destruction to source-defined -2 AC')


# Source spells CvSpellInterface.spellSanctify/spellRobGrave:
# Sanctifying city ruins or graveyards: -1 AC, improvement removed.
# Robbing a graveyard: +1 AC and consumes the graveyard, with the original
# random grave loot still pending.
actiontype=root/'core/src/com/unciv/models/UnitAction.kt'
a=actiontype.read_text()
needle='    EmmSpreadAshenVeil("Spread the Ashen Veil"),'
assert a.count(needle)==1
a=a.replace(needle,needle+'''
    EmmSanctify("Sanctify"),
    EmmRobGrave("Rob Grave"),''')
actiontype.write_text(a)
actions=root/'core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt'
a=actions.read_text()
needle='''        addSkipAction(unit)'''
assert a.count(needle)==1
a=a.replace(needle,'''        if (unit.civ.gameInfo.ruleset.buildings.containsKey("Herbalist")) {
            val improvement = unit.getTile().improvement
            if ("Life I" in unit.promotions.promotions &&
                (improvement == "City ruins" || improvement == "Graveyard")) {
                yield(UnitAction(UnitActionType.EmmSanctify,
                    action = if (unit.hasMovement()) ({
                        unit.getTile().removeImprovement()
                        unit.civ.gameInfo.changeEmmArmageddon(-1)
                        unit.useMovementPoints(1f)
                    }) else null))
            }
            if (improvement == "Graveyard" && unit.isMilitary()) {
                yield(UnitAction(UnitActionType.EmmRobGrave,
                    action = if (unit.hasMovement()) ({
                        unit.getTile().removeImprovement()
                        unit.civ.gameInfo.changeEmmArmageddon(1)
                        unit.useMovementPoints(1f)
                    }) else null))
            }
        }
'''+needle)
actions.write_text(a)
print('Linked source-faithful Sanctify (-1) and grave robbing (+1) AC changes')


# Civilization alignment is source-derived from the pinned selected EMM leaders.
# When a major civilization is eliminated: Good +5 AC, Evil -5 AC, Neutral 0.
alignment_source=json.loads((mod/'docs/data/emm-leader-alignments.json').read_text())['selectedCivilizations']
assert len(alignment_source)==19
alignment_delta={'ALIGNMENT_GOOD':5,'ALIGNMENT_EVIL':-5,'ALIGNMENT_NEUTRAL':0}
alignment_map='mapOf('+', '.join(f'"{name}" to {alignment_delta[x["alignment"]]}' for name,x in sorted(alignment_source.items()))+')'
civfile=root/'core/src/com/unciv/logic/civilization/Civilization.kt'
v=civfile.read_text()
needle='''    fun destroy(notificationLocation: HexCoord? = null) {
        revealMapWhenDefeated()'''
assert v.count(needle)==1
v=v.replace(needle,'''    fun destroy(notificationLocation: HexCoord? = null) {
        if (isMajorCiv() && gameInfo.ruleset.buildings.containsKey("Herbalist")) {
            // EMM CvEventManager.onSetPlayerAlive: source-selected leader alignment.
            val delta = EMM_LEADER_ELIMINATION_AC[civName] ?: 0
            if (delta != 0) gameInfo.changeEmmArmageddon(delta)
        }
        revealMapWhenDefeated()'''.replace('EMM_LEADER_ELIMINATION_AC',alignment_map))
civfile.write_text(v)
print('Installed source-derived +5 Good/-5 Evil elimination Armageddon rules')
