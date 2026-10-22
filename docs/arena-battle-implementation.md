# Arena Battle — gameplay implementation and remaining gaps (2026-10-22)

**Status:** JSON-only implementation committed; **not tested in-game**. Rollback: `checkpoint/pre-arena-happiness-slave-2026-10-22`. This implementation uses upstream Unciv uniques and no fork/engine modifications.

## EMM Continued source (pinned `60b0ec3740083162aaab7bf8491761a54a65a610`)

- `python/entrypoints/CvSpellInterface.py`: `reqArenaBattle`, `spellArenaBattle` — https://github.com/bewlay/extramodmod/blob/60b0ec3740083162aaab7bf8491761a54a65a610/python/entrypoints/CvSpellInterface.py
- `XML/Units/CIV4SpellInfos.xml`: `SPELL_ARENA_BATTLE` — https://github.com/bewlay/extramodmod/blob/60b0ec3740083162aaab7bf8491761a54a65a610/XML/Units/CIV4SpellInfos.xml
- `XML/Text/Buildings.xml` has `TXT_KEY_BUILDING_ARENA` but no exact `TXT_KEY_BUILDING_ARENA_PEDIA`: do **not** pass off narrative descriptions as verbatim original EMM Civilopedia background/history.
- The source EMM `UNIT_SLAVE` is a non-buildable captive class that may emerge through other effects; the current mod lacks that acquisition logic.

EMM battle effects: +3 to **city happiness timer per battle**, regardless of win/loss; 50% chance to win or lose. Winning unit gains **1–6 random XP**, and damage is **set to 25**; defeated unit dies. Winning Slave converts into a Warrior while preserving original unit data. Human player's melee/recon/Slave eligibility; AI only certain low-level Weak units.

## Unciv implementation

### Arena building

`jsons/Buildings.json` retains Arena as the Balseraphs replacement for Training Yard and its current +2 Sword training XP. A single `Comment` unique on the city/building screen describes active effects; source-unavailable lore is not represented as a claimed EMM quote. Unit type action implementations are not repeated in the city builder.

### Temporary Happiness bonus — new

`jsons/UnitPromotions.json`, `Arena Battle` promotion, now includes:

```
[+1 Happiness] <for [3] turns>
```

Upstream Unciv's `UniqueType.ConditionalTimedUnique` converts this into a triggered civilization-wide temporary unique and stores it in `civInfo.temporaryUniques`, which automatically expires. It is unconditional so **both** wins and losses yield the bonus.

The reward is explicitly a **proxy**: Unciv uses empire-wide Happiness; EMM modifies a *specific city's* existing happiness timer. Unlike EMM's cumulative duration, multiple concurrent temporary bonuses can **stack in magnitude**. A battle therefore adds +1 empire-wide Happiness for 3 turns, potentially multiple +1 bonuses simultaneously, rather than extending a city timer.

Supporting engine source:
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/UniqueTriggerActivation.kt
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/TemporaryUnique.kt
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/civilization/transients/CivInfoStatsForNextTurn.kt

### Winning Slave conversion — new

`jsons/Units.json` includes `Slave`, an *Unbuildable* civilian unit with cost 60 and movement 2, matching the EMM catalog's cost and untrainable role at this implementation stage. It has:

```
Can upgrade to [Warrior] <for units with [Arena Victory]> <in cities with a [Arena]>
[This Unit] gains the [Arena Battle] promotion <for all movement> <in cities with a [Arena]>
```

On 50% win, `Arena Battle` gives `Arena Victory` status, then 3 XP and 25 damage, adds timed Happiness, then calls:

```
[This Unit] upgrades for free <for [Slave] units> <for units with [Arena Victory]>
```

Upstream Unciv `UnitUpgradeManager.performUpgrade` places the new upgraded type with `copiedFrom = unit`; this is expected to retain promotions, status, XP and other unit state. It is conditional on a successful battle, so ordinary Slave upgrades to Warrior should not be available (the Warrior pathway unique is gated behind the victory status and city Arena). We have **not yet implemented acquisition of Slaves** by enslavement, capture or events. This means conversion is implemented *for eventual acquisition*, not practically exercised in regular gameplay yet.

Supporting source:
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/map/mapunit/UnitUpgradeManager.kt
- https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/UniqueTriggerActivation.kt

### Kept from previous Arena iteration

- Sword + Scout unit classes receive the Arena Battle action only when they are in a city containing Arena.
- 50% random victory status; win +3 XP and **take** 25 damage (not set damage to 25); lose destroys unit.
- `Arena Victory` status expires after 1 turn; there is no instantaneous cleanup, because winning Slaves need this status to qualify for the Warrior upgrade. This status is hidden from the world map.

## Acceptance tests still required

1. Train a Sword or Scout unit in/bring into Balseraphs city with Arena: **Arena Battle action exists and uses all movement**. No action outside city.
2. Win: unit receives +3 XP, takes +25 damage; lose: unit destroyed. Both outcomes cause +1 Happiness in empire statistics; record exact expiry after 3 turns.
3. Battle twice with distinct units on same turn; verify two temporary bonuses stack (+2 Happiness), and expire after their individual three-turn timers. This differs intentionally from source's extending city happiness timer.
4. Spawn/import a Slave in the debug editor or a disposable test save: verify Arena Battle appears only in Arena city and Slave is not buildable normally.
5. Slave win: **Warrior appears instead of Slave**, inherits full XP and promotions; check exact position, damage, movement, hidden one-turn status, and no auto-repeat/recursion. Slave loss: no Warrior remains. Test if city military slot is occupied and replacement cannot be placed at the same tile.
6. Save and reload during an active temporary Happiness bonus and after a Slave conversion. Verify no unintended persistence, duplicated reward or crashes.
7. Test action under AI, in other nations' cities and with units that have exhausted movement.
8. Future source parity: random 1–6 XP; damage *set* to 25; city-local nonstacking happiness timer; full Slave acquisition, activities and conversion; EMM AI selection criteria.

**Validation:** Parsed mod JSON; source inspected for supported trigger, temporary-unique, upgrade and upgrade-copy semantics. **No Android gameplay test or ruleset validator run**.
