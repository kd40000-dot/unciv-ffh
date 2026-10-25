#!/usr/bin/env python3
"""Bespoke Balseraph character silhouettes; never recolor Amurite character files."""
from PIL import Image, ImageDraw
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"Images/TileSets/AmuritesSimple/Units/Generated"
OUT.mkdir(parents=True,exist_ok=True)
S=4
INK=(42,30,38,255); GOLD=(238,189,34,255); RED=(169,36,64,255)
CREAM=(245,226,180,255); BLACK=(65,42,59,255); PURPLE=(117,65,117,255)
TEAL=(43,143,142,255); SKIN=(221,174,142,255)
def render(role):
    im=Image.new("RGBA",(512,512),(0,0,0,0));d=ImageDraw.Draw(im)
    def p(pts,col,width=10):
        pts=[(int(x*S),int(y*S)) for x,y in pts];d.polygon(pts,fill=col);d.line(pts+[pts[0]],fill=INK,width=width,joint="curve")
    def l(pts,col,width=5):
        d.line([(int(x*S),int(y*S)) for x,y in pts],fill=INK,width=(width+3)*S,joint="curve")
        d.line([(int(x*S),int(y*S)) for x,y in pts],fill=col,width=width*S,joint="curve")
    # Long mismatched striped hosiery and curled pointed shoes
    p([(43,79),(57,78),(54,109),(34,113),(28,107)],PURPLE)
    p([(65,78),(81,79),(89,109),(78,114),(65,108)],RED)
    p([(32,103),(53,105),(49,116),(16,116),(20,110)],GOLD)
    p([(72,103),(87,105),(109,113),(109,118),(73,117)],BLACK)
    for y in (87,96):p([(42,y),(55,y),(54,y+4),(38,y+4)],CREAM,4)
    for y in (88,98):p([(70,y),(82,y),(84,y+4),(72,y+4)],GOLD,4)
    # Distinct harlequin costume with diamond panels
    p([(36,38),(66,33),(87,40),(92,80),(30,82)],PURPLE)
    p([(40,45),(60,39),(56,78),(34,80)],RED)
    p([(66,39),(82,45),(89,78),(58,80)],GOLD)
    p([(50,46),(62,57),(49,69),(38,58)],BLACK,6)
    p([(75,46),(86,57),(75,69),(64,57)],RED,6)
    # Ruffled asymmetric collar
    p([(35,41),(23,30),(41,32),(45,21),(55,34),(65,23),(75,33),(90,27),(84,45),(66,42),(55,47)],CREAM)
    p([(23,35),(36,41),(28,72),(14,70)],SKIN)
    p([(84,41),(100,37),(109,75),(94,78)],SKIN)
    p([(26,55),(36,58),(31,73),(19,69)],GOLD,6)
    p([(94,56),(105,53),(112,75),(99,79)],RED,6)
    # Completely featureless blank festival mask, no facial expression
    p([(45,15),(75,15),(80,34),(69,43),(50,42),(42,33)],CREAM)
    p([(47,18),(64,15),(58,39),(47,37)],(227,202,165,255),0)
    # 3 pointed carnival jester cap, clean silhouette
    p([(43,18),(28,2),(21,13),(34,26)],RED)
    p([(54,15),(58,0),(73,16),(64,23)],PURPLE)
    p([(72,18),(99,7),(91,29),(76,28)],GOLD)
    for x,y,col in ((20,13,GOLD),(58,2,RED),(99,7,RED)):
        d.ellipse(((x-4)*S,(y-4)*S,(x+4)*S,(y+4)*S),fill=col,outline=INK,width=7)
    if role=="Warrior":
        # Theatrical but unmistakable armament: jagged axe and shield
        l([(104,96),(104,22)],(114,73,50,255),4)
        p([(99,27),(117,16),(126,35),(109,46)],(198,205,209,255))
        p([(11,58),(31,52),(35,82),(17,91),(6,78)],TEAL)
        p([(15,62),(27,61),(29,80),(18,85)],GOLD,5)
    else:
        # Acrobatic scout with narrow spear and fluttering striped scarf.
        l([(102,113),(102,14)],(104,73,45,255),3)
        p([(97,19),(102,3),(108,19)],(195,208,209,255))
        p([(35,35),(14,31),(8,45),(32,48)],TEAL)
        p([(13,33),(7,38),(29,44),(34,39)],CREAM,4)
    # Never draw eyes, nose, mouth, beard or backgrounds.
    return im
all_result=[]
for role in ("Warrior","Scout"):
    dest=OUT/f"{role}-Balseraphs.png"
    im=render(role);im.save(dest,optimize=True)
    assert im.getpixel((0,0))[3]==0 and im.mode=="RGBA"
    all_result.append(dest)
manifest=ROOT/"art/PLACEHOLDER_SPRITES.json"
data=json.loads(manifest.read_text())
for row in data["sprites"]:
    if row.get("civilization")=="Balseraphs" and row.get("unit") in ("Warrior","Scout"):
        row["revision"]="bespoke-harlequin-v3"
        row["source"]="individually constructed faceless Balseraph carnival character, NOT a recolor of an Amurite sprite"
        row["reviewNeeded"]=True
manifest.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
atlas=ROOT/"placeholder-generated.atlas"
txt=atlas.read_text()
for role in ("Warrior","Scout"):
    path=f"Images/TileSets/AmuritesSimple/Units/Generated/{role}-Balseraphs.png"
    start=txt.index(path+"\n")
    end=txt.find("\n\n",start)
    if end<0:end=len(txt)
    part=txt[start:end].replace("size: 128, 128","size: 512, 512").replace("orig: 128, 128","orig: 512, 512")
    txt=txt[:start]+part+txt[end:]
atlas.write_text(txt)
print("Built two bespoke Balseraph characters with transparent 512px RGBA PNGs.")
