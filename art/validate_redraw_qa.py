#!/usr/bin/env python3
"""Reject missing artwork, unapproved mass output or reference recolors.
Review data is in REDRAW_QA.json. Never mark images approved automatically.
"""
import json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
data=json.loads((root/"art/REDRAW_QA.json").read_text())
manifest=json.loads((root/"art/PLACEHOLDER_SPRITES.json").read_text())
existing={row["path"]:row for row in manifest["sprites"]}
assert len(data["entries"])==len({x["path"] for x in data["entries"]})
for entry in data["entries"]:
    assert entry["path"] in existing, entry["path"]
    assert entry["unit"].lower() not in ("worker","settler")
    assert entry["civilization"]!="Amurites"
    assert entry["status"] in ("rejected-needs-redraw","awaiting-review","accepted")
    if entry["status"]=="accepted":
        assert entry["styleQuality"]=="pass" and entry["themeColors"]=="pass"
        assert entry["reviewed"] is True
        assert entry["replacement"] is not None
        file=root/entry["replacement"]
        assert file.is_file(),file
        with Image.open(file) as img:
            assert img.mode=="RGBA" and img.size==(512,512),file
            assert img.getpixel((0,0))[3]==0
            assert img.getpixel((511,511))[3]==0
print("Review status:", {key:sum(x["status"]==key for x in data["entries"]) for key in ("rejected-needs-redraw","awaiting-review","accepted")})
