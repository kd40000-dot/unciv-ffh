#!/usr/bin/env python3
"""Fail CI if any portrait is absent from the runtime atlas or atlas is malformed."""
import json
import re
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT/"docs/data/emm-leader-portraits.json").read_text(encoding="utf-8"))
expect = {f'LeaderIcons/{e["leaderName"]}' for e in manifest["entries"]}
assert len(expect) == 19
assert json.loads((ROOT/"Atlases.json").read_text(encoding="utf-8")) == ["game"]

atlas = (ROOT/"game.atlas").read_text(encoding="utf-8")
lines = atlas.splitlines()
assert lines[1:6] == ["game.png", "size: 1024, 1024", "format: RGBA8888",
                       "filter: MipMapLinearLinear, MipMapLinearLinear", "repeat: none"]
names = re.findall(r"^LeaderIcons/(.+)$", atlas, flags=re.MULTILINE)
assert len(names) == 19 and {f"LeaderIcons/{n}" for n in names} == expect
assert len(set(names)) == 19
rects = []
for name in names:
    pattern = re.compile(
        r"^LeaderIcons/" + re.escape(name) +
        r"\n  rotate: false\n  xy: (\d+), (\d+)\n  size: (\d+), (\d+)"
        r"\n  orig: (\d+), (\d+)\n  offset: 0, 0\n  index: -1$",
        re.MULTILINE)
    found = pattern.search(atlas)
    assert found, name
    x,y,w,h,origw,origh = map(int, found.groups())
    assert w == h == origw == origh == 160
    assert 0 <= x and 0 <= y and x+w <= 1024 and y+h <= 1024
    rects.append((x,y,w,h))
for i,(x,y,w,h) in enumerate(rects):
    for xx,yy,ww,hh in rects[i+1:]:
        assert x+w <= xx or xx+ww <= x or y+h <= yy or yy+hh <= y, "Overlapping images"

png = (ROOT/"game.png").read_bytes()
assert png[:8] == b"\x89PNG\r\n\x1a\n"
cursor, header, ended = 8, None, False
while cursor < len(png):
    assert cursor + 12 <= len(png)
    length = struct.unpack_from(">I",png,cursor)[0]
    typ = png[cursor+4:cursor+8]
    data_end = cursor+8+length
    assert data_end+4 <= len(png)
    assert (zlib.crc32(png[cursor+4:data_end])&0xffffffff)==struct.unpack_from(">I",png,data_end)[0], typ
    if typ == b"IHDR":
        header=struct.unpack_from(">IIBBBBB",png,cursor+8)
    if typ == b"IEND":
        assert data_end+4 == len(png)
        ended=True
        break
    cursor=data_end+4
assert ended and header == (1024,1024,8,6,0,0,0), header
print(f"OK: packed atlas exists and contains {len(names)} unique correctly sized leader images")
