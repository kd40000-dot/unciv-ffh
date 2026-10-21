#!/usr/bin/env python3
"""Convert extracted authentic FfH2/EMM leader DDS art into Unciv PNG portraits.

Input: a directory containing individual DDS files extracted from original FfH2
art FPK archives (or previously extracted equivalent image files).
This script cannot extract the FPK archives themselves. No substitute art is generated.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/data/emm-leader-portraits.json"

def find_source(directory: Path, relative_dds: str) -> Path | None:
    relative = relative_dds.replace("\\", "/").lstrip("/")
    direct = directory / relative
    if direct.is_file():
        return direct
    # Case-insensitive path lookup, accounting for a possible "Assets/" prefix
    wanted = relative.lower()
    candidates = [p for p in directory.rglob("*.dds") if p.is_file()]
    for p in candidates:
        normalized = p.relative_to(directory).as_posix().lower()
        if normalized.endswith(wanted):
            return p
    # Some independently extracted packs flatten all art paths
    return next((p for p in candidates if p.name.lower() == Path(relative).name.lower()), None)

def convert(source: Path, output: Path, *, size: int, border: int, overwrite: bool):
    if output.exists() and not overwrite:
        raise FileExistsError(f"Existing portrait will not be overwritten: {output}")
    with Image.open(source) as image:
        image.load()
        image = image.convert("RGBA")
        if image.width < 32 or image.height < 32:
            raise ValueError(f"Suspiciously small source image: {source}: {image.size}")
        image = ImageOps.contain(image, (size-2*border, size-2*border), method=Image.Resampling.LANCZOS)
        result = Image.new("RGBA", (size, size), (0,0,0,0))
        result.alpha_composite(image, ((size-image.width)//2, (size-image.height)//2))
        output.parent.mkdir(parents=True, exist_ok=True)
        result.save(output, "PNG", optimize=True)
    with Image.open(output) as verify:
        verify.verify()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extracted_art_dir", type=Path, help="Directory of original unpacked FfH2 DDS files")
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--border", type=int, default=10, help="Transparent outer padding in pixels")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--allow-partial", action="store_true", help="Create available portraits even if the full 19 are not in the input")
    args = parser.parse_args()
    if not (100 <= args.size <= 512 and 0 <= args.border < args.size // 4):
        parser.error("size must be 100–512 and border must be less than 1/4 of size")
    if not args.extracted_art_dir.is_dir():
        parser.error(f"Directory not found: {args.extracted_art_dir}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    missing, found = [], []
    for entry in manifest["entries"]:
        original = find_source(args.extracted_art_dir, entry["emmPortraitDdsPath"])
        if original is None:
            missing.append(entry)
        else:
            found.append((entry, original))
    if missing and not args.allow_partial:
        for e in missing:
            print(f"MISSING: {e['leaderName']}: {e['emmPortraitDdsPath']}")
        raise SystemExit(f"Aborted without writing: {len(missing)} of {len(manifest['entries'])} original DDS textures missing. Use --allow-partial for explicit partial imports.")
    count = 0
    for entry, source in found:
        output = ROOT / entry["targetPngPath"]
        try:
            convert(source, output, size=args.size, border=args.border, overwrite=args.overwrite)
        except Exception as e:
            print(f"FAILED: {entry['leaderName']}: {e}")
            raise
        count += 1
        print(f"OK: {source} -> {output.relative_to(ROOT)}")
    print(f"Imported {count} original leader portraits; missing {len(missing)}.")
    if missing:
        for e in missing: print(f"MISSING: {e['leaderName']}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
