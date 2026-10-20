#!/usr/bin/env python3
"""Repack the five user-approved Amurite unit designs exactly as supplied.

The source is one losslessly cropped collage of figures/icons made from:
  Firebow, Wizard, Chanter: user's approved three-column art sheet (62207.png)
  Adept, Govannon: user's approved five-column art sheet (62208.png)
No generation, drawing or change to clothing / pose / effects is performed.
WebP encoding is used only to transport the original approved cutouts.
"""
from __future__ import annotations

import base64
import hashlib
from io import BytesIO
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
NAMES=("Firebow","Wizard","Chanter","Adept","Govannon")
W,H,PAD=1024,512,4
SOURCES=[ROOT/"development"/"assets"/f"approved_part{i}.b64" for i in range(4)]
EXPECTED_SHA256="2c8f9a9dfa1d2aceba729cf9a52ae5e4c7afb3226953958a401f63771c9cc63b"

def image_in_square(im:Image.Image,w:int=84,h:int=84)->Image.Image:
    im=im.convert("RGBA")
    bounds=im.getbbox()
    if not bounds:
        raise ValueError("Approved source contains empty unit artwork")
    im=im.crop(bounds)
    im.thumbnail((w-2,h-2),Image.Resampling.LANCZOS)
    dest=Image.new("RGBA",(w,h))
    dest.alpha_composite(im,((w-im.width)//2,(h-im.height)//2))
    return dest

def load_source()->Image.Image:
    text="".join(p.read_text("ascii").strip() for p in SOURCES)
    raw=base64.b64decode(text,validate=True)
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=EXPECTED_SHA256:
        raise ValueError(f"Wrong approved artwork SHA256: {digest}")
    im=Image.open(BytesIO(raw)).convert("RGBA")
    if im.size!=(400,160):
        raise ValueError(f"Approved source expected 400x160, got {im.size}")
    return im

def make_assets()->None:
    sheet=load_source()
    for i,name in enumerate(NAMES):
        sx=i*80
        # Top row is the already-approved Unciv map figure. Bottom row
        # is that same sheet's user-approved icon (not a newly generated one).
        sprite=image_in_square(sheet.crop((sx,0,sx+80,80)))
        icon=sheet.crop((sx,80,sx+80,160)).resize((96,96),Image.Resampling.LANCZOS)
        dest=ROOT/"Images"/"UnitIcons"/(name+".png")
        dest.parent.mkdir(parents=True,exist_ok=True)
        icon.save(dest,optimize=True)
        for tileset in ("FantasyHex","AbsoluteUnits"):
            dest=ROOT/"Images"/"TileSets"/tileset/"Units"/(name+".png")
            dest.parent.mkdir(parents=True,exist_ok=True)
            sprite.save(dest,optimize=True)

def apply_govannon_pixel_sprite()->None:
    """Replace Govannon map art only; preserve all other approved unit sprites/icons."""
    source=ROOT/"development"/"assets"/"govannon-pixel-03.png.b64"
    raw=base64.b64decode(source.read_text("ascii").strip(),validate=True)
    im=Image.open(BytesIO(raw)).convert("RGBA")
    if im.size!=(84,84) or not im.getchannel("A").getextrema()[0]==0:
        raise ValueError("Govannon pixel sprite must be 84x84 and transparent")
    for tileset in ("FantasyHex","AbsoluteUnits"):
        dest=ROOT/"Images"/"TileSets"/tileset/"Units"/"Govannon.png"
        im.save(dest,optimize=True)

def pack_atlas()->None:
    # Import installed portrait/art source unchanged; downscale only for
    # the texture atlas. Keep full-resolution originals in Images.
    regions=[]
    for name,maxdim in (("LeaderIcons/Valledia",256),("NationIcons/Amurites",128)):
        im=Image.open(ROOT/"Images"/(name+".png")).convert("RGBA")
        im.thumbnail((maxdim,maxdim),Image.Resampling.LANCZOS)
        regions.append((name,im))
    for name in NAMES:
        key="UnitIcons/"+name
        regions.append((key,Image.open(ROOT/"Images"/(key+".png")).convert("RGBA")))
    for tileset in ("FantasyHex","AbsoluteUnits"):
        for name in NAMES:
            key=f"TileSets/{tileset}/Units/{name}"
            regions.append((key,Image.open(ROOT/"Images"/(key+".png")).convert("RGBA")))
    atlas=Image.new("RGBA",(W,H))
    lines=["","game.png",f"size: {W}, {H}","format: RGBA8888",
           "filter: MipMapLinearLinear, MipMapLinearLinear","repeat: none"]
    x=y=PAD
    rowheight=0
    for key,im in regions:
        w,h=im.size
        if x+w+PAD>W:
            x=PAD
            y+=rowheight+PAD
            rowheight=0
        if y+h+PAD>H:
            raise ValueError(f"Atlas doesn't fit: {key}")
        atlas.alpha_composite(im,(x,y))
        lines += [key,"  rotate: false",f"  xy: {x}, {y}",f"  size: {w}, {h}",
                  f"  orig: {w}, {h}","  offset: 0, 0","  index: -1"]
        x+=w+PAD
        rowheight=max(rowheight,h)
    atlas.save(ROOT/"game.png",optimize=True)
    (ROOT/"game.atlas").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (ROOT/"Atlases.json").write_text('["game"]\n',encoding="utf-8")
    for key,_ in regions:
        assert "\n"+key+"\n" in (ROOT/"game.atlas").read_text()
    print("Packed",len(regions),"approved image atlas regions")

if __name__=="__main__":
    make_assets()
    apply_govannon_pixel_sprite()
    pack_atlas()
