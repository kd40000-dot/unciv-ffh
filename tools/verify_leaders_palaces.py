#!/usr/bin/env python3
"""Verify EMM leader XML trait bonuses and civilization palace source conversion."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
ref=load("docs/data/emm-leader-palace-fidelity.json")
civs=load("docs/data/emm-civilizations.json")
nations={x["name"]:x for x in load("jsons/Nations.json")}
buildings={x["name"]:x for x in load("jsons/Buildings.json")}
promotions={x["name"]:x for x in load("jsons/UnitPromotions.json")}
source=load("docs/data/emm-unit-building-catalog.json")
palaceOriginal={x["id"]:x for x in source["buildings"]}
assert ref["commit"]==civs["commit"]==source["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
traits=ref["traits"]
assert len(ref["palaceSources"])==19 and len([b for b in buildings if not b['name'].endswith(' (Spell)')])==76 and len(nations)==20
effects={
    "TRAIT_FINANCIAL":["[+25]% [Gold] [in all cities]"],
    "TRAIT_CREATIVE":["[+2 Culture] [in all cities]","[+10]% [Culture] [in all cities]"],
    "TRAIT_INGENUITY":["[-50]% Gold cost of upgrading","Gain [50] [Gold]"],
    "TRAIT_AGGRESSIVE":[f"All newly-trained [{category}] units [in all cities] receive the [Combat I] promotion"
      for category in ("Sword","Mounted","Scout","Magic","Archery","Disciple")],
    "TRAIT_ARCANE":["All newly-trained [Magic] units [in all cities] receive the [Mobility I] promotion"],
    "TRAIT_SPIRITUAL":["All newly-trained [Disciple] units [in all cities] receive the [Mobility I] promotion"],
}
assert traits["TRAIT_FINANCIAL"]["commerceModifiers"]==[25,0,0]
assert traits["TRAIT_CREATIVE"]["commerceChanges"]==[0,0,2]
assert traits["TRAIT_CREATIVE"]["commerceModifiers"]==[0,0,10]
assert traits["TRAIT_INGENUITY"]["iStartingGold"]==50
assert traits["TRAIT_INGENUITY"]["iUpgradeCostModifier"]==-50
assert traits["TRAIT_AGGRESSIVE"]["freePromotions"]==["PROMOTION_COMBAT1"]
assert set(traits["TRAIT_AGGRESSIVE"]["freeUnitCombats"])=={"UNITCOMBAT_ADEPT","UNITCOMBAT_ARCHER","UNITCOMBAT_DISCIPLE","UNITCOMBAT_MELEE","UNITCOMBAT_MOUNTED","UNITCOMBAT_RECON"}
assert traits["TRAIT_ARCANE"]["freePromotions"]==["PROMOTION_MOBILITY1","PROMOTION_POTENCY"]
assert traits["TRAIT_SPIRITUAL"]["freePromotions"]==["PROMOTION_MOBILITY1","PROMOTION_FAVORED"]
assert "Disciple" in promotions["Mobility I"]["unitTypes"]
for sel in civs["leaderSelections"]:
    assert set(sel["implementedTraits"])<=set(sel["traits"])
    assert set(sel["partialTraits"])<=set(sel["traits"])
    n=nations[sel["civilization"]]
    for trait, lines in effects.items():
        for line in lines:
            assert (line in n.get("uniques",[]))==(trait in sel["traits"]), (sel["civilization"],trait,line)
    for trait in ("TRAIT_FINANCIAL","TRAIT_CREATIVE","TRAIT_INGENUITY","TRAIT_AGGRESSIVE"):
        assert (trait in sel["implementedTraits"])==(trait in sel["traits"]),(sel["civilization"],trait)
    for trait in ("TRAIT_ARCANE","TRAIT_SPIRITUAL"):
        assert (trait in sel["partialTraits"])==(trait in sel["traits"]),(sel["civilization"],trait)
assert ref["palaceCommerceProxy"]["sourceCommerce"]==8
assert ref["palaceCommerceProxy"]["uncivScience"]==4
assert ref["palaceCommerceProxy"]["uncivGold"]==4
assert "Palace" in buildings and buildings["Palace"]["isNationalWonder"]
for rec in ref["palaceSources"]:
    s=palaceOriginal[rec["sourceId"]]
    assert rec["sourceYieldChanges"]==s["yieldChanges"]==[0,1,8]
    assert s["happiness"]==rec["sourceHappiness"]==1 and s["capital"]
    assert s["cost"]==rec["sourceCost"]==160
    name=rec["civilization"]
    palace=buildings[name+" Palace"]
    assert palace["uniqueTo"]==name and palace["replaces"]=="Palace"
    assert palace["cost"]==s["cost"] and palace["production"]==s["yieldChanges"][1]
    assert palace["science"]==4 and palace["gold"]==4 and palace["happiness"]==s["happiness"]
    assert palace["isNationalWonder"] and "Indicates the capital city" in palace["uniques"]
print("OK: 19 source-derived faction palaces, 69 buildings and EMM selected-leader trait coverage verified")
