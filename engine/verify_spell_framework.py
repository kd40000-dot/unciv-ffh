#!/usr/bin/env python3
"""Fail-fast EMM engine ruleset checks before Kotlin compilation.

Only source-backed metadata and graph consistency are asserted here. This
does NOT establish engine gameplay equivalence or satisfy Android QA.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def entries(filename):
    return json.loads((ROOT / "jsons" / filename).read_text(encoding="utf-8"))

spells = entries("EMMSpells.json")
promotions = {x["name"]: x for x in entries("UnitPromotions.json")}
units = {x["name"]: x for x in entries("Units.json")}

assert spells and len({x["name"] for x in spells}) == len(spells)
valid_targets = {"SELF", "FRIENDLY", "ENEMY"}
valid_effects = {"STATUS", "HEAL", "DAMAGE", "SUMMON"}
for spell in spells:
    name = spell["name"]
    assert spell["sourceId"].startswith("SPELL_"), name
    assert spell.get("target", "SELF") in valid_targets, name
    assert spell["effect"] in valid_effects, name
    assert spell.get("radius", 0) >= 0, name
    assert spell.get("maxCastsPerTurn", 1) >= 1, name
    if spell["effect"] == "STATUS":
        assert spell["status"] in promotions, name
        assert spell["duration"] >= 1, name
    if spell["effect"] == "SUMMON":
        assert spell["summonUnit"] in units, name
        assert spell.get("summonDuration", 0) >= 0, name
    if spell["effect"] in {"HEAL", "DAMAGE"}:
        assert spell["amount"] > 0, name

sources = {
    "Haste": ("Body I", "SPELL_HASTE"),
    "Courage": ("Spirit I", "SPELL_COURAGE"),
    "Maelstrom": ("Air II", "SPELL_MAELSTROM"),
    "Summon Fire Elemental": ("Fire III", "SPELL_SUMMON_FIRE_ELEMENTAL"),
    "Raise Skeleton": ("Death I", "SPELL_RAISE_SKELETON"),
    "Repair": ("Enchantment I", "SPELL_REPAIR"),
}
for spell in spells:
    if spell["name"] not in sources:
        continue
    promotion, source_id = sources[spell["name"]]
    assert spell["sourceId"] == source_id, spell["name"]
    assert any(u.startswith(f"Can cast EMM spell [{spell['name']}]") for u in promotions[promotion]["uniques"]), spell["name"]

by_name = {s["name"]: s for s in spells}
assert by_name["Maelstrom"]["radius"] == 2
assert by_name["Maelstrom"]["amount"] == 15
assert by_name["Maelstrom"]["damageLimit"] == 30
assert by_name["Raise Skeleton"]["summonDuration"] == 0
assert by_name["Raise Skeleton"]["immobileOnCreate"]
assert by_name["Repair"]["amount"] == 20
assert by_name["Repair"]["eligibleUnitTypes"] == ["Siege", "Melee Water", "Civilian Water"]
assert "Golem" in by_name["Repair"]["eligibleNameContains"]
assert by_name["Summon Fire Elemental"]["summonDuration"] > 0
assert promotions["Courage (Spell)"]["uniques"] == ["Not shown on world screen"]
print("EMM framework registry valid:", len(spells), "spells; all effects/references and source-derived Maelstrom values verified")
