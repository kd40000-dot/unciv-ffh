# Lanun Pirate Cove: first playable faction improvement

**Source:** [ExtraModMod Continued commit 60b0ec3740083162aaab7bf8491761a54a65a610](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610). Compared `XML/Units/CIV4SpellInfos.xml` (`SPELL_PIRATE_COVE`), `XML/Terrain/CIV4ImprovementInfos.xml` (all three Pirate stages), and `python/entrypoints/CvSpellInterface.py` (`reqPirateCove`). Detailed original values are in [the pinned source ledger](data/emm-lanun-pirate-coves.json).

## Implemented in this milestone

**Lanun Workboats** gain the native Unciv action **Create Pirate Cove**, using `Can instantly construct a [Pirate Cove] improvement <by consuming this unit> <for [Lanun] Civilizations>`. The Workboat is *the existing UNIT_WORKBOAT* (Fishing, cost 30, movement 2); no fictional unit type or free construction is created.

The new `Pirate Cove` tile improvement is **uniqueTo: Lanun** and has **turnsToBuild: -1** (blocks normal worker construction; the separate consuming special action places it instantly). It enforces these EMM source placement requirements using Unciv's improvement rules:

- Coast only
- In the player's own territory (not outside borders)
- Empty/unimproved tile
- No visible resource
- Next to a land tile
- The workboat is consumed by the special creation action

The source Cove has yields [0 Food, 0 Production, 2 Commerce], +10% defense, and 10 pillage Gold. The Unciv Cove grants **+1 Gold and +1 Science**, a documented 50/50 proxy for the original adjustable Commerce; the +10% defense is direct, and pillage loot is approximately +10 Gold in Unciv's random-loot system.

## Source-only follow-on stages (not active yet)

| Stage | Original yields: Food / Production / Commerce | Defense | Upgrade after |
| --- | --- | --- | --- |
| Pirate Cove | 0 / 0 / 2 | +10% | 10 turns → Pirate Harbor |
| Pirate Harbor | 1 / 1 / 3 | +20% | 20 turns → Pirate Port |
| Pirate Port | 2 / 2 / 4 | +30% | Final stage |

EMM evolves these improvements automatically by time since **the tile improvement was constructed**. Stock Unciv lacks a JSON field implementing that per-tile timed upgrade, so only **Pirate Cove** is available in-game. The Harbor and Port are inventoried, not invented as buildable replacements; the lack of maturation significantly understates the late-game Lanun improvement economy.

EMM also checks every tile in a **5-by-5 coordinate square around the target** and blocks construction if another Pirate Cove, Harbor, or Port exists. Unciv has no verified `improvement within radius` placement restriction, so this spacing rule is **not enforced**. Avoid spamming multiple Coves close together if you want source-faithful play.

The engine's `unimproved` filter may treat a pillaged improvement as unimproved, whereas EMM rejects tiles with an improvement already present. Replacing a pillaged improvement is therefore another known edge-case limitation.

## Game test (Android / desktop)

1. Update the mod and **start a fresh game** as **Lanun** with coastal access.
2. Research **Fishing**, build a **Workboat** (30 Production) and move into a **coastal water tile owned by Lanun** next to land, without a resource or improvement.
3. Select the Workboat and choose **Create Pirate Cove**. Check that the Workboat is **consumed** and a **Pirate Cove** appears. When a city works the tile, confirm it provides **+1 Science and +1 Gold** above the Coast base tile yield, plus the original +10% defensive bonus.
4. Confirm **non-Lanun Workboats** do not have the Pirate Cove action.
5. Check that the action is unavailable on Ocean, on a resource tile, on a tile outside Lanun borders, and on a coastal tile that is not next to land.
6. A Cove will **not** automatically upgrade to Harbor or Port in this milestone; this is a known omission, not a newly introduced regression.

**Verification status:** Source values, target unique templates, placement-condition logic and the source ledger were inspected against the preserved Unciv engine and pinned EMM code. The new special unit action needs a real gameplay check before being marked verified. Automated `tools/verify_lanun_cove.py` runs in GitHub Actions along with the other ruleset checks.

## Next implementation dependency

To complete the Lanun line, we need an engine-side or officially supported Unciv ruleset mechanic for **time-since-improvement-construction upgrades** and the **cove spacing radius**. Neither is claimed to be implemented here.
