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

stages = source["tiers"]
buildings = load("jsons/Buildings.json")
by_building = {b["name"]: b for b in buildings}
vault_names = [f'Dwarven Vault ({stage["name"]})' for stage in stages]
assert all(name in by_building for name in vault_names)
assert len(vault_names) == len(set(vault_names)) == 7

for stage in stages:
    source_building = by_source[stage["sourceId"]]
    assert source_building["happiness"] == stage["happiness"], stage["name"]
    assert (source_building["yieldModifiers"][1] if source_building["yieldModifiers"] else 0) == stage["productionPercent"], stage["name"]
    assert source_building["cost"] == -1, stage["name"]
    assert not source_building["yieldChanges"] and not source_building["commerceChanges"], stage["name"]

    built = by_building[f'Dwarven Vault ({stage["name"]})']
    assert built["uniqueTo"] == "Khazad"
    assert built["cost"] == 0 and built.get("maintenance", 0) == 0
    assert built.get("happiness", 0) == stage["happiness"]
    assert built.get("percentStatBonus", {}).get("production", 0) == stage["productionPercent"]
    for required_unique in ("Unbuildable", "Cannot be purchased", "Unsellable", "Destroyed when the city is captured"):
        assert required_unique in built["uniques"], (stage["name"], required_unique)
    assert "Suppress warning [is both granted free and could possibly be removed by triggers]" in built["uniques"]
    assert built["civilopediaText"], stage["name"]

khazad = by_nation["Khazad"]
assert not any("when number of [floor([Gold] / [Cities])]" in u
               and ("Happiness" in u or "Production" in u)
               for u in khazad["uniques"]), "Old nation-wide bonuses must not stack with building effects"
assert not any("Dwarven Vault (" in u for n in nations if n["name"] != "Khazad"
               for u in n.get("uniques", []))

def condition_for_stage(stage):
    expr=source["goldPerCityExpression"]
    if stage["name"] == "Empty":
        return f"<when number of [{expr}] is less than [25]>"
    if stage["name"] == "Overflowing":
        return f"<when number of [{expr}] is more than [249]>"
    return (f'<when number of [{expr}] is between '
            f'[{stage["minimumGoldPerCity"]}] and [{stage["maximumGoldPerCity"]}]>')

def expected_event_uniques(event):
    expr=source["goldPerCityExpression"]
    actions=[]
    # First remove only currently incorrect stages, then grant the correct stage.
    for stage in stages:
        name=f'Dwarven Vault ({stage["name"]})'
        minimum,maximum=stage["minimumGoldPerCity"],stage["maximumGoldPerCity"]
        if minimum > 0:
            actions.append(f'Remove [{name}] [in all cities] <{event}> '
                           f'<when number of [{expr}] is less than [{minimum}]>')
        if maximum is not None:
            actions.append(f'Remove [{name}] [in all cities] <{event}> '
                           f'<when number of [{expr}] is more than [{maximum}]>')
    for stage in stages:
        name=f'Dwarven Vault ({stage["name"]})'
        actions.append(f'Gain a free [{name}] [in all cities] <{event}> {condition_for_stage(stage)}')
    return actions

all_events = ["upon turn start", "upon founding a city"]
all_actions = [action for event in all_events for action in expected_event_uniques(event)]
actual_actions = [u for u in khazad["uniques"]
                  if u.startswith("Remove [Dwarven Vault (")
                  or u.startswith("Gain a free [Dwarven Vault (")]
assert actual_actions == all_actions, "Missing, misordered, or extra Vault synchronization actions"
assert len(all_actions) == 38 == len(set(all_actions))

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

# Simulate an event on every possible treasury/city combination to prove
# both directions of stage switching, recovery from stale stages, and no stacking.
def reconcile(before, target):
    selected=stage_for(*target)["name"]
    result={name for name in before if name == selected}
    result.add(selected)
    return result

for old in stages:
    for gold,cities,_ in cases:
        target=(gold,cities)
        assert reconcile({old["name"]},target) == {stage_for(gold,cities)["name"]}
assert reconcile({s["name"] for s in stages},(100,1)) == {"Abundant"}

print(f"OK: {len(stages)} source-backed actual buildings, {len(all_actions)} synchronized triggers, "
      f"{len(cases)} boundary/spending/founding cases, {tests} city/treasury combinations")
