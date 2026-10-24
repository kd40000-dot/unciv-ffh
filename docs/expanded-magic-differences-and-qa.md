# Expanded magic: differences and test gates

Working branch: `feature/expanded-magic-2026-10-24`. Rollback checkpoint: `checkpoint/pre-full-magic-2026-10-24` at `ae94e78090f2c80363e0856a5ebe2769b91c76e8`.

## Scope and correctness

- EMM Continued has **355** SpellInfo XML records at pinned commit `60b0ec3740083162aaab7bf8491761a54a65a610`. They are **not** 355 independent arcane sphere spells: many are special abilities, faction rituals, equipment handoffs and internal mechanics.
- **257** SpellInfo records use `PyResult` or `PyRequirement`, so any faithful recreation must examine Python code and game state (not just XML).
- Treat every newly-added spell as **unverified** until it passes Unciv mod-ci **and** on-device action/target/effect/expiry tests. Static JSON checks are necessary but not sufficient.
- Never substitute an empire-wide promotion for same-tile or adjacent-target spell effects. It would affect every eligible unit in the entire civilization.
- No engine changes in this branch. Unsupported effects must be documented, not silently fabricated.

## Original EMM → Unciv differences currently known

| EMM spell | Current mod representation | Difference / missing behavior | State |
|---|---|---|---|
| Blaze (Fire I) | Create Smoke improvement | No spread, auto-expiration or ordinary hostile-territory ignition; fixed 5-damage proxy | Player-tested basic action |
| Haste (Body I) | Self-cast two-turn Hasted status, +1 movement | Doesn't buff co-located friendly living units or remove Slow | Player-tested basic action |
| Enchanted Blade (Enchantment I) | Temporary adjacent Sword aura, +20% strength | EMM grants lasting individual melee promotions and removes Rusted | Player-tested combat bonus |
| Spring (Water I) | Own unimproved Desert → Plains, remove local Smoke | Limited targeting and terrain behavior vs EMM Python rules | Not player-tested |
| Inspiration (Mind I) | Two-turn +2 Science conditional status in city center | EMM establishes a city building with +2 Science and +1 Great Sage point / turn; no Great Sage points | Not player-tested |
| Treetop Tactics (Nature I) | Two-turn caster Forest strength status, +10% | No EMM withdrawal bonus, Ancient Forest distinction or other friendly-unit recipients | Player-tested combat bonus |
| Courage (Spirit I) | **New dev-branch prototype:** two-turn caster aura granting adjacent units +10 healing when healing | EMM applies Courage promotion to eligible living units on same tile: fear immunity, +10 same-tile healing, exploration result bonus +5, chance to expire. Current proxy has no fear immunity, exploration bonus, same-tile targeting or random expiry | **Unverified: dev branch only** |

## Compact batch QA procedure (not yet executed)

- [ ] Run all `tools/verify_*.py` static checks on the **feature branch**.
- [ ] Run official Unciv `mod-ci` on the feature branch; fix invalid unique types, filters and references.
- [ ] Run Unciv **Locate mod errors**.
- [ ] Confirm promotion unlock only with matching sphere Mana and Channeling I.
- [ ] Confirm cast option appears only in intended location (friendly/enemy tiles, improvement state, terrain).
- [ ] Verify caster lives unless EMM explicitly consumes it; validate movement action cost and ability to repeat.
- [ ] Test status duration, stacking/refresh, opponent-turn effects and save/load.
- [ ] Test loss of mana, retuning nodes, pillaged nodes and city/tile capture.
- [ ] Compare effects on friendly, neutral, enemy and immune targets; verify AI behavior where applicable.
- [ ] Regress the six spells already present.
- [ ] Spirit I: Build a Spirit Node, learn promotion, measure wounded adjacent unit healing with and without active caster aura; verify it expires after 2 turns and doesn't boost a nonadjacent unit.
- [ ] Water I: Verify Desert to Plains transformation and Smoke cleanup with the exact terrain and ownership restrictions.
- [ ] Mind I: Verify accumulated Science **versus** ordinary Science-per-turn over both status turns; check expiration and no stacking.

## Future spells and unsupported effects

For each line in `docs/emm-full-spell-inventory.md`, before coding: inspect EMM SpellInfo, referenced promotions/buildings/improvements and the Python result/requirement if any; verify target and duration; check Unciv unique parser and AI; classify as **faithful native**, **explicit proxy**, or **requires engine extension**; add a test scenario and difference notes. Do not label any inventory row implemented until it has an executable effect.
