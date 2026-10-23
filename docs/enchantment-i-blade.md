# Enchantment I → Enchanted Blade: localized buff proxy

**Date:** October 23, 2026. **Status:** Committed, awaiting Android gameplay verification.

**Pinned EMM source:** `bewlay/extramodmod` commit `60b0ec3740083162aaab7bf8491761a54a65a610`:
- `XML/Units/CIV4PromotionInfos.xml`: `PROMOTION_ENCHANTMENT1` needs Channeling I + Enchantment Mana; `PROMOTION_ENCHANTED_BLADE` supplies +20% melee combat strength (attack and defense); `PROMOTION_RUSTED` penalizes melee combat.
- `XML/Units/CIV4SpellInfos.xml`: `SPELL_ENCHANTED_BLADE` adds the Enchanted Blade promotion to valid nearby units and removes Rusted.

## What is implemented

Unciv does not support selecting specific friendly melee units for a triggered spell in the same way as EMM. Applying `[mapUnitFilter] units gain [promotion]` directly would instead grant a promotion to **all matching units throughout the entire civilization**, which would be seriously overpowered. To avoid that, the first implementation is a **temporary local aura**.

- **Enchantment I** is a learnable promotion on Magic casters, requiring Channeling I and **Enchantment Mana**.
- Its native action, **`[This Unit] gains the [Enchanted Blade Aura] status for [2] turn(s)`**, spends all caster movement and keeps the caster alive. A second cast refreshes the duration, not the number of bonuses.
- **Enchanted Blade Aura** is a hidden, two-turn status carrying `[20]% Strength bonus for [Sword] units within [1] tiles`. Unciv uses the same native nearby-unit modifier mechanism as Great Generals. Sword-type friendly units receive +20% strength while in range of a caster with an active aura; they lose it when it expires or they leave range. This is not a permanent buff on the target.
- Only Sword-class units are targeted in this initial version, corresponding to most melee infantry in the present mod. Some other EMM melee-type equivalents outside `Sword` may be omitted.
- EMM's Rusted removal is not yet implemented; no general Rusted combat debuff has been introduced.

## Android gameplay verification

1. Update the mod. Research **Alteration**, build an **Enchantment Node** on Raw Mana, and check that the empire has **1 Enchantment Mana**.
2. Gain enough XP with an Adept, Wizard, Mage or Archmage to select **Enchantment I** (requires Channeling I). Confirm it does not appear without Enchantment Mana.
3. Stand next to a friendly **Sword-class** unit, note its combat modifier against an enemy, and cast **`gains the Enchanted Blade Aura status`**. Check the caster spends its movement but survives.
4. With the Sword unit within one hex of the caster, check the unit gets **+20% Strength** in combat. Move the Sword unit more than one tile away and confirm the aura bonus disappears.
5. Wait for the two-turn status to expire and confirm nearby units lose the bonus. Casting again should refresh, not stack multiple +20% effects.
6. Confirm Archery and Mounted units do not receive the Sword-filtered bonus. Save and reload to confirm the status remains consistent.

**Validation:** `tools/verify_enchantment_i.py` plus official `Unciv.jar mod-ci` workflow.
