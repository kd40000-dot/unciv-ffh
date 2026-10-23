# Khazad Dwarven Vaults — seven auto-swapping city buildings

**Implementation:** Seven source-derived Dwarven Vault tiers are now **real, individually named Khazad buildings**, automatically granted and replaced using native Unciv uniques. Source thresholds/effects were originally gameplay-verified as *nation-level bonuses* on October 21, 2026. The **new building-based swap implementation and icon display still require Android in-game testing**.

**EMM Continued reference:** [pinned upstream `60b0ec3740083162aaab7bf8491761a54a65a610`](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610). Source: `python/FfH/FfHDefines.py`, `XML/Buildings/CIV4BuildingInfos.xml`. Structured source audit: [source ledger](data/emm-khazad-vaults.json).

## Stages, applied once per owned Khazad city

| Floor(treasury Gold / owned cities) | Visible city building | City Happiness | City Production |
| ---: | --- | ---: | ---: |
| Under 25 | Dwarven Vault (Empty) | −2 | 0% |
| 25–49 | Dwarven Vault (Low) | −1 | 0% |
| 50–74 | Dwarven Vault (Normal) | 0 | 0% |
| 75–99 | Dwarven Vault (Stocked) | +1 | 0% |
| 100–149 | Dwarven Vault (Abundant) | +2 | +10% |
| 150–249 | Dwarven Vault (Full) | +2 | +25% |
| 250+ | Dwarven Vault (Overflowing) | +3 | +40% |

All seven building definitions are `uniqueTo: Khazad`, `Unbuildable`, `Cannot be purchased` and `Unsellable`. They have no construction/maintenance cost and are `Destroyed when city captured`. These are *automatically installed buildings*, not things a player has to produce. Each building holds its **own** source-accurate Happiness and percentage Production effect. All nine previous nation-level Gold conditionals have been **removed** to avoid double bonuses.

There are seven individual icons in `Images/BuildingIcons/`, registered under `khazad-vaults.atlas` in `Atlases.json`. The icon artwork is an original icon set generated for the port, not a claim of pixel identity with original EMM icon art.

## Lifecycle and important caveat

On **Khazad turn start**, 12 mutually exclusive out-of-range removal triggers clear stages that do not match the treasury/city ratio, then seven matching free-building grants install the appropriate stage in every Khazad city. This works through native `Remove [building] [in all cities]` and `Gain a free [building] [in all cities]` with `<upon turn start>` and the original `floor([Gold] / [Cities])` Countables expressions. The identical 19-action reconciliation is also triggered `<upon founding a city>`, updating all existing cities and the new city immediately after founding.

Removal runs **before** grants to avoid temporary overlapping buildings. Matching existing stages are not removed, so the game does not repeatedly reconstruct the same building each turn.

**The visible vault state and its effects update at synchronization events, not instantly after every Gold transaction.** Spending Gold or receiving Gold *during your turn* may leave the old building until your next turn starts. This is an acknowledged JSON-only limit and is different from the previously verified continuously evaluated nation-level conditionals. City capture, changing city ownership, and unusual rapid treasury changes also require testing.

Game-engine implementation references:
- [`TurnManager.startTurn`](https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/civilization/managers/TurnManager.kt) triggers civ-wide turn-start uniques before city start turns.
- [`CityFounder.foundCity`](https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/city/managers/CityFounder.kt) triggers civ-wide city-founding uniques after the city has been created.
- [`UniqueTriggerActivation`](https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/UniqueTriggerActivation.kt) handles free-building grants and direct removal.
- [`Building.kt`](https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/Building.kt) supports nonconstructible building entries and no-selling restrictions.

## Android QA checklist

1. Update the mod and begin a **new Khazad game**. Found first city with under 25 Gold. Confirm exactly one **Dwarven Vault (Empty)** in the city's buildings and a −2 Happiness effect.
2. At one city, save Gold to exactly **25, 50, 75, 100, 150, 250**. End the turn after crossing each threshold; verify the previous vault disappears, the new matching vault building/icon appears, and the effects match the table.
3. Confirm no old/nation-level bonus remains (especially Abundant +2/+10%, Full +2/+25%, and Overflowing +3/+40%).
4. Spend Gold down from Overflowing to Empty. Check **before** advancing (old stage may remain) and **after** turn start (correct new stage).
5. At 250 Gold and one city, found a second: 250/2 = 125, so **both cities** should immediately display Abundant and get +2 Happiness/+10% Production. At 49 Gold / two cities, floor(24.5) correctly stays Empty.
6. Confirm the player cannot construct, purchase or sell any Vault stage, and other nations do not get the buildings.
7. Save/reload with different vault tiers and check for duplicate buildings. Test conquest, selling/rebuying other buildings, and a city without enough room/production to ensure the Vault still appears.
8. Compare the city building screen and Happiness/Production breakdown. If an icon or modifier is missing, record the game version, Gold, city count, stage shown and actual stats.

## Static checks and remaining gaps

The `tools/verify_khazad_vaults.py` verifier covers all seven EMM source entries, stage-specific buildings, cost/unbuildable treatment, stage effects, removal-before-grant ordering, both event types, no legacy nation bonus, boundary cases and 36k+ Gold/city combinations. `tools/verify_roster.py` maps the seven stage names to their EMM source IDs, allowing an original cost of `-1` (script-created in Civ IV) to become Unciv cost 0 and an Unbuildable unique.

Remaining fidelity gaps: instant building replacement after arbitrary treasury changes (native turn-start events only), visual equality to EMM's original icons, and Android end-to-end gameplay verification. The previous implementation **was** gameplay verified; this replacement implementation has **not** yet been user-tested.
