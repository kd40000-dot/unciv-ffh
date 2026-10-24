# Mind I → Inspiration (city research magic)

**Implemented:** October 24, 2026. **Status:** Code committed; gameplay verification on Android pending.

## EMM Continued reference

Pinned upstream EMM commit `60b0ec3740083162aaab7bf8491761a54a65a610`:
- `XML/Units/CIV4PromotionInfos.xml`: `PROMOTION_MIND1` requires Channeling I and Mind Mana.
- `XML/Units/CIV4SpellInfos.xml`: `SPELL_INSPIRATION` requires Mind I and Channeling I, can be cast only in a city, and creates `BUILDING_INSPIRATION`.
- The EMM spell maintains **+2 research and +1 Great Sage point per turn** through the Inspiration building while a Mind I caster sustains it in that city (not an ordinary permanently constructible building).

## Unciv implementation

Two new entries in `UnitPromotions.json`:

- **Mind I:** a Magic-unit promotion, available only with Mind Mana and Channeling I. Casting action:
  `[This Unit] gains the [Inspiration (Spell)] status for [2] turn(s) <for all movement> <with [Mind Mana]> <in [City center] tiles>`.
- **Inspiration (Spell):** a non-learnable temporary status:
  `Gain [2] Science <upon turn start> <in [City center] tiles> <with [Mind Mana]>`.

The caster must stand on a city center when casting, spends all its movement, and remains alive. While its status lasts, **+2 Science is credited directly to the player's empire at turn start** if the unit remains on a city center and the empire retains Mind Mana. This is a city-occupancy conditional, not a permanent city building, and can be refreshed by recasting after the status expires. Moving out of the city stops the award.

**Known deviations:** Science is awarded as an empire stat rather than a visible +2 city yield in the city management screen; there is no city Inspiration building and no +1 Great Sage generation. The effect is not indefinitely sustained and needs recasting every two turns. Multiple separate inspired casters may each provide science, matching the general possibility of staffing multiple cities, but unlike EMM, multiple casters in the same city may stack if each has the status.

**Native engine grounding:** Unciv's `UnitTurnManager.startTurn()` triggers `TriggerUponTurnStart` uniques on the unit. `UniqueTriggerActivation.OneTimeGainStat` accepts Science as a civ-wide stat and adds it to the empire. The `ConditionalInTiles` modifier filters the unit's current tile.

## Android gameplay checks

1. Research **Divination**, construct a **Mind Node** on Raw Mana, and confirm **1 Mind Mana** is available.
2. Give an Adept (or Wizard, Mage, Archmage) enough experience to learn **Mind I**. Verify learning is gated by Mind Mana.
3. Move this caster into one of your **city centers**. Cast the native action `gains the Inspiration (Spell) status`; confirm movement is spent, unit survives.
4. Note empire Science progress just before your next turn, and compare to a control situation. **The inspired caster should contribute exactly +2 Science at turn start**, over the regular city output.
5. Move the caster off the city center while the status is active: the next turn should **not** receive the 2 Science from this caster. Move back while the status remains and it may resume.
6. After the two-turn status expires, confirm it no longer awards the extra science. Recast on a city center and verify it resumes. Check that the action is not available outside a city center or without Mind Mana.
7. Verify saving/reloading works without duplicate bonuses or loss of the temporary status.

**Validation:** `tools/verify_mind_i.py` and the official Unciv mod-ci checks. Static validation is not proof of the actual research gain; confirm the effect in-game before marking verified.
