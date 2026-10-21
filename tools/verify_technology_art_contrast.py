#!/usr/bin/env python3
"""Check full-color tech art is registered as untinted Unciv portraits."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "docs/data/ffh-technology-icons.json").read_text())
atlas = (root / "techart.atlas").read_text()
regions = [line[len("TechPortraits/"):] for line in atlas.splitlines() if line.startswith("TechPortraits/")]
names = set(manifest["mappings"])
assert len(regions) == len(names) == manifest["matchedCount"] == 52, (len(regions), len(names))
assert set(regions) == names, (set(regions) ^ names)
assert not any(line.startswith("TechIcons/") for line in atlas.splitlines()), "Color icons must not be era-tinted"
assert "techart.png" in atlas
assert "techart" in json.loads((root / "Atlases.json").read_text())
assert (root / "techart.png").exists()
print("OK: all 52 full-color tech DDS images load as untinted TechPortraits")
