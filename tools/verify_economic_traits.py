#!/usr/bin/env python3
"""Audit implemented EMM Raider/Barbarian economic effects and remaining gaps."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def data(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
source=data("docs/data/emm-leader-palace-fidelity.json")
civdata=data("docs/data/emm-civilizations.json")
nations={c["name"]:c for c in data("jsons/Nations.json")}
improvements=data("jsons/TileImprovements.json")
assert source["commit"]==civdata["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
raider=source["traits"]["TRAIT_RAIDERS"]
barbarian=source["traits"]["TRAIT_BARBARIAN"]
assert raider["iPillagingGold"]==100
assert raider["freePromotions"]==["PROMOTION_COMMANDO"]
assert barbarian["commerceModifiers"]==[0,-10,0]
RAIDER="200% Yield from pillaging tiles"
BARBARIAN="[-10]% Science [in all cities]"
selected=civdata["leaderSelections"]
assert len(selected)==19
raiders={s["civilization"] for s in selected if "TRAIT_RAIDERS" in s["traits"]}
barbarians={s["civilization"] for s in selected if "TRAIT_BARBARIAN" in s["traits"]}
assert raiders=={"Hippus","Svartalfar"}
assert barbarians=={"Doviello"}
for leader in selected:
    n=nations[leader["civilization"]]
    assert (RAIDER in n.get("uniques",[]))==(leader["civilization"] in raiders),leader["civilization"]
    assert (BARBARIAN in n.get("uniques",[]))==(leader["civilization"] in barbarians),leader["civilization"]
    assert ("TRAIT_RAIDERS" in leader.get("partialTraits",[]))==(leader["civilization"] in raiders)
    assert ("TRAIT_BARBARIAN" in leader.get("partialTraits",[]))==(leader["civilization"] in barbarians)
    assert n["uniques"].count(RAIDER)<=1 and n["uniques"].count(BARBARIAN)<=1
pillage=[]
for improvement in improvements:
    for unique in improvement.get("uniques",[]):
        if unique.startswith("Pillaging this improvement yields"):
            pillage.append((improvement["name"],unique))
            assert re.fullmatch(r"Pillaging this improvement yields (?:approximately )?\[\+\d+ Gold\]",unique),improvement["name"]
assert len(pillage)>=8,pillage
# PercentYieldFromPillaging applies the number as a multiplier (200% -> 2x);
# never use 100% for the EMM '100% EXTRA pillage Gold' modifier.
assert RAIDER.startswith("200%") and len(raiders)==2 and len(barbarians)==1
print(f"OK: {len(selected)} selected EMM leaders, {len(pillage)} Gold-only pillage sources, 2 Raider factions and Doviello Barbarian economic penalty")
