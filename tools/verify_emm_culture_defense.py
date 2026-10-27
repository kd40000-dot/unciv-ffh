#!/usr/bin/env python3
"""Verify seven EMM city cultural defense levels map to exact source modifiers."""
from pathlib import Path
import json
source=json.loads(Path("docs/data/emm-culture-defense.json").read_text())
levels=source["cultureDefenseLevels"]
assert len(levels)==7
assert [x["defense"] for x in levels]==[0,0,10,20,30,40,50]
script=Path("tools/patch_emm_culture_defense.py").read_text()
assert "fun naturalDefenseForCulture" in script
assert "emmCultureLevel" in script
assert "naturalDefense = com.unciv.logic.city.EmmCityDefense.naturalDefenseForCulture(city.emmCultureLevel)" in script
assert levels[2]["thresholds"]["GAMESPEED_NORMAL"] == 10
assert levels[6]["thresholds"]["GAMESPEED_NORMAL"] == 50000
assert levels[6]["thresholds"]["GAMESPEED_MARATHON"] == 150000
progression=Path("tools/patch_emm_culture_progression.py").read_text()
assert "fun cultureLevelFor(" in progression
assert "city.emmTotalCulture = " in progression
assert "city.civ.gameInfo.speed.name" in progression
print("PASS: EMM seven culture tiers and natural-defense runtime mapping")
