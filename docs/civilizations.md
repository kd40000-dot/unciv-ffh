# Complete playable EMM civilizations — initial conversion

Source: [ExtraModMod Continued `60b0ec3740083162aaab7bf8491761a54a65a610`](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610).

## Included
- **19** normal source-playable civilizations, authentic ordered city-name lists and their EMM faction colors.
- Actual EMM leader selection: one per Unciv nation; all leader IDs and trait sets are in [the source inventory](data/emm-civilizations.json).
- **50** new unique faction units and **10** new faction buildings with supported base classes; **102** units (including Lucian and Lightbringer) and **69** buildings overall.
- **37** faction unit/building class bans where their source class default exists in this ruleset.
- EMM starting technologies via `Starts with [tech]` except nonresearchable Seafaring for Lanun.

## Leader traits and races
Aggressive: free Combat I on trained melee/mounted/recon units. Charismatic: +1 Happiness per city and 25% less XP per promotion. Creative: +2 Culture per city. Industrious: +50% wonder Production. Philosophical: +100% Great Person production. Ingenuity: -50% Gold upgrade costs.

Other traits are named for identification but mechanically incomplete.

**Clan of Embers:** Orc. **Ljosalfar:** Elf. **Khazad and Luchuirp:** Dwarf (hill movement approximation). **Svartalfar:** Dark Elf (forest movement and combat approximation). These promotions are granted to trained military land units, not necessarily initial starting units.

## Important incomplete mechanics
**Infernal** and **Mercurians** are recorded as EMM source civilizations with `bPlayable=0` and `bAIPlayable=0`; they require event-based arrival, so neither is offered as a normal starting nation.

Ancient-era source starting-unit classes/counts now use native one-time nation triggers. Initial racial promotions, special hero powers, later-era starts and map-dependent unit placement still need testing.

Lanun starts with source-only special `TECH_SEAFARING`, which remains unavailable in our regular research tree, so the source starting bonus is deferred rather than replaced with Fishing.

The 19 normal faction palaces now have source-derived production, happiness and a documented approximation of EMM commerce. Arcane and Spiritual traits are still only partly functional; faction mana grants, religions, alignment and scripted civilization mechanics remain deferred.

## Checks
CI verifies source data, source-derived unit stats and costs, technology references, nation names, starting techs, race grants, unique replacements and Unciv mod-ci output. Android playtesting is still outstanding.

### Faction upgrade-chain audit (October 21, 2026)

The 50 added faction units were compared against the pinned EMM unit-class upgrade definitions. **63 source-backed routes** across **31 faction units** now use native Unciv upgrades: the first available destination via `upgradesTo`, additional destinations via `Can upgrade to [unit]`. Destinations use generic class names so Unciv can resolve each faction's own replacement, for example Moroi → Champion (Calabim Vampire) and Centaur Archer → Knight (Kuriotates Centaur Lancer).

Of the source upgrade links, **14** lead to classes absent from this ruleset (notably Immortal, Shadow, Druid, Cannon and religious priest classes). One otherwise present destination is intentionally omitted: Svartalfar Swordsman → Chariot, because the Svartalfar prohibit Chariots. These paths will only be added when their prerequisite units/systems are ported or the source restrictions can be represented. A source unit with no upgrade targets is not given a fictional route.

The civilization verifier now compares every added unit's full destination list with pinned EMM source data and applies class bans. **Gameplay verification remains outstanding**, including confirming faction-replacement resolution for actual upgraded units on Android.

### Other remaining fidelity work

Ancient-era starting units now use the source EMM classes and counts, including Lucian and Lightbringer. Racial effects on initially granted units, hero specials and later-era starts remain incomplete. Palace bonuses, traits and religion/alignment still need work.

## Ancient-era starting rosters

All 19 normal civilizations now have source-defined starting units through Unciv's one-time game-initialization nation triggers, including class-based unique replacements. See [starting-unit conversion and limits](starting-units.md). Android gameplay validation is pending.

## Native trait and palace audit (October 21, 2026)

Native Unciv effects now cover Financial (+25% Gold), Creative (+10% Culture in addition to +2 flat Culture), Ingenuity (+50 starting Gold), and additional Aggressive Combat I categories. Arcane and Spiritual grant Mobility I to newly trained Magic/Disciple units; source Potency and Favored effects remain deferred. All 19 normal palace building variants have source-defined cost 160, +1 Production, +1 Happiness, and an explicitly approximate 4 Science + 4 Gold conversion of the source's 8 flexible commerce. Full details: [leader and palace fidelity ledger](leader-palace-fidelity.md). Android gameplay remains to be tested.

## Economic traits and raiding (October 21, 2026)

Hippus and Svartalfar now receive the +100% pillage Gold element of their Raiders trait using Unciv's `100% Yield from pillaging tiles` multiplier; this works on Gold-only loot in the current mod. Doviello's Barbarian trait now applies the EMM -10% research modifier as -10% Science. Commando first strikes/enemy routes and barbarian diplomacy remain deferred. [Economic trait audit](economic-traits.md).

### Raiders multiplier correction

In-game calculation audit identified a percentage semantics bug: native Unciv `toPercent()` interprets 100% as a 2× total multiplier and 200% as 3×. Hippus and Svartalfar now use the correct `100% Yield from pillaging tiles`; see the [test protocol](economic-test-protocol.md) for the expected Gold distribution. Doviello's -10% Science remained correct.

### Lanun Pirate Cove ability — October 21, 2026

Added a Lanun-only Workboat improvement action: create **Pirate Cove** on an eligible coastal tile and consume the Workboat. Native restrictions cover owned/coastal/empty/resource-free/next-to-land tiles. Cove yields +1 Gold and +1 Science (proxy for EMM's +2 flexible commerce), +10% defense and approximate 10 Gold pillage. Timed upgrades to Pirate Harbor and Pirate Port, and two-tile spacing, remain deferred pending engine support. The user confirms that all implemented Cove functionality works as expected within the known Unciv engine limitations; Harbor/Port maturation and spacing remain deferred. [Mechanics and gameplay verification](lanun-pirate-cove.md).

### Khazad dynamic Dwarven Vault economy — October 21, 2026

Seven EMM gold-per-city vault stages are now functional through Unciv conditional arithmetic: Gold reserve divided by owned city count, floored. Their source Happiness and Production modifiers are tied exclusively to Khazad and can rise or fall with saved/spent Gold and city founding. The corresponding vault status buildings are not auto-inserted; only the economic bonuses are implemented. [Source thresholds and testing](khazad-vaults.md). Lanun Pirate Cove placement and Khazad Vault threshold/bonus behavior were user-tested and reported working on October 21, 2026.
