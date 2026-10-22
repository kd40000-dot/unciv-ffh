# Open fidelity gaps — living audit

Last audited: 2026-10-22. Target: ExtraModMod Continued at `60b0ec3740083162aaab7bf8491761a54a65a610`.

**Scope:** Work already introduced or partially converted in this Unciv port. This is a *live backlog of differences*, not a claim that unlisted source systems are finished. Update an entry only after source comparison, engine validation and (where applicable) in-game testing. Status: **Missing**, **Proxy**, **Partial**, **Needs QA**, **Cosmetic**. Source records are catalogued in `docs/data/`; see also `docs/compatibility.md`.

## P0 — Core gameplay and correctness

| ID | Touched system | Remaining deviation / unfinished work | Status | Definition of done |
| --- | --- | --- | --- | --- |
| H01 | City health | Actual health/unhealthiness, population effects, terrain/resource/building contributions, Expansive trait and a player-visible health UI absent. Aqueduct/Herbalist/Infirmary Food bonuses are placeholders, **not health**. | Proxy | Functionally test health calculations, population growth and original building/trait effects; replace proxies |
| B01 | Ordinary buildings | Monument/Theatre culture, Inn/Harbor gold, Lighthouse food and several training-XP values are provisional, not source-exact. Specialists, domain-production, trade routes and other effects remain. | Proxy | Source-audit every building field and custom effect; replace invented yields and test |
| B02 | Maintenance/economy | Courthouse +2 Gold does not equal EMM -40% city maintenance; Forum -50%, Lanun Harbor -10%, Taverns +10% maintenance unimplemented. Civ IV commerce slider absent. | Proxy | Compatible maintenance/economic model with source-tested values |
| B03 | Faction buildings | Six faction replacements now preserve basic proxy effects from their ordinary buildings (Reliquary Culture, Forum Gold, Lanun Harbor Gold/coastal requirement, Arena and Sculptors Studio training XP). These are not original special abilities. Warrens has a +100% Sword/Scout/Archery/Mounted production proxy (not duplicate units; eligibility incomplete), Arena arena mechanics, Grigori Tavern/Forum specialization, Lanun trade economy, Luchuirp construct mechanics, Reliquary religion and other faction-specific effects remain unfinished. | Missing/Partial | Source-derived distinctive effects working in game |
| C01 | Metal equipment | 28 Sword-unit bonuses are rounded percentage proxies for fixed +1/+2/+4; eligibility incomplete; bonuses tied dynamically to resources instead of outfitting; no tier-specific equipment promotions or Rust/refit. Metal Weaponry is an eligibility marker only. | Proxy | Correct eligible-unit list, mutually exclusive equip states, visible accurate tier, original interactions |
| C02 | Combat mechanics | First strikes, collateral damage, withdrawal, typed damage, resistances, healing modifiers, immunity, siege specifics and battle formulas only partly mapped. | Partial | Source-backed test matrix versus EMM rules |
| C03 | Promotions | 32 Unciv promotions versus 305 EMM source promotions; many missing. Promotion prerequisites (especially AND/OR and tech requirements), racial effects, free grants and XP/level mechanics not source-exact. | Partial | Full compatible promotion inventory and legal advancement paths |
| C04 | Unit upgrades | 102 of 356 source unit records implemented; 112 locally valid upgrade edges but 14 source links to missing classes deferred, and class restrictions/upgrade costs need playtesting. | Partial | Full relevant chains and valid nation substitutions |
| R01 | Resource availability | 16 of 68 resource types; generation/distribution approximate. Thirteen `requiredResource` units use Unciv stockpile-style costs rather than EMM nonconsuming access gates; alternative resource OR requirements mostly absent. | Proxy | Source-faithful unit requirements and resource economy |
| M01 | Magic | Mage/Wizard/Archmage self-heal action verified in game but not an EMM spell. No mana nodes, mana spheres, spell prerequisites, casting rules, summons, durations or resistance. | Partial | Actual mana-linked spells and functional caster progression |
| M02 | Caster progression | Adept→Mage→Archmage exists; required levels (Mage 4, Archmage 6), channeling behavior, experience and availability restrictions are not faithful. | Partial | Tested caster rank and spell acquisition gates |

## P1 — Civilization identity, religion and world rules

| ID | Touched system | Remaining deviation / unfinished work | Status | Definition of done |
| --- | --- | --- | --- | --- |
| N01 | Leader traits | Arcane/Spiritual only grant Mobility I, lacking Potency/Favored; Organized civic upkeep, Expansive health, Raiders Commando/first strike, Barbarian alliance, Adaptive, Insane, Summoner incomplete. | Partial | Each active leader trait verified against EMM |
| N02 | Palaces | Nineteen faction palaces have approximate 4 Science + 4 Gold instead of adjustable 8 Commerce, and lack mana grants and scripted effects. | Proxy | Proper economics and faction-specific bonuses |
| N03 | Starting units/races | Starting rosters tested, but initial racial promotions, source-specific unit starts, later-era starts and placement rules need verification. | Partial | Full start-scenario test matrix |
| N04 | Khazad Vaults | Seven treasury-per-city tiers tested; vault buildings/status labels are not physically changed. Edge cases/long games remain. | Proxy/Needs QA | Matching user-visible states and extensive turn tests |
| N05 | Lanun Pirate Cove | Placement and basic yields tested; 10/20-turn Pirate Harbor/Port evolution, spatial exclusion and exact commerce/defense/pillage mechanics missing. | Proxy | Source-consistent progression and spacing |
| N06 | Raiding / Doviello | Hippus/Svartalfar double pillage gold and Doviello -10% science tested; enemy-road Commando, first strikes and barbarian diplomacy absent. | Partial | Complete trait behavior |
| N07 | Religions and alignment | Religious names/tech routes have partial scaffolding but religion founding/spread, priesthood, temples, holy cities, alignments and conversion mechanics absent. | Missing | Playable religion/faith system |
| N08 | Heroes / world spells | Lucian starting hero exists without full unique mechanics. Hero roster and nation world spells missing. | Partial | Source-consistent hero limitations and world spells |
| W01 | World systems | Armageddon Counter, infernal/Mercurian arrival, lairs, events, wilderness, terrain transformation and victory conditions largely missing or rudimentary. | Missing/Proxy | End-to-end event and victory scenarios |
| W02 | Civics / city economy | Civics, health, specialists, maintenance and FfH happiness model not reproduced. | Missing | Valid civic choices and source-derived city accounting |
| T01 | Technology | 82 researchable techs and layout present; 11 OR prerequisites approximated; special nonresearchable techs, source restrictions and related effects incomplete. | Partial | Accurate unlock and prereq graph |
| A01 | AI and balance | No verified multi-turn AI campaign, difficulty balance, complete game or victory regression. | Needs QA | Reproducible automated and Android long-game tests |

## P2 — Player experience and presentation

| ID | Touched system | Remaining deviation / unfinished work | Status | Definition of done |
| --- | --- | --- | --- | --- |
| P01 | Technology artwork | Square FFH icon art currently displayed in circular Unciv slots, with some distortion/alignment issues; user explicitly deferred this. | Cosmetic | Circular-safe art, correct scale and centering |
| P02 | Civilization emblems | Current icon presentation accepted but a few source art/cropping details may need polish; do not prioritize. | Cosmetic | Final visual pass |
| P03 | Unit/building visuals | Many original sprites and specialized promotions/spell icons not yet imported. | Partial | Source-consistent visual coverage |
| P04 | Civilopedia | 304 entries load, but some prose is generic, incomplete or not source-specific; explanations must track actual implemented effects and disclose proxies. | Partial | Complete, accurate, useful descriptions |
| P05 | Diplomacy | 133 original lore-inspired leader strings included; first contact verified; remaining triggers and exact source correspondence not established. | Needs QA | Test all dialogue contexts and document intentional original prose |

## Rules for future work
1. Every milestone should reference one or more open IDs, update their statuses and add new gaps discovered.
2. **Gameplay verified** does not mean **source faithful**; preserve those as distinct labels.
3. Never close health (H01) because Food proxies work, nor equipment (C01) because Metal Weaponry tooltip works.
4. Do not call a numerical JSON check an in-game test. Make a checkpoint before disruptive changes.
5. Prefer updating this ledger and `docs/compatibility.md` in the same commit as gameplay changes.
