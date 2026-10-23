# Fire I — Blaze (first playable spell)

**Status:** First mod-only spell prototype committed October 23, 2026. **User gameplay-verified on October 23, 2026:** Fire I promotion appears when Fire Mana is available; Create Smoke works on eligible terrain; caster survives and movement is consumed. Enemy adjacency damage and other edge cases have not been separately confirmed. Validation at `tools/verify_fire_i.py`.

Source: ExtraModMod Continued commit `60b0ec3740083162aaab7bf8491761a54a65a610`. `XML/Units/CIV4PromotionInfos.xml` defines `PROMOTION_FIRE1` with Fire Mana prerequisite and Channeling I. `XML/Units/CIV4SpellInfos.xml` defines `SPELL_BLAZE`, Channeling I + Fire I, `IMPROVEMENT_SMOKE` creation on the caster's plot. `python/entrypoints/CvSpellInterface.py` specifies that Blaze requires Forest/Ancient Forest/Jungle and not already smoking/burning.

## Native Unciv conversion

- Added promotion **Fire I** for **Magic** unit type, prerequisite **Channeling I**, `Only available <with [Fire Mana]>` so the promotion requires an actual Fire Mana node resource.
- Fire I contains `Can instantly construct a [Smoke] improvement <for all movement> <with [Fire Mana]>`. This directly grants **Blaze** as a unit action to eligible Fire I casters who still own Fire Mana, consumes the caster's full movement, and does **not** consume the unit.
- Added **Smoke** tile improvement, instant-action-only (`turnsToBuild: -1`), on Forest/Jungle, only unimproved tiles within friendly owned territory. Smoke damages enemy units ending their turn on an adjacent tile for **5 HP** via a native improvement unique. The effect remains on the map until another improvement replaces it; no automatic fire spread or timed smoke expiration.
- Magic units **Adept**, **Mage**, and **Archmage** already carry Channeling I, so they can learn Fire I when promoted with Fire Mana available. No changes to their underlying stats or node construction.
- Spell is limited to forest/jungle **in owned territory** to avoid allowing a permanent damaging improvement to be dropped onto opponent territory, and only to unimproved tiles to avoid deleting valuable infrastructure.
- The smoke's 5 damage is a **gameplay proxy**, not an EMM source value. EMM's smoke spreads into fire with more complex processing; Unciv's JSON uniques cannot reproduce that simulation.

## Android gameplay test

1. Update the mod. In a game where the Fire Node already produces **1 Fire Mana**, use an Adept with enough XP to select a promotion. Verify **Fire I** becomes available; temporarily disconnect Fire Mana and verify it is unavailable on another caster.
2. Promote an Adept to Fire I. Move it onto an **owned, unimproved Forest or Jungle** tile.
3. Tap the unit's **Create Smoke** action (the Unciv native improvement action standing in for EMM's Blaze). Confirm it consumes movement but **not** the Adept, changes the tile improvement to Smoke, and keeps the underlying Forest/Jungle terrain.
4. End the turn with an enemy unit adjacent to Smoke. Confirm it takes **5 damage** when that enemy unit ends its turn nearby.
5. Confirm Smoke cannot be created on unwooded land, a pre-improved Forest, or a foreign tile, and cannot be repeatedly stacked on the same tile.
6. Save/load; check Fire I and Smoke persistence.

## Limitations and future work

- Blaze is presented with Unciv's action label **Create Smoke**, rather than a custom standalone spell picker and spell animation.
- It does not reproduce spreading fire, EMM Smoke expiration, Ancient Forest support, or EMM's hostile-territory burning rules.
- Fire I requires earned XP and a promotion selection in Unciv. Native promotions do not automatically unlock based on mana access.
- This first prototype proves actual magic actions are possible within normal mod files. Additional schools can use the same promotion/unique framework, but require individual translations and testing.
