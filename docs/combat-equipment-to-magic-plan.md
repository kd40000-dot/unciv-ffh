# Combat, equipment, and magic conversion gates

Reference: ExtraModMod Continued commit `60b0ec3740083162aaab7bf8491761a54a65a610`.

## Combat audit (2026-10-21)
- 102 unit definitions and 112 known primary/secondary upgrade links are reference-valid.
- Combat I–V now allow Disciple unit types, matching EMM's UNITCOMBAT_DISCIPLE eligibility.
- City Raider I now allows Disciple unit types, matching the source; City Raider II–III remain restricted by the source's later-tier lists.
- Basic strength, city assault/defense, terrain, mobility and racial effects have translations; first strikes, withdrawal, collateral attacks, resistances, damage types and spell combat are incomplete.
- Static reference validity is not in-game combat validation.

## Metal equipment — not yet implemented faithfully
EMM's Copper, Iron, and Mithril weapon bonuses are not equivalent to consuming one strategic resource to manufacture each unit. Do not apply `requiredResource` indiscriminately to melee units: that changes roster accessibility and source balance.

Before implementation:
1. Extract equipment promotions and their specific source strength values and promotion replacement/eligibility behavior.
2. Determine whether stock Unciv supports a non-consuming 'has connected resource' condition when granting a *promotion to existing units*, and whether that can update automatically when a resource is lost.
3. Test side-by-side values: base unit, Copper, Iron, Mithril; connected/lost resource; newly trained unit vs veteran.
4. If dynamic equipment cannot be represented via stock JSON, document a conscious fixed bonus proxy or engine-extension requirement rather than claiming equipment parity.

### Strategic resources caution
Current `requiredResource` entries on 13 units are *stockpile-consuming* Unciv fields. The EMM source generally gates recruitment on access rather than spending permanent resource slots. They are functional restrictions but **not resource-system fidelity**; reevaluate before production balance is considered finalized.

## Magic: implementation order
1. **Mana inventory.** Extract mana resource and node types from pinned EMM and choose tile/spawn representation; validate resource revelation, improvement and ownership rules.
2. **Caster ranks.** Fix level/XP constraints for Mage and Archmage and test Adept/Mage/Archmage ability progression. Current Channeling I–III promotions are markers, not spells.
3. **Spell spheres.** Source-map each sphere promotion, its mana prerequisites and access by caster rank. Do not create decorative promotions that imply functional magic.
4. **First functional spell slice.** Prioritize healing, haste, elemental direct effects and one summon, but only after identifying *validated* Unciv action uniques or a documented supported engine extension. Test target selection, once-per-turn usage, range, duration and AI behavior.
5. **Mana interaction.** Test multiple copies of mana, loss of resource, promotion inheritance and ownership transfer.
6. **Expansion.** Add remaining spell types, channeling, affinity, summoned-unit expiration and spell resistance as supporting primitives become available.

## Release gates
- Parse all changed JSON and check object references.
- Use Unciv mod-ci / in-game 'Locate mod errors' on the proposed ruleset.
- Verify representative combat promotions, magic actions and resource edge cases in an Android session.
- A source inventory or schema-valid JSON file is not proof of equivalent gameplay.

## Reference implementation to examine: Fantasia (Unciv)
- Repository: https://github.com/amfauzn/Fantasia
- Unciv ruleset with Mage, Monk and other fantasy classes, plus skills, monsters, dungeons and fantasy progression.
- Before developing mana, spells and caster actions, inspect Fantasia's JSON uniques, unit promotions and available actions for patterns that Unciv actually supports; record compatibility with the target Unciv version.
- Adapt only validated implementation techniques; retain ExtraModMod Continued as the source of gameplay semantics and balance. Fantasia's mechanics are not automatically equivalent to FFH2 magic.

## Provisional first functional caster action (2026-10-21)
- Added `[This Unit] heals [15] HP <for all movement>` to Mage, Archmage and Amurite Wizard. This is a **test of Unciv's native unit-triggered action plumbing**, inspired by Fantasia's use of native magical unit/promotional abilities; it is not asserted to match a named EMM spell.
- Verify the action appears for wounded casters, heals exactly 15 HP, consumes remaining movement, and is unavailable to Adepts. This is **not yet Android-tested**. The action is intentionally self-targeted; adjacent healing, spell spheres, mana requirements and cast limits remain future work.
- Technical reference: https://github.com/amfauzn/Fantasia and https://yairm210.github.io/Unciv/Modders/uniques/ .

## First equipment implementation (2026-10-22)

- Added **exclusive dynamic combat-strength proxies** for 28 selected melee/Sword units, based on civilization access to Copper, Iron or Mithril and the appropriate Bronze Working, Iron Working or Mithril Working technology.
- EMM's reference values are Bronze +1, Iron +2, Mithril +4 *flat* combat strength. Stock Unciv uses percentage strength uniques, so each affected unit receives an integer-rounded percent relative to its base strength to approximate those values. For example a strength-4 Swordsman receives +25%, +50%, or +100%. Flat bonuses cannot be reproduced exactly for every unit in native Unciv JSON.
- Only one tier activates at a time: Mithril supersedes Iron and Copper; Iron supersedes Copper. Effects update dynamically with resource availability (subject to game-engine evaluation). Unlike source equipment promotions, they do not require returning to a connected city for refitting. No combat-stat inflation from multiple tiers is intended.
- Deliberately excludes Warrior, golem constructs and Pyre Zombie. Eligibility on all remaining source-specific units is **provisional**, pending a complete EMM `bUseWeaponTier` audit; mounted and other non-Sword types are not covered in this first pass.
- This **does not** implement visible equipment promotions, original fixed-strength semantics, equipment-vs-equipment matchup modifiers, Rust removal/repair, a Forge refit requirement, or source-specific unit-by-unit weapon eligibility.
- Gameplay validation pending: compare identical units with only Copper, then Iron, then Mithril connected; ensure one tier applies, loses strength when the resource is disconnected, and honors technology requirements. Run Unciv's *Locate mod errors* before longer games.
