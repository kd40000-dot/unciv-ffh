# Native sphere spell continuation — 2026-10-25

Branch: `checkpoint/emm-engine-safety-2026-10-25`. Main and previous checkpoints remain unmodified.

## Engine changes
- Added `eligiblePromotions` support in the serialized EMM spell schema and matching executor. An eligible promotion, matching unit name, or valid unit type qualifies when any category is configured. Promotion names validated by Python static checks.
- Migrated four sphere spell actions from self-status or aura proxies into native recipient-targeting spell registry: `Destroy Undead`, `Charm Person`, `Blinding Light`, `Fair Winds`.
- Source manifest status and native cast grants are synchronized. A connector-side structural check found 355 EMM records, 36 native definitions, 36 grants, and no missing source/native mappings.

## Specific native proxies requiring EMM fidelity work

| Spell | Current gameplay prototype | Missing or approximate original mechanics |
|---|---|---|
| Destroy Undead, Life II | 20 damage to enemy Undead-tagged or named undead within one hex | Source `PyResult`, exact damage and resistance, radius, other creature categories, bCausesWar |
| Charm Person, Mind II | Living enemy units within 1 hex receive two-turn -15% Strength | Charm immunity, loyalty and source control/skip-turn effects, probabilistic resistance, range |
| Blinding Light, Sun II | Enemies within 1 hex receive two-turn -20% Strength | EMM source blindness / unit-action denial rather than Strength penalty, exact selection |
| Fair Winds, Air I | Friendly water-unit recipients within 1 hex gain a two-turn +20% Strength bonus | Source navigation/movement effect and same-plot stacking; current effect is not faithful |

None of these four are claimed EMM-exact. The goal remains full source parity, including rewrites when additional native engine services become available.

## Build / QA state

- Source metadata and native grant counts structurally reconciled with connector read.
- Regression assertions committed, not yet confirmed passed in CI.
- Kotlin compilation, Android APK build and live playthrough unverified.
- `checkpoint/emm-engine-safety-2026-10-25` is the new continuation branch. Earlier `checkpoint/emm-spell-wiring-inventory-2026-10-25` and main are preserved.

Next: native city/terrain API, equipment and player-targeting, damage resistance and deterministic duration, resurrection/stateful world spells.
