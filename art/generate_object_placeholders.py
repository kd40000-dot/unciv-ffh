#!/usr/bin/env python3
"""Build transparent flat-2D placeholders for FFH buildings, mana nodes and improvements."""
import json, pathlib, re, math
from PIL import Image, ImageDraw
ROOT=pathlib.Path(__file__).resolve().parents[1]
categories=[("Buildings.json","BuildingIcons","BuildingIcons"),
            ("TileImprovements.json","ImprovementIcons","TileImprovementIcons")]
manifest=json.loads((ROOT/"art/PLACEHOLDER_SPRITES.json").read_text())
rows=[]
def safe(s):return s.replace("/","-").replace("\\","-")
def draw_obj(name,kind):
    im=Image.new("RGBA",(384,384),(0,0,0,0))
    d=ImageDraw.Draw(im)
    dark="#28222d";wall="#777382";hi="#c3ac92";roof="#844d64";wood="#765c4c"
    def poly(pts,fill,edge=dark):
        pts=[(int(x*3),int(y*3)) for x,y in pts]
        d.polygon(pts,fill=fill)
        if edge:d.line(pts+[pts[0]],fill=edge,width=10,joint="curve")
    def line(pts,fill,width=5):d.line([(x*3,y*3) for x,y in pts],fill=fill,width=width*3,joint="curve")
    low=name.lower()
    if "mana" in low or "node" in low:
        col={"fire":"#ed6946","water":"#42a7bb","earth":"#b79461","ice":"#81d1d9",
          "death":"#a68bb8","life":"#79b96a","sun":"#e7b862","shadow":"#56526e",
          "air":"#a7d2e2","nature":"#6fba8f","entropy":"#947d76"}.get(next((x for x in ("fire","water","earth","ice","death","life","sun","shadow","air","nature","entropy") if x in low),""),"#9c6dcb")
        poly([(13,103),(27,87),(99,87),(112,104),(104,114),(20,114)],"#6e6875")
        poly([(52,8),(76,31),(93,83),(59,107),(29,77),(39,31)],col)
        poly([(52,8),(62,39),(59,107),(29,77),(39,31)],"#ddddda",None)
        poly([(62,39),(93,83),(59,107)],col,None)
    elif any(x in low for x in ("road","remove","farm","pasture","plantation","camp","forest","fishing","quarry")):
        poly([(9,98),(64,72),(115,97),(66,117)],"#7b9e72")
        if "road" in low:poly([(40,103),(75,81),(94,93),(60,114)],"#beb5a8")
        elif "farm" in low:
            for i in range(4):line([(22+i*15,94),(46+i*15,76)],"#ddc380",4)
        else:
            poly([(27,81),(51,48),(79,78)],roof)
            poly([(36,79),(70,79),(70,107),(36,106)],wood)
    else:
        # Stone tower, timber roof, arched entrance; role-specific silhouette variation
        poly([(15,98),(30,91),(101,92),(114,104),(103,116),(20,116)],"#5d6471")
        poly([(30,45),(96,44),(97,100),(29,100)],wall)
        poly([(22,47),(64,17),(106,46)],roof)
        poly([(56,100),(56,75),(65,66),(74,76),(75,101)],dark,None)
        poly([(35,60),(43,58),(43,72),(35,73)],hi)
        poly([(84,59),(92,58),(92,73),(84,72)],hi)
        if any(x in low for x in ("dungeon","prison","crypt","tomb")):
            poly([(46,21),(79,21),(94,50),(32,50)],"#494451")
            for q in (49,62,75):line([(q,58),(q,81)],dark,2)
        if "gate" in low or "portal" in low:
            poly([(35,52),(91,52),(90,100),(35,101)],"#595976")
            poly([(47,60),(80,60),(80,100),(47,100)],"#52b6ac",None)
        if "forge" in low:poly([(78,40),(93,32),(91,13),(105,32),(100,53)],"#ec9859")
        if "temple" in low:poly([(52,13),(76,13),(76,34),(52,34)],"#dbc58e")
    return im.resize((128,128),Image.Resampling.LANCZOS)
for src,folder,region in categories:
    for item in json.loads((ROOT/"jsons"/src).read_text()):
        name=item["name"];path=ROOT/"Images"/folder/(safe(name)+".png")
        if path.exists():continue
        path.parent.mkdir(parents=True,exist_ok=True)
        draw_obj(name,folder).save(path,optimize=True)
        rows.append({"path":str(path.relative_to(ROOT)),"object":name,"category":folder,"status":"placeholder","source":"procedural geometric object icon, not canonical EMM artwork"})
atlas=[]
for row in rows:
    path=row["path"];name=path.split("/")[-1][:-4];reg=row["category"]
    alias="BuildingIcons" if reg=="BuildingIcons" else "TileImprovementIcons"
    atlas.extend([path,"size: 128, 128","format: RGBA8888","filter: Linear, Linear","repeat: none",
      alias+"/"+name,"  rotate: false","  xy: 0, 0","  size: 128, 128","  orig: 128, 128","  offset: 0, 0","  index: -1",""])
(ROOT/"placeholder-objects.atlas").write_text("\n".join(atlas)+"\n")
allAtlases=json.loads((ROOT/"Atlases.json").read_text())
if "placeholder-objects" not in allAtlases:allAtlases.append("placeholder-objects")
(ROOT/"Atlases.json").write_text(json.dumps(allAtlases,indent=2)+"\n")
manifest["objects"]=rows;manifest["objectsCount"]=len(rows)
(ROOT/"art/PLACEHOLDER_SPRITES.json").write_text(json.dumps(manifest,indent=2)+"\n")
md=ROOT/"art/PLACEHOLDER_SPRITES.md"
with md.open("a") as f:
    f.write(f"\n## Building and improvement objects ({len(rows)} new placeholders)\n\n| Name | Type | Path |\n|---|---|---|\n")
    for r in rows:f.write(f"| {r['object']} | {r['category']} | {r['path']} |\n")
print("Generated",len(rows),"new placeholder building and improvement object icons.")
