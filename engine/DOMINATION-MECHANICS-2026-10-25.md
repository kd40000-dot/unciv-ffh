# Domination implementation checkpoint — 2026-10-25

## Source verification
Pinned EMM `bewlay/extramodmod` commit `60b0ec3740083162aaab7bf8491761a54a65a610`:
- XML `XML/Units/CIV4SpellInfos.xml`, `SPELL_DOMINATION`: requires Mind III, one-tile range, resistable, `iResistModify=10`, excludes friendly/team, neutral and nonliving units.
- Python `python/entrypoints/CvSpellInterface.py`, `reqDomination`/`spellDomination`: eligible war-enemy living units cannot have Loyalty; selects one target ranked `baseCombatStr()*10 + (100 - resistChance)`; capture on a successful resistance check preserves/converts unit state, sets immobility, and failed resistance strips the caster's Mind III promotion. The AI source condition restricts eligible resistance chance to <=20; human player permits <=95.

## New native behavior
- `Domination` is now an explicit `DOMINATE` effect instead of a temporary -35% Strength status.
- Targets a single living enemy military unit within range one, refuses Loyalty-protected recipients, and uses Unciv's `MapUnit.capturedBy(caster.civ)` to transfer unit ownership instead of applying a combat penalty.
- Native capture zeroes the captured unit's movement and performs tile-eligibility checks in pinned Unciv.
- Among eligible enemies, target selection prioritizes base combat strength only. This differs from EMM's resistance-weighted ranking.
- The casting action is still gated by ownership of Mind III, movement and the spell budget.

## IMPORTANT: Remaining parity gaps
- **Resist chance is not implemented**: current engine capture succeeds deterministically. EMM's `getResistChance`, roll, AI eligibility limit and Mind III removal upon failure must be ported before gameplay parity.
- Source target ranking uses resistance chance, not current recipient health.
- Civ IV stacks, promotions of captured units and siege/naval eligibility need on-device verification.
- Current `isLiving` is a heuristic and excludes some name categories; use EMM unit flags for exact immunity.
- Full Kotlin compile, Android build and gameplay acceptance have **not** been completed for this checkpoint.

## Test plan
- [ ] War-enemy living unit captured and appears in caster's unit list, with zero movement
- [ ] Friendly, neutral, nonliving and Loyalty-protected units cannot be captured
- [ ] Strongest eligible target chosen from adjacent recipients
- [ ] Unit promotions, health, XP and names survive the transfer
- [ ] Capture on a stacked or occupied tile safely relocates if required
- [ ] Save and reload transferred units
- [ ] Add EMM-calculated resistance, failure and lost Mind III after source-derived odds are implemented
