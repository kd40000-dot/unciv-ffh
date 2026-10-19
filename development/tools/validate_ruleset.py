#!/usr/bin/env python3
"""Static references and JSON check, not an Unciv engine validation."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[2] / "jsons"
data = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in root.glob("*.json")}
assert data["ModOptions"]["isBaseRuleset"] is True
named = lambda xs: {x["name"] for x in xs}
techs = [t for col in data["Techs"] for t in col["techs"]]
names = named(techs)
civs = named(data["Nations"])
unitNames = named(data["Units"])
unitTypes = named(data["UnitTypes"])
improvements = named(data["TileImprovements"])
terrains = named(data["Terrains"])
assert len(techs) == len(names)
for tech in techs:
    assert set(tech.get("prerequisites", [])) <= names, tech
for unit in data["Units"]:
    assert unit["unitType"] in unitTypes, unit["name"]
    assert unit.get("requiredTech") in names | {None}, unit["name"]
    assert unit.get("uniqueTo") in civs | {None}, unit["name"]
    assert unit.get("replaces") in unitNames | {None}, unit["name"]
    assert unit.get("upgradesTo") in unitNames | {None}, unit["name"]
for building in data["Buildings"]:
    assert building.get("requiredTech") in names | {None}, building["name"]
    assert building.get("uniqueTo") in civs | {None}, building["name"]
for imp in data["TileImprovements"]:
    assert imp.get("techRequired") in names | {None}, imp["name"]
for res in data["TileResources"]:
    assert res["improvement"] in improvements, res["name"]
    assert set(res["terrainsCanBeFoundOn"]) <= terrains, res["name"]
assert {"Amurites", "Bannor", "Ljosalfar", "Clan of Embers", "Barbarians", "Spectator"} <= civs
print(f"OK: {len(data)} JSON files, {len(techs)} technologies, {len(unitNames)} units.")

# Replicate GithubAPI.isValidModFolder root classification to catch invalid archives.
repo = root.parent
root_items = [f for f in repo.iterdir() if f.name != ".git"]  # Git metadata is not part of GitHub ZIP archives
known_dirs = ("Images", "jsons", "maps", "music", "scenarios", "sounds", "voices", ".github")
good = sum(1 for f in root_items if (
    (f.is_dir() and (f.name in known_dirs or f.name.startswith("Images.")))
    or (f.is_file() and (f.suffix.lower() in (".md", ".atlas", ".png")
        or f.name.lower() in ("preview.jpg", "atlases.json", ".nomedia", "license")))
))
bad = len(root_items) - good
assert good > bad, f"Unciv rejects mod archive root: {good} good, {bad} bad"
print(f"Unciv archive structure OK: {good} recognized, {bad} unrecognized root entries")
