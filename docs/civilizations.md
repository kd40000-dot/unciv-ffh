# Complete playable EMM civilizations — initial conversion

Source: [ExtraModMod Continued `60b0ec3740083162aaab7bf8491761a54a65a610`](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610).

## Included
- **19** normal source-playable civilizations, authentic ordered city-name lists and their EMM faction colors.
- Actual EMM leader selection: one per Unciv nation; all leader IDs and trait sets are in [the source inventory](data/emm-civilizations.json).
- **50** new unique faction units and **10** new faction buildings with supported base classes; **100** units and **50** buildings overall.
- **37** faction unit/building class bans where their source class default exists in this ruleset.
- EMM starting technologies via `Starts with [tech]` except nonresearchable Seafaring for Lanun.

## Leader traits and races
Aggressive: free Combat I on trained melee/mounted/recon units. Charismatic: +1 Happiness per city and 25% less XP per promotion. Creative: +2 Culture per city. Industrious: +50% wonder Production. Philosophical: +100% Great Person production. Ingenuity: -50% Gold upgrade costs.

Other traits are named for identification but mechanically incomplete.

**Clan of Embers:** Orc. **Ljosalfar:** Elf. **Khazad and Luchuirp:** Dwarf (hill movement approximation). **Svartalfar:** Dark Elf (forest movement and combat approximation). These promotions are granted to trained military land units, not necessarily initial starting units.

## Important incomplete mechanics
**Infernal** and **Mercurians** are recorded as EMM source civilizations with `bPlayable=0` and `bAIPlayable=0`; they require event-based arrival, so neither is offered as a normal starting nation.

EMM source starting units are recorded but not reproduced precisely, because this Unciv mod uses shared era starting units. This particularly affects Khazad, Ljosalfar, Doviello and Malakim.

Lanun starts with source-only special `TECH_SEAFARING`, which remains unavailable in our regular research tree, so the source starting bonus is deferred rather than replaced with Fishing.

Faction palace variants, unique spells, alignment, religion, civics, leader personality and several unique-unit effects need future work. Most EMM leader traits are not yet executable equivalents.

## Checks
CI verifies source data, source-derived unit stats and costs, technology references, nation names, starting techs, race grants, unique replacements and Unciv mod-ci output. Android playtesting is still outstanding.
