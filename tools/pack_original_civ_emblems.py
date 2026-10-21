#!/usr/bin/env python3
"""Pack original FfH2 civilization flag alpha art from an extracted pak0.fpk ZIP.

Requires Pillow: `python3 -m pip install Pillow`
Usage: `python3 tools/pack_original_civ_emblems.py /path/to/assets.zip`
Optional: `--output-root /tmp/pack-test` (defaults to repository root).

The Civ IV team-color .dds files have WHITE RGB with alpha indicating the actual
faction symbol. Calabim and Illians use inverse alpha; Elohim embeds two opaque
horizontal strips. All three cases need fixes before packing for Unciv.
"""
from pathlib import Path
from PIL import Image, ImageOps
import argparse
import io
import zipfile

MAP = {
    'Amurites':'amurites', 'Balseraphs':'balseraphs', 'Bannor':'bannor',
    'Calabim':'calabim', 'Clan of Embers':'clanofembers', 'Doviello':'doviello',
    'Elohim':'elohim', 'Grigori':'grigori', 'Hippus':'hippus',
    'Illians':'illians', 'Khazad':'khazad', 'Kuriotates':'kuriotates',
    'Lanun':'lanun', 'Ljosalfar':'ljosalfar', 'Luchuirp':'luchuirp',
    'Malakim':'malakim', 'Sheaim':'sheaim', 'Sidar':'sidar',
    'Svartalfar':'svartalfar'
}
PAGE_WIDTH, PAGE_HEIGHT = 1024, 512
CELL, GAP, MARGIN, COLUMNS = 128, 8, 4, 7

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('assets_zip',type=Path,help='ZIP containing art/interface/teamcolor/*.dds')
    parser.add_argument('--output-root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    root=args.output_root
    image_folder=root/'Images.Emblems'/'NationIcons'
    image_folder.mkdir(parents=True,exist_ok=True)
    page=Image.new('RGBA',(PAGE_WIDTH,PAGE_HEIGHT),(0,0,0,0))
    atlas=['','emblems.png',f'size: {PAGE_WIDTH}, {PAGE_HEIGHT}',
           'format: RGBA8888', 'filter: MipMapLinearLinear, MipMapLinearLinear',
           'repeat: none']
    with zipfile.ZipFile(args.assets_zip) as archive:
        for i, (nation, key) in enumerate(sorted(MAP.items())):
            path=f'art/interface/teamcolor/{key}flag.dds'
            with Image.open(io.BytesIO(archive.read(path))) as source:
                image=source.convert('RGBA')
            if image.size!=(128,128):
                raise ValueError(f'{path}: expected 128x128, found {image.size}')
            alpha=image.getchannel('A')
            if key in ('calabim','illians'):
                alpha=alpha.point(lambda a:255-a)
            if key=='elohim':
                px=alpha.load()
                for y in (*range(16),*range(112,128)):
                    for x in range(128):
                        px[x,y]=0
            alpha=alpha.point(lambda a:0 if a<=4 else a)
            symbol=Image.new('RGBA',(128,128),(255,255,255,0))
            symbol.putalpha(alpha)
            bounds=symbol.getbbox()
            if bounds is None: raise ValueError(f'{path}: no symbol remained')
            cropped=symbol.crop(bounds)
            fitted=ImageOps.contain(cropped,(120,120),method=Image.Resampling.LANCZOS)
            packed=Image.new('RGBA',(CELL,CELL),(255,255,255,0))
            packed.alpha_composite(fitted,((CELL-fitted.width)//2,(CELL-fitted.height)//2))
            packed.save(image_folder/(nation+'.png'),optimize=True)
            x=MARGIN+(i%COLUMNS)*(CELL+GAP)
            y=MARGIN+(i//COLUMNS)*(CELL+GAP)
            assert x+CELL<=PAGE_WIDTH and y+CELL<=PAGE_HEIGHT
            page.alpha_composite(packed,(x,y))
            atlas.extend([f'NationIcons/{nation}','  rotate: false',f'  xy: {x}, {y}',
                          f'  size: {CELL}, {CELL}',f'  orig: {CELL}, {CELL}',
                          '  offset: 0, 0','  index: -1'])
    page.save(root/'emblems.png',optimize=True)
    (root/'emblems.atlas').write_text('\n'.join(atlas)+'\n',encoding='utf-8')
    print(f'Packed {len(MAP)} transparent nation symbols into emblems.png / emblems.atlas')

if __name__=='__main__':
    main()
