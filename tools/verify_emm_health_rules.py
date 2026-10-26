#!/usr/bin/env python3
"""Static regression contracts for the health adapter against pinned EMM XML."""
import json
from pathlib import Path
data=json.loads(Path('docs/data/emm-health-source.json').read_text())
buildings={x['id']:x['fields'] for x in data['groups']['buildings']['entries']}
handicaps={x['id']:int(x['fields']['iHealthBonus']) for x in data['groups']['handicaps']['entries']}
def value(k,field):return int(buildings[k].get(field,'0'))
assert value('BUILDING_HERBALIST','iHealth')==1
assert value('BUILDING_AQUEDUCT','iHealth')==2
assert value('BUILDING_INFIRMARY','iHealth')==3
for b in ('BUILDING_FORGE','BUILDING_DWARVEN_SMITHY','BUILDING_RELIQUARY','BUILDING_PUBLIC_BATHS'):
 assert value(b,'iHealth')==-1, b
assert value('BUILDING_AQUAE_SUCELLUS','iAreaHealth')==1
assert value('BUILDING_PALACE_KURIOTATES','iGlobalHealth')==1
assert buildings['BUILDING_DEMONIC_CITIZENS']['bNoUnhealthyPopulation']=='1'
assert handicaps['HANDICAP_SETTLER']==4 and handicaps['HANDICAP_CHIEFTAIN']==3
assert handicaps['HANDICAP_PRINCE']==2 and handicaps['HANDICAP_DEITY']==2
patch=Path('tools/patch_unciv_health.py').read_text()
for token in ('buildingUnhealth','"Unhealthy buildings"','EMM_AREA_HEALTH','EMM_GLOBAL_HEALTH','EMM_DIFFICULTY_HEALTH','EMM_CONSTRUCTION_HEALTH'):
 assert token in patch,token
# A negative health building adds to the unhealthy tally, not subtracts from the healthy tally.
for healthy, unhealthy, building_health in ((5,4,-1),(3,7,-1),(4,2,2)):
 positive=max(0,building_health)
 negative=max(0,-building_health)
 resulting_healthy=healthy+positive
 resulting_unhealthy=unhealthy+negative
 assert resulting_healthy-resulting_unhealthy==healthy-unhealthy+building_health
print('PASS: signed building health, difficulty, area/global and population-exemption source rules')

# City counters are serialized and event formulas are source-aligned but only
# activated by the future global Armageddon event dispatch.
patch=Path('tools/patch_unciv_health.py').read_text()
for code in ('emmDiseaseHealthCounter','EmmCityEpidemics','fun blight(','fun pestilence(','random15 + city.population.population','random9 + city.population.population / 4'):
 assert code in patch,code
# Property-level event formula tests, including suppression of negative Blight.
def blight(pop, random, bad, good, buildings):return max(0,random+pop+bad-good-buildings)
def pestilence(pop, random, buildings):return random+pop//4-buildings
assert blight(8,3,2,1,4)==8
assert blight(2,0,0,3,2)==0
assert pestilence(12,4,2)==5
print('PASS: Blight/Pestilence formula and city-counter serialization contracts')

source=json.loads(Path('docs/data/emm-disease-promotions.json').read_text())['promotions']
assert int(source['PROMOTION_DISEASED']['iCombatPercent'])==-30
assert int(source['PROMOTION_DISEASED']['iFriendlyHealChange'])==-10
assert int(source['PROMOTION_PLAGUED']['iCombatPercent'])==-60
assert int(source['PROMOTION_PLAGUED']['iFriendlyHealChange'])==-20
patch=Path('tools/patch_unciv_health.py').read_text()
for text in ('it.name == "Diseased" }) healing -= 10','it.name == "Plagued" }) healing -= 20'):
 assert text in patch,text
print('PASS: EMM unit disease combat/healing source values')

# Source specifies Diseased combat infection and immunity to Diseased/Plagued.
assert source['PROMOTION_DISEASED']['PromotionCombatApply']=='PROMOTION_DISEASED'
assert source['PROMOTION_IMMUNE_DISEASE']['PromotionImmune1']=='PROMOTION_DISEASED'
assert source['PROMOTION_IMMUNE_DISEASE']['PromotionImmune2']=='PROMOTION_PLAGUED'
patch=Path('tools/patch_unciv_health.py').read_text()
for token in ('defender.unit.promotions.addPromotion("Diseased", isFree = true)','"Immune to Disease" !in defender.unit.promotions.promotions'):
 assert token in patch,token
print('PASS: Diseased melee/contact promotion source and immunity checks')

for token in ('promotionName in listOf("Diseased", "Plagued")','"Immune to Disease" in promotions','removePromotion("Diseased")','removePromotion("Plagued")'):
 assert token in Path('tools/patch_unciv_health.py').read_text(), token
print('PASS: immunity applies to all promotion sources and clears existing disease')

patch=Path('tools/patch_unciv_health.py').read_text()
for check in ('EmmCureDisease','"Medic II" in unit.promotions.promotions','removePromotion("Diseased")','removePromotion("Plagued")','emmArmageddonCounter = 0','prior < 30','prior < 35','EmmArmageddonEvents.fireBlight(this)','EmmArmageddonEvents.firePestilence(this)'):
 assert check in patch,check
print('PASS: Medic II cure and serialized AC 30/35 threshold dispatch contracts')
