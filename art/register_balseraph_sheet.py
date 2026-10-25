#!/usr/bin/env python3
"""Register the 16 approved Balseraph sheet crops once their PNGs are available.
Does not redraw, recolor, or silently substitute preexisting art.
"""
import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/"Images/TileSets/AmuritesSimple/Units/Generated"
NAMES=["Warrior","Scout","Archer","Phalanx","Horseman","Champion","Mage",
       "Harlequin","Adept","Archmage","Berserker","Taskmaster","Assassin",
       "Mimic","Hunter","Balseraphs Swordsman"]
def filename(n):
    return "Balseraphs Swordsman.png" if n=="Balseraphs Swordsman" else n+"-Balseraphs.png"
def register():
    missing=[n for n in NAMES if not (DEST/filename(n)).exists()]
    if missing: raise RuntimeError("Missing extracted approved Balseraph PNGs: "+repr(missing))
    for n in NAMES:
        with Image.open(DEST/filename(n)) as im:
            assert im.mode=="RGBA" and im.size==(512,512),n
            assert im.getpixel((0,0))[3]==0,n
    atlas=ROOT/"placeholder-generated.atlas"
    contents=atlas.read_text()
    for n in NAMES:
        file=filename(n)
        path="Images/TileSets/AmuritesSimple/Units/Generated/"+file
        title=file[:-4]
        start=contents.find(path+"\n")
        block=(path+"\nsize: 512, 512\nformat: RGBA8888\nfilter: Linear, Linear\nrepeat: none\n"
            +"TileSets/AmuritesSimple/Units/"+title+"\n  rotate: false\n  xy: 0, 0\n"
            +"  size: 512, 512\n  orig: 512, 512\n  offset: 0, 0\n  index: -1\n"
            +"TileSets/AbsoluteUnits/Units/"+title+"\n  rotate: false\n  xy: 0, 0\n"
            +"  size: 512, 512\n  orig: 512, 512\n  offset: 0, 0\n  index: -1")
        if start>=0:
            end=contents.find("\n\n",start)
            if end<0:end=len(contents)
            contents=contents[:start]+block+contents[end:]
        else:
            contents=contents.rstrip()+"\n\n"+block+"\n"
    atlas.write_text(contents)
    log=ROOT/"art/PLACEHOLDER_SPRITES.json"
    data=json.loads(log.read_text())
    for n in NAMES:
        path="Images/TileSets/AmuritesSimple/Units/Generated/"+filename(n)
        row=next((r for r in data["sprites"] if r["path"]==path),None)
        if row is None:
            row={"path":path,"unit":n,"civilization":"Balseraphs","race":"human"}
            data["sprites"].append(row)
        row.update(status="placeholder",revision="approved-sprite-sheet-crop",
                   source="Balseraphs 4x4 image-generated sheet approved by user; extracted without recoloring",
                   reviewNeeded=False)
    data["count"]=len(data["sprites"])
    log.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
    print("Registered",len(NAMES),"Balseraph sheet sprites.")
if __name__=="__main__":register()
