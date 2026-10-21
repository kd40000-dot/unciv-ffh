# Compatibility ledger

Reference EMM Continued commit: `60b0ec3740083162aaab7bf8491761a54a65a610`.

| Mechanic | Status | Details |
| --- | --- | --- |
| All normal EMM civilizations and leaders | Implemented, untested | 19 normal civilizations, exact city lists/colors and Ancient-era starting rosters; 2 event-spawn factions deferred |
| Complete researchable technology tree | Implemented, engine-validated | 82 EMM technologies, source costs and rows/columns; 11 OR prerequisites approximated; 2 column-era exceptions, 2 special nonresearchable techs inventoried |
| Source-derived units and buildings | Partial, untested | 102 units and 69 buildings; 63 faction upgrade routes mapped from source, 14 missing-class routes deferred, 1 civ-prohibited route omitted |
| Resources, improvements and terrain | Approximated | Added Copper, Mithril, Reagents; basic EMM source resource gates; terrain and rates approximate |
| Hero units and world spells | Partial, untested | Lucian added as Doviello's starting hero; hero powers and world spells still deferred |
| Mana nodes, spells, caster progression | Partial, untested | Channeling marker promotions; Adept → Mage → Archmage upgrade; no spells or mana magic |
| Religions and alignment | Not implemented | Later milestone |
| Armageddon Counter | Not implemented | Engine feasibility unknown |
| Lairs and random events | Approximated | Two generic ruins rewards |
| Civics and FfH happiness | Not implemented | Unciv city economy remains |
| AI / long games / victory | Untested | Domination victory included |

Static source checks have been performed; the official Unciv `mod-ci` result has not been independently confirmed for the latest commit. The user has verified the starting rosters, faction palaces and earlier leader effects on Android. Raider pillage income and Doviello Science have also been user-tested and accepted as verified for now. Multi-turn AI/regression games remain unverified.

Progression conversion details: [promotions, upgrades and resources](promotions-upgrades-resources.md).

### Leader and palace effects (October 21, 2026)

All 19 normal EMM civilization palaces have source-derived Production, Happiness and costs; the original 8 flexible Commerce is approximated as +4 Science and +4 Gold because Unciv does not have Civ IV's commerce slider. Source-linked native trait effects now include Financial, Creative, Ingenuity and expanded Aggressive. Arcane and Spiritual are partially mapped through Mobility I; Organized's civic upkeep, Expansive's health, Raider's special promotions, Adaptive, Barbarian, Summoner and Insane remain deferred. See [the source and limitation ledger](leader-palace-fidelity.md).

### Raiding and barbarian economics — October 21, 2026

Hippus and Svartalfar receive double Gold from improvements pillaged (source Raiders +100% pillage Gold; native Unciv `100% Yield from pillaging tiles`), while Doviello receives -10% Science from the Barbarian trait. Enemy-road Commando behavior, free first strikes and barbarian alliances are not native equivalents and remain deferred. See [economic trait coverage](economic-traits.md). The user confirmed the palace and earlier leader effects, and on October 21, 2026 reported that both corrected Raider pillage income and Doviello Science appear to work as expected. Treat the economic effects as gameplay-verified provisionally; the user will report any later issues.

### Economic percentage regression (October 21, 2026)

Native Unciv defines `Float.toPercent()` as `1 + value/100`; therefore `100% Yield from pillaging tiles` correctly grants +100% Raider Gold (2× loot). A previously committed `200%` bonus instead produced 3× loot. The engine-derived correction and sample numeric expectations are included in [economic regression protocol](economic-test-protocol.md) and checked in `tools/verify_economic_traits.py`. Doviello's -10% Science correctly scales to 90% of the city's unmodified Science.

### Lanun Pirate Cove milestone — October 21, 2026

The Lanun Workboat can now place a **Pirate Cove** on an unoccupied, un-improved, resource-free Coast tile owned by Lanun and next to land; it is consumed by the action. The Cove preserves the source +2 commerce through a +1 Science/+1 Gold fixed split, +10% defense and source 10 pillage Gold as Unciv's approximate loot. The source **Pirate Harbor/Port automatic maturation** (10 and 20 turns) and the **5×5 cove-spacing exclusion** are not supported natively and are explicitly deferred. The user tested the Pirate Cove action and reported it works on October 21, 2026. Consider first-stage Cove placement gameplay-verified; any later issues will be reported. See [Lanun Pirate Cove QA](lanun-pirate-cove.md).

### Khazad dynamic Dwarven Vaults — October 21, 2026

Seven original EMM Vault stages now change with **floor(treasury Gold / number of owned cities)**. Khazad receive source Happiness (-2 / -1 / 0 / +1 / +2 / +2 / +3 per city) and Production (0 / 0 / 0 / 0 / +10% / +25% / +40% per city) using mutually exclusive native Unciv Countables expression conditionals. All 7 stage thresholds match the pinned EMM source. The original vault **buildings and status labels are not physically swapped into cities**: these are dynamic nation bonuses instead. The user reports the prescribed Khazad Vault tests produced the expected results on October 21, 2026, including dynamic treasury-per-city behavior and tier-dependent Happiness and Production. Treat the tested behavior as **gameplay-verified**; exhaustive edge cases, long games and future engine changes are not yet verified. See [the Vault mechanic and QA](khazad-vaults.md).
