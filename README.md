# Fall from Heaven — Unciv

A **standalone Unciv base ruleset prototype**, with **ExtraModMod Continued** as the authoritative target.

## Expanded magic source-backed test release (October 24, 2026)

**Safety checkpoint:** [pre-full-magic-2026-10-24](https://github.com/kd40000-dot/unciv-ffh/tree/checkpoint/pre-full-magic-2026-10-24), commit `ae94e78090f2c80363e0856a5ebe2769b91c76e8`.

This release contains **63 sphere-rank promotions** (21 EMM schools × three ranks), **67 sphere-associated spells** represented by native executable actions or carefully documented proxies, 21 pre-existing Mana Node resource conversions, 21 new spell-created units (including Malakim Sand Lion), five city-spell buildings, two dimensional improvements, and five additional EMM faction/unit spell proxies (Burning Blood, Sprint, Whiteout, Spores, Sand Lion). Of the **355** source spell definitions, **288** are non-sphere actions and not all are portable without the missing religion, faction, item, lair, world-spell and custom game-engine subsystems. Existing Arena and Lanun cove actions are already partially ported outside the magic framework.

**Source-based and engine-validated, not gameplay-verified:** GitHub Actions official Unciv `mod-ci` and repository static checks have passed. Android action selection, combat balance, turn duration, unit expiration, city spell persistence, and AI still require the player's in-game tests. EMM units cast temporary summons that disappear automatically; stock Unciv's native unit creation leaves them persistent. Temporary summons therefore have a manual dismiss action but no faithful automatic expiration. Promotion aura and same-tile targeting, direct enemy damage, spell resistance, Great Sage point generation and EMM Python effects may also differ.

Documents: [full 355-source inventory](docs/emm-full-spell-inventory.md), [individual spell Android checklist](docs/magic-spell-by-spell-android-qa.md), [detailed differences and test gates](docs/expanded-magic-differences-and-qa.md), [original mana node instructions](docs/mana-nodes.md).

## Erebus diplomacy flavor

The **19 playable civilization leaders now have distinct introductions, neutral/hostile greetings, declarations of war, reactions to attacks, defeat lines and trade requests** (133 total lines). These are **new lore-inspired dialogue**, not quoted FfH2/EMM dialogue: the pinned source's accessible diplomacy text contains generic Civilization IV lines, not original custom greetings for these leaders. **First-contact greetings have passed user gameplay testing (October 21, 2026)**; other diplomatic triggers still await verification. Provenance: [dialogue ledger](docs/data/erebus-diplomacy-dialogue.json), [implementation and QA](docs/erebus-diplomacy.md).

## Leader portraits — import preparation

**All 19 leader portraits have now been imported from the user's supplied artwork archive** as 256×256 PNGs in `Images/LeaderIcons/`, matching the exact Unciv leader names. See [portrait mappings, source and gameplay QA](docs/original-leader-portraits.md). **Portraits did not appear in the first Android test because the mod lacked packed image atlases; this is now addressed with `game.atlas`/`game.png`. **Verified in Unciv on Android by user (October 21, 2026): portraits display correctly after atlas fix.****

## Civilization emblems — original transparent FfH2 flags

All 19 playable civilizations now use **the original transparent faction symbols** from the `art/interface/teamcolor/*flag.dds` files in the user's extracted `pak0.fpk` (`assets.zip`). These are native `NationIcons`: Unciv draws its standard faction-colored circular background and tints the symbols, without any second disc, square badge or border. The dedicated `emblems.png`/`emblems.atlas` is included in `Atlases.json`, preserving the previously gameplay-verified leader portraits. [Original DDS provenance, exceptions and testing](docs/civilization-emblems.md). **Android gameplay test of this replacement version pending.** The previous cleaned circular-button emblems were gameplay-verified before the original-flag replacement.

## Mana-node foundation (October 23, 2026)

Added Raw Mana map deposits, all **21** EMM sphere Mana resources and improvements, and source-technology-gated **Adept** node construction. Each finished node supplies one sphere Mana resource to the owning empire; sphere rank promotions and spell actions are now under development and Android testing. Node construction/retuning have already been user-tested on Android; spell behavior still requires systematic verification. See [mana-node mechanics and QA](docs/mana-nodes.md).

## First early-game slice

Includes **19 normally playable EMM civilizations**, the EMM-derived technology tree, **124 unit definitions** and **81 buildings** (including spell-created content), plus terrain, resources and improvements. This is **not yet a complete port**. Starting rosters, faction palaces, leader traits, Raider pillage income, Doviello Science, and Lanun Pirate Cove functionality within Unciv's supported limitations have received positive user gameplay verification. Khazad Vault Gold-per-city thresholds and bonuses have now also received positive gameplay verification; other systems and long games still need testing. The user will report any economic-trait issues found later.

Install with Unciv → Mods → Download mod from URL:

`https://github.com/kd40000-dot/unciv-ffh`

See [full civilization roster](docs/civilizations.md), [leader traits and palaces](docs/leader-palace-fidelity.md), [economic/raiding traits](docs/economic-traits.md), [economic gameplay test protocol](docs/economic-test-protocol.md), [Lanun Pirate Cove mechanic](docs/lanun-pirate-cove.md), [Khazad Dwarven Vaults](docs/khazad-vaults.md), [source starting units](docs/starting-units.md), [promotions, upgrades and resources](docs/promotions-upgrades-resources.md), [unit and building source conversion](docs/units-and-buildings.md), [complete technology tree](docs/technology-tree.md), [test steps and limitations](docs/first-playable-slice.md), [development plan](docs/implementation-plan.md), and [compatibility ledger](docs/compatibility.md).

Pinned authoritative game source: [EMM Continued](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610).

Old pre-reset implementation remains archived in `archive/pre-reset-2026-10-21` and was **not reused**.
