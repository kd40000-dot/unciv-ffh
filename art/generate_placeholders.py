#!/usr/bin/env python3
"""Deterministic, transparent flat 2D temporary art for FFH/EMM. Never overwrite approved art."""
import json, pathlib, re, math, hashlib
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "Images/TileSets/AmuritesSimple/Units/Generated"
OUT.mkdir(parents=True,exist_ok=True)
units=json.loads((ROOT/"jsons/Units.json").read_text())
nations=json.loads((ROOT/"jsons/Nations.json").read_text())
all_png={p.name for p in (ROOT/"Images").rglob("*.png")}
previous_manifest=ROOT/'art/PLACEHOLDER_SPRITES.json'
created=(json.loads(previous_manifest.read_text()).get('sprites',[]) if previous_manifest.exists() else [])
D=384
def shade(rgb,f):
    return tuple(max(0,min(255,int(v*f))) for v in rgb[:3])+(255,)
def color(rgb):
    if isinstance(rgb,str): return rgb
    return tuple(rgb[:3])+(255,)
def sprite(name,kind,civ,rgb,race):
    S=3
    im=Image.new("RGBA",(D,D),(0,0,0,0))
    d=ImageDraw.Draw(im)
    dark=(39,32,39,255)
    metal=(196,202,207,255)
    skin={"orc":(108,148,85,255),"vampire":(208,200,190,255),"elf":(228,193,155,255),"dwarf":(178,119,83,255),"undead":(183,188,180,255),"human":(192,143,108,255)}.get(race,(187,148,115,255))
    main=color(rgb); hi=shade(main,1.22); lo=shade(main,.58)
    def polygon(points,fill,outline=dark,width=10):
        pts=[(round(x*S),round(y*S)) for x,y in points]
        d.polygon(pts,fill=fill)
        if outline: d.line(pts+[pts[0]],fill=outline,width=width,joint="curve")
    def line(points,fill,width=7): d.line([(int(x*S),int(y*S)) for x,y in points],fill=fill,width=width*S,joint="curve")
    low=name.lower()
    water=(" Water" in kind or any(w in low for w in ("galley","frigate","trireme","caravel","galleon","privateer","ship","workboat","queen of the line")))
    monster=any(w in low for w in ("wolf","lion","tiger","bear","spider","horse","elephant","griffon","dragon","wyvern","hawk","gorilla","lizard","myconid","skeleton","spectre","wraith","golem","elemental","djinn","treant","eye","imp","demon","angel","giant","ogre","hydra"))
    if water:
        polygon([(12,69),(113,69),(95,100),(28,100)],lo)
        polygon([(22,69),(103,69),(96,76),(25,76)],main)
        line([(63,69),(63,12)],(90,64,50,255),4)
        polygon([(68,16),(101,57),(68,57)],hi)
        polygon([(58,19),(25,59),(58,59)],(222,210,190,255))
        polygon([(13,104),(40,99),(63,104),(94,99),(114,105),(99,112),(74,110),(54,113),(28,110)],(62,136,156,220),None)
    elif monster and ("golem" in low or "elemental" in low or "ogre" in low or "giant" in low):
        polygon([(31,17),(93,17),(98,45),(29,45)],skin)
        polygon([(25,43),(99,43),(89,90),(38,90)],main)
        polygon([(35,86),(57,83),(55,119),(27,120)],lo)
        polygon([(70,83),(90,85),(104,119),(75,120)],lo)
        polygon([(20,45),(36,49),(38,91),(13,94)],hi)
        polygon([(91,48),(105,45),(112,94),(91,92)],hi)
        polygon([(42,48),(75,48),(85,72),(32,76)],shade(main,1.13),None)
    elif monster:
        polygon([(24,74),(43,48),(87,46),(105,73),(88,91),(39,91)],main)
        polygon([(73,47),(92,28),(111,37),(108,65),(90,70)],skin)
        polygon([(25,80),(42,81),(37,118),(20,118)],lo)
        polygon([(73,83),(92,83),(95,118),(77,118)],lo)
        polygon([(14,55),(36,39),(48,45),(23,75)],lo)
        if "dragon" in low or "wyvern" in low:
            polygon([(52,50),(14,8),(28,73)],shade(main,.75))
            polygon([(62,48),(112,10),(96,68)],hi)
        elif "spider" in low: 
            for p in [16,38,85,106]:line([(p,68),(p+(-12 if p<60 else 12),94)],dark,4)
    else:
        polygon([(40,76),(63,76),(55,119),(34,120)],lo)
        polygon([(69,75),(87,76),(96,120),(72,119)],lo)
        if race in ("vampire","undead"):polygon([(27,40),(99,40),(110,97),(62,81),(15,98)],(66,44,68,255))
        polygon([(34,18),(83,18),(91,39),(28,42)],skin)
        if race=="elf":
            polygon([(28,30),(14,25),(30,42)],skin)
            polygon([(85,30),(101,24),(86,42)],skin)
        if race=="orc":
            polygon([(31,29),(18,17),(36,37)],skin)
            polygon([(82,29),(96,15),(87,38)],skin)
        if race=="dwarf":polygon([(38,33),(82,33),(76,56),(48,56)],(125,78,53,255))
        polygon([(25,46),(94,46),(84,88),(35,89)],main)
        polygon([(36,49),(72,48),(84,72),(30,78)],hi,None)
        polygon([(22,47),(36,49),(27,92),(13,90)],skin)
        polygon([(87,48),(100,49),(111,91),(95,92)],skin)
        polygon([(37,19),(46,9),(76,11),(91,28),(77,24),(47,28)],lo)
        if any(x in low for x in ("archer","crossbow","hunter","ranger","marksman","bow")):
            line([(99,27),(110,111)],(100,66,43,255),4)
            line([(99,27),(117,69),(110,111)],(230,220,187,255),1)
        elif any(x in low for x in ("mage","wizard","adept","druid","shaman","priest","chanter","summon","lich")):
            line([(107,118),(107,16)],(113,77,51,255),4)
            polygon([(99,16),(113,9),(123,25),(109,38),(96,31)],(70,191,165,255))
        else:
            line([(107,102),(106,27)],(100,66,43,255),4)
            polygon([(99,24),(112,18),(119,57),(102,61)],metal)
            polygon([(91,54),(121,53),(119,64),(92,65)],dark)
    # Distinguish clan/race through clean flat colors; never draw face or background.
    return im.resize((128,128),Image.Resampling.LANCZOS)
def race_for(name,civ):
    s=(name+" "+(civ or "")).lower()
    if any(w in s for w in ("clan of embers","goblin","orc","ogre","lizardman")):return "orc"
    if any(w in s for w in ("calabim","vampire","moroi")):return "vampire"
    if any(w in s for w in ("ljosalfar","svartalfar")):return "elf"
    if any(w in s for w in ("khazad","luchuirp","dwarf")):return "dwarf"
    if any(w in s for w in ("skeleton","lich","spectre","wraith","undead")):return "undead"
    return "human"
def clean(s):return re.sub(r"[\\/]", "-",s)
def add(unit,civ=None,force=False):
    name=unit["name"]
    filename=clean(name+("-"+civ if civ else ""))+".png"
    if filename in all_png or (OUT/filename).exists():return
    # Do not replace any approved art: only new files, all explicitly tracked.
    nation=next((n for n in nations if n.get("name")==civ),{})
    raw=nation.get("outerColor",[148,67,99])
    rgb=raw if isinstance(raw,list) and len(raw)>=3 else [148,67,99]
    path=OUT/filename
    sprite(name,unit.get("unitType",""),civ,rgb,race_for(name,civ)).save(path,optimize=True)
    created.append({"path":str(path.relative_to(ROOT)),"unit":name,"civilization":civ,"race":race_for(name,civ),"status":"placeholder","source":"procedural flat 2D silhouette, not canonical EMM artwork"})
# Every Unit definition receives a generic sprite if none exists.
for unit in units:add(unit)
# For shared units, create unique faction-race/colored silhouettes, without touching approved existing sprites.
shared=[u for u in units if not u.get("uniqueTo")]
for nation in nations:
    civ=nation.get("name","")
    if not nation.get("outerColor") or civ in ("Barbarians","Spectator"):continue
    for unit in shared:add(unit,civ)
# Race-specific faction units are also generated when the base art was already present.
for unit in units:
    if unit.get("uniqueTo"):add(unit,unit["uniqueTo"])
# Pack a text atlas referring to individual transparent PNG pages.
atlas=[]
for row in created:
    path=row["path"];stem=path.split("/")[-1][:-4]
    atlas.extend([path,"size: 128, 128","format: RGBA8888","filter: Linear, Linear","repeat: none",
      "TileSets/AmuritesSimple/Units/"+stem,
      "  rotate: false","  xy: 0, 0","  size: 128, 128","  orig: 128, 128","  offset: 0, 0","  index: -1",
      "TileSets/AbsoluteUnits/Units/"+stem,
      "  rotate: false","  xy: 0, 0","  size: 128, 128","  orig: 128, 128","  offset: 0, 0","  index: -1",""])
(ROOT/"placeholder-generated.atlas").write_text("\n".join(atlas)+"\n")
atlases=json.loads((ROOT/"Atlases.json").read_text())
if "placeholder-generated" not in atlases: atlases.append("placeholder-generated")
(ROOT/"Atlases.json").write_text(json.dumps(atlases,indent=2)+"\n")
log=ROOT/"art/PLACEHOLDER_SPRITES.json"
log.parent.mkdir(exist_ok=True)
log.write_text(json.dumps({"generator":"art/generate_placeholders.py","count":len(created),"sprites":created},indent=2)+"\n")
(ROOT/"art/PLACEHOLDER_SPRITES.md").write_text("# Generated placeholder artwork\n\n"
    +f"Total new PNGs: **{len(created)}**. Every entry below is a placeholder and not verified EMM-exact. Existing sprites were left unchanged.\n\n"
    +"| Sprite | Civ | Race | File |\n|---|---|---|---|\n"
    +"\n".join("| "+r["unit"].replace("|","/")+" | "+(r["civilization"] or "generic")+" | "+r["race"]+" | "+r["path"]+" |" for r in created)+"\n")
print(f"Generated {len(created)} new transparent PNG unit sprites. Approved sprites preserved.")
