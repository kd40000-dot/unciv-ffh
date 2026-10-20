#!/usr/bin/env python3
"""Build an Unciv-ready atlas from approved Amurite art. Run from any cwd."""
from __future__ import annotations

import base64
import io
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
IMAGES = ROOT / 'Images'
SHEET = ROOT / 'development/assets/amurite_unit_concept_sprites.b64'
NAMES = ('Firebow', 'Govannon', 'Wizard')
TILESETS = ('FantasyHex', 'AbsoluteUnits')
W, H, PAD = 1024, 512, 4


def save_image(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def make_units() -> None:
    data = base64.b64decode(SHEET.read_text('ascii').strip(), validate=True)
    sheet = Image.open(io.BytesIO(data)).convert('RGBA')
    assert sheet.size == (192, 72), f'Bad sprite sheet: {sheet.size}'
    for i, name in enumerate(NAMES):
        original = sheet.crop((i * 64, 0, (i + 1) * 64, 72))
        bounds = original.getbbox()
        if bounds is None:
            raise ValueError(f'Empty {name} sprite')
        trimmed = original.crop(bounds)
        body = trimmed.copy()
        body.thumbnail((76, 80), Image.Resampling.LANCZOS)
        sprite = Image.new('RGBA', (84, 84))
        sprite.alpha_composite(body, ((84 - body.width) // 2, (84 - body.height) // 2))
        for tileset in TILESETS:
            save_image(sprite, IMAGES / 'TileSets' / tileset / 'Units' / f'{name}.png')
        portrait = trimmed.copy()
        portrait.thumbnail((82, 86), Image.Resampling.LANCZOS)
        icon = Image.new('RGBA', (96, 96))
        icon.alpha_composite(portrait, ((96 - portrait.width) // 2, (96 - portrait.height) // 2))
        save_image(icon, IMAGES / 'UnitIcons' / f'{name}.png')


def source_regions() -> list[tuple[str, Image.Image]]:
    regions = []
    for logical, size in (('LeaderIcons/Valledia', 256), ('NationIcons/Amurites', 128)):
        img = Image.open(IMAGES / f'{logical}.png').convert('RGBA')
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
        regions.append((logical, img))
    for name in NAMES:
        logical = f'UnitIcons/{name}'
        regions.append((logical, Image.open(IMAGES / f'{logical}.png').convert('RGBA')))
    for tileset in TILESETS:
        for name in NAMES:
            logical = f'TileSets/{tileset}/Units/{name}'
            regions.append((logical, Image.open(IMAGES / f'{logical}.png').convert('RGBA')))
    return regions


def build_atlas() -> None:
    atlas = Image.new('RGBA', (W, H))
    lines = ['', 'game.png', f'size: {W}, {H}', 'format: RGBA8888',
             'filter: MipMapLinearLinear, MipMapLinearLinear', 'repeat: none']
    x = y = PAD
    row_height = 0
    regions = source_regions()
    for name, image in regions:
        width, height = image.size
        if x + width + PAD > W:
            x = PAD
            y += row_height + PAD
            row_height = 0
        if y + height + PAD > H:
            raise RuntimeError(f'Atlas exceeds {W}x{H}: {name}')
        atlas.alpha_composite(image, (x, y))
        lines.extend((name, '  rotate: false', f'  xy: {x}, {y}',
                      f'  size: {width}, {height}', f'  orig: {width}, {height}',
                      '  offset: 0, 0', '  index: -1'))
        row_height = max(row_height, height)
        x += width + PAD
    atlas.save(ROOT / 'game.png', optimize=True)
    (ROOT / 'game.atlas').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (ROOT / 'Atlases.json').write_text('[game]\n', encoding='utf-8')
    print('Packed', len(regions), 'regions into Unciv game.atlas')


if __name__ == '__main__':
    make_units()
    build_atlas()
