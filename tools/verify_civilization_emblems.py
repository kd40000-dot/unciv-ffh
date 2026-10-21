#!/usr/bin/env python3
"""Validate transparent FfH2 nation symbols and Android texture atlas without Pillow."""
import json
import re
import struct
import zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'docs/data/erebus-civilization-emblems.json').read_text(encoding='utf-8'))
nations=json.loads((ROOT/'jsons/Nations.json').read_text(encoding='utf-8'))
expected={n['name'] for n in nations if n['name']!='Barbarians'}
entries=manifest['nations']
assert len(entries)==19 and {e['name'] for e in entries}==expected
assert len({e['output'] for e in entries})==19
assert manifest['engineType']=='NationIcons'
assert manifest['sourceArchive']=='assets.zip (extracted from pak0.fpk)'
assert manifest['outputDimensions']==[128,128]

def read_png(path,width,height):
    png=path.read_bytes()
    assert png.startswith(bytes.fromhex('89504e470d0a1a0a')),path
    at=8;header=None;end=False;has_idat=False
    while at<len(png):
        assert at+12<=len(png),path
        length=struct.unpack_from('>I',png,at)[0]
        typ=png[at+4:at+8]
        end_data=at+8+length
        assert end_data+4<=len(png),path
        crc=struct.unpack_from('>I',png,end_data)[0]
        assert crc==(zlib.crc32(png[at+4:end_data])&0xffffffff),(path,typ)
        if typ==b'IHDR':
            header=struct.unpack_from('>IIBBBBB',png,at+8)
        elif typ==b'IDAT':
            has_idat=True
        elif typ==b'IEND':
            end=True
            assert end_data+4==len(png),path
            break
        at=end_data+4
    assert end and has_idat and header==(width,height,8,6,0,0,0),(path,header)

for entry in entries:
    name=entry['name']
    assert entry['output']==f'Images.Emblems/NationIcons/{name}.png'
    assert entry['originalSourcePath'].endswith('flag.dds')
    assert re.fullmatch(r'[a-f0-9]{64}',entry['sourceSha256'])
    read_png(ROOT/entry['output'],128,128)
    assert not (ROOT/f'Images.Emblems/NationPortraits/{name}.png').exists(),name
read_png(ROOT/'emblems.png',1024,512)

atlas=json.loads((ROOT/'Atlases.json').read_text(encoding='utf-8'))
assert set(atlas)>={'game','emblems'}
assert (ROOT/'game.png').exists() and (ROOT/'game.atlas').exists(), 'Original leader atlas missing'
s=(ROOT/'emblems.atlas').read_text(encoding='utf-8')
assert s.startswith('\nemblems.png\nsize: 1024, 512\nformat: RGBA8888\n')
assert 'NationPortraits/' not in s
regions=re.findall(r'^NationIcons/(.+)$',s,flags=re.MULTILINE)
assert len(regions)==19 and set(regions)==expected
records=[]
for name in regions:
    p=re.compile(r'^NationIcons/'+re.escape(name)+r'\n  rotate: false\n  xy: (\d+), (\d+)\n  size: (\d+), (\d+)\n  orig: (\d+), (\d+)\n  offset: 0, 0\n  index: -1$',re.M)
    m=p.search(s)
    assert m is not None,name
    x,y,w,h,origw,origh=map(int,m.groups())
    assert w==h==origw==origh==128
    assert 0<=x and 0<=y and x+w<=1024 and y+h<=512
    for xx,yy,ww,hh in records:
        assert x+w<=xx or xx+ww<=x or y+h<=yy or yy+hh<=y, name
    records.append((x,y,w,h))
print('OK: 19 original FfH2 transparent NationIcons, no old NationPortraits, valid Android atlas; leader atlas retained')
