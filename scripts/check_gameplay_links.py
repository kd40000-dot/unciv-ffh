#!/usr/bin/env python3
"""Verify Fall from Heaven / Unciv unit upgrades and strategic resources."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1] / "jsons"
def load(name):
    return json.loads((ROOT / (name + ".json")).read_text(encoding="utf-8"))

units = load("Units")
techs = {t["name"] for col in load("Techs") for t in col.get("techs", [])}
resources = {r["name"] for r in load("TileResources")}
promotions = {p["name"] for p in load("UnitPromotions")}
nations = {n["name"] for n in load("Nations")}
by_name = {u["name"]: u for u in units}
errors = []
edges = {}
alt = re.compile(r"^Can upgrade to \[([^\]]+)\]$")
for u in units:
    name = u["name"]
    destinations = [u["upgradesTo"]] if u.get("upgradesTo") else []
    destinations += [m.group(1) for text in u.get("uniques", []) if (m := alt.fullmatch(text))]
    edges[name] = destinations
    for dest in destinations:
        if dest not in by_name:
            errors.append(f"{name}: missing upgrade target {dest}")
        if dest == name:
            errors.append(f"{name}: self-upgrade")
    if u.get("requiredTech") and u["requiredTech"] not in techs:
        errors.append(f"{name}: missing technology {u['requiredTech']}")
    if u.get("requiredResource") and u["requiredResource"] not in resources:
        errors.append(f"{name}: missing resource {u['requiredResource']}")
    if u.get("uniqueTo") and u["uniqueTo"] not in nations:
        errors.append(f"{name}: missing nation {u['uniqueTo']}")
    if u.get("replaces") and u["replaces"] not in by_name:
        errors.append(f"{name}: missing replaced unit {u['replaces']}")
    for promo in u.get("promotions", []):
        if promo not in promotions:
            errors.append(f"{name}: missing promotion {promo}")
for p in load("UnitPromotions"):
    for parent in p.get("prerequisites", []):
        if parent not in promotions:
            errors.append(f"{p['name']}: missing prerequisite promotion {parent}")
# Upgrade cycles are always suspect; warn without failing, since rulesets
# may intentionally allow some conversions.
cycles = set()
for name in edges:
    seen = set()
    def walk(node):
        if node in seen:
            cycles.add(node)
            return
        if node not in edges:
            return
        seen.add(node)
        for dest in edges[node]:
            walk(dest)
        seen.remove(node)
    walk(name)
print(f"Units: {len(units)}, upgrade edges: {sum(map(len, edges.values()))}, errors: {len(errors)}")
for e in errors: print("ERROR:", e)
for c in sorted(cycles): print("WARNING: upgrade cycle through", c)
sys.exit(bool(errors))
