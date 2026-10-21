# Fall from Heaven — Unciv

A **standalone Unciv base ruleset prototype**, with **ExtraModMod Continued** as the authoritative target.

## Erebus diplomacy flavor

The **19 playable civilization leaders now have distinct introductions, neutral/hostile greetings, declarations of war, reactions to attacks, defeat lines and trade requests** (133 total lines). These are **new lore-inspired dialogue**, not quoted FfH2/EMM dialogue: the pinned source's accessible diplomacy text contains generic Civilization IV lines, not original custom greetings for these leaders. **First-contact greetings have passed user gameplay testing (October 21, 2026)**; other diplomatic triggers still await verification. Provenance: [dialogue ledger](docs/data/erebus-diplomacy-dialogue.json), [implementation and QA](docs/erebus-diplomacy.md).

## First early-game slice

Includes **19 normally playable EMM civilizations**, the EMM-derived technology tree, **102 units** and **69 buildings**, plus terrain, resources and improvements. This is **not yet a complete port**. Starting rosters, faction palaces, leader traits, Raider pillage income, Doviello Science, and Lanun Pirate Cove functionality within Unciv's supported limitations have received positive user gameplay verification. Khazad Vault Gold-per-city thresholds and bonuses have now also received positive gameplay verification; other systems and long games still need testing. The user will report any economic-trait issues found later.

Install with Unciv → Mods → Download mod from URL:

`https://github.com/kd40000-dot/unciv-ffh`

See [full civilization roster](docs/civilizations.md), [leader traits and palaces](docs/leader-palace-fidelity.md), [economic/raiding traits](docs/economic-traits.md), [economic gameplay test protocol](docs/economic-test-protocol.md), [Lanun Pirate Cove mechanic](docs/lanun-pirate-cove.md), [Khazad Dwarven Vaults](docs/khazad-vaults.md), [source starting units](docs/starting-units.md), [promotions, upgrades and resources](docs/promotions-upgrades-resources.md), [unit and building source conversion](docs/units-and-buildings.md), [complete technology tree](docs/technology-tree.md), [test steps and limitations](docs/first-playable-slice.md), [development plan](docs/implementation-plan.md), and [compatibility ledger](docs/compatibility.md).

Pinned authoritative game source: [EMM Continued](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610).

Old pre-reset implementation remains archived in `archive/pre-reset-2026-10-21` and was **not reused**.
