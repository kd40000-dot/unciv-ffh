#!/usr/bin/env python3
"""Verify promotion/upgrade/resource conversion against the pinned EMM Continued source."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(path): return json.loads((ROOT / path).read_text(encoding="utf-8"))
d=load("docs/data/emm-promotions-upgrades-resources.json")
proms=load("jsons/UnitPromotions.json")
units=load("jsons/Units.json")
resources=load("jsons/TileResources.json")
types=load("jsons/UnitTypes.json")
nations=load("jsons/Nations.json")
assert d["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
assert len(d["promotions"])==305 and len(d["unitProgression"])==356 and len(d["resourceDefinitions"])==68
prom_names={p["name"] for p in proms}
unit_names={u["name"] for u in units}
res_names={r["name"] for r in resources}
type_names={t["name"] for t in types}
assert len(prom_names)==len(proms)
assert len(unit_names)==len(units)
assert len(res_names)==len(resources)
assert {"Copper","Mithril","Reagents","Horses","Iron"} <= res_names
assert {"Combat I","Combat II","Combat III","Combat IV","Combat V","City Raider I","Shock","Cover","Orc","Elf","Channeling I"} <= prom_names
source_by_id={x["id"]:x for x in d["unitProgression"]}
aliases={r["name"]:r["sourceId"] for r in load("docs/data/emm-civilizations.json")["addedUnits"]}
aliases["Disciple of the Ashen Veil"]="UNIT_DISCIPLE_THE_ASHEN_VEIL"
name_for=lambda n:aliases.get(n,"UNIT_"+n.removeprefix("Ljosalfar ").removeprefix("Amurites ").upper().replace(" ","_"))
for u in units:
    assert u["unitType"] in type_names,u["name"]
    source=source_by_id[name_for(u["name"])]
    for p in u.get("promotions",[]):
        assert p in prom_names,(u["name"],p)
    targets=[u["upgradesTo"]] if u.get("upgradesTo") else []
    targets += [v[len("Can upgrade to ["):-1] for v in u.get("uniques",[]) if v.startswith("Can upgrade to [") and v.endswith("]")]
    assert len(targets)==len(set(targets)),(u["name"],targets)
    assert all(t in unit_names for t in targets),(u["name"],targets)
    for t in targets:
        target=next(x for x in units if x["name"]==t)
        source_target=source_by_id[name_for(target["name"])]
        assert source_target["classId"] in source["upgrades"],(u["name"],t)
    for v in u.get("uniques",[]):
        if v.startswith("Can only be built <with ["):
            r=v.split("[")[-1].split("]")[0]
            assert r in res_names,(u["name"],r)
for p in proms:
    assert all(t in type_names for t in p.get("unitTypes",[])),p["name"]
    assert all(q in prom_names for q in p.get("prerequisites",[])),p["name"]
for r in resources:
    if "revealedBy" in r:
        techs={t["name"] for c in load("jsons/Techs.json") for t in c["techs"]}
        assert r["revealedBy"] in techs,r["name"]
assert len(d["implementedPromotionIds"])==26

# Check major EMM combat promotion numeric effects, not just their names and references.
by_promotion={p["name"]:p for p in proms}
source_promotions={p["id"]:p for p in d["promotions"]}
for i in range(1,6):
    name="Combat "+("I","II","III","IV","V")[i-1]
    p=by_promotion[name]
    assert "[+20]% Strength" in p["uniques"],name
    assert source_promotions[f"PROMOTION_COMBAT{i}"]["combat"]==20,name
for i in (1,2,3):
    name="City Raider "+("I","II","III")[i-1]
    p=by_promotion[name]
    assert "[+30]% Strength <vs cities>" in p["uniques"],name
    assert source_promotions[f"PROMOTION_CITY_RAIDER{i}"]["cityAttack"]==30,name
assert "[+1] Movement" in by_promotion["Mobility I"]["uniques"]
assert "[+1] Sight" in by_promotion["Sentry"]["uniques"]
for civ,promotion in (("Clan of Embers","Orc"),("Ljosalfar","Elf")):
    n=next(n for n in nations if n["name"]==civ)
    assert any("receive the ["+promotion+"] promotion" in v for v in n.get("uniques",[])),civ
print(f"OK: {len(proms)} promotions, {len(units)} source-derived units, {len(res_names)} resources; EMM upgrade and promotion references verified.")
