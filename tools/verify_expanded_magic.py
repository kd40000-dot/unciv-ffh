#!/usr/bin/env python3
"""Expanded magic static audit. Does NOT establish game-engine or UI correctness."""
import json
import re
from pathlib import Path

root=Path(__file__).resolve().parents[1]
def objects(name):
    data=json.loads((root/"jsons"/name).read_text(encoding="utf-8"))
    values=[x["name"] for x in data]
    assert len(values)==len(set(values)),f"Duplicate names in {name}"
    return {x["name"]:x for x in data}
p=objects("UnitPromotions.json")
u=objects("Units.json")
b=objects("Buildings.json")
i=objects("TileImprovements.json")
r=objects("TileResources.json")
spheres="Air Body Chaos Creation Death Dimensional Earth Enchantment Entropy Fire Force Ice Law Life Metamagic Mind Nature Shadow Spirit Sun Water".split()
assert len(spheres)==21
for sphere in spheres:
    assert sphere+" Mana" in r
    assert sphere+" Node" in i
    assert "Provides [1] ["+sphere+" Mana]" in i[sphere+" Node"]["uniques"]
    for tier,index in [("I",1),("II",2),("III",3)]:
        name=f"{sphere} {tier}"
        v=p[name]
        assert v["unitTypes"]==["Magic"],name
        assert v["uniques"],name
        want="Channeling I" if index==1 else f"{sphere} {('I' if index==2 else 'II')}"
        assert want in v["prerequisites"],(name,v["prerequisites"])
        if index==1:assert f"Only available <with [{sphere} Mana]>" in v["uniques"],name
        else:assert f"Only available <for units with [Channeling {tier}]>" in v["uniques"],name
for name in ["Skeleton (Summoned)","Spectre (Summoned)","Pit Beast (Summoned)","Fireball (Summoned)","Magic Missile (Summoned)","Ice Elemental (Summoned)","Einherjar (Summoned)","Air Elemental (Summoned)","Flesh Golem (Summoned)","Wraith (Summoned)","Earth Elemental (Summoned)","Fire Elemental (Summoned)","Runewyn (Summoned)","Djinn (Summoned)","Mistform (Summoned)","Aurealis (Summoned)","Water Elemental (Summoned)","Floating Eye (Summoned)","Returned Soul (Summoned)","Lich"]:
    assert name in u,name
    assert "Unbuildable" in u[name]["uniques"],name
for name in ["Growth (Spell)","Blessing (Spell)","Wall of Stone (Spell)","Hope (Spell)","Illumination (Spell)"]:
    assert name in b,name
for name in ["Labyrinth (Spell)","Rift (Spell)"]:
    assert name in i,name
for unit in ["Adept","Mage","Wizard","Archmage"]:
    assert "Channeling I" in u[unit]["promotions"],unit
for unit in ["Mage","Wizard","Archmage"]:
    assert "Channeling II" in u[unit]["promotions"],unit
assert "Channeling III" in u["Archmage"]["promotions"]
# Scan native template references, including those within modified promotion actions.
missing=[]
for promo in p.values():
    for unique in promo.get("uniques",[]):
        for unit in re.findall(r"Free \[([^]]+)\] appears",unique):
            if unit not in u:missing.append(("unit",promo["name"],unit))
        for building in re.findall(r"Gain a free \[([^]]+)\]",unique):
            if building not in b:missing.append(("building",promo["name"],building))
        for target in re.findall(r"Can transform to \[([^]]+)\]",unique):
            if target not in u:missing.append(("transform",promo["name"],target))
        for target in re.findall(r"Can instantly construct a \[([^]]+)\] improvement",unique):
            if target not in i:missing.append(("improvement",promo["name"],target))
        for status in re.findall(r"gains the \[([^]]+)\] status",unique):
            if status not in p:missing.append(("status",promo["name"],status))
assert not missing,missing
print(f"OK: {len(spheres)*3} sphere ranks, {len(u)} units, {len(b)} buildings, {len(i)} improvements, linked spell action targets")
