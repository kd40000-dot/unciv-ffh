#!/usr/bin/env python3
"""Verify Khazad's EMM-source vault stages and the exact Unciv gold-per-city conditionals."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

source = load("docs/data/emm-khazad-vaults.json")
catalog = load("docs/data/emm-unit-building-catalog.json")
nations = load("jsons/Nations.json")
by_source = {b["id"]: b for b in catalog["buildings"]}
by_nation = {n["name"]: n for n in nations}
assert source["commit"] == catalog["commit"] == "60b0ec3740083162aaab7bf8491761a54a65a610"
assert source["selectedCivilization"] == "Khazad"
assert source["goldPerCityExpression"] == "floor([Gold] / [Cities])"
assert len(source["tiers"]) == 7
assert [t["name"] for t in source["tiers"]] == [
    "Empty", "Low", "Normal", "Stocked", "Abundant", "Full", "Overflowing"]
assert [t["minimumGoldPerCity"] for t in source["tiers"]] == [0,25,50,75,100,150,250]
assert [t["maximumGoldPerCity"] for t in source["tiers"]] == [24,49,74,99,149,249,None]
assert [t["happiness"] for t in source["tiers"]] == [-2,-1,0,1,2,2,3]
assert [t["productionPercent"] for t in source["tiers"]] == [0,0,0,0,10,25,40]

def condition(t):
    expression = source["goldPerCityExpression"]
    if t["name"] == "Empty":
        return f"<when number of [{expression}] is less than [25]>"
    if t["name"] == "Overflowing":
        return f"<when number of [{expression}] is more than [249]>"
    return f'<when number of [{expression}] is between [{t["minimumGoldPerCity"]}] and [{t["maximumGoldPerCity"]}]>'

all_effects = []
for stage in source["tiers"]:
    building = by_source[stage["sourceId"]]
    assert building["happiness"] == stage["happiness"], stage["name"]
    assert (building["yieldModifiers"][1] if building["yieldModifiers"] else 0) == stage["productionPercent"], stage["name"]
    assert building["cost"] == -1, stage["name"]
    assert not building["yieldChanges"] and not building["commerceChanges"], stage["name"]

    expected = []
    if stage["happiness"] != 0:
        modifier = f'{stage["happiness"]:+d}'
        expected.append(f"[{modifier} Happiness] [in all cities] {condition(stage)}")
    if stage["productionPercent"]:
        expected.append(f'[+{stage["productionPercent"]}]% Production [in all cities] {condition(stage)}')
    assert stage["uniques"] == expected, stage["name"]
    all_effects.extend(expected)

khazad = by_nation["Khazad"]
actual = [u for u in khazad["uniques"] if "when number of [floor([Gold] / [Cities])]" in u]
assert actual == all_effects
assert len(actual) == len(set(actual)) == 9
for nation in nations:
    if nation["name"] != "Khazad":
        assert not any("when number of [floor([Gold] / [Cities])]" in u for u in nation.get("uniques",[])), nation["name"]

def stage_for(gold, cities):
    assert cities >= 1
    avg = math.floor(gold / cities)
    for stage in reversed(source["tiers"]):
        if avg >= stage["minimumGoldPerCity"]:
            return stage
    return source["tiers"][0] # Negative treasury also uses Empty.

# Source-threshold boundaries, fractional gold per city, spending and city founding.
cases = [
    (0,1,"Empty"),(24,1,"Empty"),(25,1,"Low"),(49,1,"Low"),
    (50,1,"Normal"),(74,1,"Normal"),(75,1,"Stocked"),(99,1,"Stocked"),
    (100,1,"Abundant"),(149,1,"Abundant"),(150,1,"Full"),
    (249,1,"Full"),(250,1,"Overflowing"),
    (49,2,"Empty"),(50,2,"Low"),(99,2,"Low"),(100,2,"Normal"),
    (149,2,"Normal"),(150,2,"Stocked"),(199,2,"Stocked"),
    (200,2,"Abundant"),(299,2,"Abundant"),(300,2,"Full"),
    (499,2,"Full"),(500,2,"Overflowing"),
    (99,4,"Empty"),(100,4,"Low"),(399,4,"Stocked"),
    (400,4,"Abundant"),(999,4,"Full"),(1000,4,"Overflowing"),
    (249,1,"Full"),(249,2,"Abundant"),(249,5,"Low"),
    (100,1,"Abundant"),(80,1,"Stocked"),(24,1,"Empty"),
    (0,10,"Empty"),(-1,1,"Empty"),(999,0+1,"Overflowing"),
]
for gold,cities,expected in cases:
    stage=stage_for(gold,cities)
    assert stage["name"] == expected, (gold,cities,stage["name"],expected)

# Emulates Unciv Countables Expression: 'floor' produces an Int countable and
# UniqueType ConditionalCountableBetween is inclusive, one stage is selected.
tests=0
for cities in range(1,13):
    for gold in range(-2,3001):
        avg=math.floor(gold/cities)
        matched=[
            t for t in source["tiers"] if (
                (avg < 25 if t["name"]=="Empty" else
                 avg > 249 if t["name"]=="Overflowing" else
                 t["minimumGoldPerCity"] <= avg <= t["maximumGoldPerCity"]))
        ]
        assert len(matched)==1 and matched[0]["name"]==stage_for(gold,cities)["name"], (gold,cities)
        tests+=1

assert "Dwarven Vault" in khazad["uniqueText"]
print(f"OK: {len(source['tiers'])} source-backed vault levels, {len(all_effects)} exclusive Khazad uniques, {len(cases)} boundary/spending/founding cases, {tests} city/treasury combinations")
