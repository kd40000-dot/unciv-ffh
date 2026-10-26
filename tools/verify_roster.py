#!/usr/bin/env python3
"""Check source-derived unit/building conversion against the pinned EMM catalog."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((R/p).read_text(encoding="utf-8"))
source=load("docs/data/emm-unit-building-catalog.json")
assert source["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
assert len(source["units"])==356
assert len(source["buildings"])==189
units=load("jsons/Units.json")
buildings=load("jsons/Buildings.json")
techs={t["name"] for col in load("jsons/Techs.json") for t in col["techs"]}
nations={n["name"] for n in load("jsons/Nations.json")}
types={x["name"] for x in load("jsons/UnitTypes.json")}
byid={r["id"]:r for r in source["units"]}
bbid={r["id"]:r for r in source["buildings"]}
rename=lambda s:s.removeprefix("UNIT_").removeprefix("BUILDING_").lower().replace("_"," ").title()
factions=load("docs/data/emm-civilizations.json")
unit_aliases={r["name"]:r["sourceId"] for r in factions["addedUnits"]}
# EMM named missionary follows its source identifier, not a civ-specific replacement.
unit_aliases["Disciple of the Ashen Veil"]="UNIT_DISCIPLE_THE_ASHEN_VEIL"
building_aliases={r["name"]:r["sourceId"] for r in factions["addedBuildings"]}
palace_aliases={r["civilization"]+" Palace":r["sourceId"] for r in load("docs/data/emm-leader-palace-fidelity.json")["palaceSources"]}
vault_aliases={f'Dwarven Vault ({r["name"]})':r["sourceId"] for r in load("docs/data/emm-khazad-vaults.json")["tiers"]}
assert len({x["name"] for x in units})==len(units)
assert len({x["name"] for x in buildings})==len(buildings)
byname={x["name"]:x for x in units}
bnames={x["name"] for x in buildings}
for item in units:
    assert item["unitType"] in types,item["name"]
    assert item["requiredTech"] in techs if "requiredTech" in item else True,item["name"]
    assert item.get("uniqueTo") in nations if "uniqueTo" in item else True,item["name"]
    assert item["replaces"] in byname if "replaces" in item else True,item["name"]
    alias=item["name"].removeprefix("Ljosalfar ").removeprefix("Amurites ")
    rec=byid.get(unit_aliases[item["name"]]) if item["name"] in unit_aliases else next((r for r in source["units"] if rename(r["id"])==alias),None)
    assert rec is not None,("No EMM unit source",item["name"])
    assert item["cost"]==rec["cost"],("Incorrect unit cost",item["name"])
    assert item["movement"]==rec["moves"],("Incorrect unit movement",item["name"])
    if rec["attack"]>0:assert item["strength"]==rec["attack"],("Incorrect combat",item["name"])
    if rec["tech"] == "TECH_NEVER":
        assert "Unbuildable" in item.get("uniques", []), item["name"]
        assert "requiredTech" not in item, item["name"]
    elif rec["tech"]:
        assert item["requiredTech"] in techs, item["name"]
for item in buildings:
    assert item["requiredTech"] in techs if "requiredTech" in item else True,item["name"]
    assert item.get("uniqueTo") in nations if "uniqueTo" in item else True,item["name"]
    assert item["replaces"] in bnames if "replaces" in item else True,item["name"]
    if item["name"]=="Palace":continue
    rec=bbid.get(vault_aliases[item["name"]]) if item["name"] in vault_aliases else (bbid.get(palace_aliases[item["name"]]) if item["name"] in palace_aliases else (bbid.get(building_aliases[item["name"]]) if item["name"] in building_aliases else next((r for r in source["buildings"] if rename(r["id"])==item["name"]),None)))
    if rec is None and item["name"]=="Cave of Ancestors":
        rec=bbid["BUILDING_CAVE_OF_ANCESTORS"]
    assert rec is not None,("No EMM building source",item["name"])
    if item["name"] in vault_aliases:
        # Civ IV auto-injected buildings have cost -1. Unciv models them as cost=0
        # with Unbuildable/Cannot be purchased, then grants them by trigger.
        assert rec["cost"]==-1 and item["cost"]==0,("Incorrect automatic vault cost",item["name"])
        assert "Unbuildable" in item["uniques"] and "Cannot be purchased" in item["uniques"]
    else:
        assert item["cost"]==rec["cost"],("Incorrect building cost",item["name"])
print(f"OK: {len(units)} units and {len(buildings)} buildings traced to the EMM inventory; costs, movement, combat and references verified.")
