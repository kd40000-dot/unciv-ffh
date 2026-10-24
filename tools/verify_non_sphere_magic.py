#!/usr/bin/env python3
"""Source-bounded regression checks for non-sphere EMM spells in the dev branch.
Static structure only; mod-ci and Android behavior testing remain mandatory.
"""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
def load(path):return {x["name"]:x for x in json.loads((root/"jsons"/path).read_text(encoding="utf-8"))}
units=load("Units.json")
promotions=load("UnitPromotions.json")
def action(name,value):
    assert value in units[name].get("uniques",[]),(name,value)
def t(n,to,gold,tech=None):
    items=[f"Can transform to [{to}]","<for [Doviello] Civilizations>",f"<costs [+{gold} Gold] stats>","<for all movement>"]
    if tech:items.append(f"<after discovering [{tech}]>")
    action(n," ".join(items))
for n in ("Warrior","Beastman"):
    t(n,"Sons Of Asena",30,"Bronze Working")
    t(n,"Battlemaster",100,"Iron Working")
for n in ("Axeman","Sons Of Asena"):t(n,"Battlemaster",70,"Iron Working")
for n in ("Worker","Slave"):t(n,"Beastman",20)
action("Lucian","[This Unit] gains the [Lucian Bronze Veteran] promotion <costs [+80 Gold] stats> <for all movement> <after discovering [Bronze Working]> <once>")
assert "[+1] Strength" in promotions["Lucian Bronze Veteran"]["uniques"]
assert "Stealth" in promotions
assert promotions["Stealth"]["unitTypes"]==["Scout"]
assert "[This Unit] gains the [Hidden (Spell)] status for [2] turn(s) <for all movement> <for units without [Hidden (Spell)]>" in promotions["Stealth"]["uniques"]
assert "Invisible to non-adjacent units" in promotions["Hidden (Spell)"]["uniques"]
s=units["Severed Soul (Summoned)"]
assert s["movement"]==2 and s["strength"]==1 and s["unitType"]=="Scout"
assert {"Unbuildable","Cannot be purchased","Cannot attack","Ignores terrain cost"} <= set(s["uniques"])
for n in ("Assassin","Beastmaster","Hunter","Ranger","Scout","Divided Soul","Ghost"):
    action(n,"Free [Severed Soul (Summoned)] appears <for all movement> <for [Sidar] Civilizations> <once>")
assert all("Free [Severed Soul (Summoned)]" not in " ".join(u.get("uniques",[])) for n,u in units.items() if u.get("uniqueTo") and u["uniqueTo"]!="Sidar")
print("OK: Doviello gold-costed conversions, Lucian upgrade, stealth and Sidar Sever Soul references")
