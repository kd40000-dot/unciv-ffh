# City health — EMM engine prototype (October 26, 2026)

**Status:** Engine patch committed, Kotlin compilation demonstrated for earlier slices; current full variant needs final build and **Android gameplay QA**. This is not yet a completed or EMM-equivalent health system.

## Authoritative source

Pinned [ExtraModMod Continued commit 60b0ec3](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610).
[Machine-readable XML health audit](data/emm-health-source.json) extracts actual source fields from `XML/Buildings/CIV4BuildingInfos.xml`, `XML/Civilizations/CIV4TraitInfos.xml`, `XML/Terrain/CIV4BonusInfos.xml` and `XML/Terrain/CIV4FeatureInfos.xml`.

## Implemented in the patched Unciv engine

The `tools/patch_unciv_health.py` changes `CityStats.kt`, before growth modifiers. Only rulesets containing both Herbalist and Infirmary activate the new calculation.

For each city:

- Unhealthiness includes **1 per population**, plus source feature penalties at the current city's radius-two map footprint.
- Health includes provisional starting health **2**, direct health of owned buildings, the **Expansive** trait (+3 for Clan of Embers, Kuriotates and Lanun in this mod), each distinct connected source-health resource, +2 for adjacent fresh water and positive feature contributions.
- A city loses **1 Food per net excess unhealthiness**, even if this causes starvation. Balanced or positive health does not add Food.
- The engine removes temporary **+1 Aqueduct, +1 Herbalist and +2 Infirmary Food proxies** when those buildings exist, so they are not double-counted.
- Example source bonuses: Aqueduct **+2**, Herbalist **+1**, Infirmary **+3**; Cattle/Deer/Fish/Sheep/Wheat **+1** each; Creation Mana and Life Mana **+1** each.
- Source feature percentages: Forest **+50%**, Jungle **−25%**, Flood plains **−40%**, with positive and negative components truncated independently to full health points.

The core health effect appears as an `Unhealthiness` negative Food line in Unciv's city stat breakdown. This is **not** a proper Civ IV health-face UI.

## Formula (initial approximation)

```
healthy = 2 [provisional base] + direct_building_health
        + expansive_health + connected_resource_health
        + (2 if fresh water) + floor(sum(positive_feature_percent)/100)
unhealthy = city_population + floor(sum(negative_feature_percent_magnitude)/100)
extra_food_consumption = max(0, unhealthy - healthy)
```

**Important outstanding deviations:** Civ IV/EMM handicap-dependent starting health, Civ IV's exact city-radius geometry (Unciv uses hex radius 2), detailed terrain owner/plot feature rules, health effects of special civics/events and area/global buildings, sanitation/disease/plague states, Blight/Pestilence, proper health UI and AI production priorities, and save/load regression. We have not confirmed that all health resource connections behave like EMM trade networks. Static compilation is not a played-game test.

## Acceptance matrix

1. On a clean EMM game with the **health-enabled APK**, verify the city stats breakdown shows no penalty at low population.
2. Raise population well beyond healthy sources: Food should fall exactly 1 per excess unhealthiness, not Happiness.
3. Construct Aqueduct, Herbalist and Infirmary individually. Each must lower Food loss by its **source health** (2 / 1 / 3), not grant raw Food.
4. Gain/lose Cattle, Fish, Life Mana, Creation Mana and record city Food before/after each. Each unique resource must affect health once regardless of quantity.
5. Compare otherwise identical Bannor vs Expansive Lanun or Clan cities: +3 threshold difference.
6. Compare river vs non-river city (+2), then two Forests (+1), four Jungles (-1), three Flood plains (-1), assuming no other differences.
7. Verify that a healthy city receives no bonus Food and that starvation works when unhealthy.
8. Save/load, capture a city, raze or disconnect resources, and run at least 20 turns of AI city growth.
9. Confirm ordinary stock Unciv rulesets are unaffected.

**Release rule:** Do not elevate the fidelity estimate or remove any gaps as complete until the patched APK is installed and the relevant scenarios are actually confirmed in-game.
