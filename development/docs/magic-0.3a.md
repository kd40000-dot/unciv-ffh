# Magic milestone 0.3a — interactive prototype

Reference: [FFH2 Magic](https://fallfromheaven.fandom.com/wiki/Magic), [Spells](https://fallfromheaven.fandom.com/wiki/Spells), and [ExtraModMod spell table](https://fallfromheaven.fandom.com/wiki/Spells_in_ExtraModMod-u).

## Implemented in Unciv

- Arcane units (Adept, Shaman, Mage, Wizard) have the selectable **Arcane Circle** action, modeled as an instant improvement construction. It consumes all of the caster's movement for that turn.
- Nature I promotion grants a selectable **Blooming Grove** action as a prototype of terrain-affecting nature magic.
- Mage and Wizard now use Channeling II; Adept and Shaman keep Channeling I.
- Body I, Spirit I, Law I, Earth I, Air I, Fire II, Death I, and Metamagic I are initial prototype promotions that give modest Unciv-native unit effects.
- Mana resource now has a map-generation rule, so nodes have a source.

## Not yet equivalent to FFH2

- Unciv's normal UnitAction set does not directly expose targeted casting of Fireball, Haste on an ally, stack heal, promotion buffs, summoned units with limited duration, or one spell per caster per turn.
- Sphere I/II/III mana ownership is not yet a real gating system: these promotions are currently skill upgrades, not strictly unlocked by typed mana resources.
- Mage aura and Fire I had earlier placeholder effects; those are not canonical spell representations.
- The Arcane Circle and Blooming Grove actions are **test mechanics**, not canonical FFH2 spells.
- The spell lists and exact effects should eventually be generated from EMM's `CIV4SpellInfos.xml` and Python callbacks, not from wiki summaries alone.

## Next implementation

1. Model all 21 EMM sphere resources and palace mana by nation.
2. Add channeling promotions gated by caster tier and tech / resource ownership.
3. Implement whichever canonical spells can be expressed as unit actions (e.g. tile alteration) without an engine fork.
4. Evaluate a minimal Unciv engine extension for the remaining targeted spells and temporary summons.
5. Test actual buttons and terrain changes on Android; the official validator checks syntax, not turn-by-turn behavior.

## Artwork

The FFH wiki provides useful visual references, but art licensing must be checked on each image's file description page. The mod currently retains the GPL-licensed Wesnoth placeholders, rather than republishing wiki graphics with unclear rights. We can replace them when original game assets can be inspected and reuse is permitted.
