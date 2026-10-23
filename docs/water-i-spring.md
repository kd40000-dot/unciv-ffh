# Water I → Spring — third playable level-I spell

**Status:** Implemented October 23, 2026; static assertions and official Unciv `mod-ci` validation required; **not yet Android gameplay-verified**.

**Pinned source:** ExtraModMod Continued commit `60b0ec3740083162aaab7bf8491761a54a65a610`:
- `XML/Units/CIV4PromotionInfos.xml`: `PROMOTION_WATER1` requires Channeling I and Water Mana.
- `XML/Units/CIV4SpellInfos.xml`: `SPELL_SPRING` requires Water I + Channeling I.
- `python/entrypoints/CvSpellInterface.py`: Spring's `SPRING_TERRAFORM_HELPER` converts Desert to Plains; Spring also extinguishes Smoke/flames in the caster's and surrounding tiles. The source requirement rejects Flood Plains.

## Unciv mod-only conversion

**Water I** is a learnable promotion for Magic units with Channeling I, only available when the civilization owns **Water Mana** (from Water Node or another legitimate source). The promotion grants two separate native trigger actions. Both consume all of the caster's movement but do not consume the unit or its mana resource.

1. **Terraform Spring**: `Turn this tile into a [Plains] tile` gated to owned, unimproved Desert tiles without Flood plains, and requiring Water Mana. Uses Unciv's native one-time base terrain-change trigger; the change is permanent.
2. **Extinguish Spring**: `Remove [Smoke] improvements from this tile` gated to an owned tile already containing a Smoke improvement, and requiring Water Mana. This directly interacts with our earlier **Fire I → Blaze** smoke effect.

**Differences from EMM:** extinguishing affects only the caster's tile, not surrounding tiles; no spreading fire/flames simulation, no Smoke radius effects. This version deliberately limits desert conversion to friendly, unimproved tiles to avoid hostile territory terraforming or unintended removal of other improvements. The game action labels are native Unciv action text rather than a custom Spring spell popup.

## Android QA

1. Use a fresh or updated game with a **Water Node**. The node requires **Elementalism**, and must supply **1 Water Mana**.
2. Give an Adept (or another Channeling I Magic caster) enough XP to select **Water I**. Verify it is not available without Water Mana.
3. Move the Water I caster onto an **owned unimproved Desert** tile (not Flood plains). Use `Turn this tile into a Plains tile`. Confirm the Desert becomes **Plains**, the caster survives, and its movement is consumed.
4. On a separate unimproved friendly Forest or Jungle, use a Fire I caster's **Blaze / Create Smoke** action to produce Smoke. Move your Water I caster onto that exact Smoke tile and use `Remove Smoke improvements from this tile`. Confirm the Smoke disappears; the underlying terrain remains.
5. Ensure the terraforming action is not offered on non-Desert terrain, improved tiles, or foreign territory, and the extinguish action isn't offered where there's no Smoke.
6. Save/reload to confirm the permanent terraforming result and Smoke removal remain. Check there was no resource loss or map corruption.

**Regression checks:** `tools/verify_water_i.py` and official Unciv CI.
