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
# Unciv RulesetValidator.addTechErrors: technology rows are 1-based.
# TechPickerScreen also assumes unique locations in a column.
positions = set()
for column in data["Techs"]:
    assert isinstance(column["columnNumber"], int) and column["columnNumber"] >= 0, column
    for tech in column["techs"]:
        assert isinstance(tech["row"], int) and tech["row"] >= 1, (
            f"Invalid tech row: {tech['name']} -> {tech['row']}"
        )
        position = (column["columnNumber"], tech["row"])
        assert position not in positions, f"Overlapping tech positions: {position}"
        positions.add(position)
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
# Stock terrain definitions reference Sheep and Rejuvenation.
# Ruin rewards need a placed tile improvement with the ruins unique.
assert "Sheep" in named(data["TileResources"]), "Terrain's Hill region needs Sheep resource"
assert "Rejuvenation" in named(data["UnitPromotions"]), "Fountain of Youth needs Rejuvenation promotion"
assert any("Provides a random bonus when entered" in x.get("uniques", [])
           for x in data["TileImprovements"]), "Ruin rewards need Ancient ruins equivalent"
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

# Test that generated graphics exist and are actually in the Android atlas.
if (repo / "game.atlas").exists():
    atlas = (repo / "game.atlas").read_text(encoding="utf-8")
    sources = json.loads((repo / "development/art/sources.json").read_text(encoding="utf-8"))
    required_images = set()
    for leader in sources["portraitSources"]:
        required_images.add(f"LeaderIcons/{leader}")
    for nation in sources["factionColors"]:
        required_images.add(f"NationIcons/{nation}")
    for unit in list(sources["unitSources"]) + list(sources["styledUnitSources"]):
        required_images.add(f"TileSets/FantasyHex/Units/{unit}")
        required_images.add(f"TileSets/AbsoluteUnits/Units/{unit}")
    for image in required_images:
        assert image in atlas, f"Graphic missing from packed Unciv atlas: {image}"
        assert (repo / "Images" / (image + ".png")).is_file(), f"Source PNG missing: {image}"
    assert not (repo / "Images/Tilesets").exists(), "Wrong capitalization: use TileSets, not Tilesets"
    print(f"PASS: {len(required_images)} expected graphic names found in packed atlas")
