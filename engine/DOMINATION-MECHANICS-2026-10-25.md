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

## Resistance implementation — 2026-10-25

Read pinned EMM `CvGameCoreDLL/CvUnit.cpp::getResistChance` and `XML/GlobalDefinesAlt.xml`:
- Base resistance **20%**, unit level **+5% per level**, spell Domination **+10%**, city center **+10%**; clamp **5–100%**.
- EMM additionally aggregates target innate/promotion resistance, caster resistance modifier, defending owner's resistance modifier, offensive owner's anti-resistance, and city magical defense. **Those modifiers are not yet implemented in our engine**, because equivalent Unciv data/model APIs have not been ported.
- EMM source selects the highest `baseCombatStr()*10 + (100-resistChance)` viable target, gates resistance to **95% for humans / 20% for AI**, then checks a random roll 0..99.
- On a resisted cast, the caster **loses Mind III**. Success transfers ownership of the chosen target, retains its identity and sets movement to zero.
- Unciv `UnitPromotions.numberOfPromotions + 1` is used as a **provisional level proxy**. The EMM native `getLevel()` does not currently have a source-exact counterpart.

**Do not call this full EMM resistance parity.** It now actually rolls and applies failure penalties, but the listed magic-resistance component system and exact level semantics remain incomplete.

### In-game test checklist (side-by-side EMM Android client)

1. Install **only a successfully produced artifact** from the `EMM engine fork Android debug build` workflow on this branch; ordinary mod installation in vanilla Unciv cannot execute these Kotlin effects.
2. Start a war, acquire a Mind III caster with remaining movement, and put a living enemy military unit one hex away. Domination should appear.
3. Verify successful capture places that unit on your side with zero movement; check promotions, XP, health and name.
4. Repeat with new units until a resisted cast occurs. On resistance, the enemy must remain enemy-owned **and the caster must lose Mind III**.
5. Place a friendly or neutral unit nearby. Neither should be dominated. Nonliving units (e.g. Golem/Skeleton), Loyalty-protected enemies, and any other immune categories should be excluded.
6. Place multiple eligible enemies at one hex. Verify a **single** recipient is selected by combat strength and approximate resistance, not all.
7. Compare recipients with different promotion levels: higher level should resist more often across many attempts, even when combat strength is similar.
8. Try an enemy standing in a city center: expected extra +10% resistance, subject to the missing city magic-defense modifier.
9. Attempt Domination without Mind III, after losing it on a failed cast, or with no remaining movement. The action should not appear/execute.
10. End turn or save/reload after both successful and resisted casts; neither owner nor Mind III state should revert.
11. Check AI-controlled casters. The source-derived **20% eligibility gate** means they may find no eligible target under the current minimum Domination resistance calculation; this is a known limitation to investigate.
12. Observe that no combat damage or former Domination -35% Strength proxy is applied.
