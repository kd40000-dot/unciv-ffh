#!/usr/bin/env python3
"""Pack all LeaderIcons PNGs into a LibGDX/Unciv-compatible game.png + game.atlas.

Run on desktop with Pillow installed. The Android Unciv client cannot pack
source images itself. Commit both generated files to the mod repository.
"""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Images/LeaderIcons"
CELL, GAP, MARGIN, COLUMNS, PAGE = 160, 8, 4, 5, 1024

def main():
    data = json.loads((ROOT/"docs/data/emm-leader-portraits.json").read_text(encoding="utf-8"))
    names = sorted(entry["leaderName"] for entry in data["entries"])
    assert len(names) == len(set(names)) == 19
    page = Image.new("RGBA", (PAGE, PAGE), (0, 0, 0, 0))
    atlas = ["", "game.png", f"size: {PAGE}, {PAGE}", "format: RGBA8888",
             "filter: MipMapLinearLinear, MipMapLinearLinear", "repeat: none"]
    for i, name in enumerate(names):
        source = SOURCE / f"{name}.png"
        assert source.is_file(), source
        with Image.open(source) as image:
            portrait = image.convert("RGBA").resize((CELL,CELL), Image.Resampling.LANCZOS)
        x = MARGIN + i % COLUMNS * (CELL + GAP)
        y = MARGIN + i // COLUMNS * (CELL + GAP)
        assert x+CELL <= PAGE and y+CELL <= PAGE
        page.alpha_composite(portrait, (x,y))
        atlas.extend([f"LeaderIcons/{name}", "  rotate: false", f"  xy: {x}, {y}",
                      f"  size: {CELL}, {CELL}", f"  orig: {CELL}, {CELL}",
                      "  offset: 0, 0", "  index: -1"])
    page.save(ROOT / "game.png", optimize=True)
    (ROOT / "game.atlas").write_text("\n".join(atlas)+"\n", encoding="utf-8")
    (ROOT / "Atlases.json").write_text('["game"]\n', encoding="utf-8")
    print(f"Packed {len(names)} leader portraits into game.png / game.atlas")

if __name__ == "__main__":
    main()
