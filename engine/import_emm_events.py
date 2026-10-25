#!/usr/bin/env python3
"""Extract EMM Civ4 random-event triggers and options into an auditable catalog.

Usage:
  python3 engine/import_emm_events.py <CIV4EventTriggerInfos.xml> <CIV4EventInfos.xml> <output.json>

This imports SOURCE DATA, not executable Python callbacks; unsupported handlers
must be ported individually. Keep the pinned EMM sources unmodified.
"""
import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def value(node, tag, default=None):
    child = node.find(tag)
    if child is None or child.text is None:
        return default
    return child.text.strip()


def entries(root, tag):
    return root.iter(tag)


def parse_trigger(node):
    result = {
        "sourceId": value(node, "Type"),
        "weight": int(value(node, "iWeight", "0")),
        "gamesActivePercent": int(value(node, "iPercentGamesActive", "100")),
        "minimumPopulation": int(value(node, "iMinPopulation", "0")),
        "recurring": value(node, "bRecurring", "0") == "1",
        "pickCity": value(node, "bPickCity", "0") == "1",
        "worldCounterMinimum": int(value(node, "iPrereqGlobalCounter", "0")),
        "requiredBuildings": [b.text.strip() for b in node.findall("BuildingsRequired/BuildingClass") if b.text],
        "requiredReligions": [b.text.strip() for b in node.findall("ReligionsRequired/ReligionType") if b.text],
        "minimumReligions": int(value(node, "iNumReligions", "0")),
        "options": [x.text.strip() for x in node.findall("Events/Event") if x.text],
        "status": "needs-engine-review",
    }
    return result


def parse_option(node):
    return {
        "sourceId": value(node, "Type"),
        "description": value(node, "Description"),
        "help": value(node, "Help"),
        "aiValue": int(value(node, "iAIValue", "0")),
        "gold": int(value(node, "iGold", "0")),
        "revoltTurns": int(value(node, "iRevoltTurns", "0")),
        "hurryAnger": int(value(node, "iHurryAnger", "0")),
        "pythonRequirement": value(node, "PythonCanDo"),
        "pythonEffect": value(node, "PythonCallback"),
        "status": "needs-engine-review",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("triggers", type=Path)
    parser.add_argument("options", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    trigger_root = ET.parse(args.triggers).getroot()
    option_root = ET.parse(args.options).getroot()
    triggers = [parse_trigger(n) for n in entries(trigger_root, "EventTriggerInfo")]
    options = [parse_option(n) for n in entries(option_root, "EventInfo")]
    ids = {o["sourceId"] for o in options}
    missing = [(t["sourceId"], e) for t in triggers for e in t["options"] if e not in ids]
    if missing:
        raise ValueError(f"Trigger options missing from source XML: {missing[:10]}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps({"triggers": triggers, "options": options}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"Inventoried {len(triggers)} EMM triggers and {len(options)} EMM options")


if __name__ == "__main__":
    main()
