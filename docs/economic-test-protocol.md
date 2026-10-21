# Economic trait QA: Hippus, Svartalfar and Doviello

## Findings from Unciv source-code inspection

Inspected preserved Unciv Kotlin implementation at `4b3232223ce18b4e6cd628c667d9f4265ccf9bb9`:

- `core/src/com/unciv/ui/components/extensions/FormattingExtensions.kt` defines `Float.toPercent() = 1 + this/100`.
- `core/src/com/unciv/logic/map/mapunit/actions/UnitActionsPillage.kt` applies `pillageYield *= unique.params[0].toPercent()` for `PercentYieldFromPillaging`. Random improvement loot is two draws from the inclusive range `0..X`, with the tile and turn driving the random seed.
- `core/src/com/unciv/logic/city/CityStats.kt` recognizes `StatPercentBonusCities` and later multiplies each Science source by `statPercentBonusesSum.science.toPercent()`.

**Discovered bug and fix:** The previous `200% Yield from pillaging tiles` produced **3×**, not 2×, because percentages express relative *bonuses*. Hippus and Svartalfar now have `100% Yield from pillaging tiles`, giving **2×**. Doviello's `[-10]% Science [in all cities]` already correctly produces **0.9× Science**.

## Expected numeric outcomes

For default speed and without additional game-progress yield modifiers, the random improvement payout distribution is:

| Improvement | Unciv loot unique | Non-Raider average (range) | Hippus/Svartalfar average (range) |
| --- | --- | --- | --- |
| Mine / Trading post / Quarry | Approximately +20 Gold | 20 (0–40) | 40 (0–80) |
| Farm | Approximately +18 Gold | 18 (0–36) | 36 (0–72) |
| Camp / Pasture / Plantation / Fishing Boats | Approximately +10 Gold | 10 (0–20) | 20 (0–40) |

The means follow from two independent uniform integer rolls `0..X`; an individual pillage is not guaranteed to equal the mean. These ranges assume the loot modifiers for game speed and progress are 1×. Other bonuses, where present, will change them.

Science examples with all other city factors held constant:

| Science before Barbarian penalty | Doviello after -10% | Unmodified civilization |
| ---: | ---: | ---: |
| 5.0 | 4.5 | 5.0 |
| 10.0 | 9.0 | 10.0 |
| 20.0 | 18.0 | 20.0 |

Unciv's city Science is calculated using floating point; the summary UI may round the displayed number. In the original first-turn 1-population case, the capital has **+4 Science from its faction Palace plus +1 Science from population**, i.e. baseline 5; Doviello should obtain 4.5 before any other modifiers.

## Manual in-game checks: fresh game required

1. **Enable the latest version of the mod and start a new game.** Existing saves may retain earlier ruleset data. Use Standard speed and a non-Raider nation (for example, Bannor) as the control.
2. **Raider display test.** Open the Hippus nation description, then Svartalfar; confirm each has `100% Yield from pillaging tiles`. Confirm the control has no pillage bonus. This checks that the corrected rule has loaded, not the calculated Gold.
3. **Raider payout test.** At war, pillage an enemy improvement (preferably a Mine or Trading post) with a Hippus or Svartalfar military unit. Record Gold immediately **before** and **after** the pillage, or use the Gold loot notification. Do the same for a control unit on another equivalent improvement at the same speed and similar game progress. Repeat several times (around 10+ samples per side is better): rewards are randomized and a single result is not a decisive comparison.
4. **Doviello test.** Start a fresh Doviello game. Found one city and inspect the Science yield or its city-stats breakdown. The source penalty should appear as `-10%` and multiply city Science by `0.9`. Compare with a newly founded one-population control capital with the same tiles, buildings, specialists, and research settings. If the game shows only rounded totals, compare the detailed breakdown or research progress across multiple turns.
5. **Regression test after updates.** Run `python3 tools/verify_economic_traits.py` (also included in GitHub Actions) before releasing subsequent economic, pillage or city-science changes.

## Reporting an actual in-game test

For each pillage, capture **civilization; improved tile; game speed; turn; Gold before; Gold after; amount received**. For Science, capture **civilization; city population; Palace; Science before/after modifiers, or the city yield breakdown; and screenshot(s)**. This is enough to investigate any discrepancy without inventing a conclusion from unrelated random rolls.

## Validation status

- **Source review:** Complete. Unciv percentage semantics, pillage payout calculation and city Science modifier consumption all confirmed in preserved engine source.
- **Mod rule change:** Corrected from 200% to 100% Raiders bonus.
- **Static regression:** Numeric percentage assertions and source-to-nation consistency checks added to CI.
- **Live Android gameplay:** Still requires a played session, or reproducible screenshots/saves. No Android playthrough was performed by the author of this document.
