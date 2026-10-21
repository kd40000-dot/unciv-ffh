#!/usr/bin/env python3
"""Verify that the Unciv technology tree faithfully reflects the pinned EMM XML extraction.

This protects source costs, positions, names, dependency choices and complete coverage.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
source = json.loads((ROOT / "docs/data/emm-technologies.json").read_text(encoding="utf-8"))
tech_columns = json.loads((ROOT / "jsons/Techs.json").read_text(encoding="utf-8"))
eras = json.loads((ROOT / "jsons/Eras.json").read_text(encoding="utf-8"))
assert source["commit"] == "60b0ec3740083162aaab7bf8491761a54a65a610"
records = source["technologies"]
assert len(records) == 84, f"Expected 84 source records, got {len(records)}"
assert len({r["sourceId"] for r in records}) == len(records), "Duplicate XML technology IDs"
source_by_id = {r["sourceId"]: r for r in records}
special = {r["sourceId"] for r in records if r["researchCost"] <= 0 or r["disabled"]}
assert special == {"TECH_NEVER", "TECH_SEAFARING"}, special
normal = [r for r in records if r["sourceId"] not in special]
assert len(normal) == 82
name_by_id = {r["sourceId"]: r["name"] for r in records}
expected_eras = {0: "Ancient era", 1: "Ancient era",
                 2: "Classical era", 3: "Classical era", 4: "Classical era",
                 5: "Medieval era", 6: "Medieval era", 7: "Medieval era",
                 8: "Medieval era"}
actual_eras = {e["name"] for e in eras}
assert actual_eras == {"Ancient era", "Classical era", "Medieval era"}
columns_by_number = {c["columnNumber"]: c for c in tech_columns}
assert set(columns_by_number) == set(range(9)), "Expected exactly nine source-layout columns"
flat = {}
for c in tech_columns:
    assert c["era"] == expected_eras[c["columnNumber"]], (c["columnNumber"], c["era"])
    for t in c["techs"]:
        assert t["name"] not in flat, "Duplicate technology " + t["name"]
        flat[t["name"]] = (c, t)
assert len(flat) == len(normal), f"Expected {len(normal)} researchable technologies; found {len(flat)}"
assert set(flat) == {r["name"] for r in normal}, "Researchable technology name set differs from source"

for record in normal:
    col, t = flat[record["name"]]
    assert col["columnNumber"] == record["gridX"] - 1, record["sourceId"]
    assert t["row"] == record["gridY"], record["sourceId"]
    assert t["cost"] == record["researchCost"], record["sourceId"]
    assert record["andPrerequisites"] or record["orPrerequisites"] or t.get("prerequisites", []) == [], record["sourceId"]
    chosen = record["andPrerequisites"] + record["orPrerequisites"][:1]
    expected = list(dict.fromkeys(name_by_id[p] for p in chosen))
    assert set(t.get("prerequisites", [])) == set(expected), (record["sourceId"], expected, t.get("prerequisites", []))
    if record["repeatable"]:
        assert "Can be continually researched" in t.get("uniques", []), record["sourceId"]
    for pre in t.get("prerequisites", []):
        assert pre in flat, f"{t['name']} requires missing {pre}"

pending = set(flat)
visited = set()
while pending:
    ready = {t for t in pending if set(flat[t][1].get("prerequisites", [])) <= visited}
    assert ready, f"Unreachable / cyclic technology prerequisites: {sorted(pending)}"
    visited.update(ready)
    pending.difference_update(ready)

multiple_or = sum(len(r["orPrerequisites"]) > 1 for r in normal)
era_exceptions = sum(r["sourceEra"] != "ERA_" + expected_eras[r["gridX"] - 1].split()[0].upper() for r in normal)
assert multiple_or == 11, multiple_or
assert era_exceptions == 2, era_exceptions
print(f"OK: {len(records)} EMM techs inventoried, {len(flat)} researchable, "
      f"{len(special)} special, {multiple_or} documented OR approximations, "
      f"{era_exceptions} era exceptions; exact costs, positions, and all dependencies verified.")
