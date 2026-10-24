# Nature I — Treetop Tactics

**Implemented:** October 23, 2026. **Gameplay status:** Gameplay-verified by user.

## Original EMM Continued source

Pinned commit `60b0ec3740083162aaab7bf8491761a54a65a610` in `bewlay/extramodmod`:
- `XML/Units/CIV4PromotionInfos.xml`: Nature I (`PROMOTION_NATURE1`) is available to Channeling I adepts with Nature Mana.
- `XML/Units/CIV4SpellInfos.xml`: `SPELL_TREETOP_TACTICS` requires Nature I and Channeling I, and its caster must be in Forest or Ancient Forest. It grants `PROMOTION_TREETOP_TACTICS`.
- `PROMOTION_TREETOP_TACTICS`: +10% attack and defense in regular Forest, +20% in Ancient Forest, plus +10% withdrawal chance. It can affect other friendly units in EMM.

## Native Unciv approximation

- **Nature I:** learnable Magic-unit promotion requiring Channeling I and Nature Mana. The spell action is native `[This Unit] gains the [Treetop Tactics] status for [2] turn(s) <for all movement> <with [Nature Mana]> <in [Forest] tiles>`.
- **Treetop Tactics:** a non-learnable two-turn status with `[+10]% Strength <when fighting in [Forest] tiles>`. Casting is self-only and spends the caster's full remaining movement without consuming the unit or Mana.
- Original EMM Ancient Forest +20% bonus, 10% withdrawal chance, lasting promotion and ally-buff targeting are **not implemented**. The Unciv mod currently lacks Ancient Forest as a distinct terrain.
- The spell can be cast only **while in a Forest tile**; the bonus applies when fighting in Forest tiles as long as the temporary status remains active.

## In-game test

1. Research **Alteration**, build a **Nature Node**, and check you receive **1 Nature Mana**.
2. Give an Adept, Wizard, Mage, or Archmage enough experience for **Nature I**. Confirm it is not learnable without Nature Mana.
3. Stand in a **Forest** tile with the Nature I caster. Cast its `gains the Treetop Tactics status` action. Confirm all movement is consumed but the caster survives.
4. Inspect the caster's combat modifiers while fighting on Forest: there should be a **+10% Strength** bonus. Test on non-Forest to ensure no bonus.
5. Check the status expires after two turns. The action should not appear outside Forest.
6. Reload a save and check that terrain restrictions and the status persist correctly.

**Validation:** `tools/verify_nature_i.py` and official Unciv mod-ci; gameplay verified by user.

## Gameplay confirmation and visibility TODO (October 24, 2026)

The user confirmed the combat bonuses work in-game for both Enchanted Blade Aura and Treetop Tactics, including seeing the modifier in the combat preview. Keep the current implementation unchanged. **Deferred UI improvement:** consider a clearer active spell indicator on the caster and/or visibly showing which nearby units benefit from Enchanted Blade Aura. Do not prioritize until the user asks to revisit it.
