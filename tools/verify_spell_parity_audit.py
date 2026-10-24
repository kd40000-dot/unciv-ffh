#!/usr/bin/env python3
"""Check the EMM 82-spell parity ledger and high-fidelity numeric effects.

A successful check establishes internal references/known EMM values only.
It does not establish Android action behavior or source-equivalent targeting.
"""
import json
import re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def named(path):
    entries=json.loads((root/"jsons"/path).read_text(encoding="utf-8"))
    return {v["name"]:v for v in entries}
p=named("UnitPromotions.json")
b=named("Buildings.json")
u=named("Units.json")
audit=(root/"docs/emm-82-spell-fidelity-audit.md").read_text(encoding="utf-8")
inventory=(root/"docs/emm-full-spell-inventory.md").read_text(encoding="utf-8")
sections={}
for header,start,end in [
    ("Perfect representation", "## Perfect representation", "## Very close representation"),
    ("Very close representation", "## Very close representation", "## Significant differences"),
    ("Significant differences", "## Significant differences", "## Source-corrected work")]:
    sub=audit[audit.index(start):audit.index(end)]
    sections[header]=set(re.findall(r"^\| ([A-Z][A-Z0-9_ ]+) \|",sub,re.M))
cases=sum(len(v) for v in sections.values())
assert cases==82,(cases,{k:len(v) for k,v in sections.items()})
assert not (sections["Perfect representation"]&sections["Very close representation"])
assert not (sections["Perfect representation"]&sections["Significant differences"])
assert not (sections["Very close representation"]&sections["Significant differences"])
assert len(sections["Perfect representation"])==0
assert len(sections["Very close representation"])==7
assert len(sections["Significant differences"])==75
ids={x.replace(" ","_") for group in sections.values() for x in group}
assert all("| SPELL_"+x+" |" in inventory for x in ids),sorted(x for x in ids if "| SPELL_"+x+" |" not in inventory)
for n,v in {
    "Growth (Spell)":{"food":2,"culture":1},
    "Hope (Spell)":{"culture":4,"happiness":1},
}.items():
    for field,expected in v.items(): assert b[n].get(field)==expected,(n,field)
assert "[10]% Food is carried over after population increases [in this city]" in b["Growth (Spell)"]["uniques"]
assert "[+50]% Great Person generation [in this city]" in b["Illumination (Spell)"]["uniques"]
assert "[+2] Strength <when defending>" in p["Stoneskin (Spell)"]["uniques"]
assert "[1] XP gained from combat" in p["Valor (Spell)"]["uniques"]
assert "Uncapturable" in p["Loyalty (Spell)"]["uniques"]
assert "Unit will heal every turn, even if it performs an action" in p["Regeneration (Spell)"]["uniques"]
assert "[10] HP when healing" in p["Regeneration (Spell)"]["uniques"]
assert "Invisible to others" in p["Hidden (Spell)"]["uniques"]
assert "Invisible to others" in p["Whiteout (Ability)"]["uniques"]
assert "Invisible to others" in u["Severed Soul (Summoned)"]["uniques"]
assert "Invisible to non-adjacent units" not in u["Severed Soul (Summoned)"]["uniques"]
for n,rank,old,new in [
    ("Sun","I","Plains","Desert"),("Sun","I","Snow","Tundra"),("Sun","I","Marsh","Plains"),
    ("Nature","III","Snow","Tundra"),("Nature","III","Tundra","Plains"),
    ("Nature","III","Desert","Plains"),("Nature","III","Plains","Grassland"),("Nature","III","Marsh","Grassland")]:
    v=p[n+" "+rank]["uniques"]
    needle=f"Turn this tile into a [{new}] tile <for all movement> <in [{old}] tiles>"
    assert any(x.startswith(needle) for x in v),(n,rank,needle)
for n in ("Skeleton (Summoned)","Spectre (Summoned)","Wraith (Summoned)","Lich"):
    assert "Undead" in u[n].get("promotions",[]),n
assert "[-20]% Strength for enemy [All] units in adjacent [All] tiles" in p["Blinding Light (Spell)"]["uniques"]
print("OK: 82 unique audited EMM spell entries, 0 perfect / 7 close / 75 significant; validated known source-derived effects")
