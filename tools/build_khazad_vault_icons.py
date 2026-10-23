#!/usr/bin/env python3
"""Generate seven original, deterministic Khazad Vault building icons and their Unciv atlas."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"Images"/"BuildingIcons"
OUT.mkdir(parents=True,exist_ok=True)
STAGES=["Empty","Low","Normal","Stocked","Abundant","Full","Overflowing"]
SIZE=160

def draw_icon(stage, rank):
    im=Image.new("RGBA",(SIZE,SIZE),(0,0,0,0))
    d=ImageDraw.Draw(im)
    # Stone arch, iron vault door and rune-like metalwork. Transparent outside silhouette.
    d.ellipse((10,3,150,147), fill=(60,59,58,255),outline=(19,18,21,255),width=4)
    d.rounded_rectangle((11,53,149,153),radius=15,fill=(74,73,71,255),outline=(22,21,24,255),width=4)
    d.ellipse((20,12,140,133),fill=(120,113,98,255),outline=(178,162,128,255),width=5)
    d.rounded_rectangle((21,66,139,146),radius=12,fill=(120,113,98,255),outline=(178,162,128,255),width=5)
    d.ellipse((32,24,128,122),fill=(36,38,43,255),outline=(18,20,24,255),width=5)
    d.rectangle((32,70,128,133),fill=(38,39,44,255))
    d.rounded_rectangle((42,37,119,137),radius=13,fill=(79,86,91,255),outline=(15,17,20,255),width=4)
    for x in (48,113):
        d.line((x,48,x,129),fill=(129,131,127,255),width=3)
        for y in (52,75,98,121):
            d.ellipse((x-2,y-2,x+2,y+2),fill=(194,180,137,255))
    for y in (51,122):
        d.line((51,y,110,y),fill=(114,117,115,255),width=3)
    d.ellipse((64,62,97,96),fill=(99,81,50,255),outline=(213,172,75,255),width=4)
    d.ellipse((72,70,89,87),fill=(37,38,40,255),outline=(225,184,92,255),width=2)
    d.line((81,70,81,87),fill=(211,171,75,255),width=2)
    # One radial gold gem per tier on the doorway; missing at Empty.
    markers=[(80,43),(101,49),(112,68),(112,103),(99,123),(61,123)]
    for x,y in markers[:min(rank,6)]:
        d.ellipse((x-5,y-5,x+5,y+5),fill=(222,169,52,255),outline=(250,219,123,255),width=2)
    # Different visible amounts of gold in front of the door.
    for n in range(rank):
        x=28+(n%4)*28
        y=130-(n//4)*12
        d.ellipse((x,y,x+24,y+11),fill=(193,126,32,255),outline=(245,197,68,255),width=2)
        d.arc((x+3,y+3,x+20,y+10),10,165,fill=(255,230,119,255),width=2)
    # Overflowing spills coins across the frame, unmistakably richer than Full.
    if stage=="Overflowing":
        for x,y in ((11,117),(122,119),(12,136),(126,140)):
            d.ellipse((x,y,x+18,y+9),fill=(204,148,42,255),outline=(251,208,85,255),width=2)
    if stage=="Empty":
        d.line((56,105,73,112,89,102,103,107),fill=(32,29,30,255),width=3)
    return im

atlas=[]
for rank,name in enumerate(STAGES):
    path=OUT/f"Dwarven Vault ({name}).png"
    draw_icon(name,rank).save(path,optimize=True)
    atlas += [f"Images/BuildingIcons/Dwarven Vault ({name}).png",
              f"size: {SIZE}, {SIZE}",
              "format: RGBA8888",
              "filter: Linear, Linear",
              "repeat: none",
              f"BuildingIcons/Dwarven Vault ({name})",
              "  rotate: false",
              "  xy: 0, 0",
              f"  size: {SIZE}, {SIZE}",
              f"  orig: {SIZE}, {SIZE}",
              "  offset: 0, 0",
              "  index: -1",
              ""]
(ROOT/"khazad-vaults.atlas").write_text("\n".join(atlas),encoding="utf-8")
manifest=ROOT/"Atlases.json"
names=json.loads(manifest.read_text(encoding="utf-8"))
if "khazad-vaults" not in names:names.append("khazad-vaults")
manifest.write_text(json.dumps(names,separators=(",",":"))+"\n",encoding="utf-8")
print(f"Generated {len(STAGES)} Khazad Vault icons and registered their atlas.")
