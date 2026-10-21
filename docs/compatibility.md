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

Static checks and Unciv command-line `mod-ci` checks completed. Android installation and multi-turn gameplay tests remain pending.

Progression conversion details: [promotions, upgrades and resources](promotions-upgrades-resources.md).

### Leader and palace effects (October 21, 2026)

All 19 normal EMM civilization palaces have source-derived Production, Happiness and costs; the original 8 flexible Commerce is approximated as +4 Science and +4 Gold because Unciv does not have Civ IV's commerce slider. Source-linked native trait effects now include Financial, Creative, Ingenuity and expanded Aggressive. Arcane and Spiritual are partially mapped through Mobility I; Organized's civic upkeep, Expansive's health, Raider's special promotions, Adaptive, Barbarian, Summoner and Insane remain deferred. See [the source and limitation ledger](leader-palace-fidelity.md).

### Raiding and barbarian economics — October 21, 2026

Hippus and Svartalfar receive double Gold from improvements pillaged (source Raiders +100% pillage Gold; native Unciv `200% Yield from pillaging tiles`), while Doviello receives -10% Science from the Barbarian trait. Enemy-road Commando behavior, free first strikes and barbarian alliances are not native equivalents and remain deferred. See [economic trait coverage](economic-traits.md). The user confirmed the prior palace and leader effects in gameplay; these new economics remain to be tested.
