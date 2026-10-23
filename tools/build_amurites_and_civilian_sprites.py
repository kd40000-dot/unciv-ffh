#!/usr/bin/env python3
"""Register all supplied Amurite sprites and recolor only the civilian sash for each civ.

Source art is NEVER overwritten. Run via GitHub Actions:
    pip install Pillow numpy
    python tools/build_amurites_and_civilian_sprites.py
"""
from __future__ import annotations

import colorsys
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Images/TileSets/AmuritesSimple/Units"
GENERATED = SOURCE / "Generated"
ATLAS = ROOT / "amurites-simple-complete.atlas"
CANVAS = 512
MAX_FIGURE = 340

AMURITES = {
    "Amurite_adept.png": "Adept",
    "Amurite_archer.png": "Archer",
    "Amurite_archmage.png": "Archmage",
    "Amurite_beastmaster.png": "Beastmaster",
    "Amurite_champion.png": "Champion",
    "Amurite_chanter.png": "Chanter",
    "Amurite_chariot.png": "Chariot",
    "Amurite_crossbowman.png": "Crossbowman",
    "Amurite_firebow.png": "Firebow",
    "Amurite_horse_archer.png": "Horse Archer",
    "Amurite_horseman.png": "Horseman",
    "Amurite_hunter.png": "Hunter",
    "Amurite_immortal.png": "Immortal",
    "Amurite_marksman.png": "Marksman",
    "Amurite_phalanx.png": "Phalanx",
    "Amurite_ranger.png": "Ranger",
    "Amurite_scout.png": "Scout",
    "Amurite_swordsman.png": "Swordsman",
    "Amurite_warrior.png": "Warrior",
    "Amurite_wizard.png": "Wizard",
    "Govannon.png": "Govannon",
}

def fit_sprite(source: Image.Image, *, align: str = "right") -> Image.Image:
    """Place visible pixels against the chosen horizontal edge without clipping.

    Alignment is applied AFTER proportional sizing, using the actual post-resize
    alpha bounding box. The top/bottom remain centered as before.
    No pixel of the character is cropped or modified by the translation.
    """
    art = source.convert("RGBA")
    bbox = art.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Completely transparent source sprite")
    art = art.crop(bbox)
    art.thumbnail((MAX_FIGURE, MAX_FIGURE), Image.Resampling.LANCZOS)
    # LANCZOS can introduce a transparent outer rim: use the real visible bounds.
    bounds = art.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("Empty sprite after scaling")
    art = art.crop(bounds)
    if align == "left":
        left = 0
    elif align == "right":
        left = CANVAS - art.width
    else:
        raise ValueError(f"Unsupported horizontal alignment: {align}")
    top = (CANVAS - art.height) // 2
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    canvas.alpha_composite(art, (left, top))
    visible = canvas.getchannel("A").getbbox()
    assert visible is not None
    assert (visible[0] == 0 if align == "left" else visible[2] == CANVAS), (align, visible)
    return canvas

def sash_mask(source: Image.Image) -> np.ndarray:
    """The provided figures have an isolated purple cloth sash at their waist.

    Restrict recoloring both by pigment and by torso position, not just hue,
    so any other decorations and all dark outlines remain untouched.
    """
    rgba = np.asarray(source.convert("RGBA"))
    hsv = np.asarray(source.convert("RGB").convert("HSV"))
    h, w = rgba.shape[:2]
    y, x = np.ogrid[:h, :w]
    mask = (
        (rgba[:, :, 3] > 40)
        & (hsv[:, :, 0] >= 178) & (hsv[:, :, 0] <= 228)
        & (hsv[:, :, 1] >= 48)
        & (hsv[:, :, 2] >= 38)
        & (y >= int(.34*h)) & (y < int(.53*h))
        & (x >= int(.29*w)) & (x < int(.74*w))
    )
    count = int(mask.sum())
    if count < 250:
        raise AssertionError(
            f"Expected purple torso sash (got {count} matching pixels of {w}x{h}); "
            "source composition or hue changed, inspect before adjusting mask"
        )
    return mask

def recolor_sash(source: Image.Image, mask: np.ndarray, rgb: list[int]) -> Image.Image:
    image = source.convert("RGBA")
    hsv = np.asarray(image.convert("RGB").convert("HSV")).copy()
    original = np.asarray(image)
    target_rgb = rgb
    # Black outerColor is not visible on an outlined character:
    # the Barbarian alternate red is selected by the caller instead.
    hue, saturation, _ = colorsys.rgb_to_hsv(*(c/255 for c in target_rgb))
    hue = int(round(hue * 255))
    saturation = int(round(saturation * 255))
    target_brightness = max(target_rgb) / 255
    # Retain the source's angular light/dark folds, adapting overall brightness.
    # For dark civs retain enough brightness that the sash is legible on a map.
    original_value = hsv[:, :, 2].astype(np.float32)
    adjusted_value = np.clip(original_value * (0.62 + 0.53 * target_brightness), 0, 255).astype("uint8")
    hsv[:, :, 0][mask] = hue
    hsv[:, :, 1][mask] = saturation
    hsv[:, :, 2][mask] = adjusted_value[mask]
    new_rgb = np.asarray(Image.fromarray(hsv, "HSV").convert("RGB"))
    output = original.copy()
    output[:, :, :3][mask] = new_rgb[mask]
    if not np.array_equal(output[:, :, 3], original[:, :, 3]):
        raise AssertionError("Unexpected alpha change")
    if not np.array_equal(output[:, :, :3][~mask], original[:, :, :3][~mask]):
        raise AssertionError("Pixel outside sash changed")
    return Image.fromarray(output, "RGBA")

def page(lines: list[str], filename: str, regions: list[str]) -> None:
    full = "Images/TileSets/AmuritesSimple/Units/Generated/" + filename
    lines += [full, f"size: {CANVAS}, {CANVAS}", "format: RGBA8888",
              "filter: Linear, Linear", "repeat: none"]
    for region in regions:
        lines += [
            region, "  rotate: false", "  xy: 0, 0",
            f"  size: {CANVAS}, {CANVAS}",
            f"  orig: {CANVAS}, {CANVAS}",
            "  offset: 0, 0", "  index: -1"
        ]
    lines.append("")

def main() -> None:
    nations = json.loads((ROOT / "jsons/Nations.json").read_text())
    civs = [n for n in nations if n["name"] != "Barbarians"]
    assert len(civs) == 19
    units = {u["name"] for u in json.loads((ROOT/"jsons/Units.json").read_text())}
    GENERATED.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    # Supply all 21 approved Amurites characters, overriding older placeholder/
    # fallback atlases by putting this atlas LAST in Atlases.json.
    for src_name, unit_name in AMURITES.items():
        source_path = SOURCE / src_name
        assert source_path.is_file(), source_path
        source = Image.open(source_path).convert("RGBA")
        name = f"{unit_name}-Amurites.png"
        fit_sprite(source).save(GENERATED/name, optimize=True)
        page(lines, name, [
            f"TileSets/AmuritesSimple/Units/{unit_name}-Amurites",
            f"TileSets/AbsoluteUnits/Units/{unit_name}-Amurites",
        ])
        print("AMURITES", unit_name, "present in unit roster:", unit_name in units)
    # Include non-Amurite generic civs as well (and Barbarians), not just Amurites.
    # Unciv automatically resolves UnitName-Civilization before UnitName.
    for unit, filename in [("Worker", "worker_1.png"), ("Settler", "settler.png")]:
        src = Image.open(SOURCE / filename).convert("RGBA")
        mask = sash_mask(src)
        print(f"SASH {unit}: {int(mask.sum())} purple pixels isolated")
        default_name = unit + ".png"
        fit_sprite(src, align="left").save(GENERATED/default_name, optimize=True)
        page(lines, default_name, [
            f"TileSets/AmuritesSimple/Units/{unit}",
            f"TileSets/AbsoluteUnits/Units/{unit}",
        ])
        for nation in nations:
            civ = nation["name"]
            target = list(nation["outerColor"])
            if max(target) < 38:  # Barbarians have black outerColor; use their red innerColor.
                target = list(nation["innerColor"])
            img = fit_sprite(recolor_sash(src, mask, target), align="left")
            name = f"{unit}-{civ}.png"
            img.save(GENERATED/name, optimize=True)
            page(lines, name, [
                f"TileSets/AmuritesSimple/Units/{unit}-{civ}",
                f"TileSets/AbsoluteUnits/Units/{unit}-{civ}",
            ])
    ATLAS.write_text("\n".join(lines) + "\n")
    atlas_list = ROOT / "Atlases.json"
    names = json.loads(atlas_list.read_text())
    names = [n for n in names if n != "amurites-simple-complete"]
    names.append("amurites-simple-complete")  # newest definitions take precedence
    atlas_list.write_text(json.dumps(names, separators=(",", ":")) + "\n")
    assert len(AMURITES)==21
    expected_pages=21 + 2 + 2*len(nations)
    assert len(list(GENERATED.glob("*.png")))==expected_pages
    assert lines.count("format: RGBA8888")==expected_pages
    for source, unit in AMURITES.items():
        assert (GENERATED/f"{unit}-Amurites.png").is_file()
    print(f"OK: registered {len(AMURITES)} Amurites sprites, 2 generic civilians, "
          f"{2*len(nations)} nation sash colors = {expected_pages} PNG pages; "
          "both AmuritesSimple and AbsoluteUnits unit sets.")

if __name__ == "__main__":
    main()
