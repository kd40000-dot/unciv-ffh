#!/usr/bin/env python3
"""Check the pinned 355-entry EMM source inventory against native action wiring.

A catalog entry does NOT mean a playable spell. Fail if anything is accidentally
reported as native without an executable definition and a promotion grant.
"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
read = lambda p: json.loads((root / p).read_text(encoding="utf-8"))
catalog = read("engine/emm-source-spell-catalog.json")
native = read("jsons/EMMSpells.json")
promotions = read("jsons/UnitPromotions.json")
assert len(catalog) == 355, f"Expected 355 pinned EMM actions; got {len(catalog)}"
ids = [s["sourceId"] for s in catalog]
assert len(ids) == len(set(ids)), "Duplicate EMM IDs"
by_id = {s["sourceId"]: s for s in catalog}
assert len(native) == len({s["sourceId"] for s in native}), "Duplicate native spell IDs"
grants = {
    u.split("Can cast EMM spell [", 1)[1].split("]", 1)[0]
    for p in promotions for u in p.get("uniques", [])
    if u.startswith("Can cast EMM spell [")
}
names = {s["name"] for s in native}
assert grants == names, f"Grant/registry mismatch: only grants={grants-names}; only definitions={names-grants}"
for spell in native:
    sid, name = spell["sourceId"], spell["name"]
    assert sid in by_id, f"Unknown source spell {sid}"
    record = by_id[sid]
    assert record["integration"] == "native-registered", (sid, record["integration"])
    assert record["nativeSpell"] == name, (sid, name)
for record in catalog:
    if record["integration"] == "native-registered":
        assert record["nativeSpell"] in names, record["sourceId"]
    else:
        assert record["integration"] == "requires-engine-review", record["sourceId"]
        assert record["nativeSpell"] is None, record["sourceId"]
print(f"Coverage verified: {len(catalog)} source actions; {len(native)} native-registered; {len(catalog)-len(native)} awaiting native integration")
