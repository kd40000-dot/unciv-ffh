# EMM economic and raiding trait conversion

Reference: [pinned ExtraModMod Continued source](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610), the `CIV4TraitInfos.xml` numeric values recorded in [source trait ledger](data/emm-leader-palace-fidelity.json), and native Unciv `UnitActionsPillage.pillageLooting` calculation.

## Newly functional elements

| Civilization | Leader trait | EMM source mechanic | Unciv behavior |
| --- | --- | --- | --- |
| Hippus (Tasunke) | Raiders | +100% Gold gained when pillaging | `200% Yield from pillaging tiles` (double loot) |
| Svartalfar (Faeryl) | Raiders | +100% Gold gained when pillaging | `200% Yield from pillaging tiles` (double loot) |
| Doviello (Charadon) | Barbarian | -10% Research commerce | `[-10]% Science [in all cities]` |

All the mod's current improvement pillage payout uniques award **Gold only** (Farm, Mine, Trading post, Camp, Pasture, Plantation, Quarry and Fishing Boats), allowing Unciv's generic yield multiplier to reproduce the Raiders Gold multiplier on present content. Unciv's pillaging code multiplies directly by the stated percentage; `100%` would mean no change, so the equivalent of EMM's +100% bonus is **200% total**. For future improvements that yield Food, Science or other stats, this generic Unciv bonus would scale those as well, making it only an approximation in that expanded ruleset. The verifier protects the current Gold-only assumption.

The Barbarian science penalty matches EMM's `commerceModifiers=[0,-10,0]` research slot; because EMM's commerce can be reallocated, the Unciv city-wide -10% Science is a close *fixed-economy* translation, not an identical commerce-system model.

## Mechanics deliberately deferred

- Raiders also gives **Commando** to certain units. EMM Commando allows enemy road use and an extra first strike. No trustworthy native Unciv representation of both behaviors was verified, so no fake or unrelated promotion has been added.
- The Doviello Barbarian trait grants **barbarian ally behavior** (`bBarbarianAlly=1`), not just the research penalty. The alliance needs gameplay/AI rules and is not implemented here.
- Organized civic upkeep, Expansive health, Adaptive, Insane and Summoner remain deferred pending their relevant gameplay systems.

## Testing

The CI verifier `tools/verify_economic_traits.py` compares every selected leader against the pinned trait data, checks all affected nation uniques and all improvement pillage payouts. Gameplay tests: (1) pillage the same Mine as Hippus or Svartalfar and another ordinary civilization at the same turn/difficulty; the Raiders payout should be doubled (allow for individual random rolls), (2) compare Doviello Science output with equivalent cities of a faction without a science trait. This test must not be mistaken for validating Commando or barbarian relations.

The previous palace and leader-effect milestone was confirmed working by the user on October 21, 2026; the economic bonuses added here have not yet been gameplay-verified.
