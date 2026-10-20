#!/usr/bin/env python3
"""Check that mod art stays deployable in stock Unciv, not only present in Images/."""
from pathlib import Path
import hashlib
import json
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
names = ("Firebow", "Wizard", "Govannon")
image_paths = [
    "LeaderIcons/Valledia", "NationIcons/Amurites",
    *(f"UnitIcons/{name}" for name in names),
    *(f"TileSets/FantasyHex/Units/{name}" for name in names),
    *(f"TileSets/AbsoluteUnits/Units/{name}" for name in names),
]
assert json.loads((ROOT / "Atlases.json").read_text()) == ["game"]
texture = (ROOT / "game.png").read_bytes()
assert texture.startswith(b"\x89PNG\r\n\x1a\n")
width, height = struct.unpack(">II", texture[16:24])
assert 0 < width <= 4096 and 0 < height <= 4096, (width, height)
data = (ROOT / "game.atlas").read_text()
assert f"size: {width}, {height}" in data
for name in image_paths:
    source = ROOT / "Images" / (name + ".png")
    assert source.is_file(), source
    assert re.search(rf"(?m)^{re.escape(name)}$", data), name
    start = data.index("\n" + name + "\n") + len(name) + 2
    lines = data[start:].splitlines()[:6]
    coords = next((line for line in lines if "xy:" in line), None)
    dims = next((line for line in lines if "size:" in line), None)
    assert coords and dims, name
    x,y = map(int, coords.split(":",1)[1].strip().split(","))
    w,h = map(int, dims.split(":",1)[1].strip().split(","))
    assert 0 <= x and 0 <= y and w > 0 and h > 0 and x+w <= width and y+h <= height, name
    print(f"OK atlas region {name}: {x},{y} {w}x{h}")
for kind in ("UnitIcons", "TileSets/FantasyHex/Units", "TileSets/AbsoluteUnits/Units"):
    hashes = [
        hashlib.sha256((ROOT/"Images"/kind/(name+".png")).read_bytes()).hexdigest()
        for name in names
    ]
    assert len(set(hashes)) == len(names), f"Unit art in {kind} must be distinct"
print("All Amurite sprites and icons present, distinct, and packed.")
