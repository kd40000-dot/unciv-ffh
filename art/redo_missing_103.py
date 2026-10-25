#!/usr/bin/env python3
"""Rework 103 earliest missing generic unit placeholders using approved Amurite art.
Preserves all approved images. This is reference-art reuse, not original character illustration.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json, colorsys, re

root=Path(__file__).resolve().parents[1]
art=root/"Images/TileSets/AmuritesSimple/Units/Generated"
manifest=root/"art/PLACEHOLDER_SPRITES.json"
data=json.loads(manifest.read_text())
existing={p.name for p in (root/"Images/TileSets/AbsoluteUnits/Units").glob("*.png")}
existing.update(p.name for p in (root/"Images/TileSets/AmuritesSimple/Units").glob("*.png"))
generic=[x for x in data["sprites"] if not x.get("civilization") and x["unit"]+".png" not in existing and x["unit"]+"-Amurites.png" not in existing]
# Last batch's missing inventory was 103; never touch approved images.
targets=generic[:103]
assert len(targets)==103, (len(targets),[x["unit"] for x in generic])
roles={
"archer":"Archer","crossbow":"Crossbowman","hunter":"Hunter","ranger":"Ranger","beastmaster":"Beastmaster",
"marksman":"Marksman","assassin":"Chanter","scout":"Scout","rogue":"Chanter",
"chariot":"Chariot","horse":"Horseman","knight":"Horseman","centaur":"Horse Archer",
"mage":"Wizard","wizard":"Wizard","archmage":"Archmage","adept":"Adept",
"shaman":"Wizard","priest":"Wizard","lich":"Archmage","druid":"Wizard",
"axeman":"Warrior","swordsman":"Swordsman","champion":"Champion","berserker":"Champion",
"paladin":"Phalanx","immortal":"Immortal","phalanx":"Phalanx","warrior":"Warrior",
"lizard":"Hunter","goblin":"Scout","ogre":"Champion"
}
def template(name):
    low=name.lower()
    for key,value in roles.items():
        if key in low:return value
    return "Warrior"
def palette(name,race):
    low=name.lower()
    if race=="orc" or any(v in low for v in ("goblin","ogre","lizard")):return (79,125,50)
    if race=="vampire":return (146,23,43)
    if race=="undead":return (100,95,134)
    if "balseraph" in low:return (226,184,34)
    if "bannor" in low:return (27,133,181)
    if "illians" in low:return (91,179,205)
    return (142,54,94)
def tinted(source,rgb,race):
    im=source.convert("RGBA")
    out=Image.new("RGBA",im.size,(0,0,0,0))
    px=im.load(); dst=out.load()
    target_h=colorsys.rgb_to_hsv(*(v/255 for v in rgb))[0]
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,a=px[x,y]
            if a==0:continue
            h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
            # Retint colorful red/pink garment panels; leave steel, leather
            # and dark polygonal outlines/shading untouched.
            red=(r>g*1.22 and r>b*1.06 and s>.25 and v>.19)
            if red:
                rr,gg,bb=colorsys.hsv_to_rgb(target_h,max(.32,s),v)
                r,g,b=int(rr*255),int(gg*255),int(bb*255)
            # Skin tint only for unmistakably warm light polygons, leaving
            # the near-black contour intact. Vampires pale, orcs green.
            elif race in ("orc","vampire") and r>85 and r>g*1.12 and g>b*.95 and .13<s<.72:
                level=(r+g+b)/3/170
                rr,gg,bb=((104,147,76) if race=="orc" else (211,207,199))
                r,g,b=[min(255,int(q*level)) for q in (rr,gg,bb)]
            dst[x,y]=(r,g,b,a)
    return out
def collect():
    done=[]
    for row in targets:
        name=row["unit"]
        role=template(name)
        path=art/(role+"-Amurites.png")
        if not path.exists():path=art/"Warrior-Amurites.png"
        with Image.open(path) as src:
            picture=tinted(src,palette(name,row.get("race","human")),row.get("race","human"))
            picture.thumbnail((448,448),Image.Resampling.LANCZOS)
            result=Image.new("RGBA",(512,512),(0,0,0,0))
            result.alpha_composite(picture,((512-picture.width)//2,(512-picture.height)//2))
            # Never alter existing approved characters: only entries explicitly
            # selected from the already labeled placeholder manifest.
            dest=root/row["path"]
            result.save(dest,optimize=True)
            row["revision"]="approved-art-derived-v2"
            row["sourceReference"]=str(path.relative_to(root))
            row["reviewNeeded"]=True
            row["status"]="placeholder"
            done.append(name)
    data["count"]=len(data["sprites"])
    data["reworked103"]=done
    manifest.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
    (root/"art/REWORKED_103.md").write_text(
      "# Reworked 103 first missing unit placeholders\n\n"
      "These are transparent 512x512 source-art adaptations from approved flat 2D Amurite references. "
      "They preserve clean geometric styling, but reuse poses and **are not original production-ready EMM character designs**. "
      "Every replacement is still tagged as a placeholder in PLACEHOLDER_SPRITES.json. "
      "Existing approved original artwork was not overwritten.\n\n"
      "| Unit | Approved reference reused |\n|---|---|\n"
      +"\n".join(f"| {r['unit']} | {r['sourceReference']} |" for r in targets)+"\n")
    print("Reworked",len(done),"transparent placeholder PNGs")
if __name__=="__main__":collect()
