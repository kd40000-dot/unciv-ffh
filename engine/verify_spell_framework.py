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

assert len(spells) >= 21 and len({x["name"] for x in spells}) == len(spells)
valid_targets = {"SELF", "FRIENDLY", "ENEMY"}
valid_effects = {"STATUS", "HEAL", "DAMAGE", "DAMAGE_STATUS", "SUMMON", "CLEANSE"}
for spell in spells:
    name = spell["name"]
    assert spell["sourceId"].startswith("SPELL_"), name
    assert spell.get("target", "SELF") in valid_targets, name
    assert spell["effect"] in valid_effects, name
    assert spell.get("radius", 0) >= 0, name
    assert spell.get("maxCastsPerTurn", 1) >= 1, name
    assert spell.get("damageLimit", 100) in range(101), name
    assert spell.get("maxActivePerCaster", 0) >= 0, name
    assert any(
        u.startswith(f"Can cast EMM spell [{name}]")
        for promotion in promotions.values()
        for u in promotion.get("uniques", [])
    ), f"No native cast action registered for {name}"
    if spell["effect"] in {"STATUS", "DAMAGE_STATUS"}:
        assert spell["status"] in promotions, name
        assert spell["duration"] == -1 or spell["duration"] >= 1, name
    if spell["effect"] == "CLEANSE":
        assert spell.get("removeStatuses"), name
        assert len(set(spell["removeStatuses"])) == len(spell["removeStatuses"]), name
        assert not any(not status.strip() for status in spell["removeStatuses"]), name
        assert all(status in promotions for status in spell["removeStatuses"]), name
    if spell["effect"] == "SUMMON":
        assert spell["summonUnit"] in units, name
        assert spell.get("summonDuration", 0) >= 0, name
    if spell["effect"] in {"DAMAGE", "DAMAGE_STATUS"}:
        assert spell.get("damageLimit", 100) in range(101), name
    if spell["effect"] in {"HEAL", "DAMAGE", "DAMAGE_STATUS"}:
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
assert by_name["Snowfall"]["amount"] == 40 and by_name["Snowfall"]["damageLimit"] == 70
assert by_name["Wither"]["amount"] == 10 and by_name["Wither"]["damageLimit"] == 40
assert by_name["Maelstrom"]["damageType"] == "LIGHTNING"
assert by_name["Snowfall"]["damageType"] == "COLD"
assert by_name["Wither"]["damageType"] == "DEATH"
for name in ("Courage", "Wither", "Regeneration", "Stoneskin", "Loyalty", "Flaming Arrows"):
    assert by_name[name]["duration"] == -1, name
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

# Check recipient-based Enchanted Blade does not regress to the old caster aura.
blade = by_name["Enchanted Blade"]
assert blade["sourceId"] == "SPELL_ENCHANTED_BLADE"
assert blade["effect"] == "STATUS" and blade["target"] == "FRIENDLY"
assert blade["radius"] == 1 and blade["duration"] == -1
assert blade["eligibleUnitTypes"] == ["Sword"]
assert blade["removeStatus"] == "Rusted (Spell)"
assert "[+20]% Strength" in promotions["Enchanted Blade (Spell)"]["uniques"]
assert any(u.startswith("Can cast EMM spell [Enchanted Blade]") for u in promotions["Enchantment I"]["uniques"])
assert not any("Enchanted Blade Aura" in u for u in promotions["Enchantment I"]["uniques"])


rust = by_name["Rust"]
assert rust["sourceId"] == "SPELL_RUST"
assert rust["effect"] == "STATUS" and rust["target"] == "ENEMY"
assert rust["radius"] == 1 and rust["duration"] == -1
assert rust["eligibleUnitTypes"] == ["Sword"]
assert rust["removeStatus"] == "Enchanted Blade (Spell)"
assert "[-10]% Strength" in promotions["Rusted (Spell)"]["uniques"]
assert any(u.startswith("Can cast EMM spell [Rust]") for u in promotions["Entropy I"]["uniques"])
assert not any("gains the [Rusted (Spell)] status" in u for u in promotions["Entropy I"]["uniques"])

dispel = by_name["Dispel Magic"]
assert dispel["sourceId"] == "SPELL_DISPEL_MAGIC"
assert dispel["effect"] == "CLEANSE" and dispel["target"] == "FRIENDLY"
assert dispel["radius"] == 1
assert set(dispel["removeStatuses"]) == {"Withered (Spell)", "Rusted (Spell)"}
assert any(u.startswith("Can cast EMM spell [Dispel Magic]") for u in promotions["Metamagic II"]["uniques"])
print("EMM framework registry valid:", len(spells), "spells; all effects/references and source-derived Maelstrom values verified")
