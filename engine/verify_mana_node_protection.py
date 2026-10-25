#!/usr/bin/env python3
"""Prevent automated workers from replacing mana improvements.

Run with: python3 engine/verify_mana_node_protection.py
"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
improvements = json.loads((root / "jsons/TileImprovements.json").read_text(encoding="utf-8"))
nodes = [entry for entry in improvements if entry["name"].endswith(" Node")]
assert len(nodes) == 21, f"Expected 21 mana node types, found {len(nodes)}"
for node in nodes:
    uniques = node.get("uniques", [])
    assert "Can only be built on [Raw Mana] tiles" in uniques, node["name"]
    assert "Will not be replaced by automated units" in uniques, node["name"]
print(f"All {len(nodes)} mana nodes are protected from automated worker replacement")
