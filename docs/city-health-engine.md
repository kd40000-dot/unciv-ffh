# City health — EMM engine prototype (October 26, 2026)

**Status:** Engine patch committed, Kotlin compilation demonstrated for earlier slices; current full variant needs final build and **Android gameplay QA**. This is not yet a completed or EMM-equivalent health system.

## Authoritative source

Pinned [ExtraModMod Continued commit 60b0ec3](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610).
[Machine-readable XML health audit](data/emm-health-source.json) extracts actual source fields from `XML/Buildings/CIV4BuildingInfos.xml`, `XML/Civilizations/CIV4TraitInfos.xml`, `XML/Terrain/CIV4BonusInfos.xml` and `XML/Terrain/CIV4FeatureInfos.xml`.

## Implemented in the patched Unciv engine

The `tools/patch_unciv_health.py` changes `CityStats.kt`, before growth modifiers. Only rulesets containing both Herbalist and Infirmary activate the new calculation.

For each city:

- Unhealthiness includes **1 per population**, plus source feature penalties at the current city's radius-two map footprint.
- Health includes difficulty-derived starting health (Settler +4, Chieftain +3, other EMM difficulty levels +2), direct health of owned buildings, the **Expansive** trait (+3 for Clan of Embers, Kuriotates and Lanun in this mod), each distinct connected source-health resource, +2 for adjacent fresh water and positive feature contributions.
- A city loses **1 Food per net excess unhealthiness**, even if this causes starvation. Balanced or positive health does not add Food.
- The mod now removes its obsolete **+1 Aqueduct, +1 Herbalist and +2 Infirmary Food proxies directly from Buildings.json**. Their building panels instead state the source health bonus through an explanatory Comment unique.
- Example source bonuses: Aqueduct **+2**, Herbalist **+1**, Infirmary **+3**; Cattle/Deer/Fish/Sheep/Wheat **+1** each; Creation Mana and Life Mana **+1** each.
- Source feature percentages: Forest **+50%**, Jungle **−25%**, Flood plains **−40%**, with positive and negative components truncated independently to full health points.

The core health penalty appears as an `Unhealthiness` negative Food line **only when excess unhealthiness exists**. A healthy city still has no city-level healthy/unhealthy count on the interface; the building descriptions now explain their health values, but a full health display remains unimplemented. The user's 2026-10-26 screenshot documented the obsolete Herbalist +1 Food display before this ruleset fix.

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

## City screen UI and art (2026-10-26)

- The health-enabled Unciv engine exposes its same calculated `healthy / unhealthy` totals in the city information panel beside the **Health normal** icon.
- The Stats popup displays health totals and a health source breakdown: provisional base, buildings, Expansive trait, connected resources, freshwater, healthy/unhealthy map features, and population. The city food penalty uses those exact computed totals.
- **Asset attribution:** `Health normal` by **sbed**, Game-icons.net, **CC BY 3.0** — https://game-icons.net/1x1/sbed/health-normal.html (source SVG retrieved during reproducible build, rendered in the Unciv stat-icon atlas). Attribution and license: https://creativecommons.org/licenses/by/3.0/ .
- Android visual/gameplay QA still required, especially font visibility and city-panel layout on narrow screens. The prototype starting health and Civ4-to-hex feature mapping remain deviations.

### 2026-10-26 follow-up: icon visibility and buildings

Player screenshot confirmed the first health totals (3 healthy / 2 unhealthy) rendered, but the stat atlas lookup returned a **white square**, and Herbalist showed only a textual Comment bonus. The replacement APK loads `Icons/EMMHealth.png` from a bundled Android `ExtraImages` asset rather than an unregistered sprite atlas entry; Herbalist (+1), Aqueduct (+2) and Infirmary (+3) display that same health icon in their selected-construction panels, and outdated Comment bonuses were removed. These visual corrections require player confirmation on the replacement APK; health remains 10% estimated fidelity until further mechanical tests.

### 2026-10-26 — Additional source-based health rules

The source extractor now includes EMM `XML/Gameinfo/CIV4HandicapInfo.xml` and writes its `iHealthBonus` values into `docs/data/emm-health-source.json`. The engine uses the matching in-game difficulty: Settler +4, Chieftain +3 and EMM Warlord/Noble/Prince/Monarch/Emperor/Immortal/Deity +2 (fallback +2 for non-EMM names). Source-defined global city health (`iGlobalHealth`) applies to every city if any of the civilization's cities has the providing building; a Kuriotates Palace grants +1 health empire-wide when present. Source `bNoUnhealthyPopulation` building effect, including Demonic Citizens, removes population-caused unhealthiness in that city when the relevant building is defined and built. This does not remove separate feature unhealthiness.

**Still missing:** correct city landmass/area health (`iAreaHealth`), full modifier interactions, richer source-specific resource and terrain breakdown, disease/Blight, AI valuation, and game verification of these new cases. XML extraction and compilation do not substitute for gameplay tests.

**Additional regression tests:** Compare Settler (+4) to Chieftain (+3) and Prince (+2) on identical cities; test two Kuriotate cities before and after constructing their Palace; verify cities with any `bNoUnhealthyPopulation` effect show no population unhealthiness while retaining negative feature health. Confirm population still consumes its usual Food; this effect eliminates **health penalty**, not basic citizen consumption.

### Area-health follow-up

The engine now reads EMM's iAreaHealth building field and applies area bonuses to same-continent cities. Aquae Sucellus has +1 area health in the pinned EMM XML. The building is not yet available in the current mod, so in-game testing of this rule awaits its port. Compare two cities on one continent and a third on another when testing.

### Disease, Blight, Pestilence — source audit (2026-10-26)

Pinned [EMM `CvRandomEventInterface.py`](https://github.com/bewlay/extramodmod/blob/60b0ec3740083162aaab7bf8491761a54a65a610/python/entrypoints/CvRandomEventInterface.py) defines:

- **Blight**, Armageddon trigger **30**: for non-Infernal cities, a random `0..14` plus population plus bad feature health, minus good feature health and positive building health. A **positive** result increases the city's temporary health penalty counter. Living units also take source-defined Death damage 25.
- **Pestilence**, Armageddon trigger **35**: for non-Infernal cities, random `0..8` plus integer `population/4` minus good building health, adding the **signed** result to the temporary health counter. Living units also take Death damage 25.
- Both events use EMM's Civ IV `changeEspionageHealthCounter`. That identifier refers to a **temporary city health penalty**, not traditional BtS espionage gameplay.

The engine patch adds a **serialized temporary city unhealthiness counter** (including cloning and city-screen/food-penalty calculation), decays it one per city turn, and supplies `EmmCityEpidemics.blight` and `pestilence` event APIs with the documented source formulas. It does **not yet trigger** these events automatically: the Armageddon Counter and event dispatcher have not been ported. It also does not yet apply their **unit Death damage**. This is infrastructure and gameplay behavior for explicitly invoked events, **not** a complete Blight/Pestilence implementation.

Outstanding: disease/plagued unit promotions and combat contagion, spell curing, disease-bearing lairs and random events, unit-type immunities, exact temporary sickness decay, event dispatch (AC 30/35), unit death damage and global Armageddon AI consequences. Never raise the score based on an event that has not been triggered and tested.

### Disease promotions — first engine integration (2026-10-26)

Pinned [EMM disease promotion inventory](data/emm-disease-promotions.json) confirms: Diseased incurs **-30% combat strength and -10 healing** in friendly, neutral and enemy territory, while Plagued incurs **-60% combat strength and -20 healing**. The mod declares these statuses and the patched Unciv engine now subtracts their healing amounts in the unit heal computation. This means the penalties apply **when the promotion is present**. The promotions do not yet spread through combat, apply themselves from random events, or implement immunity/cures. Their saved-unit and in-game interactions have not been accepted by the player yet.

Source-backed city Blight/Pestilence event code exists, but the global Armageddon Counter (30/35 threshold dispatch) is not yet present; no automatic catastrophe is claimed. The latest APK build passes CI but needs gameplay checks of the stats display, sickness persistence and turn decay.
