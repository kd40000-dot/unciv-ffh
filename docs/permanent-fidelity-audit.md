# EMM → Unciv permanent gameplay fidelity audit

**Baseline:** 2026-10-26. **Target:** [ExtraModMod Continued](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610) at `60b0ec3740083162aaab7bf8491761a54a65a610`.

**Canonical data:** [25-system fidelity-scorecard.json](data/fidelity-scorecard.json). This page is the human-readable governance and history document; the JSON supplies the exact scores, evidence, remaining differences and source-file starting points for each system.

## Baseline scorecard

| ID | EMM system | Fidelity estimate |
|---|---|---:|
| F01 | Civilization-specific mechanics | 25% |
| F02 | Magic and mana | 15% |
| F03 | Religions | 5% |
| F04 | Alignment | 0% |
| F05 | Heroes and world units | 10% |
| F06 | World spells | 0% |
| F07 | Civics and government | 0% |
| F08 | Combat system | 30% |
| F09 | Promotions and experience | 20% |
| F10 | Equipment and weapon metals | 20% |
| F11 | Summoning and transformations | 5% |
| F12 | Stealth and covert operations | 5% |
| F13 | City health and disease | 35% |
| F14 | Happiness and war weariness | 15% |
| F15 | City economy and maintenance | 25% |
| F16 | Population, specialists and slavery | 15% |
| F17 | Culture and territory | 30% |
| F18 | Resources and improvements | 35% |
| F19 | Armageddon Counter | 0% |
| F20 | Hell terrain and transformation | 5% |
| F21 | Wilderness and barbarian factions | 5% |
| F22 | Lairs, dungeons and exploration | 5% |
| F23 | Diplomacy, councils and vassalage | 10% |
| F24 | Advanced tactics, forts and revolutions | 5% |
| F25 | Victory conditions | 10% |
| | **Equal-weight mean (historic baseline snapshot)** | **12.0%** |

**Correction:** The earlier conversational ~14% overall estimate was an arithmetic error. The exact simple average of its 25 proposed percentages is 11.8%, which is the immutable initial baseline before the October 26 health prototype; current estimate is 12.9%.

## Evidence standards and definitions

- **Missing:** the required EMM gameplay behavior is not present; cosmetic names, descriptions or JSON stubs do not count.
- **Early:** small functional slices or substantial proxies, far from a faithful system.
- **Partial:** significant working mechanics, but incomplete roster, formulas, timing or interactions.
- **Needs QA:** implementation appears present but lacks specific in-game confirmation. This is a verification flag, not proof of correctness.
- **Faithful:** source-defined mechanic, inputs, output, limitations, lifecycle and AI path verified to match EMM within explicitly disclosed and justified deviations.
- **In-game confirmed:** only an explicit player test or reproducible game execution, with date, build and expected/observed result; a CI pass is **not** gameplay confirmation.
- **Source paths** in the JSON are an audit search map to the pinned EMM tree, not assertions that every listed path was independently checked field-by-field. For formulas and script behavior, inspect referenced EMM XML **and Python/C++** and add exact symbol/line/commit details on the relevant implementation change.
- **Percent** is an evidence-backed but subjective estimate of EMM behavioral fidelity, **not** a count of source XML entries or engineering hours. Give major behavior more weight than scaffolding. Never increase it merely because code was written.
- **Scope:** these 25 mechanics exclude traditional BtS espionage, artwork and audio; these are a **gameplay** scorecard, not total-project completion. EMM stealth/covert rules remain in scope.
- When older living notes conflict with newer feature documentation, record the conflict. The JSON references the most relevant local documentation; stale historical notes must not be silently treated as current.

## Mandatory completion protocol for every gameplay task

1. Before touching code, identify impacted F01–F25 systems and inspect their current score, source paths, confirmed tests and `remainingDifferences`. Cite the pinned EMM XML/Python/C++ definition for the task.
2. Implement in the mod/engine; check mod loading, formulas, AI usage, and unintended regressions. List intentional deviations; distinguish proxies clearly.
3. In **the same change as the gameplay implementation**, update affected objects in `docs/data/fidelity-scorecard.json`: `status`, `percent` (only with justification), `portEvidence`, `gameplayConfirmed` (only for actual tests), `remainingDifferences`, `verification`, `lastReviewed`, and `updatedBy`.
4. Recalculate the 25-system equal-weight average using `python3 scripts/check_fidelity_audit.py` or `python3 scripts/check_fidelity_audit.py --summary`. Update this page's **Current scorecard** snapshot in the same commit when any score changes; do not erase baseline rows.
5. Add a one-paragraph dated entry to the history below identifying commit/PR, affected systems, old → new scores, evidence, tests performed, failed/untested cases, and new gaps.
6. For substantial features include an Android acceptance checklist; record **tested** vs **needs test** separately.
7. Do not close an item without testing all required input/output and lifecycle edge cases. Unverified edge cases remain gaps even when the UI appears correct.

CI rejects gameplay-file changes without an updated audit data file when the workflow can see the triggering commit. CI also verifies all 25 rows, unique IDs, 0–100 bounds, required fields and documentation synchronization.

## Current scorecard

The current scores are those in [fidelity-scorecard.json](data/fidelity-scorecard.json); current implementation-only estimate is **15.12% equal-weight**. On each score-changing task, regenerate the table with `python3 scripts/check_fidelity_audit.py --summary` and paste the output here, preserving the baseline above.

## Current scoring policy — implementation completeness (2026-10-26)

**Current equal-weight implementation estimate: 15.0%.** The individual percentage
scores rate the breadth and source fidelity of implemented gameplay behavior,
without discounting the score simply because the player has not yet tested it
in-game. Compile/static results and user-tested outcomes are retained as
separate evidence fields rather than blended into the fidelity percentage.

This corrects F19 Armageddon Counter **0% → 30%**: the original entry was stale
after persisted AC, counter sources, threshold dispatch and the reusable
source-derived event engine were implemented. It does not imply that full EMM
Armageddon conditions, events, Death damage or Hell terrain are present.
F13 health/disease remains **35%**: the recently committed provisional epidemic
damage patcher is not a fully integrated typed Death damage implementation.

**Development policy:** Defer interactive gameplay QA until health and its
closely related disease/Armageddon systems are implemented as close to 100%
source completeness as feasible. Maintain automated consistency checks and
compilation throughout development. Player testing neither contributes to
nor reduces these implementation-only percentage estimates.

### 2026-10-27 — Cumulative implementation fidelity reassessment

- **F08 combat: 30% → 32%.** The engine now has a promotion-derived typed resistance registry and an actual HP application API using EMM's double-roll calculation. This is direct damage only; combat-wide typed strength and exact defensive context are not yet ported.
- **F13 health/disease: 35% → 40%.** Earlier milestones introduced disease transmission/cures, epidemic city counters, Blight/Pestilence typed Death damage applied to real units, a dynamic EMM living-status counter, nine nonliving racial promotions, eight innate unit mappings, and an Infernal default-race creation hook.
- Blight and Pestilence damage RNG streams are now separately keyed, avoiding duplicate rolls when both thresholds trigger on the same turn.
- **Overall 25-system equal-weight mean: 14.4% → 14.68%**, rounded **14.7%**.
- This is a source-implementation estimate only. Latest Android compilation and gameplay acceptance are not established, so no verified-runtime claims are made. Missing mechanics and approximate damage inputs remain explicit.

### 2026-10-27 — Typed defensive-strength source integration

- **F08 combat: 32% → 35%; F13 health/disease: 40% → 42%.** The typed damage adapter now imports original EMM base defensive strength for **299** units and typed combat components for **96** units and **14** promotions, folding those into damage-resistance context for applicable unit names.
- Added pinned EMM reference JSON, a generator post-patch, Android build workflow integration and idempotent source-mapping regression checks. Separated Blight/Pestilence RNG streams and restored epidemic patch idempotence.
- **Overall 25-system average: 14.68% → 14.88%**, rounded **14.9%**. This is implementation coverage, not gameplay verification.
- **Still incomplete:** Exact EMM level persistence, city defensive modifier, promotions changing base defense, full typed combat in normal battles and source-mapped spells/terrain damage. CI compilation and player testing not confirmed for this generated patch.

### 2026-10-27 — Typed damage reaches ordinary combat strength

- **F08 combat 35% → 38%.** An EMM-scoped generated `BattleDamage.kt` hook now scales both attacker and defender combat strengths using source unit/promotion typed components and current opponent typed resistances. This changes ordinary combat's strength ratio rather than applying erroneous additional direct HP damage.
- CI gained an idempotent fixture regression for both directions; the Android engine build workflow applies the new patch after generating the typed resistance and defense libraries.
- **Overall equal-weight average: 14.88% → 15.0%.** No player verification was counted. Android compilation remains unconfirmed for this integration.
- This is not exact Civ IV battle resolution: Unciv ratio/damage math, unit-name matching, exact base modifiers, level and city defense remain pending.

### 2026-10-27 — Persistent EMM levels and city-defense formula

- Added a serialized `MapUnit.emmLevel` field updated when a genuine purchased promotion is gained and copied during unit stat/upgrade copying, instead of equating level to all innate and free promotions. Typed direct damage now reads this field.
- Ported `CvCity::getTotalDefense` and `CvCity::getDefenseModifier` exact arithmetic to a reusable Kotlin kernel, including additive building/natural/owner/ranged defense, occupation suppression, and bombardment damage scaling.
- Added idempotent source-transform tests and Android build generation steps for both systems.
- F08 **38→39**, F09 **20→21**, F13 **42→43**; equal-weight **15.00→15.12%**. Implementation-only estimates. No gameplay verification performed.
- Remaining barriers to *full* source fidelity: many EMM level assignment/upgrade pathways, city natural-defense culture levels, building/owner/ranged defenses, bombardment state, city capture/occupation data, and actual runtime city-defense binding into `EmmTypedDamage`. Successful generated Android compilation has not yet been independently confirmed.

## Change history

### 2026-10-26 — Initial audit
- Baseline `F01`–`F25` created from the October 26 gameplay audit and repository's source ledgers.
- Approximately 11.8% average estimated fidelity (25 systems, equal weights).
- Confirmed user tests have been recorded separately from static validations; all other mechanics remain unverified until explicit test evidence.
- Historic gaps in `docs/open-fidelity-gaps.md` may be stale relative to the October 23–24 magic documentation. Do not interpret historic omissions as current.


### 2026-10-26 — Health engine prototype (F13)
- F13 **0% → 5%**; equal-weight **11.8% → 12.0%**. Added `tools/patch_unciv_health.py` and automated APK build workflow.
- Net unhealthiness contributes a negative Food entry to city stats **before growth modifiers**, while ordinary Unciv rulesets remain untouched by the ruleset guard.
- **Status: unverified / provisional**. Health source values in this prototype (baseline, Aqueduct, Herbalist, Infirmary) are not yet source-checked; no Android playtest, city UI, terrain/resources, Expansive trait or disease. No claim of EMM-equivalent health.
- Existing Food-proxy building bonuses remain and must be removed only as part of a validated migration to the health-enabled engine.

### 2026-10-26 — Source-backed city health expanded (F13)
- F13 **5% → 10%**; equal-weight scorecard **12.0% → 12.2%**. Kotlin engine patch compiles and the city food penalty now includes EMM-derived building, Expansive trait, connected resource (including Life/Creation Mana), fresh-water and feature health; old health building Food proxies are neutralized in this engine.
- Source: pinned EMM health field extraction `docs/data/emm-health-source.json`; engine `tools/patch_unciv_health.py`; test matrix `docs/city-health-engine.md`.
- **No gameplay verification yet.** Difficulty-dependent starting health (currently provisional +2), exact area/feature accounting, disease, proper UI and AI response remain unresolved. APK build status must be checked separately.

### 2026-10-26 — City health display (F13)
- City panel receives a health icon with `healthy/unhealthy` totals and net health; Stats popup receives a source breakdown using the same CityStats calculation as the Food penalty, so the display is not an independent proxy.
- Game-icons.net `Health normal` by sbed is used under CC BY 3.0, with attribution recorded in `docs/city-health-engine.md`.
- F13 **remains at 10%** (overall remains **12.2%**) pending compiled UI build and in-game review. UI does not resolve missing EMM disease and starting health rules.

### 2026-10-26 — Expanded source-faithful health foundations (F13)
- F13 **10% → 12%**; equal-weight gameplay fidelity **12.2% → 12.3%** (rounded).
- Additional pinned EMM `CIV4HandicapInfo.xml` inventory and difficulty starting health (Settler +4, Chieftain +3, others +2); `iGlobalHealth` buildings including Kuriotates Palace; `bNoUnhealthyPopulation` building rules. Reuses existing health totals, detailed city health UI and food penalties.
- **Not yet player tested:** differences at lower difficulty, global health across cities, effects of special buildings. Area health, disease, Blight and richer AI support remain open. Build validation tracked in Actions.

### 2026-10-26 — Signed building health and source checks (F13)
- F13 **12% → 14%**, total gameplay scorecard **12.3% → 12.4%** (rounded). The old adapter incorrectly treated Forge, Dwarven Smithy, Reliquary and Public Baths negative-health source values as subtraction from healthy totals; they now contribute to the unhealthy counter while preserving the correct net-Food effect. Their construction info uses signed icon bonuses, rather than only three hard-coded health buildings.
- Added static EMM-source checks in `tools/verify_emm_health_rules.py` to guard against sign regressions, with the Android workflow executing them.
- **Gameplay verification pending:** city growth, negative building effects, source health contributions, area/global effects, save/reload, disease and Armageddon effects. This percentage is an estimate, not proof of completeness.

### 2026-10-26 — Disease, Blight and Pestilence first source-backed slice (F13)
- F13 **14% → 16%**; overall gameplay scorecard **12.4%** (rounded). The engine now stores a serialized temporary sickness counter in cities, applies its effects as extra unhealthiness, and exposes helper functions implementing EMM Blight/Pestilence sickness formulas.
- EMM source references: `python/entrypoints/CvRandomEventInterface.py` (Blight threshold 30, Pestilence threshold 35) and `XML/Units/CIV4PromotionInfos.xml` (Diseased -30% combat, Plagued -60%). The latter combat strength values are present in the port's promotion data.
- **Not complete or verified in-game:** Blight/Pestilence are not automatically triggered until the Armageddon Counter is implemented, unit damage and disease transmission/cures/immunity remain absent, and Kotlin build plus in-game save/load/decay tests are needed. UI simulation alone is not equivalent to full EMM disease behavior.

#### Disease combat/healing source milestone
- F13 **16% → 17%**; overall gameplay **12.4% → 12.5%** (rounded). From pinned EMM `CIV4PromotionInfos.xml`, added Diseased -30% and Plagued -60% combat penalties to the mod, and implemented their respective -10/-20 healing modifiers in the health engine. Exact XML status definitions are preserved in `docs/data/emm-disease-promotions.json`.
- **Unverified in game:** transmission through combat, immunity, curing, auto-promotion from lairs/events, and the Blight/Pestilence Armageddon triggers all remain incomplete; test APK compile result recorded separately.

#### Disease contact transmission and immunity
- F13 **17% → 18%**; 25-system mean **12.5%** rounded. Combat now has a source-derived Diseased transmission hook, and the promotion manager blocks Diseased and Plagued when Immune to Disease is present; granting immunity also removes existing infections. This does **not** replace the missing curing spell or prove EMM combat infection edge cases.
- Android compilation and gameplay confirmation are tracked separately. Blight/Pestilence remain inactive without a global Armageddon dispatcher.

### 2026-10-26 — Medic II cure and Armageddon threshold dispatch (F13)
- F13 **18% → 20%**, overall equal-weight fidelity **12.5% → 12.6%**. Adds a Cure Disease unit action for Medic II, preliminary Medic I/II ruleset promotion availability, serialized Armageddon Counter 0–100 and one-shot threshold event dispatch of Blight at 30 and Pestilence at 35.
- **Incomplete:** no source-faithful AC increase/decrease triggers are connected, so normal gameplay cannot yet fire the events; no unit Death damage, Healing Salve, exact Cure Disease targeting semantics, full Medic promotion effects or robust gameplay tests. Source EMM references in `docs/city-health-engine.md`.

### 2026-10-26 — First normal-play source-backed AC progression
- F13 **20% → 22%**; 25-system mean **12.6% → 12.7%** rounded. Pinned `XML/Gameinfo/CIV4ReligionInfo.xml`: first founding of Ashen Veil +5 AC, Octopus Overlords +3 AC, spread of Ashen Veil +1 AC per newly reached city. Religion-founding technologies from `python/CvEventManager.py` now generate these deltas when researched. A source-traced buildable Disciple of the Ashen Veil (`UNIT_DISCIPLE_THE_ASHEN_VEIL`, cost 60, strength 3, move 1) can spread the Veil through a normal city-center unit action, granting its source-based AC change.
- **Faithfulness caveat:** the temporary missionary action and serialized religion city flag are not a full EMM religion system. Natural passive spreading, AI missionary use, holy-city rules, religion buildings/civics, and numerous other AC changes are pending. Reaching Blight (30) or Pestilence (35) requires enough genuine research-and-conversion actions; no made-up per-turn counter increases were added.
- Unciv build and validation passing only confirm code/package checks, not successful in-game epidemic trigger testing.

### 2026-10-26 — Expanded source-backed Armageddon counter sources (F13)
- F13 **22% → 26%**, 25-system gameplay average **12.7% → 12.8%** rounded. New engine hooks cover selected leader elimination alignment (+5 Good / −5 Evil, year 5+, once), source Order/Veil conflicts (35% incoming victory; ±1 AC), Life I Sanctify (−1), Rob Grave (+1), and Necrototem permanent destruction (−2). New Order Disciple is source-traced for missionary conflicts.
- 19 leader alignments extracted from pinned `CIV4LeaderHeadInfos.xml`; 52 signed `iGlobalCounter` event-choice values extracted from pinned `CIV4EventInfos.xml`, with a callable API but **not** active source-compatible random events. Reference registry `docs/data/emm-armageddon-sources.json` records what remains unported.
- Android build and full mod validation passed. In-game testing of new spells/religion/elimination cases is still outstanding; automated random-event selection, special source spells and world scenarios require further engine work, and Blight/Pestilence unit Death damage is unfinished. This is not 100% AC fidelity.

### 2026-10-26 — Armageddon Peace and event callback expansion (F13)
- F13 **26% → 27%**; 25-system equal-weight gameplay fidelity **12.8% → 12.9%** rounded. Source-backed Elohim Corlindale unit and its Peace action are now in the engine, using the EMM spell prerequisite, sacrifice, war-ending and integer half-AC effect.
- Four source-derived random-event callbacks now have registered AC deltas: Flare Entropy +2; Flare Life −2; Sign Aeron +3; Sign Sirona −3. **Not automatically triggered.** The 52 EMM event-choice AC delta registry is also still conditional on future event selection/trigger integration.
- Incomplete: Seven Pines peace site, event eligibility/scheduling and side effects, more C++ sources, live player verification of Corlindale and related pathways. Kotlin CI success and Android build are separate gates from gameplay testing.

### 2026-10-26 — EMM native event decision UI and source-derived event catalog (F13)
- F13 **27% → 29%**; the 25-system mean **12.9% → 13.0%** rounded. The engine builds a typed catalog from the 23 pinned EMM Armageddon event triggers, including weighted selection, activation percentage, preconditions, recurrence flags and all choice identifiers. Pinned EMM `CIV4EraInfos.xml` specifies `iEventChancePerTurn=4` across all available eras; the 1% provisional roll was replaced by this source rate for the supported scheduler (not yet full Civ IV RNG/game-speed parity).
- Human players now see a native modal choice dialog for **Witch, Holy Child and Demonic Tome** rather than console-only resolution. **Holy Child 3** now applies its source -25 gold, -2 city population and +10 AC with eligibility checks and a saved target city; other safe choices already present remain available. AI resolves safe choices automatically. A successful Kotlin + Android build verifies compilation only, not full gameplay acceptance.
- **Still incomplete:** 20 of 23 triggers are source-indexed but intentionally disabled; most of the 52 Armageddon-related choices require effects/callbacks/eligibility not yet ported, exact Civ IV random event scheduling and AI decision heuristics differ, and player gameplay tests are pending. This is a substantial event-framework milestone, not completion of the full EMM event system.

### 2026-10-26 — Source-gated Armageddon event family expansion (F13)
- F13 **29% → 31%**, overall equal-weight gameplay fidelity **13.0%** rounded. Added source-gated Shrine of Camulos (+1 AC choice, Training Yard, population 3+, 10% active-games threshold), Necro-Cannibalism (+3 AC evil-aligned choice, AC 65+, population 5+), Iron Orb (75 gold + Library, only original do-nothing refusal currently) and Strange Adept (Mage Guild, original refusal). Native dialogs and AI safe resolutions now cover **7/23** source-inventoried Armageddon random event families.
- The remaining 16 families and other event choices still require faithful consequences, Python conditions and the rest of their gameplay prerequisites; dynamic alignment and full original random-event probability weighting remain limited. A successful Android build confirms compilation but not in-game event dialogs or effects. No unimplemented outcomes have been allowed to apply only their AC deltas.

### 2026-10-26 — Library research event and Sobs (F13)
- **F13 32% → 33%**, overall simple 25-system average **13.08% → 13.12%** (both approximately **13.1%**). **Iron Orb 2** now consumes 75 Gold, adds 2 Armageddon and grants 2 persistent city research from an existing Library, grounded in the source's `BUILDINGCLASS_LIBRARY`, `COMMERCE_RESEARCH` and `iExtraCommerce=2`. This is stored in the city save state and applies while the Library remains. **Sobs 1** is a newly playable eighth Armageddon-related event family at AC ≥10 and city population ≥3, applying −1 persistent local happiness. Target selection now associates Iron Orb with a Library city, rather than an arbitrary population-eligible city.
- **Pending:** original Civ IV building-extra-commerce accounting parity, in-game choice/persistence acceptance, 15 unscheduled families and missing choices requiring plot effects, unit spawning/promotions, XML/Python callbacks, religions, diplomacy and full probability selection.

### 2026-10-26 — EMM unit/promotion/tile event effect milestone (F13)
- F13 **33% → 35%**, 25-category mean **13.1% → 13.2%**. Added shared, validated unit spawning/free promotion application, mapped tile improvement removal, and serialized event-specific selected unit IDs and tile HexCoords. Verified the pinned EMM **War Games** source predicate and event options 1/2, source **Winds from Hell** Windmill destruction, and **Necro-Cannibalism 3** Doviello Warrior-class spawn with Cannibalize (+10 HP after killing a unit, using native Unciv on-kill healing).
- Source-mapped **Windmill** is now buildable after Construction on hills, with base +1 Food/+1 Production/+1 Commerce. The EMM Machinery-dependent additional +1 Production/+1 Commerce and more precise source event unit-aliveness distinctions are not fully ported.
- Corrected `GameInfo.clone()` to deep-copy the Armageddon Counter, one-shot flags and all EMM event pending/resolved state, including city, unit and tile event targets, which the pinned engine's manual clone implementation otherwise silently omitted.
- Playable random-event family count now **10/23**, with restricted, source-aligned choice sets. Device event UI and save/load acceptance remain untested, and unit/tile promotion classes for other event families must still be ported. The source-based checklist and estimates should not be interpreted as 100% EMM fidelity.
