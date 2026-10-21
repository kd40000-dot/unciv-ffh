#!/usr/bin/env python3
"""Verify 19 civilization emblem images, atlas regions, and retained leader portraits."""
import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT/"docs/data/erebus-civilization-emblems.json").read_text())
nations = json.loads((ROOT/"jsons/Nations.json").read_text())
expected = {n["name"] for n in nations if n["name"] != "Barbarians"}
entries = manifest["nations"]
assert len(entries) == len(expected) == 19
assert {e["name"] for e in entries} == expected
assert len({e["output"] for e in entries}) == 19
assert manifest["engineType"] == "NationPortraits"

def png_check(path, target):
    data=path.read_bytes()
    assert data[:8] == bytes.fromhex("89504e470d0a1a0a"), path
    at=8; header=None; end_found=False
    while at < len(data):
        assert at+12 <= len(data), path
        length=struct.unpack_from(">I",data,at)[0]
        kind=data[at+4:at+8]
        next_pos=at+8+length
        assert next_pos+4<=len(data), path
        actual=struct.unpack_from(">I",data,next_pos)[0]
        assert actual == (zlib.crc32(data[at+4:next_pos]) & 0xffffffff), path
        if kind==b"IHDR":
            header=struct.unpack_from(">IIBBBBB",data,at+8)
        if kind==b"IEND":
            end_found=True
            assert next_pos+4 == len(data), path
            break
        at=next_pos+4
    assert end_found and header is not None
    assert header[:4] == (target,target,8,6), (path,header)

for e in entries:
    assert e["output"] == f'Images.Emblems/NationPortraits/{e["name"]}.png'
    png_check(ROOT/e["output"],96)

png_check(ROOT/"emblems.png",512)
atlases=json.loads((ROOT/"Atlases.json").read_text())
assert "game" in atlases and "emblems" in atlases
assert (ROOT/"game.png").exists() and (ROOT/"game.atlas").exists(), "Leader atlas must remain intact"
s=(ROOT/"emblems.atlas").read_text()
assert "emblems.png" in s
assert s.count("NationPortraits/") == 19
for e in entries:
    assert f'NationPortraits/{e["name"]}\n' in s, e["name"]
    assert f'LeaderIcons/{e["name"]}' not in s
print("OK: 19 emblem sprites, source mapping, PNG CRC/dimensions, separate atlas and retained leader atlas")
