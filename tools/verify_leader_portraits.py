#!/usr/bin/env python3
"""Verify source-accurate EMM leader art mappings and, optionally, imported PNGs."""
import argparse
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--require-art", action="store_true", help="Fail unless all 19 original PNG portraits are in the mod")
args = parser.parse_args()
manifest = json.loads((ROOT/"docs/data/emm-leader-portraits.json").read_text(encoding="utf-8"))
nations = json.loads((ROOT/"jsons/Nations.json").read_text(encoding="utf-8"))
playable = {n["name"]: n for n in nations if n["name"] != "Barbarians"}
entries = manifest["entries"]
assert manifest["sourceRevision"] == "60b0ec3740083162aaab7bf8491761a54a65a610"
assert len(entries) == len(playable) == 19
assert set(e["civilization"] for e in entries) == set(playable)
assert len(set(e["targetPngPath"] for e in entries)) == 19
assert len(set(e["emmPortraitDdsPath"].lower() for e in entries)) == 19
missing = []
for item in entries:
    assert item["leaderName"] == playable[item["civilization"]]["leaderName"], item["civilization"]
    assert item["targetPngPath"] == f'Images/LeaderIcons/{item["leaderName"]}.png'
    assert item["emmPortraitDdsPath"].lower().endswith(".dds")
    assert item["emmLeaderArtId"].startswith("ART_DEF_LEADER_")
    output = ROOT / item["targetPngPath"]
    if not output.exists():
        missing.append(item["leaderName"])
        continue
    with Image.open(output) as image:
        image.verify()
    with Image.open(output) as image:
        assert image.format == "PNG" and image.mode == "RGBA", str(output)
        assert image.width == image.height and 100 <= image.width <= 512, str(output)
print(f"OK: {len(entries)} source art mappings, {len(entries)-len(missing)} installed images, {len(missing)} missing images")
if missing:
    print("MISSING (not yet installed): " + ", ".join(missing))
    if args.require_art:
        raise SystemExit(1)
