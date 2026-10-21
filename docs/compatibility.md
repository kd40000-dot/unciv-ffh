# Compatibility ledger

Reference EMM Continued commit: `60b0ec3740083162aaab7bf8491761a54a65a610`.

| Mechanic | Status | Details |
| --- | --- | --- |
| Four nations, leaders, cities | Implemented, untested | Names and cities sourced from EMM XML |
| Complete researchable technology tree | Implemented, engine-validated | 82 EMM technologies, source costs and rows/columns; 11 OR prerequisites approximated; 2 column-era exceptions, 2 special nonresearchable techs inventoried |
| Source-derived units and buildings | Implemented, untested | 47 buildable unit entries and 40 buildings from EMM source; no invented faction units; tech/cost/combat/movement traced to source |
| Resources, improvements and terrain | Approximated | Initial Unciv terrain scaffold; source-specific bonuses and mana not yet modeled |
| Hero units and world spells | Deferred | 356 total unit records inventoried; nonbuildable/hero entries not ported into gameplay yet |
| Mana nodes, spells, caster progression | Not implemented | Adept has provisional ranged combat only |
| Religions and alignment | Not implemented | Later milestone |
| Armageddon Counter | Not implemented | Engine feasibility unknown |
| Lairs and random events | Approximated | Two generic ruins rewards |
| Civics and FfH happiness | Not implemented | Unciv city economy remains |
| AI / long games / victory | Untested | Domination victory included |

Static checks and Unciv command-line `mod-ci` checks completed. Android installation and multi-turn gameplay tests remain pending.
