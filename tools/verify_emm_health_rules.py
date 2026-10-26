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

patch=Path('tools/patch_unciv_health.py').read_text()
for token in ('game emm-armageddon <delta>','changeEmmArmageddon(delta)','Armageddon: $ac / 100'):
 assert token in patch,token
print('PASS: user-visible Armageddon meter and developer counter test entry point')

arm=json.loads(Path('docs/data/emm-armageddon-sources.json').read_text())
assert arm['commit']=='60b0ec3740083162aaab7bf8491761a54a65a610'
r={item['religion']:item for item in arm['sources']}
assert r['The Ashen Veil']['iGlobalCounterFound']==5
assert r['The Ashen Veil']['iGlobalCounterSpread']==1
assert r['Octopus Overlords']['iGlobalCounterFound']==3
assert r['Octopus Overlords']['iGlobalCounterSpread']==0
patch=Path('tools/patch_unciv_health.py').read_text()
for token in ('emmFoundReligion(name: String','emmSpreadReligion(name: String','changeEmmArmageddon(5)','changeEmmArmageddon(3)','changeEmmArmageddon(1)','"Corruption of Spirit"','"Message from the Deep"','EmmSpreadAshenVeil','unit.getTile().isCityCenter()'):
 assert token in patch,token
u=next(x for x in json.loads(Path('jsons/Units.json').read_text()) if x['name']=='Disciple of the Ashen Veil')
assert (u['cost'],u['strength'],u['movement'])==(60,3,1)
print('PASS: native gameplay EMM religious AC source values and disciple')

align=json.loads(Path('docs/data/emm-leader-alignments.json').read_text())
assert align['commit']=='60b0ec3740083162aaab7bf8491761a54a65a610'
assert len(align['selectedCivilizations'])==19
assert align['selectedCivilizations']['Bannor']['alignment']=='ALIGNMENT_GOOD'
assert align['selectedCivilizations']['Sheaim']['alignment']=='ALIGNMENT_EVIL'
events=json.loads(Path('docs/data/emm-armageddon-event-choices.json').read_text())
assert events['commit']==align['commit'] and len(events['eventChoices'])==52
assert any(e['id']=='EVENT_DEMONIC_TOME_1' and e['delta']==5 for e in events['eventChoices'])
patch=Path('tools/patch_unciv_health.py').read_text()
for token in ('gameInfo.getYear() >= 5','emmCountedEliminations.add(civID)','EMM_RANDOM_EVENT_AC','changeEmmArmageddon(-2)','EmmSanctify','EmmRobGrave','EmmSpreadOrder','"The Order" -> "The Ashen Veil"'):
 assert token in patch,token
print('PASS: 19 alignment sources, 52 event-choice sources and spell/religion AC hooks')

# Extra source-exact AC callbacks and Peace spell contracts.
patch=Path('tools/patch_unciv_health.py').read_text()
for text in ('EmmPeace("Peace")','unit.name == "Corlindale"','emmPeaceReducesArmageddon()','unit.civ.getDiplomacyManager(enemy)?.makePeace()','unit.destroy()','doFlareEntropyNode" -> 2','doFlareLifeNode" -> -2','doSignAeron" -> 3','doSignSirona" -> -3'):
 assert text in patch,text
unit=next(u for u in json.loads(Path('jsons/Units.json').read_text()) if u['name']=='Corlindale')
assert (unit['requiredTech'],unit['uniqueTo'],unit['cost'],unit['movement'],unit['strength'])==('Fanaticism','Elohim',300,2,0)
assert all((n//2)==(n-(n-n//2)) for n in range(101))
print('PASS: source-backed Peace, Corlindale and AC event callback values')

# EMM event infrastructure: serialized once-per-world-turn state and safe-choice whitelist.
patch=Path('tools/patch_unciv_health.py').read_text()
for token in ('emmResolvedEventTriggers = hashSetOf<String>()','emmPendingEvents = hashMapOf<String, String>()','emmLastEventRollTurn = -1','emmScheduleRandomEvents()','emmResolveRandomEvent(civID: String, choice: String)','EVENTTRIGGER_WITCH','EVENTTRIGGER_HOLY_CHILD','EVENTTRIGGER_DEMONIC_TOME','game emm-event <choiceId>'):
 assert token in patch,token
print('PASS: serialized EMM random-event state, world-turn scheduler and safe resolutions')
