#!/usr/bin/env python3
"""Verify pinned innate EMM nonliving promotions and their Unciv assignment."""
import json
from pathlib import Path
source=json.loads(Path("docs/data/emm-nonliving-races.json").read_text())
units=json.loads(Path("jsons/Units.json").read_text())
promotions={x["name"] for x in json.loads(Path("jsons/UnitPromotions.json").read_text())}
assert source["sourceCommit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
assert len(source["innateUnitPromotions"])==78
assert set(source["nonlivingPromotions"])=={"Angel","Avatar","Demon","Elemental","Golem","Illusion","Puppet","Rift","Undead"}
assert set(source["nonlivingPromotions"])<=promotions
assigned=0
for u in units:
    key="UNIT_"+u["name"].upper().replace(" ","_").replace("-","_")
    innate=source["innateUnitPromotions"].get(key,[])
    if not innate: continue
    assert set(innate)<=set(u.get("promotions",[])),(u["name"],innate)
    assigned+=1
assert assigned>=8,assigned
assert source["defaultCivilizationRace"]["CIVILIZATION_INFERNAL"]=="PROMOTION_DEMON"
print(f"PASS: 9 nonliving promotions, {assigned} mapped Unciv unit types, 78 pinned source unit mappings")
print("NOTE: civilization default-race assignment at unit creation remains a separate engine integration.")
