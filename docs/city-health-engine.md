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

### Diseased combat transmission (2026-10-26)

The pinned EMM `PROMOTION_DISEASED` has `PromotionCombatApply=PROMOTION_DISEASED`; `PROMOTION_IMMUNE_DISEASE` lists Disease and Plagued as blocked incoming promotions. The engine combat hook now attempts to add Diseased to a surviving defender when an attacking Diseased unit also survives and the defender is neither immune nor already diseased/plagued. It is guarded to the EMM ruleset, leaving base Unciv unaffected.

**Not yet faithful or player tested:** reciprocal defensive combat infection may be required by EMM's C++ implementation; exact applicability to nonliving targets, cure spells (including Healing Salve and Cure Disease), the process of granting Immune to Disease, and disease from lairs/events. The spell source shows that Healing Salve removes Diseased, Plagued, Poisoned and Withered from the caster, but this is not yet exposed as an in-game action. Do not mark these as complete.

### 2026-10-26 — Direct engine support for cures and Armageddon thresholds

Our Unciv fork is now intentionally **engine-modified**: preserving vanilla engine compatibility is not a constraint. New `UnitActionType.EmmCureDisease` exposes a **Medic II** cure action to remove Diseased/Plagued from co-located allied units; the mod currently supplies a preliminary Medic I → Medic II chain for Disciples so this can be tested, but the remaining EMM Medic bonuses and precise spell conditions are not ported.

The engine's serialized `GameInfo.emmArmageddonCounter` and event flags track a global 0–100 counter. `changeEmmArmageddon(delta)` dispatches Blight at crossing 30 and Pestilence at crossing 35, applying source-based city sickness formulas to cities. The trigger methods are real, but **source-accurate contributions to the global counter are not yet connected**, so the counter ordinarily remains zero. Event unit Death damage is not implemented. The dispatcher therefore is functional infrastructure rather than an automatically occurring EMM Armageddon loop. The source Blight/Pestilence callbacks are in `python/entrypoints/CvRandomEventInterface.py`, and the global counter effects have further source locations in `python/CvEventManager.py` and `CvGameCoreDLL`.

**Next acceptance tests**: select a Disciple with Medic II sharing a tile with Diseased/Plagued units and verify Cure Disease removes the statuses; test save/reload of `emmArmageddonCounter` and the city sickness counter; test crossing 29→30 and 34→35 using a development entry point, and verify thresholds only dispatch once. The initial event hook still lacks a player-facing Armageddon meter, living-only unit damage, and the actual AC-generating events.

### AC acceptance entry point

The EMM engine now shows `Armageddon: N / 100` on the city screen and supports the developer console command `game emm-armageddon <delta>` to change the serialized AC for controlled tests. Test crossing 29 → 30 and 34 → 35 and then save/load to confirm the one-shot event flags. This is not automatic source-derived AC progression; EMM counter-changing gameplay events still need wiring.

### Source-based AC changes reachable during ordinary play (2026-10-26)

Pinned EMM `XML/Gameinfo/CIV4ReligionInfo.xml` defines `iGlobalCounterFound=5` and `iGlobalCounterSpread=1` for Ashen Veil, and `iGlobalCounterFound=3` for Octopus Overlords. `python/CvEventManager.py` links Ashen Veil to **Corruption of Spirit** and Octopus Overlords to **Message from the Deep**. These exact founding and spreading values are captured in `docs/data/emm-armageddon-sources.json` and wired to EMM tech-research completion in the patched engine. Only the **first** founding of each religion in a game grants founding AC; state survives save/load. The initial Ashen Veil founding also establishes the religion in the founding city.

A playable, EMM-source-mapped **Disciple of the Ashen Veil** (unit source `UNIT_DISCIPLE_THE_ASHEN_VEIL`, cost 60, attack 3, movement 1) is buildable after Corruption of Spirit. When inside a city center which has not yet received the Veil, it has a **Spread the Ashen Veil** action: consume the disciple, mark that city as reached, and add exactly +1 AC. City reach records persist across saves and prevent repeated point farming in an already-converted city. This is a **temporary dedicated spread mechanism** in place of EMM's larger Civ IV religion system. It does not give the city full religion-specific buildings, income, political preferences, conversion pressure, or normal Civ IV AI conversion yet. It also currently requires manual player spread; it is not the original passive or AI religious propagation system.

With enough distinct conversions, these are **normal gameplay actions**, not debug-only AC changes. Crossing 30/35 invokes the existing Blight/Pestilence city effects. **This is not proof of the complete global catastrophe system**: player tests, original death-damage event effects, more AC sources (alignment-based elimination, religion conflicts, spells/events, Necrototem) and native religion/missionary mechanics remain outstanding. No unsupported automatic per-turn Armageddon increase has been introduced.

### 2026-10-26 — Expanded EMM Armageddon sources

The pinned source audit found additional AC changes and implemented them without adding generic per-turn increases:

- **Leader-alignment elimination:** EMM `python/CvEventManager.py:onSetPlayerAlive` gives **+5** for defeated Good civilizations and **−5** for defeated Evil civilizations, only from AD 5 onward. The selected default alignments for all 19 playable leaders were extracted directly from `XML/Civilizations/CIV4LeaderHeadInfos.xml` into `docs/data/emm-leader-alignments.json`. The modified Unciv civilization destruction hook applies these effects once per eliminated civilization, using saved deduplication. Dynamic religion/civic-driven alignment changes still need porting.
- **Order–Veil religious conflict:** The source `CvEventManager.py:onReligionSpread` tests a 35% incoming-religion victory when the Order enters a Veil city or vice versa, except holy cities. It can remove a religion, reduce population by one and change AC by **−1** for an Order victory or **+1** for a Veil victory. Interim buildable Disciples of the Order and Ashen Veil expose the conversion route; the complete Civ IV religion system is not yet present.
- **Terrain/spells:** Pinned `CvSpellInterface.py:spellSanctify` removes ruins/graveyards and reduces AC by **1**; `spellRobGrave` consumes a graveyard and increases AC by **1**. Life I units can access Sanctify on the corresponding improved tile; military units can trigger an interim Rob Grave action. EMM grave-loot rolls, original exact spell prerequisite logic and graveyard generation remain deferred. Destroying a **Necrototem** permanently through pillaging reduces AC by **2**, from `CvEventManager.py:onImprovementDestroyed`. Source improvements are declared but generation remains pending.
- **52 EMM event choices:** All nonzero `iGlobalCounter` values were extracted from `XML/Events/CIV4EventInfos.xml` into `docs/data/emm-armageddon-event-choices.json`, and registered through `GameInfo.applyEmmArmageddonEventChoice(id)`. This API does **not** autonomously trigger any random event. Prerequisite conditions, choice UI, random event scheduling, and companion effects must be implemented before declaring these events present during normal play.
- **Still open:** Peace/Seven Pines halving of AC, Flare Entropy/Life Node callbacks, Aeron/Sirona sign callbacks, special Mercurian Gela (−10) scenario event, other C++ counter changes, dynamic alignment, full religious pressure, AI conversions, and original Blight/Pestilence unit Death damage.

**Verification:** Static ruleset and Android compilation pass; the new source-specific scenarios have not yet been player-verified. Do not describe the 52-event registry as 52 playable events.

### 2026-10-26 — Additional Armageddon counter sources: Peace and random-event callbacks

- **Corlindale Peace:** pinned EMM `XML/Units/CIV4SpellInfos.xml:SPELL_PEACE` requires `UNITCLASS_CORLINDALE`, sacrifice of the caster, and `CvSpellInterface.spellPeace` ends the caster's wars before reducing the global counter by its integer half. We have added the source-based Elohim hero Corlindale (Fanaticism; 300 cost, 0 attack, 2 movement) and a playable engine Peace unit action guarded by an active war. This is a genuine selectable counter source, contingent on the mod and Android engine build, but still awaiting player testing.
- **Seven Pines:** `SPELL_PEACE_SEVEN_PINES` also halves the counter after making peace, but is guarded by the original Seven Pines unique improvement, plot activation and one-use rule. Its matching improvement generation and special plot state are **not yet implemented**. The shared halving function exists but does not falsely make Seven Pines available anywhere.
- **Four random-event callbacks:** pinned `CvRandomEventInterface.py` supplies `doFlareEntropyNode +2`, `doFlareLifeNode -2`, `doSignAeron +3`, and `doSignSirona -3` AC. Their values are now registered in the engine's `applyEmmArmageddonEventCallback`, recorded in `docs/data/emm-armageddon-event-callbacks.json`. This is an API, **not** automatic random-event generation. The Entropy/Life callbacks' original adjacent-tile plot-counter effects also remain pending.
- **Still missing for complete Armageddon fidelity:** all original event trigger prerequisites, world-event scheduling, player choices, unported C++ sources, dynamic alignment, Seven Pines activation, and original unit Death damage from Blight/Pestilence. Do not count a registered effect as player-tested or as a playable event.

### EMM random events — complete source extraction, runtime still incomplete (2026-10-26)

`docs/data/emm-armageddon-event-triggers.json` is extracted directly from pinned `XML/Events/CIV4EventTriggerInfos.xml` and `CIV4EventInfos.xml`, with **23 triggers, all their choice IDs, the 52 counter-affecting options, trigger prerequisites and other XML effect fields**. The permanent CI regression `tools/verify_emm_armageddon_events.py` checks the exact records and expressly rejects mistaking a counter delta for a complete event implementation. For example **Demonic Tome 1** grants technology progress beyond AC +5, **Holy Child 2** changes gold, happiness and health beyond AC −10, and **Witch 1** changes city health and happiness beyond AC +2. A fidelity implementation must preserve eligibility (population, AC threshold, terrain/feature/resource/improvement, tech/building, civilization, PythonCanDo), scheduling/recurrence, genuine player choices, **all** choice effects and Python callbacks, and serialization of resolved/pending events. These events are still not scheduled in game and their effects are not dispatched as finished actions. No artificial random counter drift was introduced.

### 2026-10-26 — First persisted EMM event runtime slice

The health engine patch now adds serialized `GameInfo.emmResolvedEventTriggers`, `emmPendingEvents`, and `emmLastEventRollTurn`, a once-per-world-turn `emmScheduleRandomEvents()` call, and `emmResolveRandomEvent(civID, choice)`. The first **three** eligible event families are Witch (population 3+, safe `EVENT_WITCH_2`, AC −1), Holy Child (AC ≥10, city population 3+, safe `EVENT_HOLY_CHILD_1`, AC −5), and Demonic Tome (AC ≥10 and Writing, safe `EVENT_DEMONIC_TOME_2`, AC −5). A preliminary **1% per eligible civilization-world-turn** roll is explicitly provisional and NOT a source-faithful EMM scheduler. AI civilizations resolve the safe choice automatically; a human receives a notification and can resolve with developer console `game emm-event EVENT_WITCH_2` (or the corresponding pending safe source choice). Completed event/civ pairs do not repeat. **No player choice popup yet.** 

The other 20 triggers and their additional options are source-inventoried but **NOT automatically executable**; they require all source eligibility conditions, corresponding effects, and callback implementations. The current runtime is framework groundwork, not the requested full event engine. The full 23-trigger registry remains in `docs/data/emm-armageddon-event-triggers.json`. Static source validation passes, Android gameplay acceptance pending.

### 2026-10-26 — Native event decisions and XML-based catalog

The event engine now compiles the **23 extracted EMM triggers into `EmmEventCatalog.kt`** with XML weights, per-game active percentages, AC thresholds, city/terrain/resource/building/unit criteria, Python eligibility callback names, recurrence flags and all choice identifiers. The catalog is future-ready; unsupported predicates and effects are **not** automatically treated as eligible.

Supported gameplay triggers remain **Witch**, **Holy Child**, and **Demonic Tome**. Eligible events now use the original XML era `iEventChancePerTurn = 4` (documented in `docs/data/emm-event-era-chances.json`), original trigger weights (all three are 400), and percent-games-active values instead of the provisional 1%/uniform selection. This is **not proof of exact Civ IV random draw order/game-speed modifiers or global event-frequency fidelity**.

Human event choices now appear as a **native modal Unciv event dialog** (using `AlertType.Event`); saved pending state and individual city targets survive saves. Choices supported without omitted side effects include Witch 2 (AC -1), Holy Child 1 (AC -5), Demonic Tome 2 (AC -5), and **Holy Child 3** (source XML: 25 gold spent, two population sacrificed in selected city, AC +10). The dialog only shows the latter when the selected city has at least population 3 and the civ has at least 25 gold. AI players continue to resolve the known-safe choices. Debug console resolution remains as a fallback.

**Still not a full EMM event engine**: the other 20 event families are source-catalogued but disabled until source-faithful eligibility, callbacks, unit/terrain/health/happiness effects and selection paths exist. Complete human choice sets, AI decision weighting, rules for repeatable events, and full simulation tests remain open.

### 2026-10-26 — Seven active EMM random-event families

The engine event scheduler now supports **7 of the 23** catalogued EMM Armageddon random-event families. Four newly wired triggers honor their source XML criteria: **Shrine of Camulos** needs a city of population 3+ with a Training Yard (and has a source 10% games-active rate), **Iron Orb** requires 75 treasury and a Library, **Strange Adept** requires a Mage Guild, and **Necro-Cannibalism** requires Armageddon 65+, a city of population 5+, and source-selected evil leader alignment for its selected choice. The player sees corresponding native choice dialogs. Camulos 1 adds +1 AC, Necro-Cannibalism 2 adds +3 AC; Iron Orb 1 and Strange Adept 1 are XML no-effect refusals. Other choices remain gated because their health, building-yield, Python callback, promotion or unit-spawn consequences aren't complete. **Dynamic alignment changes are not yet honored** for Necro-Cannibalism; only source-selected starting alignment is covered. This is a constrained playable expansion, **not** full event-system fidelity. In-game validation remains outstanding.

### 2026-10-26 — Reusable source-backed event numeric effects

The engine now generates `EmmEventEffects.kt` from the pinned `docs/data/emm-armageddon-event-triggers.json`, admitting only choices whose other XML fields are fully covered by **gold, population, permanent city health, permanent city happiness, and Armageddon-counter adjustments**. The generic resolver first checks the player's treasury and the selected city's remaining population; it then applies each permitted numeric effect, updates the affected city's statistics, and records resolution. Existing bespoke Holy Child 3 numeric handling was replaced by the shared pipeline.

Newly enabled choices: **Witch 1** (+1 permanent city happiness, −3 permanent city health, +2 AC); **Holy Child 2** (−50 gold, +1 permanent city happiness, +1 permanent city health, −10 AC). These are drawn from the pinned XML, not invented. `City.emmEventHealth` and `City.emmEventHappiness` serialize and are included in computed city health and happiness; other event effects still needing promotions, units, tile modifications, dynamic alignment, religion, Python callbacks, or diplomatic effects remain gated. The generic effect registry's presence does **not** imply all catalogued choices have matching runtime eligibility or are clickable.

Compilation and Android CI verification pending for this milestone; gameplay acceptance not yet recorded.

### 2026-10-26 — EMM event buildings and city-unhappiness effects

The shared EMM event-effect handler now supports **Iron Orb 2**, preserving its pinned source XML effect: **−75 civilization gold, +2 permanent Library research in the affected city, and +2 Armageddon Counter**. The event must occur in a city with a Library, and the +2 science remains conditional on that city retaining its Library. The modifier is serialized in `City.emmEventLibraryScience`, cloned with city state, displayed in the city research breakdown, and recomputed when city statistics change. Iron Orb 1 (refuse) remains available. The original event-specific library building modifier is modeled as a city-scoped bonus conditioned on the Library, pending more precise per-building serialization.

**Sobs** is the eighth enabled family: AC ≥10, an eligible city population ≥3, and original Sobs 1 choice giving **−1 permanent local happiness**, represented by existing `emmEventHappiness`. Other Sobs choices needing Spirit Mana and Infernal civilization/commerce effects remain gated. The optional Iron Orb research choice requires an eligible Library city and at least 75 gold. Native dialogs, human resolution and AI's safe refusal still work through the common event queue. Android in-game testing remains outstanding.
