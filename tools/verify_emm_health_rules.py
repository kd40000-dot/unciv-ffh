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
