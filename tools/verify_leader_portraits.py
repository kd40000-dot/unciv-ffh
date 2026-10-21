#!/usr/bin/env python3
"""Validate source mapping and every installed Unciv leader portrait PNG without Pillow."""
import argparse
import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

def verify_png(path):
    data = path.read_bytes()
    assert data.startswith(PNG_MAGIC), f"Invalid PNG header: {path}"
    cursor, header, seen_iend = 8, None, False
    while cursor < len(data):
        assert cursor + 12 <= len(data), f"Truncated PNG: {path}"
        chunk_length = struct.unpack_from(">I", data, cursor)[0]
        chunk_type = data[cursor + 4:cursor + 8]
        start, end = cursor + 8, cursor + 8 + chunk_length
        assert end + 4 <= len(data), f"Truncated PNG chunk: {path}"
        actual_crc = struct.unpack_from(">I", data, end)[0]
        expected_crc = zlib.crc32(data[cursor + 4:end]) & 0xffffffff
        assert actual_crc == expected_crc, f"Corrupt PNG CRC: {path}, {chunk_type!r}"
        if chunk_type == b"IHDR":
            assert header is None and chunk_length == 13, f"Invalid PNG IHDR: {path}"
            header = struct.unpack_from(">IIBBBBB", data, start)
        if chunk_type == b"IEND":
            assert chunk_length == 0, f"Invalid PNG end: {path}"
            seen_iend = True
            assert end + 4 == len(data), f"Trailing PNG data: {path}"
            break
        cursor = end + 4
    assert header is not None and seen_iend, f"Incomplete PNG: {path}"
    width, height, bit_depth, color_type, compression, filtering, interlace = header
    assert width == height == 256, f"Expected 256px square: {path}"
    assert bit_depth == 8 and color_type == 6, f"Expected RGBA PNG: {path}"
    assert compression == filtering == interlace == 0, f"Unsupported PNG encoding: {path}"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-art", action="store_true", help="Fail unless all 19 portrait images are present")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "docs/data/emm-leader-portraits.json").read_text(encoding="utf-8"))
    nations = json.loads((ROOT / "jsons/Nations.json").read_text(encoding="utf-8"))
    playable = {n["name"]: n for n in nations if n["name"] != "Barbarians"}
    entries = manifest["entries"]
    assert manifest["sourceRevision"] == "60b0ec3740083162aaab7bf8491761a54a65a610"
    assert len(entries) == len(playable) == 19
    assert {e["civilization"] for e in entries} == set(playable)
    assert len({e["targetPngPath"] for e in entries}) == 19
    assert len({e["emmPortraitDdsPath"].lower() for e in entries}) == 19
    missing = []
    for entry in entries:
        assert entry["leaderName"] == playable[entry["civilization"]]["leaderName"]
        assert entry["targetPngPath"] == f'Images/LeaderIcons/{entry["leaderName"]}.png'
        assert entry["emmPortraitDdsPath"].lower().endswith(".dds")
        assert entry["emmLeaderArtId"].startswith("ART_DEF_LEADER_")
        path = ROOT / entry["targetPngPath"]
        if path.exists():
            verify_png(path)
        else:
            missing.append(entry["leaderName"])
    print(f"OK: {len(entries)} EMM mappings; {len(entries)-len(missing)} validated 256px RGBA PNG portraits; {len(missing)} missing")
    if missing:
        print("Missing: " + ", ".join(missing))
        if args.require_art:
            raise SystemExit(1)

if __name__ == "__main__":
    main()
