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
from PIL import Image, ImageDraw, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
NAMES=("Firebow","Wizard","Chanter","Adept","Govannon")
W,H,PAD=1024,1024,4
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
    # Original 84px figure is twice the height of stock Unciv units.
    # Scale the artwork, not its 84px texture region; preserve crisp pixel edges.
    bounds=im.getbbox()
    if bounds is None:
        raise ValueError("Empty Govannon art")
    figure=im.crop(bounds)
    target_height=43
    target_width=max(1,round(figure.width*target_height/figure.height))
    figure=figure.resize((target_width,target_height),Image.Resampling.NEAREST)
    scaled=Image.new("RGBA",(84,84))
    # Shift right so the fixed portrait badge does not obscure his head.
    scaled.alpha_composite(figure,((84-target_width)//2+12,84-target_height-5))
    # Composite Govannon portrait onto opaque dark green backing.
    icon_path=ROOT/"Images"/"UnitIcons"/"Govannon.png"
    icon=Image.open(icon_path).convert("RGBA")
    background=Image.new("RGBA",icon.size,(34,47,34,255))
    background.alpha_composite(icon)
    background.save(icon_path,optimize=True)
    for tileset in ("FantasyHex","AbsoluteUnits"):
        dest=ROOT/"Images"/"TileSets"/tileset/"Units"/"Govannon.png"
        scaled.save(dest,optimize=True)

def apply_chanter_pixel_sprite()->None:
    """Install approved Chanter sprite at the same 43px height as Govannon."""
    source=ROOT/"development"/"assets"/"chanter-pixel-06.png.b64"
    raw=base64.b64decode(source.read_text("ascii").strip(),validate=True)
    im=Image.open(BytesIO(raw)).convert("RGBA")
    if im.size!=(84,84) or im.getbbox() is None:
        raise ValueError("Chanter map sprite must be a nonempty 84x84 PNG")
    bounds=im.getbbox()
    if bounds[3]-bounds[1]!=43:
        raise ValueError(f"Chanter must match Govannon's 43px height: {bounds}")
    for tileset in ("FantasyHex","AbsoluteUnits"):
        dest=ROOT/"Images"/"TileSets"/tileset/"Units"/"Chanter.png"
        im.save(dest,optimize=True)

def apply_adept_first_pose()->None:
    """Approved first Adept pose: original low-resolution pixel art."""
    source=ROOT/"development"/"assets"/"adept-approved-08.png.b64"
    im=Image.open(BytesIO(base64.b64decode(source.read_text("ascii").strip(),validate=True))).convert("RGBA")
    if im.size!=(84,84) or not im.getbbox():
        raise ValueError("Adept sprite must be nonempty 84x84")
    bounds=im.getbbox()
    if bounds[3]-bounds[1]!=43:
        figure=im.crop(bounds)
        width=max(1,round(figure.width*43/figure.height))
        figure=figure.resize((width,43),Image.Resampling.NEAREST)
        im=Image.new("RGBA",(84,84))
        im.alpha_composite(figure,(42-width//2,84-43-5))
    for tileset in ("FantasyHex","AbsoluteUnits"):
        im.save(ROOT/"Images"/"TileSets"/tileset/"Units"/"Adept.png",optimize=True)

def apply_wizard_front_sprite()->None:
    """Use the user-approved front-facing Wizard at 43px, preserving other units."""
    source=ROOT/"development"/"assets"/"wizard-front-09.png.b64"
    im=Image.open(BytesIO(base64.b64decode(source.read_text("ascii").strip(),validate=True))).convert("RGBA")
    if im.size!=(84,84) or not im.getbbox():
        raise ValueError("Wizard sprite must be nonempty 84x84")
    bounds=im.getbbox()
    if bounds[3]-bounds[1]!=43:
        raise ValueError(f"Wizard visible height must be 43px: {bounds}")
    if im.getchannel("A").getextrema()[0]!=0:
        raise ValueError("Wizard sprite background must be transparent")
    for tileset in ("FantasyHex","AbsoluteUnits"):
        im.save(ROOT/"Images"/"TileSets"/tileset/"Units"/"Wizard.png",optimize=True)

def apply_firebow_pixel_sprite()->None:
    """Repair Firebow using the known-good original approved sprite source.

    The prior firebow-pixel-10.png.b64 image produced visible corruption in
    Unciv. Do not use that source again. Instead rebuild from the already
    approved sprite in the verified five-character source collage.
    """
    sheet=load_source()
    figure=sheet.crop((0,0,80,80)).convert("RGBA")
    bounds=figure.getbbox()
    if bounds is None:
        raise ValueError("Missing approved Firebow figure")
    figure=figure.crop(bounds)
    # Downsample deliberately to the same low-resolution character scale
    # as the stock Warrior, then retain hard pixel edges.
    width=max(1,round(figure.width*43/figure.height))
    figure=figure.resize((width,43),Image.Resampling.NEAREST)
    sprite=Image.new("RGBA",(84,84))
    sprite.alpha_composite(figure,((84-width)//2,84-43-5))
    for tileset in ("FantasyHex","AbsoluteUnits"):
        sprite.save(ROOT/"Images"/"TileSets"/tileset/"Units"/"Firebow.png",optimize=True)

def apply_simple_badges_and_sprite_offsets()->None:
    """Simple opaque symbol badges and a common offset for every map figure.

    The existing figures are preserved pixel-for-pixel; only their position
    within the transparent 84x84 texture changes.
    """
    purple=(67,38,111,255)
    rim=(192,159,230,255)
    white=(250,244,255,255)
    def make_badge(name):
        # Render at 96px, then store the same 96px icon atlas region.
        icon=Image.new("RGBA",(96,96))
        d=ImageDraw.Draw(icon)
        d.ellipse((5,5,90,90),fill=rim)
        d.ellipse((11,11,84,84),fill=purple)
        if name in ("Adept","Wizard","Govannon"):
            # Flame, drawn as a recognizable single white silhouette.
            d.polygon([(49,19),(59,39),(58,48),(69,40),(69,61),
                       (63,72),(51,79),(38,75),(28,65),(29,52),
                       (40,36),(41,54),(48,48)],fill=white)
            d.polygon([(49,50),(55,61),(50,72),(43,68),(42,61)],fill=purple)
        elif name=="Firebow":
            # Bow and arrow.
            d.arc((25,17,69,79),65,292,fill=white,width=7)
            d.line((39,21,63,74),fill=white,width=4)
            d.line((19,49,75,49),fill=white,width=6)
            d.polygon([(78,49),(62,40),(62,58)],fill=white)
        else:
            # Short sword, matching the minimal weapon-symbol style.
            d.polygon([(64,19),(73,28),(48,57),(40,49)],fill=white)
            d.polygon([(66,16),(79,17),(76,30),(70,33),(61,24)],fill=white)
            d.line((34,53,52,69),fill=white,width=8)
            d.line((25,62,43,80),fill=white,width=7)
        return icon

    for name in NAMES:
        make_badge(name).save(ROOT/"Images"/"UnitIcons"/f"{name}.png",optimize=True)
        for tileset in ("FantasyHex","AbsoluteUnits"):
            path=ROOT/"Images"/"TileSets"/tileset/"Units"/f"{name}.png"
            original=Image.open(path).convert("RGBA")
            bbox=original.getbbox()
            if not bbox:
                raise ValueError(f"Missing visible sprite: {name}")
            figure=original.crop(bbox)
            if figure.height!=43:
                width=max(1,round(figure.width*43/figure.height))
                figure=figure.resize((width,43),Image.Resampling.NEAREST)
            if figure.width>65:
                # Prevent a wide source from being cropped off the tile.
                width=65
                figure=figure.resize((width,43),Image.Resampling.NEAREST)
            canvas=Image.new("RGBA",(84,84))
            # Badge occupies the upper-left of the unit; put body right of it.
            x=min(84-figure.width, max(0,42-figure.width//2+14))
            canvas.alpha_composite(figure,(x,84-43-5))
            canvas.save(path,optimize=True)
            assert canvas.getbbox()[3]-canvas.getbbox()[1]==43
    print("Installed simple weapon/flame badges and aligned five 43px figures")

# Native icon entries for the first gameplay-capable mana system. The art is
# deliberately simple: distinct resource/Improvement icons and small map gems.
MANA_COLORS={
    "Raw Mana":(158,119,209),
    "Body Mana":(92,190,100),
    "Fire Mana":(231,117,60),
    "Mind Mana":(106,164,227),
    "Death Mana":(173,155,211),
}
MANA_SPHERES=("Body","Fire","Mind","Death")

def build_mana_icon(name:str,kind:str="resource")->Image.Image:
    """Draw a tiny pixelated crystal, not a photorealistic tile icon."""
    rgb=MANA_COLORS[name]
    im=Image.new("RGBA",(32,32))
    d=ImageDraw.Draw(im)
    dark=(30,29,45,255)
    base=tuple(rgb)+(255,)
    light=tuple(min(255,c+52) for c in rgb)+(255,)
    shadow=tuple(max(0,c-53) for c in rgb)+(255,)
    if kind=="improvement":
        d.ellipse((4,22,27,29),fill=dark)
        d.rectangle((9,15,22,24),fill=(69,65,83,255),outline=dark)
        d.rectangle((12,18,19,24),fill=(110,104,129,255))
    d.polygon([(16,3),(25,12),(21,24),(11,26),(6,14)],fill=dark)
    d.polygon([(16,5),(23,13),(19,22),(12,24),(8,14)],fill=base)
    d.polygon([(16,5),(16,20),(8,14)],fill=light)
    d.polygon([(16,20),(19,22),(12,24)],fill=shadow)
    d.rectangle((14,8,15,10),fill=(254,253,243,255))
    return im.resize((64,64),Image.Resampling.NEAREST)

def make_mana_art()->list[str]:
    names=[]
    def save_icon(key,im):
        path=ROOT/"Images"/(key+".png")
        path.parent.mkdir(parents=True,exist_ok=True)
        im.save(path,optimize=True)
        names.append(key)
    for name in MANA_COLORS:
        save_icon("ResourceIcons/"+name,build_mana_icon(name))
        if name=="Raw Mana":
            save_icon("TileSets/FantasyHex/Tiles/"+name,build_mana_icon(name))
        else:
            save_icon("UnitPromotionIcons/"+name.replace(" Mana",""),build_mana_icon(name))
    # Promotion icons are essential for seeing the magic progression in
    # Unciv's upgrade picker. Multi-rank promotions (I/II/III) reuse one icon.
    symbols={
        "Channeling":"Raw Mana",
        "Hastened":"Body Mana",
        "Spellstaff":"Raw Mana",
        "Hero":"Fire Mana",
        "Marksman":"Fire Mana",
        "Dimensional":"Mind Mana",
    }
    for name,palette in symbols.items():
        save_icon("UnitPromotionIcons/"+name,build_mana_icon(palette))
    for sphere in MANA_SPHERES:
        key=sphere+" Node"
        icon=build_mana_icon(sphere+" Mana","improvement")
        save_icon("ImprovementIcons/"+key,icon)
        save_icon("TileSets/FantasyHex/Tiles/"+key,icon)
    return names

def make_spell_asset_art()->list[str]:
    """Pixel-native 84x84 Skeleton sprite and simple Smoke icon/overlay.

    Kept separate from all five approved Amurite character sources.
    Geometry uses deliberate flat-color pixel blocks; no lossy resampling.
    """
    generated=[]
    def save(key:str,im:Image.Image):
        path=ROOT/"Images"/(key+".png")
        path.parent.mkdir(parents=True,exist_ok=True)
        im.save(path,optimize=True)
        generated.append(key)

    # 22x22 pixel-art silhouette enlarged twice: ~44 actual sprite pixels.
    sk=Image.new("RGBA",(22,22))
    d=ImageDraw.Draw(sk)
    outline=(24,25,33,255)
    bone=(223,220,197,255)
    shade=(152,151,135,255)
    dark=(58,55,65,255)
    leather=(100,76,67,255)
    iron=(172,180,181,255)
    d.ellipse((7,0,14,7),fill=outline)
    d.rectangle((8,1,13,6),fill=bone)
    d.rectangle((8,3,9,4),fill=dark)
    d.rectangle((12,3,13,4),fill=dark)
    d.rectangle((10,5,11,5),fill=shade)
    d.rectangle((8,8,14,13),fill=outline)
    d.rectangle((9,8,13,11),fill=bone)
    for x in (10,12):
        d.line((x,9,x,11),fill=shade,width=1)
    d.rectangle((8,12,14,13),fill=leather)
    d.line((7,8,5,13),fill=outline,width=3)
    d.line((7,8,5,12),fill=bone,width=1)
    d.line((14,8,17,13),fill=outline,width=3)
    d.line((14,8,17,12),fill=bone,width=1)
    d.rectangle((4,13,6,15),fill=bone)
    d.rectangle((16,13,18,14),fill=bone)
    d.line((9,14,8,19),fill=outline,width=3)
    d.line((13,14,14,19),fill=outline,width=3)
    d.line((9,14,8,18),fill=bone,width=1)
    d.line((13,14,14,18),fill=bone,width=1)
    d.line((6,19,9,20),fill=outline,width=2)
    d.line((13,19,16,20),fill=outline,width=2)
    # Worn short sword in right hand.
    d.line((18,12,20,4),fill=dark,width=3)
    d.line((18,12,20,4),fill=iron,width=1)
    d.line((16,12,20,13),fill=leather,width=2)
    doubled=sk.resize((44,44),Image.Resampling.NEAREST)
    figure=doubled.crop(doubled.getbbox()).resize((34,43),Image.Resampling.NEAREST)
    sprite=Image.new("RGBA",(84,84))
    sprite.alpha_composite(figure,(49,36))
    for tileset in ("FantasyHex","AbsoluteUnits"):
        save(f"TileSets/{tileset}/Units/Skeleton",sprite)
    icon=Image.new("RGBA",(96,96))
    ic=ImageDraw.Draw(icon)
    ic.ellipse((4,4,91,91),fill=(48,42,64,255),outline=(181,156,197,255),width=4)
    skull=sk.crop((7,0,15,8)).resize((48,48),Image.Resampling.NEAREST)
    icon.alpha_composite(skull,(24,20))
    ic.line((32,77,64,77),fill=bone,width=8)
    save("UnitIcons/Skeleton",icon)
    save("UnitPromotionIcons/Undead",icon)

    smoke=Image.new("RGBA",(32,32))
    sm=ImageDraw.Draw(smoke)
    smoke_dark=(61,58,71,245)
    smoke_mid=(125,117,137,229)
    smoke_light=(185,170,188,219)
    sm.ellipse((7,17,27,29),fill=smoke_dark)
    sm.ellipse((3,14,19,25),fill=smoke_mid)
    sm.ellipse((10,8,26,22),fill=smoke_light)
    sm.ellipse((4,4,16,15),fill=smoke_mid)
    sm.ellipse((15,1,26,12),fill=smoke_dark)
    smoke=smoke.resize((64,64),Image.Resampling.NEAREST)
    save("ImprovementIcons/Smoke",smoke)
    for tileset in ("FantasyHex","AbsoluteUnits"):
        save(f"TileSets/{tileset}/Tiles/Smoke",smoke)
    return generated

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
    for key in make_mana_art()+make_spell_asset_art():
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
    apply_chanter_pixel_sprite()
    apply_adept_first_pose()
    apply_wizard_front_sprite()
    apply_firebow_pixel_sprite()
    apply_simple_badges_and_sprite_offsets()
    pack_atlas()
