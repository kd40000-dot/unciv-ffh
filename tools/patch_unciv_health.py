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
alignment_source=json.loads(Path('docs/data/emm-leader-alignments.json').read_text())['selectedCivilizations']
assert len(alignment_source)==19
alignment_delta={'ALIGNMENT_GOOD':5,'ALIGNMENT_EVIL':-5,'ALIGNMENT_NEUTRAL':0}
alignment_map='mapOf('+', '.join(f'"{name}" to {alignment_delta[x["alignment"]]}' for name,x in sorted(alignment_source.items()))+')'
civfile=root/'core/src/com/unciv/logic/civilization/Civilization.kt'
v=civfile.read_text()
needle='''    fun destroy(notificationLocation: HexCoord? = null) {
        revealMapWhenDefeated()'''
assert v.count(needle)==1
v=v.replace(needle,'''    fun destroy(notificationLocation: HexCoord? = null) {
        if (isMajorCiv() && gameInfo.getYear() >= 5 &&
            gameInfo.ruleset.buildings.containsKey("Herbalist") &&
            gameInfo.emmCountedEliminations.add(civID)) {
            // EMM CvEventManager.onSetPlayerAlive: source-selected leader alignment.
            val delta = EMM_LEADER_ELIMINATION_AC[civName] ?: 0
            if (delta != 0) gameInfo.changeEmmArmageddon(delta)
        }
        revealMapWhenDefeated()'''.replace('EMM_LEADER_ELIMINATION_AC',alignment_map))
civfile.write_text(v)
print('Installed source-derived +5 Good/-5 Evil elimination Armageddon rules')


# EMM XML defines exactly 52 event-choice Armageddon deltas. This registry
# is invoked from the future source-faithful random event implementation;
# do not randomly generate these choices without their XML trigger rules.
choices=json.loads(Path('docs/data/emm-armageddon-event-choices.json').read_text())['eventChoices']
assert len(choices)==52
choices_map='mapOf('+', '.join(f'"{x["id"]}" to {x["delta"]}' for x in choices)+')'
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='    fun changeEmmArmageddon(delta: Int) {'
assert g.count(needle)==1
g=g.replace(needle,'''    fun applyEmmArmageddonEventChoice(sourceEventId: String): Boolean {
        val sourceDeltas = EMM_RANDOM_EVENT_AC
        val delta = sourceDeltas[sourceEventId] ?: return false
        changeEmmArmageddon(delta)
        return true
    }

'''.replace('EMM_RANDOM_EVENT_AC',choices_map)+needle)
gamefile.write_text(g)
print('Added all 52 EMM event-choice AC source deltas to engine API')

gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='    var emmPestilenceTriggered = false'
assert g.count(needle)==1
g=g.replace(needle,needle+'\n    var emmCountedEliminations = hashSetOf<String>()')
gamefile.write_text(g)


# EMM source onReligionSpread: Order/Veil conflict gives AC -1 or +1
# on the 35% incoming-faith victory outcome (except holy cities).
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='''        emmSpreadReligion(name, city)
    }

    fun emmSpreadReligion(name: String, city: com.unciv.logic.city.City) {'''
assert g.count(needle)==1
g=g.replace(needle,'''        city.emmHolyCityOf = name
        emmSpreadReligion(name, city)
    }

    fun emmSpreadReligion(name: String, city: com.unciv.logic.city.City) {''')
needle='''        if (name == "The Ashen Veil") changeEmmArmageddon(1)
    }'''
assert g.count(needle)==1
g=g.replace(needle,'''        if (name == "The Ashen Veil") changeEmmArmageddon(1)
        if (city.emmHolyCityOf == null) {
            val opposing = when (name) {
                "The Order" -> "The Ashen Veil"
                "The Ashen Veil" -> "The Order"
                else -> null
            }
            if (opposing != null && opposing in city.emmEstablishedReligions) {
                // EMM CvEventManager.onReligionSpread: 35% for the incoming faith.
                val incomingWins = city.state.stateBasedRandom(
                    "EMM.OrderVeil." + turns + "." + name
                ).nextInt(100) < 35
                if (incomingWins) {
                    city.emmEstablishedReligions.remove(opposing)
                    if (city.population.population > 1)
                        city.population.setPopulation(city.population.population - 1)
                    changeEmmArmageddon(if (name == "The Order") -1 else 1)
                } else {
                    city.emmEstablishedReligions.remove(name)
                }
            }
        }
    }''')
gamefile.write_text(g)
cityfile=root/'core/src/com/unciv/logic/city/City.kt'
c=cityfile.read_text()
needle='    var emmEstablishedReligions = hashSetOf<String>()'
assert c.count(needle)==1
c=c.replace(needle,needle+'\n    var emmHolyCityOf: String? = null')
needle='        toReturn.emmEstablishedReligions.addAll(emmEstablishedReligions)'
assert c.count(needle)==1
c=c.replace(needle,needle+'\n        toReturn.emmHolyCityOf = emmHolyCityOf')
cityfile.write_text(c)
tech=root/'core/src/com/unciv/logic/civilization/managers/TechManager.kt'
t=tech.read_text()
needle='''                "Message from the Deep" -> civInfo.gameInfo.emmFoundReligion("Octopus Overlords", civInfo.cities.first())'''
assert t.count(needle)==1
t=t.replace(needle,needle+'''
                "Orders from Heaven" -> civInfo.gameInfo.emmFoundReligion("The Order", civInfo.cities.first())''')
tech.write_text(t)
print('Added source-specific Order/Veil 35% clash, AC, and population loss')

# Add Order disciple action using the source -1 clash outcome when victorious.
actiontype=root/'core/src/com/unciv/models/UnitAction.kt'
a=actiontype.read_text()
needle='    EmmSpreadAshenVeil("Spread the Ashen Veil"),'
assert a.count(needle)==1
a=a.replace(needle,needle+'\n    EmmSpreadOrder("Spread the Order"),')
actiontype.write_text(a)
actions=root/'core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt'
a=actions.read_text()
needle='''        addSkipAction(unit)'''
assert a.count(needle)==1
a=a.replace(needle,'''        if (unit.name == "Disciple of the Order" &&
            unit.civ.gameInfo.ruleset.buildings.containsKey("Herbalist")) {
            val city = unit.getTile().getCity()
            if (unit.getTile().isCityCenter() && city != null &&
                "The Order" !in city.emmEstablishedReligions &&
                "The Order" in unit.civ.gameInfo.emmFoundedReligions) {
                yield(UnitAction(UnitActionType.EmmSpreadOrder,
                    action = if (unit.hasMovement()) ({
                        unit.civ.gameInfo.emmSpreadReligion("The Order", city)
                        unit.destroy()
                    }) else null))
            }
        }
'''+needle)
actions.write_text(a)
print('Exposed EMM Order disciple and source-faithful opposing-religion AC conflict')


# EMM CvSpellInterface.spellPeace and spellPeaceSevenPines both remove floor(AC/2)
# from the global counter. This engine entry point is shared by both spell routes.
# We do not expose it to arbitrary ordinary units: each spell still requires
# its original Corlindale / Seven Pines eligibility and peace-making effect.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='    fun changeEmmArmageddon(delta: Int) {'
assert g.count(needle)==1
g=g.replace(needle,'''    /**
     * Source: EMM CvSpellInterface.spellPeace and spellPeaceSevenPines.
     * Both reduce AC by half, using Python/Civ IV integer truncation.
     * Call after executing the spell's required diplomatic peace effect.
     */
    fun emmPeaceReducesArmageddon() {
        if (!ruleset.buildings.containsKey("Herbalist")) return
        changeEmmArmageddon(-(emmArmageddonCounter / 2))
    }

'''+needle)
gamefile.write_text(g)
print('Installed source-exact Peace/Seven Pines shared Armageddon reduction API')


# Source EMM SPELL_PEACE: UNITCLASS_CORLINDALE, only available during war;
# ends wars with all living non-barbarian players, halves AC, consumes caster.
actiontype=root/'core/src/com/unciv/models/UnitAction.kt'
a=actiontype.read_text()
needle='    EmmRobGrave("Rob Grave"),'
assert a.count(needle)==1
a=a.replace(needle,needle+'\n    EmmPeace("Peace"),')
actiontype.write_text(a)
actions=root/'core/src/com/unciv/logic/map/mapunit/actions/UnitActions.kt'
a=actions.read_text()
needle='''        addSkipAction(unit)'''
assert a.count(needle)==1
a=a.replace(needle,'''        if (unit.name == "Corlindale" &&
            unit.civ.gameInfo.ruleset.buildings.containsKey("Herbalist")) {
            val enemies = unit.civ.gameInfo.civilizations.filter { other ->
                other != unit.civ && other.isAlive() && !other.isBarbarian &&
                    unit.civ.isAtWarWith(other)
            }
            if (enemies.isNotEmpty()) {
                yield(UnitAction(UnitActionType.EmmPeace,
                    action = if (unit.hasMovement()) ({
                        for (enemy in enemies)
                            unit.civ.getDiplomacyManager(enemy)?.makePeace()
                        unit.civ.gameInfo.emmPeaceReducesArmageddon()
                        unit.destroy()
                    }) else null))
            }
        }
'''+needle)
actions.write_text(a)
print('Added Corlindale Peace spell: peacemaking, AC halving, sacrifice')


# EMM CvRandomEventInterface callbacks with independent AC deltas.
# Scheduling/eligibility and non-AC side effects remain part of the original
# random-event implementation; don't synthesize random events here.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='    fun applyEmmArmageddonEventChoice(sourceEventId: String): Boolean {'
assert g.count(needle)==1
g=g.replace(needle,'''    fun applyEmmArmageddonEventCallback(sourceCallback: String): Boolean {
        val delta = when (sourceCallback) {
            "doFlareEntropyNode" -> 2
            "doFlareLifeNode" -> -2
            "doSignAeron" -> 3
            "doSignSirona" -> -3
            else -> return false
        }
        changeEmmArmageddon(delta)
        return true
    }

'''+needle)
gamefile.write_text(g)
print('Registered source-exact EMM random-event callbacks (not fake spontaneous triggers)')


# Durable EMM random-event scheduler; only source choices with NO other effects
# are eligible at this stage. Unported choices must not be auto-resolved.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='    var emmPestilenceTriggered = false'
assert g.count(needle)==1
g=g.replace(needle,needle+'''
    var emmResolvedEventTriggers = hashSetOf<String>()
    var emmPendingEvents = hashMapOf<String, String>()
    var emmLastEventRollTurn = -1

    fun emmResolveRandomEvent(civID: String, choice: String): Boolean {
        val event = emmPendingEvents[civID] ?: return false
        val accepted = when(event) {
            "EVENTTRIGGER_WITCH" -> "EVENT_WITCH_2"
            "EVENTTRIGGER_HOLY_CHILD" -> "EVENT_HOLY_CHILD_1"
            "EVENTTRIGGER_DEMONIC_TOME" -> "EVENT_DEMONIC_TOME_2"
            else -> return false
        }
        if (choice != accepted) return false
        if (!applyEmmArmageddonEventChoice(choice)) return false
        emmPendingEvents.remove(civID)
        emmResolvedEventTriggers.add(civID + ":" + event)
        return true
    }

    fun emmScheduleRandomEvents() {
        if (!ruleset.buildings.containsKey("Herbalist") ||
            emmLastEventRollTurn == turns) return
        emmLastEventRollTurn = turns
        val roll = kotlin.random.Random(turns * 41081 + civilizations.size * 397)
        for (civ in civilizations) {
            if (!civ.isAlive() || civ.isBarbarian || emmPendingEvents.containsKey(civ.civID)) continue
            val eligible = arrayListOf<String>()
            if (civ.cities.any { it.population.population >= 3 }) {
                eligible.add("EVENTTRIGGER_WITCH")
                if (emmArmageddonCounter >= 10) eligible.add("EVENTTRIGGER_HOLY_CHILD")
            }
            if (emmArmageddonCounter >= 10 && civ.tech.isResearched("Writing"))
                eligible.add("EVENTTRIGGER_DEMONIC_TOME")
            eligible.removeAll { emmResolvedEventTriggers.contains(civ.civID + ":" + it) }
            if (eligible.isEmpty() || roll.nextInt(100) != 0) continue
            val selected = eligible[roll.nextInt(eligible.size)]
            emmPendingEvents[civ.civID] = selected
            if (!civ.isHuman()) {
                val safe = when(selected) {
                    "EVENTTRIGGER_WITCH" -> "EVENT_WITCH_2"
                    "EVENTTRIGGER_HOLY_CHILD" -> "EVENT_HOLY_CHILD_1"
                    else -> "EVENT_DEMONIC_TOME_2"
                }
                emmResolveRandomEvent(civ.civID, safe)
            } else {
                civ.addNotification(
                    "An EMM random event is awaiting resolution: " + selected,
                    com.unciv.logic.civilization.NotificationCategory.General
                )
            }
        }
    }
''')
needle='''                turns++
                if (DebugUtils.SIMULATE_UNTIL_TURN != 0)'''
assert g.count(needle)==1
g=g.replace(needle,'''                turns++
                emmScheduleRandomEvents()
                if (DebugUtils.SIMULATE_UNTIL_TURN != 0)''')
gamefile.write_text(g)

console=root/'core/src/com/unciv/ui/screens/devconsole/ConsoleGameCommands.kt'
v=console.read_text()
needle='''        "emm-armageddon" to ConsoleAction'''
assert v.count(needle)==1
v=v.replace(needle,'''        "emm-event" to ConsoleAction("game emm-event <choiceId>") { console, params ->
            if (!console.gameInfo.emmResolveRandomEvent(
                    console.gameInfo.currentPlayerCiv.civID, params[0].toString()
                ))
                throw ConsoleErrorException("No pending event with this choice")
            DevConsoleResponse.OK
        },

'''+needle)
console.write_text(v)
print('Installed serialized random event queue, scheduler, and choice resolution')


# Native EMM event decision dialog using Unciv's existing PopupAlert pipeline.
# Keeps pending choice state until the player explicitly selects a supported
# fully-implemented consequence.
alert=root/'core/src/com/unciv/ui/screens/worldscreen/AlertPopup.kt'
v=alert.read_text()
needle='''    private fun addEvent(): Boolean {'''
assert v.count(needle)==1
v=v.replace(needle,'''    private fun addEmmEvent(): Boolean {
        val eventId = gameInfo.emmPendingEvents[viewingCiv.civID] ?: return false
        if (popupAlert.value != "EMM_EVENT:" + eventId) return false
        val caption = when(eventId) {
            "EVENTTRIGGER_WITCH" -> "A witch has appeared in your lands"
            "EVENTTRIGGER_HOLY_CHILD" -> "The Holy Child"
            "EVENTTRIGGER_DEMONIC_TOME" -> "A Demonic Tome has been discovered"
            else -> return false
        }
        addGoodSizedLabel(caption)
        val options = when(eventId) {
            "EVENTTRIGGER_WITCH" -> listOf(
                "EVENT_WITCH_2" to "Reject the witch (Armageddon -1)"
            )
            "EVENTTRIGGER_HOLY_CHILD" -> listOf(
                "EVENT_HOLY_CHILD_1" to "Protect the child (Armageddon -5)",
                "EVENT_HOLY_CHILD_3" to "Sacrifice two population and 25 gold (Armageddon +10)"
            )
            else -> listOf(
                "EVENT_DEMONIC_TOME_2" to "Destroy the tome (Armageddon -5)"
            )
        }
        for ((id, description) in options) {
            if (!gameInfo.emmCanResolveEvent(viewingCiv.civID, id)) continue
            val button = description.toTextButton()
            button.onActivation {
                if (gameInfo.emmResolveRandomEvent(viewingCiv.civID, id)) close()
            }
            add(button).row()
        }
        getScrollPane()?.fadeScrollBars = false
        return true
    }

    private fun addEvent(): Boolean {
        if (popupAlert.value.startsWith("EMM_EVENT:")) return addEmmEvent()''')
alert.write_text(v)

# Retain explicit choice validation and save a city target for city events.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='''    var emmPendingEvents = hashMapOf<String, String>()'''
assert g.count(needle)==1
g=g.replace(needle,needle+'''
    var emmPendingEventCities = hashMapOf<String, String>()''')
needle='''    fun emmResolveRandomEvent(civID: String, choice: String): Boolean {'''
assert g.count(needle)==1
g=g.replace(needle,'''    fun emmCanResolveEvent(civID: String, choice: String): Boolean {
        val event = emmPendingEvents[civID] ?: return false
        if (choice == "EVENT_HOLY_CHILD_3" && event == "EVENTTRIGGER_HOLY_CHILD") {
            val civ = civilizations.firstOrNull { it.civID == civID } ?: return false
            val city = civ.cities.firstOrNull { it.id == emmPendingEventCities[civID] }
                ?: return false
            return civ.gold >= 25 && city.population.population >= 3
        }
        return when (event) {
            "EVENTTRIGGER_WITCH" -> choice == "EVENT_WITCH_2"
            "EVENTTRIGGER_HOLY_CHILD" -> choice == "EVENT_HOLY_CHILD_1"
            "EVENTTRIGGER_DEMONIC_TOME" -> choice == "EVENT_DEMONIC_TOME_2"
            else -> false
        }
    }

'''+needle)
needle='''            "EVENTTRIGGER_HOLY_CHILD" -> "EVENT_HOLY_CHILD_1"
            "EVENTTRIGGER_DEMONIC_TOME" -> "EVENT_DEMONIC_TOME_2"'''
assert g.count(needle)==1
g=g.replace(needle,'''            "EVENTTRIGGER_HOLY_CHILD" ->
                if (choice == "EVENT_HOLY_CHILD_3") "EVENT_HOLY_CHILD_3" else "EVENT_HOLY_CHILD_1"
            "EVENTTRIGGER_DEMONIC_TOME" -> "EVENT_DEMONIC_TOME_2"''',1)
needle='''        if (choice != accepted) return false
        if (!applyEmmArmageddonEventChoice(choice)) return false'''
assert g.count(needle)==1
g=g.replace(needle,'''        if (choice != accepted) return false
        if (choice == "EVENT_HOLY_CHILD_3") {
            if (!emmCanResolveEvent(civID, choice)) return false
            val civ = civilizations.first { it.civID == civID }
            val city = civ.cities.first { it.id == emmPendingEventCities[civID] }
            civ.addGold(-25)
            city.population.setPopulation(city.population.population - 2)
        }
        if (!applyEmmArmageddonEventChoice(choice)) return false''')
needle='''        emmPendingEvents.remove(civID)
        emmResolvedEventTriggers.add(civID + ":" + event)'''
assert g.count(needle)==1
g=g.replace(needle,'''        emmPendingEvents.remove(civID)
        emmPendingEventCities.remove(civID)
        emmResolvedEventTriggers.add(civID + ":" + event)''')
needle='''            emmPendingEvents[civ.civID] = selected
            if (!civ.isHuman()) {'''
assert g.count(needle)==1
g=g.replace(needle,'''            emmPendingEvents[civ.civID] = selected
            if (selected != "EVENTTRIGGER_DEMONIC_TOME")
                civ.cities.firstOrNull { it.population.population >= 3 }?.let {
                    emmPendingEventCities[civ.civID] = it.id
                }
            if (!civ.isHuman()) {''')
needle='''                civ.addNotification(
                    "An EMM random event is awaiting resolution: " + selected,
                    com.unciv.logic.civilization.NotificationCategory.General
                )'''
assert g.count(needle)==1
g=g.replace(needle,'''                civ.popupAlerts.add(
                    com.unciv.logic.civilization.PopupAlert(
                        com.unciv.logic.civilization.AlertType.Event, "EMM_EVENT:" + selected
                    )
                )''')
gamefile.write_text(g)
print('Added native EMM event choice popup and source-backed Holy Child sacrifice effect')


# Generate a typed reusable engine-side source catalog for all 23 EMM event
# triggers. Eligibility checks can be progressively added without copying XML
# numbers into game logic or silently treating unsupported predicates as valid.
event_registry=json.loads(Path('docs/data/emm-armageddon-event-triggers.json').read_text())
assert len(event_registry['events'])==23
era_chances=json.loads(Path('docs/data/emm-event-era-chances.json').read_text())['eraEventChancePercent']
assert set(era_chances.values())=={4}
def ks(value):
    return json.dumps(str(value),ensure_ascii=False)
def kl(values):
    return 'listOf('+', '.join(ks(v) for v in values)+')'
definitions=[]
for event in event_registry['events']:
    c=event['criteria']
    definitions.append('''        EmmEventTrigger(
            id=%s, weight=%d, percentActive=%d, minAC=%d,
            minPopulation=%d, minTreasury=%d,
            prerequisiteTech=%s, needsCity=%s,
            needsPlots=%s, needsUnits=%s,
            terrain=%s, features=%s, improvements=%s,
            resources=%s, pythonConditions=%s,
            civilizations=%s, buildings=%s,
            recurring=%s, choices=%s
        )'''%(
        ks(event['id']),c['weight'],c['percentGamesActive'],c['minAC'],
        c['minPopulation'],c['minTreasury'],
        'null' if not c['prereqTech'] else ks(c['prereqTech'].removeprefix('TECH_').replace('_',' ').title()),
        str(bool(c['city'])).lower(),str(bool(c['plots'])).lower(),str(bool(c['units'])).lower(),
        kl(c['terrain']),kl(c['features']),kl(c['improvements']),
        kl(c['bonuses']),kl(c['python']),kl(c['civilizations']),
        kl(c['buildingClass']),str(bool(c['recurring'])).lower(),
        kl([x['id'] for x in event['choices']])
    ))
catalog=root/'core/src/com/unciv/logic/EmmEventCatalog.kt'
catalog.write_text('''package com.unciv.logic

/** Parsed at build time from the pinned EMM event XML. */
data class EmmEventTrigger(
    val id: String,
    val weight: Int,
    val percentActive: Int,
    val minAC: Int,
    val minPopulation: Int,
    val minTreasury: Int,
    val prerequisiteTech: String?,
    val needsCity: Boolean,
    val needsPlots: Boolean,
    val needsUnits: Boolean,
    val terrain: List<String>,
    val features: List<String>,
    val improvements: List<String>,
    val resources: List<String>,
    val pythonConditions: List<String>,
    val civilizations: List<String>,
    val buildings: List<String>,
    val recurring: Boolean,
    val choices: List<String>
)

/** All 23 original triggers, not all enabled until full XML effects are supported. */
object EmmEventCatalog {
    const val eraChance = 4
    val triggers = listOf(
%s
    )
    val byId = triggers.associateBy { it.id }
}
'''%(',\n'.join(definitions)))
print('Generated EMM catalog with 23 source-derived trigger records and source era chance')


# The source EMM catalog now owns the supported three trigger weights and
# the original per-era event chance. Unsupported predicates are not enabled.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='''            if (eligible.isEmpty() || roll.nextInt(100) != 0) continue
            val selected = eligible[roll.nextInt(eligible.size)]'''
assert g.count(needle)==1
g=g.replace(needle,'''            if (eligible.isEmpty() ||
                roll.nextInt(100) >= EmmEventCatalog.eraChance) continue
            val weighted = eligible.mapNotNull { id ->
                val definition = EmmEventCatalog.byId[id] ?: return@mapNotNull null
                if (roll.nextInt(100) >= definition.percentActive) null
                else definition
            }
            if (weighted.isEmpty()) continue
            val totalWeight = weighted.sumOf { it.weight }
            var choiceRoll = roll.nextInt(totalWeight)
            val selected = weighted.first { definition ->
                choiceRoll -= definition.weight
                choiceRoll < 0
            }.id''')
gamefile.write_text(g)
print('Replaced arbitrary 1%/uniform event selection with source era chance and XML trigger weights')


# Next native event families: source eligibility and complete XML choices.
# Only choices whose full non-AC fields are empty are eligible.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='''            "EVENTTRIGGER_DEMONIC_TOME" -> choice == "EVENT_DEMONIC_TOME_2"
            else -> false'''
assert g.count(needle)==1
g=g.replace(needle,'''            "EVENTTRIGGER_DEMONIC_TOME" -> choice == "EVENT_DEMONIC_TOME_2"
            "EVENTTRIGGER_SHRINE_CAMULOS" -> choice == "EVENT_SHRINE_CAMULOS_1"
            "EVENTTRIGGER_NECRO_CANNIBALISM" -> choice == "EVENT_NECRO_CANNIBALISM_2"
            "EVENTTRIGGER_IRON_ORB" -> choice == "EVENT_IRON_ORB_1"
            "EVENTTRIGGER_STRANGE_ADEPT" -> choice == "EVENT_STRANGE_ADEPT_1"
            else -> false''')
needle='''            "EVENTTRIGGER_DEMONIC_TOME" -> "EVENT_DEMONIC_TOME_2"
            else -> return false'''
assert g.count(needle)==1
g=g.replace(needle,'''            "EVENTTRIGGER_DEMONIC_TOME" -> "EVENT_DEMONIC_TOME_2"
            "EVENTTRIGGER_SHRINE_CAMULOS" -> "EVENT_SHRINE_CAMULOS_1"
            "EVENTTRIGGER_NECRO_CANNIBALISM" -> "EVENT_NECRO_CANNIBALISM_2"
            "EVENTTRIGGER_IRON_ORB" -> "EVENT_IRON_ORB_1"
            "EVENTTRIGGER_STRANGE_ADEPT" -> "EVENT_STRANGE_ADEPT_1"
            else -> return false''')
needle='''        if (!applyEmmArmageddonEventChoice(choice)) return false
        emmPendingEvents.remove(civID)'''
assert g.count(needle)==1
g=g.replace(needle,'''        // Original XML: the two decline choices have no counter or secondary effect.
        if (choice !in listOf("EVENT_IRON_ORB_1", "EVENT_STRANGE_ADEPT_1") &&
            !applyEmmArmageddonEventChoice(choice)) return false
        emmPendingEvents.remove(civID)''')
needle='''            if (emmArmageddonCounter >= 10 && civ.tech.isResearched("Writing"))
                eligible.add("EVENTTRIGGER_DEMONIC_TOME")'''
assert g.count(needle)==1
g=g.replace(needle,'''            if (emmArmageddonCounter >= 10 && civ.tech.isResearched("Writing"))
                eligible.add("EVENTTRIGGER_DEMONIC_TOME")
            // Source event: Shrine of Camulos, population 3+ and Training Yard,
            // only active in 10% of games; the catalog enforces that roll.
            if (civ.cities.any { city ->
                city.population.population >= 3 &&
                city.cityConstructions.containsBuildingOrEquivalent("Training Yard")
            }) eligible.add("EVENTTRIGGER_SHRINE_CAMULOS")
            // Source event: Iron Orb requires >=75 treasury and Library.
            if (civ.gold >= 75 && civ.cities.any { city ->
                city.cityConstructions.containsBuildingOrEquivalent("Library")
            }) eligible.add("EVENTTRIGGER_IRON_ORB")
            if (civ.cities.any { city ->
                city.cityConstructions.containsBuildingOrEquivalent("Mage Guild")
            }) eligible.add("EVENTTRIGGER_STRANGE_ADEPT")
            // Source necro-cannibalism: AC 65+, city 5+, evil alignment
            // for choice #2. Dynamic alignment remains a separate TODO.
            if (emmArmageddonCounter >= 65 &&
                civ.civName in setOf(
                    "Balseraphs", "Calabim", "Clan of Embers", "Doviello",
                    "Illians", "Sheaim", "Svartalfar"
                ) && civ.cities.any { it.population.population >= 5 })
                eligible.add("EVENTTRIGGER_NECRO_CANNIBALISM")''')
needle='''                val safe = when(selected) {
                    "EVENTTRIGGER_WITCH" -> "EVENT_WITCH_2"
                    "EVENTTRIGGER_HOLY_CHILD" -> "EVENT_HOLY_CHILD_1"
                    else -> "EVENT_DEMONIC_TOME_2"
                }'''
assert g.count(needle)==1
g=g.replace(needle,'''                val safe = when(selected) {
                    "EVENTTRIGGER_WITCH" -> "EVENT_WITCH_2"
                    "EVENTTRIGGER_HOLY_CHILD" -> "EVENT_HOLY_CHILD_1"
                    "EVENTTRIGGER_SHRINE_CAMULOS" -> "EVENT_SHRINE_CAMULOS_1"
                    "EVENTTRIGGER_NECRO_CANNIBALISM" -> "EVENT_NECRO_CANNIBALISM_2"
                    "EVENTTRIGGER_IRON_ORB" -> "EVENT_IRON_ORB_1"
                    "EVENTTRIGGER_STRANGE_ADEPT" -> "EVENT_STRANGE_ADEPT_1"
                    else -> "EVENT_DEMONIC_TOME_2"
                }''')
gamefile.write_text(g)

alert=root/'core/src/com/unciv/ui/screens/worldscreen/AlertPopup.kt'
v=alert.read_text()
needle='''            "EVENTTRIGGER_DEMONIC_TOME" -> "A Demonic Tome has been discovered"
            else -> return false'''
assert v.count(needle)==1
v=v.replace(needle,'''            "EVENTTRIGGER_DEMONIC_TOME" -> "A Demonic Tome has been discovered"
            "EVENTTRIGGER_SHRINE_CAMULOS" -> "The Shrine of Camulos"
            "EVENTTRIGGER_NECRO_CANNIBALISM" -> "Necro-Cannibalism"
            "EVENTTRIGGER_IRON_ORB" -> "The Iron Orb"
            "EVENTTRIGGER_STRANGE_ADEPT" -> "A Strange Adept"
            else -> return false''')
needle='''            else -> listOf(
                "EVENT_DEMONIC_TOME_2" to "Destroy the tome (Armageddon -5)"
            )'''
assert v.count(needle)==1
v=v.replace(needle,'''            "EVENTTRIGGER_SHRINE_CAMULOS" -> listOf(
                "EVENT_SHRINE_CAMULOS_1" to "Honor Camulos (Armageddon +1)"
            )
            "EVENTTRIGGER_NECRO_CANNIBALISM" -> listOf(
                "EVENT_NECRO_CANNIBALISM_2" to "Permit the practice (Armageddon +3)"
            )
            "EVENTTRIGGER_IRON_ORB" -> listOf(
                "EVENT_IRON_ORB_1" to "Leave the orb untouched"
            )
            "EVENTTRIGGER_STRANGE_ADEPT" -> listOf(
                "EVENT_STRANGE_ADEPT_1" to "Turn the adept away"
            )
            else -> listOf(
                "EVENT_DEMONIC_TOME_2" to "Destroy the tome (Armageddon -5)"
            )''')
alert.write_text(v)
print('Enabled four source-gated EMM event families with full-effect-safe choices')


# Reusable EMM event-choice effect interpreter. Only XML effect fields that
# the engine can execute faithfully are allowed into the gameplay whitelist.
# Built from source JSON at build time rather than hand-maintained deltas.
eventdata=json.loads(Path('docs/data/emm-armageddon-event-triggers.json').read_text())
supported_fields={'Type','Description','Button','Civilopedia','iMaxNumReligions','iAIValue',
    'iGlobalCounter','bPickCity','iGold','iPopulationChange','iHappy','iHealth'}
effectmap={}
for trigger in eventdata['events']:
    for choice in trigger['choices']:
        fields=choice['fields']
        extras={k for k in fields if k not in supported_fields}
        if extras: continue
        vals={k:int(fields.get(k,['0'])[0]) for k in
            ('iGlobalCounter','iGold','iPopulationChange','iHappy','iHealth')}
        effectmap[choice['id']]=vals
assert effectmap['EVENT_WITCH_1']['iHealth']==-3
assert effectmap['EVENT_HOLY_CHILD_2']['iGold']==-50
def entry(name,values):
    return '        %s to EmmEventEffect(%d, %d, %d, %d, %d)'%(
        ks(name),values['iGlobalCounter'],values['iGold'],
        values['iPopulationChange'],values['iHappy'],values['iHealth'])
effectfile=root/'core/src/com/unciv/logic/EmmEventEffects.kt'
effectfile.write_text('''package com.unciv.logic

/** Whitelisted complete numeric effects, extracted from EMM EventInfos XML. */
data class EmmEventEffect(
    val armageddon: Int,
    val gold: Int,
    val population: Int,
    val happiness: Int,
    val health: Int
)
object EmmEventEffects {
    val choices = mapOf(
%s
    )
}
'''%(',\n'.join(entry(n,v) for n,v in sorted(effectmap.items()))))

cityfile=root/'core/src/com/unciv/logic/city/City.kt'
c=cityfile.read_text()
needle='    var emmDiseaseHealthCounter = 0'
assert c.count(needle)==1
c=c.replace(needle,needle+'''
    /** Persistent EMM city event effects distinct from temporary epidemic unhealth. */
    var emmEventHealth = 0
    var emmEventHappiness = 0
''')
needle='        toReturn.emmDiseaseHealthCounter = emmDiseaseHealthCounter'
assert c.count(needle)==1
c=c.replace(needle,needle+'''
        toReturn.emmEventHealth = emmEventHealth
        toReturn.emmEventHappiness = emmEventHappiness''')
cityfile.write_text(c)

city_stats=root/'core/src/com/unciv/logic/city/CityStats.kt'
v=city_stats.read_text()
needle='''            val totalUnhealthy = unhealthyPopulation + featureUnhealth + buildingUnhealth + city.emmDiseaseHealthCounter'''
assert v.count(needle)==1
v=v.replace(needle,'''            val eventUnhealth = (-city.emmEventHealth).coerceAtLeast(0)
            val eventHealthy = city.emmEventHealth.coerceAtLeast(0)
            val totalUnhealthy = unhealthyPopulation + featureUnhealth + buildingUnhealth +
                city.emmDiseaseHealthCounter + eventUnhealth''')
needle='''            emmHealthInfo = healthySources to totalUnhealthy'''
assert v.count(needle)==1
v=v.replace(needle,'''            emmHealthInfo = (healthySources + eventHealthy) to totalUnhealthy''')
needle='''                "Healthy buildings" to buildingHealth,'''
assert v.count(needle)==1
v=v.replace(needle,needle+'''
                "Event health" to city.emmEventHealth,''')
needle='''            val netUnhealthy = (totalUnhealthy - healthySources).coerceAtLeast(0)'''
assert v.count(needle)==1
v=v.replace(needle,'''            val netUnhealthy = (totalUnhealthy - healthySources - eventHealthy).coerceAtLeast(0)''')
needle='''        happinessList = newHappinessList'''
assert v.count(needle)==1
v=v.replace(needle,'''        if (city.emmEventHappiness != 0)
            newHappinessList["EMM random events"] = city.emmEventHappiness.toFloat()
'''+needle)
city_stats.write_text(v)

# This gate is shared by UI, AI, and debug console.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='''        if (choice == "EVENT_HOLY_CHILD_3" && event == "EVENTTRIGGER_HOLY_CHILD") {'''
assert g.count(needle)==1
g=g.replace(needle,'''        val effect = EmmEventEffects.choices[choice] ?: return false
        val civ = civilizations.firstOrNull { it.civID == civID } ?: return false
        if (effect.gold < 0 && civ.gold < -effect.gold) return false
        if (effect.population != 0 || effect.health != 0 || effect.happiness != 0) {
            val city = civ.cities.firstOrNull { it.id == emmPendingEventCities[civID] }
                ?: return false
            if (city.population.population + effect.population < 1) return false
        }
'''+needle)
needle='''            "EVENTTRIGGER_WITCH" -> choice == "EVENT_WITCH_2"'''
assert g.count(needle)==1
g=g.replace(needle,'''            "EVENTTRIGGER_WITCH" ->
                choice == "EVENT_WITCH_2" || choice == "EVENT_WITCH_1"''',1)
needle='''            "EVENTTRIGGER_HOLY_CHILD" -> choice == "EVENT_HOLY_CHILD_1"'''
assert g.count(needle)==1
g=g.replace(needle,'''            "EVENTTRIGGER_HOLY_CHILD" ->
                choice == "EVENT_HOLY_CHILD_1" || choice == "EVENT_HOLY_CHILD_2"''',1)
needle='''        if (choice != accepted) return false'''
assert g.count(needle)==1
g=g.replace(needle,'''        if (!emmCanResolveEvent(civID, choice)) return false
        if (choice != accepted &&
            choice !in listOf("EVENT_WITCH_1", "EVENT_HOLY_CHILD_2")) return false''')
needle='''        if (choice == "EVENT_HOLY_CHILD_3") {
            if (!emmCanResolveEvent(civID, choice)) return false
            val civ = civilizations.first { it.civID == civID }
            val city = civ.cities.first { it.id == emmPendingEventCities[civID] }
            civ.addGold(-25)
            city.population.setPopulation(city.population.population - 2)
        }
        // Original XML: the two decline choices have no counter or secondary effect.
        if (choice !in listOf("EVENT_IRON_ORB_1", "EVENT_STRANGE_ADEPT_1") &&
            !applyEmmArmageddonEventChoice(choice)) return false'''
assert g.count(needle)==1
g=g.replace(needle,'''        val effect = EmmEventEffects.choices[choice] ?: return false
        val civ = civilizations.first { it.civID == civID }
        if (effect.gold != 0) civ.addGold(effect.gold)
        if (effect.population != 0 || effect.health != 0 || effect.happiness != 0) {
            val city = civ.cities.first { it.id == emmPendingEventCities[civID] }
            if (effect.population != 0)
                city.population.setPopulation(city.population.population + effect.population)
            city.emmEventHealth += effect.health
            city.emmEventHappiness += effect.happiness
            city.cityStats.update()
        }
        if (effect.armageddon != 0) changeEmmArmageddon(effect.armageddon)''')
gamefile.write_text(g)

alert=root/'core/src/com/unciv/ui/screens/worldscreen/AlertPopup.kt'
v=alert.read_text()
needle='''            "EVENTTRIGGER_WITCH" -> listOf(
                "EVENT_WITCH_2" to "Reject the witch (Armageddon -1)"
            )'''
assert v.count(needle)==1
v=v.replace(needle,'''            "EVENTTRIGGER_WITCH" -> listOf(
                "EVENT_WITCH_1" to "Accept the witch (+1 city happiness, -3 health; Armageddon +2)",
                "EVENT_WITCH_2" to "Reject the witch (Armageddon -1)"
            )''')
needle='''                "EVENT_HOLY_CHILD_1" to "Protect the child (Armageddon -5)",'''
assert v.count(needle)==1
v=v.replace(needle,needle+'''
                "EVENT_HOLY_CHILD_2" to "Support the child (-50 gold, +1 city happiness, +1 health; Armageddon -10)",''')
alert.write_text(v)
print('Generated generic EMM numeric event effects, integrated persistent city health/happiness and two new source choices')


# Source-faithful building-linked commerce effect from Iron Orb 2,
# and the Sobs event's numeric-only outcome.
data=json.loads(Path('docs/data/emm-armageddon-event-triggers.json').read_text())
ev={e['id']:e for e in data['events']}
orb=next(c for c in ev['EVENTTRIGGER_IRON_ORB']['choices'] if c['id']=='EVENT_IRON_ORB_2')
assert orb['fields']['BuildingClass']==['BUILDINGCLASS_LIBRARY']
assert orb['fields']['CommerceType']==['COMMERCE_RESEARCH']
assert orb['fields']['iExtraCommerce']==['2']
assert orb['fields']['iGold']==['-75']
sobs=next(c for c in ev['EVENTTRIGGER_SOBS']['choices'] if c['id']=='EVENT_SOBS_1')
assert sobs['fields']['iHappy']==['-1']
assert ev['EVENTTRIGGER_SOBS']['criteria']['minAC']==10

# Extend the effect table with a typed building-science modifier, never apply
# the bonus to cities where the required building is missing.
effects=root/'core/src/com/unciv/logic/EmmEventEffects.kt'
v=effects.read_text()
needle='''    val health: Int
)'''
assert v.count(needle)==1
v=v.replace(needle,'''    val health: Int,
    val libraryScience: Int = 0
)''')
needle='''    val choices = mapOf('''
assert v.count(needle)==1
v=v.replace(needle,'''    val choices = mapOf(
        "EVENT_IRON_ORB_2" to EmmEventEffect(2, -75, 0, 0, 0, 2),''')
effects.write_text(v)

cityfile=root/'core/src/com/unciv/logic/city/City.kt'
c=cityfile.read_text()
needle='    var emmEventHappiness = 0'
assert c.count(needle)==1
c=c.replace(needle,needle+'''
    /** Extra permanent Library research generated by source EMM event effects. */
    var emmEventLibraryScience = 0''')
needle='        toReturn.emmEventHappiness = emmEventHappiness'
assert c.count(needle)==1
c=c.replace(needle,needle+'''
        toReturn.emmEventLibraryScience = emmEventLibraryScience''')
cityfile.write_text(c)
stats=root/'core/src/com/unciv/logic/city/CityStats.kt'
v=stats.read_text()
needle='''        newBaseStatTree.children["Buildings"] = statsFromBuildings'''
assert v.count(needle)==1
v=v.replace(needle,needle+'''
        if (city.emmEventLibraryScience != 0 &&
            city.cityConstructions.containsBuildingOrEquivalent("Library"))
            newBaseStatTree.addStats(
                Stats(science = city.emmEventLibraryScience.toFloat()),
                "EMM Library event"
            )''')
stats.write_text(v)

gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='''        if (effect.population != 0 || effect.health != 0 || effect.happiness != 0) {'''
assert g.count(needle)==2
g=g.replace(needle,'''        if (effect.libraryScience != 0) {
            val city = civ.cities.firstOrNull { it.id == emmPendingEventCities[civID] }
                ?: return false
            if (!city.cityConstructions.containsBuildingOrEquivalent("Library"))
                return false
        }
'''+needle,1)
needle='''            "EVENTTRIGGER_IRON_ORB" -> choice == "EVENT_IRON_ORB_1"'''
assert g.count(needle)==1
g=g.replace(needle,'''            "EVENTTRIGGER_IRON_ORB" ->
                choice == "EVENT_IRON_ORB_1" || choice == "EVENT_IRON_ORB_2"
            "EVENTTRIGGER_SOBS" -> choice == "EVENT_SOBS_1"''',1)
needle='''            "EVENTTRIGGER_IRON_ORB" -> "EVENT_IRON_ORB_1"'''
assert g.count(needle)==2
g=g.replace(needle,'''            "EVENTTRIGGER_IRON_ORB" ->
                if (choice == "EVENT_IRON_ORB_2") choice else "EVENT_IRON_ORB_1"
            "EVENTTRIGGER_SOBS" -> "EVENT_SOBS_1"''',1)
needle='''            choice !in listOf("EVENT_WITCH_1", "EVENT_HOLY_CHILD_2")) return false'''
assert g.count(needle)==1
g=g.replace(needle,'''            choice !in listOf("EVENT_WITCH_1", "EVENT_HOLY_CHILD_2",
                "EVENT_IRON_ORB_2")) return false''')
needle='''        if (effect.gold != 0) civ.addGold(effect.gold)'''
assert g.count(needle)==1
g=g.replace(needle,'''        if (effect.libraryScience != 0) {
            val libraryCity = civ.cities.first { it.id == emmPendingEventCities[civID] }
            libraryCity.emmEventLibraryScience += effect.libraryScience
            libraryCity.cityStats.update()
        }
'''+needle)
needle='''            if (civ.cities.any { it.population.population >= 3 }) {
                eligible.add("EVENTTRIGGER_WITCH")
                if (emmArmageddonCounter >= 10) eligible.add("EVENTTRIGGER_HOLY_CHILD")
            }'''
assert g.count(needle)==1
g=g.replace(needle,'''            if (civ.cities.any { it.population.population >= 3 }) {
                eligible.add("EVENTTRIGGER_WITCH")
                if (emmArmageddonCounter >= 10) {
                    eligible.add("EVENTTRIGGER_HOLY_CHILD")
                    eligible.add("EVENTTRIGGER_SOBS")
                }
            }''')
needle='''            if (selected != "EVENTTRIGGER_DEMONIC_TOME")
                civ.cities.firstOrNull { it.population.population >= 3 }?.let {
                    emmPendingEventCities[civ.civID] = it.id
                }'''
assert g.count(needle)==1
g=g.replace(needle,'''            if (selected != "EVENTTRIGGER_DEMONIC_TOME") {
                val eventCity = when (selected) {
                    "EVENTTRIGGER_IRON_ORB" ->
                        civ.cities.firstOrNull {
                            it.cityConstructions.containsBuildingOrEquivalent("Library")
                        }
                    "EVENTTRIGGER_STRANGE_ADEPT" ->
                        civ.cities.firstOrNull {
                            it.cityConstructions.containsBuildingOrEquivalent("Mage Guild")
                        }
                    "EVENTTRIGGER_SHRINE_CAMULOS" ->
                        civ.cities.firstOrNull {
                            it.population.population >= 3 &&
                            it.cityConstructions.containsBuildingOrEquivalent("Training Yard")
                        }
                    "EVENTTRIGGER_NECRO_CANNIBALISM" ->
                        civ.cities.firstOrNull { it.population.population >= 5 }
                    else -> civ.cities.firstOrNull { it.population.population >= 3 }
                }
                if (eventCity != null) emmPendingEventCities[civ.civID] = eventCity.id
            }''')
needle='''                    "EVENTTRIGGER_IRON_ORB" -> "EVENT_IRON_ORB_1"'''
assert g.count(needle)==1
g=g.replace(needle,needle+'''
                    "EVENTTRIGGER_SOBS" -> "EVENT_SOBS_1"''')
gamefile.write_text(g)

alert=root/'core/src/com/unciv/ui/screens/worldscreen/AlertPopup.kt'
v=alert.read_text()
needle='''            "EVENTTRIGGER_IRON_ORB" -> "The Iron Orb"'''
assert v.count(needle)==1
v=v.replace(needle,needle+'''
            "EVENTTRIGGER_SOBS" -> "Sobs in the city"''')
needle='''            "EVENTTRIGGER_IRON_ORB" -> listOf(
                "EVENT_IRON_ORB_1" to "Leave the orb untouched"
            )'''
assert v.count(needle)==1
v=v.replace(needle,'''            "EVENTTRIGGER_IRON_ORB" -> listOf(
                "EVENT_IRON_ORB_1" to "Leave the orb untouched",
                "EVENT_IRON_ORB_2" to "Pay 75 gold for +2 permanent Library research (Armageddon +2)"
            )
            "EVENTTRIGGER_SOBS" -> listOf(
                "EVENT_SOBS_1" to "Endure the sorrow (-1 city happiness)"
            )''')
alert.write_text(v)
print('Enabled Iron Orb original Library science bonus and new Sobs event via shared saved numeric effects')


# Reusable EMM event unit/tile effect interfaces. The transaction gates map
# source unit classes to actual ruleset names and skips absent promotions.
# Unported EMM-only units/promotions are deliberately NOT fabricated.
eventmethods=root/'core/src/com/unciv/logic/EmmEventWorldEffects.kt'
eventmethods.write_text('''package com.unciv.logic

import com.unciv.logic.civilization.Civilization
import com.unciv.logic.city.City
import com.unciv.logic.map.mapunit.MapUnit
import com.unciv.logic.map.tile.Tile

/** Shared engine operations for source XML unit, promotion and map effects. */
object EmmEventWorldEffects {
    /** Atomic prerequisite checking prevents partial unit/promotion outcomes. */
    fun spawnWithPromotions(
        civ: Civilization, city: City, unitName: String,
        promotionNames: List<String>, count: Int
    ): Boolean {
        if (count < 1 || count > 20 ||
            !civ.gameInfo.ruleset.units.containsKey(unitName) ||
            promotionNames.any { !civ.gameInfo.ruleset.unitPromotions.containsKey(it) })
            return false
        val created = mutableListOf<MapUnit>()
        repeat(count) {
            val unit = civ.units.placeUnitNearTile(city.getCenterTile().position, unitName)
            if (unit == null) {
                for (placed in created) placed.destroy()
                return false
            }
            created.add(unit)
        }
        for (placed in created)
            for (promotion in promotionNames)
                placed.promotions.addPromotion(promotion, true)
        return true
    }

    /** Delete only the event's specified improvement, never a replacement. */
    fun removeNamedImprovement(tile: Tile, expectedName: String): Boolean {
        if (tile.improvement != expectedName) return false
        tile.removeImprovement()
        return true
    }

    /** War Games original selection predicate (living attacker with experience).
     *  EMM's special Alive flag needs a unit-type source audit: reject obvious
     *  civilian/zero-strength units and use available combat unit rules.
     */
    fun eligibleWarGamesUnit(unit: MapUnit): Boolean =
        !unit.isCivilian() && unit.baseUnit.strength > 0 &&
            unit.promotions.totalXpProduced() > 0
}
''')
print('Installed reusable source-validated unit spawn, free promotions and conditional map removal helpers')

# War Games unit target is persisted across save/load just as city targets are.
gamefile=root/'core/src/com/unciv/logic/GameInfo.kt'
g=gamefile.read_text()
needle='''    var emmPendingEventCities = hashMapOf<String, String>()'''
assert g.count(needle)==1
g=g.replace(needle,needle+'''
    /** ID of the exact combat unit affected by a random event. */
    var emmPendingEventUnits = hashMapOf<String, Int>()''')
needle='''        val effect = EmmEventEffects.choices[choice] ?: return false'''
assert g.count(needle)==2
g=g.replace(needle,'''        if (event == "EVENTTRIGGER_WAR_GAMES") {
            if (choice != "EVENT_WAR_GAMES_1" && choice != "EVENT_WAR_GAMES_2")
                return false
            val civ = civilizations.firstOrNull { it.civID == civID } ?: return false
            val target = civ.units.getUnitById(emmPendingEventUnits[civID] ?: return false)
                ?: return false
            if (!EmmEventWorldEffects.eligibleWarGamesUnit(target)) return false
        }
'''+needle,1)
needle='''            "EVENTTRIGGER_SOBS" -> choice == "EVENT_SOBS_1"'''
assert g.count(needle)==1
g=g.replace(needle,needle+'''
            "EVENTTRIGGER_WAR_GAMES" ->
                choice == "EVENT_WAR_GAMES_1" || choice == "EVENT_WAR_GAMES_2"''')
needle='''            "EVENTTRIGGER_SOBS" -> "EVENT_SOBS_1"'''
assert g.count(needle)==2
g=g.replace(needle,needle+'''
            "EVENTTRIGGER_WAR_GAMES" ->
                if (choice == "EVENT_WAR_GAMES_2") choice else "EVENT_WAR_GAMES_1"''',1)
needle='''        if (effect.libraryScience != 0) {'''
assert g.count(needle)==2
g=g.replace(needle,'''        if (event == "EVENTTRIGGER_WAR_GAMES") {
            val selectedUnit = civ.units.getUnitById(emmPendingEventUnits[civID]!!)
                ?: return false
            if (choice == "EVENT_WAR_GAMES_1") selectedUnit.destroy()
            if (choice == "EVENT_WAR_GAMES_2")
                selectedUnit.promotions.XP = (selectedUnit.promotions.XP - 1).coerceAtLeast(0)
        }
'''+needle,1)
needle='''        emmPendingEventCities.remove(civID)'''
assert g.count(needle)==1
g=g.replace(needle,needle+'''
        emmPendingEventUnits.remove(civID)''')
needle='''            if (emmArmageddonCounter >= 10 && civ.tech.isResearched("Writing"))'''
assert g.count(needle)==1
g=g.replace(needle,'''            if (emmArmageddonCounter >= 2 && civ.units.getCivUnits()
                .any { EmmEventWorldEffects.eligibleWarGamesUnit(it) })
                eligible.add("EVENTTRIGGER_WAR_GAMES")
'''+needle)
needle='''            emmPendingEvents[civ.civID] = selected'''
assert g.count(needle)==1
g=g.replace(needle,needle+'''
            if (selected == "EVENTTRIGGER_WAR_GAMES")
                civ.units.getCivUnits()
                    .firstOrNull { EmmEventWorldEffects.eligibleWarGamesUnit(it) }
                    ?.let { emmPendingEventUnits[civ.civID] = it.id }''')
needle='''                    "EVENTTRIGGER_SOBS" -> "EVENT_SOBS_1"'''
assert g.count(needle)==1
g=g.replace(needle,needle+'''
                    "EVENTTRIGGER_WAR_GAMES" -> "EVENT_WAR_GAMES_2"''')
gamefile.write_text(g)

# Engine source says unit promotions are stored by name; only grant if all
# event promotion names exist. Actual source ID/unit-class conversion remains
# gated by the canonical roster.
alert=root/'core/src/com/unciv/ui/screens/worldscreen/AlertPopup.kt'
v=alert.read_text()
needle='''            "EVENTTRIGGER_SOBS" -> "Sobs in the city"'''
assert v.count(needle)==1
v=v.replace(needle,needle+'''
            "EVENTTRIGGER_WAR_GAMES" -> "War Games"''')
needle='''            "EVENTTRIGGER_SOBS" -> listOf(
                "EVENT_SOBS_1" to "Endure the sorrow (-1 city happiness)"
            )'''
assert v.count(needle)==1
v=v.replace(needle,needle+'''
            "EVENTTRIGGER_WAR_GAMES" -> listOf(
                "EVENT_WAR_GAMES_1" to "Disband the veteran unit (Armageddon -2)",
                "EVENT_WAR_GAMES_2" to "Spare the unit (-1 experience)"
            )''')
alert.write_text(v)
print('Wired source War Games veteran unit targeting/disbanding and reusable unit/tile event effect APIs')
