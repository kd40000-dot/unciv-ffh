# Khazad Dwarven Vaults — dynamic Gold-per-city mechanics

**Status:** Implemented in the base ruleset; source/static verification added to CI. **Gameplay verification: passed in user testing (October 21, 2026).**

**Pinned authoritative EMM Continued source:** [commit 60b0ec3740083162aaab7bf8491761a54a65a610](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610). EMM's `python/FfH/FfHDefines.py` provides vault thresholds [0,25,50,75,100,150,250] and chooses the highest threshold not exceeding treasury Gold divided by number of cities. `XML/Buildings/CIV4BuildingInfos.xml` defines the corresponding Happiness and Production effects. Machine-readable audit: [EMM Khazad Vaults source ledger](data/emm-khazad-vaults.json).

## Seven vault levels — source exact

| Treasury Gold per city | Vault stage | Happiness **per city** | Production **per city** |
| ---: | --- | ---: | ---: |
| Below 25 | Empty | -2 | — |
| 25–49 | Low | -1 | — |
| 50–74 | Normal | 0 | — |
| 75–99 | Stocked | +1 | — |
| 100–149 | Abundant | +2 | +10% |
| 150–249 | Full | +2 | +25% |
| 250+ | Overflowing | +3 | +40% |

The Normal stage has no bonus/penalty, so it needs no active unique. Every other stage uses exclusive conditional uniques. No static free Gold or unrelated Gold production effect is added.

## Native Unciv implementation — no engine fork needed

The critical mechanic is the **integer Gold reserve per owned city**, not total Gold nor income per turn:

```
floor([Gold] / [Cities])
```

Unciv's **Countables** recognizes `Gold` as the stored treasury reserve (even when evaluated from a city), `Cities` as owned-city count, and `Expression` as a numeric expression with `floor`, division and nested Countables. `ConditionalCountableBetween` compares the result inclusively; `Conditionals` checks a city-scoped unique in its matching game context. `floor` is required because Unciv rounds the final evaluated expression with `roundToInt`; raw `Gold/Cities` would incorrectly advance a vault when the ratio rounds up.

For example, Abundant uniquely grants:

```
[+2 Happiness] [in all cities] <when number of [floor([Gold] / [Cities])] is between [100] and [149]>
[+10]% Production [in all cities] <when number of [floor([Gold] / [Cities])] is between [100] and [149]>
```

All bonuses are on **Khazad** `Nations.json` (not on a constructible vault building). Source vault buildings have production cost -1 and are script-provisioned; native Unciv does not have a mechanism for showing seven mutually exclusive auto-assigned city buildings. Representing their effects through dynamic civilization uniques is intentional and mechanically close but not UI-identical.

**The conditions react to a changing treasury and city count when the engine refreshes city/civilization stats.** In-game tests should confirm that totals refresh immediately after changes or, at latest, on the following turn. The code paths were audited against preserved Unciv Kotlin sources. On October 21, 2026, the user reported that the requested Vault tests yield the expected results. This verifies the exercised Gold-per-city thresholds and dynamic Happiness/Production bonuses in gameplay, rather than every possible edge case or engine version.

## Testing — first two-city and spending exercises

1. Update the mod and begin a **new Khazad game**. Found the first city. With under **25 total Gold**, inspect Happiness: the city should have the **-2 Empty vault** penalty relative to an equivalent non-Khazad control.
2. Save Gold until **25**, then **50**, **75**, **100**, **150** and **250** with **one city**. Confirm penalties/bonuses at each step using the city stats breakdown and Production. Note the Khazad's separate Industrious wonder bonus; compare ordinary Production to isolate vault effects.
3. Found a **second city** while holding **250 Gold**. The Gold-per-city ratio falls from **250 (Overflowing)** to **125 (Abundant)**. Both cities should now receive **+2 Happiness, +10% Production**, replacing +3/+40%; 250 Gold should not remain Overflowing after expansion.
4. Increase savings to **500 Gold with two cities** to recover **Overflowing**. Spend Gold (unit upgrading or purchasing where supported), and confirm that a lower tier applies after treasury changes.
5. At **49 Gold with two cities**, floor(49/2) = 24, so the status is **Empty** rather than Low. At 50 Gold with two cities, it becomes **Low**. This distinguishes correct integer division from rounding.
6. Check **non-Khazad** civilizations for absence of vault bonuses.

Report any mismatch with the **current treasury Gold**, **city count**, **city Happiness before/after**, **city Production before/after**, and whether you advanced a turn. We can use this to determine whether the issue is the conditional expression, city-stats refresh, or another production modifier.

## Regression and remaining differences

CI runs `python3 tools/verify_khazad_vaults.py`: source-building values, seven stages, the nine required uniques, no effects on other nations, exact floor-vs-round boundary cases, founding/spending examples, and tens of thousands of city-count/Gold pairs.

The seven named vault buildings are **not physically inserted into cities**; their effects are represented through Nation uniques instead. Source-accurate behavior also depends on the game's update cadence for stored-Gold conditionals, for which the user has confirmed the prescribed gameplay tests behaved as expected. Further edge cases and future engine updates remain untested. Vault art and a dedicated UI badge/status display are deferred.
