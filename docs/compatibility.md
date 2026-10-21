# Compatibility ledger

Reference EMM Continued commit: `60b0ec3740083162aaab7bf8491761a54a65a610`.

| Mechanic | Status | Details |
| --- | --- | --- |
| All normal EMM civilizations and leaders | Implemented, untested | 19 normally playable civilizations, exact city lists and source colors; 2 event-spawn factions deferred |
| Complete researchable technology tree | Implemented, engine-validated | 82 EMM technologies, source costs and rows/columns; 11 OR prerequisites approximated; 2 column-era exceptions, 2 special nonresearchable techs inventoried |
| Source-derived units and buildings | Partial, untested | 100 units and 50 buildings; 63 faction upgrade routes mapped from source, 14 missing-class routes deferred, 1 civ-prohibited route omitted |
| Resources, improvements and terrain | Approximated | Added Copper, Mithril, Reagents; basic EMM source resource gates; terrain and rates approximate |
| Hero units and world spells | Deferred | 356 total unit records inventoried; nonbuildable/hero entries not ported into gameplay yet |
| Mana nodes, spells, caster progression | Partial, untested | Channeling marker promotions; Adept → Mage → Archmage upgrade; no spells or mana magic |
| Religions and alignment | Not implemented | Later milestone |
| Armageddon Counter | Not implemented | Engine feasibility unknown |
| Lairs and random events | Approximated | Two generic ruins rewards |
| Civics and FfH happiness | Not implemented | Unciv city economy remains |
| AI / long games / victory | Untested | Domination victory included |

Static checks and Unciv command-line `mod-ci` checks completed. Android installation and multi-turn gameplay tests remain pending.

Progression conversion details: [promotions, upgrades and resources](promotions-upgrades-resources.md).
