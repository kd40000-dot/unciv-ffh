#!/usr/bin/env python3
"""Validate leader-specific Unciv dialogue and explicit source/provenance notes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
read = lambda f: json.loads((ROOT / f).read_text(encoding="utf-8"))
nations = read("jsons/Nations.json")
ledger = read("docs/data/erebus-diplomacy-dialogue.json")
fields = ["introduction", "neutralHello", "hateHello", "declaringWar", "attacked", "defeated", "tradeRequest"]
assert ledger["fields"] == fields
assert ledger["leaderCount"] == 19
assert "NOT verbatim" in ledger["adaptation"]
assert len(ledger["characters"]) == 19
playable = [nation for nation in nations if nation["name"] != "Barbarians"]
assert len(playable) == 19
assert set(ledger["characters"]) == {n["name"] for n in playable}
placeholders = {
    "We greet you in the name of our people.", "Greetings.", "Speak quickly.",
    "Our banners are raised against you.", "You shall pay for this trespass.",
    "Our people will remember.", "Will you consider this exchange?"
}
for nation in playable:
    entry = ledger["characters"][nation["name"]]
    assert entry["leader"] == nation["leaderName"]
    for field in fields:
        line = nation[field]
        assert line == entry[field], (nation["name"], field)
        assert isinstance(line, str) and len(line) >= 12
        assert line not in placeholders, (nation["name"], field)
        assert line == line.strip() and not any(c in line for c in "\n\r<>")
        assert len(line) < 320, (nation["name"], field)

for field in fields:
    assert len({n[field] for n in playable}) == 19, field
print(f"OK: {len(playable)} unique leader dialogue sets and {len(playable)*len(fields)} validated fields")
