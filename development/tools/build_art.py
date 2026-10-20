#!/usr/bin/env python3
"""Build Unciv-compatible 2D graphics from attributed GPL Wesnoth sources.

The portraits are deliberately labelled *stand-ins* in art/sources.json:
no claim is made that they depict the original EMM leaders.
Run this on a desktop/CI machine; Android cannot pack textures.
"""
import io
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT / "development/art/sources.json").read_text())
REV = manifest["sourceRevision"]
ART_URL = "https://raw.githubusercontent.com/wesnoth/wesnoth/" + REV + "/"
PALETTE = manifest["factionColors"]

def fetch_one(pair):
    path = pair[1]
    url = ART_URL + quote(manifest["sourceRoot"] + path, safe="/")
    req = Request(url, headers={"User-Agent": "Unciv-FFH-art-build/0.2"})
    with urlopen(req, timeout=40) as response:
        raw = response.read()
    return path, Image.open(io.BytesIO(raw)).convert("RGBA")

def mkdir(p):
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def scaled_sprite(source, size=88):
    bbox = source.getchannel("A").getbbox()
    if bbox:
        source = source.crop(bbox)
    source.thumbnail((size, size), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", (size, size))
    canvas.alpha_composite(source, ((size-source.width)//2, (size-source.height)//2))
    return canvas

def faction_color(name):
    h = PALETTE.get(name, "#695c58").lstrip("#")
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def make_portrait(source, color):
    # Small illustrated badge with original source picture unaltered in content.
    w = 256
    base = Image.new("RGBA", (w,w))
    px = base.load()
    r,g,b = color
    for y in range(w):
        for x in range(w):
            center = max(0.40,1.15-((x-w/2)**2+(y-w/2)**2)**0.5/245)
            px[x,y]=(int(r*center*.48+10),int(g*center*.48+15),int(b*center*.48+22),255)
    # Keep aspect ratio and include the complete character silhouette.
    box = source.getchannel("A").getbbox()
    if box:
        source=source.crop(box)
    source.thumbnail((226,228),Image.Resampling.LANCZOS)
    base.alpha_composite(source,((w-source.width)//2,w-source.height-7))
    out=Image.new("RGBA",(w,w))
    d=ImageDraw.Draw(out)
    d.rounded_rectangle((4,4,252,252),radius=28,fill=(0,0,0,0),outline=(*color,255),width=5)
    d.arc((13,13,243,243),5,175,fill=(238,212,160,230),width=3)
    d.arc((13,13,243,243),185,355,fill=(238,212,160,230),width=3)
    return Image.alpha_composite(base,out)

def draw_emblem(faction, size=128):
    S=4
    im=Image.new("RGBA",(size*S,size*S))
    d=ImageDraw.Draw(im)
    white=(255,255,255,255)
    def xy(vals): return tuple(int(v*S) for v in vals)
    def polygon(coords, fill=white):d.polygon([(int(x*S),int(y*S)) for x,y in coords],fill=fill)
    if faction=="Amurites":
        d.ellipse(xy((22,22,106,106)),outline=white,width=5*S)
        d.ellipse(xy((46,46,82,82)),outline=white,width=4*S)
        polygon([(64,5),(75,53),(123,64),(75,76),(64,122),(52,76),(5,64),(52,53)])
        d.ellipse(xy((55,55,73,73)),fill=(48,55,85,255))
    elif faction=="Bannor":
        polygon([(64,6),(106,21),(104,78),(91,100),(64,123),(37,100),(24,78),(22,21)])
        polygon([(61,29),(67,29),(69,73),(87,65),(91,71),(69,86),(68,105),(61,105),(60,86),(37,71),(41,65),(60,73)])
        d.rectangle(xy((52,17,76,25)),fill=white)
    elif faction=="Ljosalfar":
        d.line([(64*S,118*S),(64*S,52*S)],fill=white,width=8*S)
        polygon([(64,22),(91,55),(81,82),(64,91),(46,82),(37,55)])
        d.line([(64*S,75*S),(39*S,51*S)],fill=(32,97,42,255),width=4*S)
        d.line([(64*S,66*S),(90*S,47*S)],fill=(32,97,42,255),width=4*S)
        d.arc(xy((32,16,96,98)),80,280,fill=white,width=3*S)
    else:
        polygon([(69,5),(88,33),(84,51),(103,68),(91,93),(64,122),(39,100),(28,80),(44,53),(38,30),(60,50)])
        polygon([(61,28),(69,55),(58,76),(71,74),(63,102),(47,83),(51,65)])
    return im.resize((size,size),Image.Resampling.LANCZOS)

def icon_for_sprite(source, color, size=160):
    bg=Image.new("RGBA",(size,size))
    d=ImageDraw.Draw(bg)
    d.ellipse((8,8,size-8,size-8),fill=(*color,234),outline=(234,214,160),width=5)
    sprite=scaled_sprite(source,124)
    sprite=sprite.resize((132,132),Image.Resampling.NEAREST)
    bg.alpha_composite(sprite,(14,14))
    return bg

def silhouette_icon(source):
    # White-on-transparent unit icon to match Unciv's UI color tint.
    source=scaled_sprite(source,172)
    a=source.getchannel("A")
    icon=Image.new("RGBA",source.size,(255,255,255,0))
    icon.putalpha(a)
    return icon

portrait_paths = manifest["portraitSources"]
unit_paths = dict(manifest["unitSources"],**manifest["styledUnitSources"])
needed=sorted(set(portrait_paths.values())|set(unit_paths.values()))
print(f"Downloading {len(needed)} distinct sprite and portrait sources")
images={}
with ThreadPoolExecutor(max_workers=7) as pool:
    futures={pool.submit(fetch_one,(i,path)):path for i,path in enumerate(needed)}
    for fut in as_completed(futures):
        path,image=fut.result()
        images[path]=image
        print("  source:",path,image.size)

for faction in PALETTE:
    draw_emblem(faction).save(mkdir(ROOT/"Images/NationIcons"/(faction+".png")))

for leader,path in portrait_paths.items():
    faction={"Valledia":"Amurites","Sabathiel":"Bannor","Arendel":"Ljosalfar","Jonas":"Clan of Embers"}[leader]
    make_portrait(images[path],faction_color(faction)).save(
        mkdir(ROOT/"Images/LeaderIcons"/(leader+".png")))

for name,path in unit_paths.items():
    image=images[path]
    icon_name=name.split("-")[0].strip() if "-" in name else name
    color=faction_color("Amurites" if "Amurites" in name else "Bannor" if "Bannor" in name else
                        "Ljosalfar" if "Ljosalfar" in name else "Clan of Embers" if "Clan of Embers" in name else "")
    sprite=scaled_sprite(image,84)
    for tileset in ("FantasyHex","AbsoluteUnits"):
        sprite.save(mkdir(ROOT/"Images/Tilesets"/tileset/"Units"/(name+".png")))
    # Do not create icon variants for styled units (their base icon is shared).
    if name in manifest["unitSources"]:
        icon_for_sprite(image,color).save(mkdir(ROOT/"Images/UnitPortraits"/(name+".png")))
        silhouette_icon(image).save(mkdir(ROOT/"Images/UnitIcons"/(name+".png")))
print("Generated",len(unit_paths),"unit sprite variants and",len(portrait_paths),"leader portraits")
