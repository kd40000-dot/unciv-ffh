# ExtraModMod Continued Ancient-era starting units

Source: [pinned EMM Continued revision `60b0ec3740083162aaab7bf8491761a54a65a610`](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610), [machine-readable civilization inventory](data/emm-civilizations.json).

## Implementation

The Ancient era still grants **1 Settler** but no generic starting Warrior. Each of the **19 EMM playable civilizations** has exact source unit counts via native Unciv nation uniques, either `Free [unit] appears <if starting in the [Ancient era]>` or `[2] free [unit] units appear <if starting in the [Ancient era]>`. The Unciv `GameStarter.placeStartingUnits()` initialization code evaluates untriggered nation uniques once at the starting tile immediately after the standard era/difficulty units. This avoids any per-turn spawning behavior or engine modification. Nearby valid tiles are required.

The base unit name is used for Warrior and Scout so `getEquivalentUnit` resolves faction replacements: Calabim Bloodpet (Warrior), Doviello Beastman (Warrior), Clan Goblin (Scout).

## EMM starting roster by civilization

| Civilization | Ancient-era starting units |
| --- | --- |
| Amurites | 1 Settler, 1 Warrior, 1 Scout |
| Balseraphs | 1 Settler, 1 Warrior, 1 Scout |
| Bannor | 1 Settler, 1 Warrior, 1 Scout |
| Calabim | 1 Settler, 1 Warrior, 1 Scout |
| Clan of Embers | 1 Settler, 1 Warrior, 1 Scout |
| Doviello | 1 Settler, 1 Warrior, 1 Scout, 1 Lucian |
| Elohim | 1 Settler, 1 Warrior, 1 Scout |
| Grigori | 1 Settler, 1 Warrior, 1 Scout |
| Hippus | 1 Settler, 1 Warrior, 1 Scout |
| Illians | 1 Settler, 1 Warrior, 1 Scout |
| Khazad | 1 Settler, 2 Warrior |
| Kuriotates | 1 Settler, 1 Warrior, 1 Scout |
| Lanun | 1 Settler, 1 Warrior, 1 Scout |
| Ljosalfar | 1 Settler, 2 Scout |
| Luchuirp | 1 Settler, 1 Warrior, 1 Scout |
| Malakim | 1 Settler, 1 Warrior, 1 Lightbringer |
| Sheaim | 1 Settler, 1 Warrior, 1 Scout |
| Sidar | 1 Settler, 1 Warrior, 1 Scout |
| Svartalfar | 1 Settler, 1 Warrior, 1 Scout |

These sum to **19 Settlers and 39 other units** across playable civilizations before difficulty-level starting bonuses.

## Previously missing EMM units

**Lucian** (Doviello): strength 3, movement 1, source cost 60, +10% strength when attacking cities. His original technology is the unresearchable `TECH_NEVER`, so he is **Unbuildable** and capped at 1 per civilization. Original Strong Lucian and Winterborn special effects remain deferred rather than guessed.

**Lightbringer** (Malakim): strength 2, movement 1, source cost 60, free Sentry (+1 sight) and new land `Disciple` class. Unlike Lucian, the source permits ordinary construction, so Lightbringer is buildable. His original religion-disciple upgrade targets are absent pending the religion milestone.

## Limits and validation

- Applies **only to Ancient-era starts**; Classical/Medieval games retain ordinary Unciv era/difficulty starts.
- Race promotions on initial free units and other special Lucian/Winterborn powers are not yet faithful.
- This uses Unciv's own initialization triggers and native replacement resolution, but **has not yet been tested on Android or in longer AI games**. Placement may fail if the starting area lacks valid land tiles.
- `tools/verify_starting_units.py` checks all rosters, source class/counts and both special units; automated Unciv mod-ci validation remains a separate required gate.
