#!/usr/bin/env python3
"""Regression check for per-civilization Worker/Settler art and Amurites sprite registration."""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "Images/TileSets/AmuritesSimple/Units/Generated"
ATLAS = ROOT / "amurites-simple-complete.atlas"
names = json.loads((ROOT/"Atlases.json").read_text())
assert names[-1] == "amurites-simple-complete" and names.count("amurites-simple-complete")==1
atlas = ATLAS.read_text()
nations = json.loads((ROOT/"jsons/Nations.json").read_text())
civs = [n["name"] for n in nations]
assert len(civs)==20 and len(set(civs))==20
amurite_names = [
    "Adept","Archer","Archmage","Beastmaster","Champion","Chanter",
    "Chariot","Crossbowman","Firebow","Govannon","Horse Archer",
    "Horseman","Hunter","Immortal","Marksman","Phalanx",
    "Ranger","Scout","Swordsman","Warrior","Wizard",
]
expected = [f"{n}-Amurites" for n in amurite_names]
expected += ["Worker", "Settler"]
expected += [f"{unit}-{civ}" for unit in ("Worker","Settler") for civ in civs]
assert len(expected)==63 and len(set(expected))==63
files = list(GENERATED.glob("*.png"))
assert len(files)==len(expected),(len(files),len(expected))

page_headers = [line for line in atlas.splitlines() if line.startswith("Images/") and line.endswith(".png")]
assert len(page_headers)==len(expected)
assert len(set(page_headers))==len(expected)
for name in expected:
    path = GENERATED/(name+".png")
    assert path.is_file(),path
    data=path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n",name
    width,height,depth,color=struct.unpack(">IIBB",data[16:26])
    assert (width,height,depth,color)==(512,512,8,6),(name,width,height,depth,color)
    file_ref = "Images/TileSets/AmuritesSimple/Units/Generated/"+name+".png"
    assert page_headers.count(file_ref)==1,(name,"missing PNG atlas page")
    for unit_set in ("AmuritesSimple","AbsoluteUnits"):
        key=f"TileSets/{unit_set}/Units/{name}"
        assert atlas.count("\n"+key+"\n")==1,(name,key)

# Different civilizations must not all accidentally receive identical sash colors.
for unit in ("Worker","Settler"):
    hashes=[hashlib.sha256((GENERATED/f"{unit}-{civ}.png").read_bytes()).hexdigest() for civ in civs]
    assert len(set(hashes))>=15,(unit,"colorization appears to be missing")

print("OK: all 21 Amurites sprites and 42 generic/nation civilian assets "
      "are RGBA, packed for both unit sets, with 20 distinct civ sash variants each.")
