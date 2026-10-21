# Amurite Magic Foundation — prototype 0.2

This is the **first playable ExtraModMod mechanics slice**, deliberately separated from the art-only releases. It is not a complete magic system.

## Changes grounded in ExtraModMod XML

| Feature | EMM source | This test mod |
| --- | --- | --- |
| Adept | `XML/Units/CIV4UnitInfos.xml`, `UNIT_ADEPT` | 90 production, Knowledge of the Ether, Mage Guild; upgrades toward Mage/Wizard |
| Wizard | `UNIT_WIZARD` | 120 production, Sorcery, upgrades from Adept via Mage replacement; cannot be trained directly |
| Firebow | `UNIT_FIREBOW` | 120 production, Bowyers, Archery Range prerequisite |
| Chanter | `UNIT_CHANTER` | 120 production, Poisons |
| Govannon | `UNIT_GOVANNON` | 480 production, Arcane Lore, maximum one currently active |
| Haste | `XML/Units/CIV4SpellInfos.xml`, `SPELL_HASTE` | Body I plus Channeling I, temporary movement effect |
| Starting mana | `XML/Civilizations/CIV4CivilizationInfos.xml`, Amurites | Body, Fire and Mind mana in nation uniques |

## The first mana → promotion → spell loop

1. Begin a new game as **Amurites / Valledia**. The three starting mana resources should appear in your strategic resource totals.
2. Research **Knowledge of the Ether** and construct a **Mage Guild**.
3. Train an **Adept**. The Mage Guild temporarily grants 10 XP so the player can choose an early sphere promotion; the original Adept has one free promotion choice and this is **not an exact implementation**.
4. Choose **Body I**, which should be selectable while your empire owns Body Mana.
5. The Adept should have a unit action based on `[This Unit] gains the [Hastened] status for [2] turn(s) <for all movement>`. Trigger it, end turn and verify the temporary movement bonus and expiry.
6. On a map with raw mana, reveal **Raw Mana** using Knowledge of the Ether, then build a **Body Node**, **Fire Node**, **Mind Node**, or **Death Node** with a Worker. Each specialized improvement provides one copy of the matching mana resource.
7. Research Sorcery, then check the Adept's upgrade to **Wizard**; test XP retention, promotions and save/reload.

## Important deviations / missing mechanics

- **Haste:** current spell is caster-only (a two-turn `Hastened` status with +1 Movement), while ExtraModMod applies Hasted to qualifying nearby units. The Unciv action consumes all movement. This is a **working prototype to test**, not verified in Android and not source-exact.
- **Mana:** each strategic mana resource gates sphere selection. Four mana-node variants implement an early node economy. This is not the complete 18-sphere ExtraModMod magic system, and node conversion/AI behavior must be tested on-device.
- **Wizard level gate:** EMM requires a level-four Adept; the level requirement is **not enforced** here. Mage/Wizard cannot be built directly, but can be upgraded when Sorcery is available.
- **Fire I, Mind I, Death I, Channeling and Spellstaff:** source-named promotions exist, but only Body I currently has a real spell action. Don't claim that Firebow can cast Blaze, Wizard can double-cast, or Govannon can teach until those effects are proven in-game.
- **Govannon:** `Limited to [1] per Civilization` limits living copies, **not lifetime hero construction**.
- **Mage Guild 10 XP:** an accessibility shortcut for testing a free promotion choice, not canonical EMM balance. This should be replaced with a more exact implementation if supported.
- **Node/icon art:** simple generated placeholders; player-approved unit sprites and portraits remain from Firebow Repair preview 1.2.
- **Sorcery tech prerequisites:** current simplified tech tree does not yet implement EMM's OR-gated Alteration/Divination/Elementalism/Necromancy research branches.

## Acceptance tests

- [ ] New Amurite capital owns Body, Fire, and Mind Mana; Bannor does not start with those mana supplies.
- [ ] Adept cannot be produced before Knowledge of the Ether and a Mage Guild.
- [ ] Mage Guild-produced Adept can choose Body I and receives a visible Haste action.
- [ ] Casting Haste consumes movement; Hastened status changes mobility, then expires.
- [ ] Raw Mana appears on generated maps and a Worker can attune it into a node after research.
- [ ] Newly acquired mana gates corresponding promotions.
- [ ] Research prerequisites and costs for Wizard, Firebow, Chanter, and Govannon are restored.
- [ ] Adept upgrades to Wizard for Amurites (not generic Mage), retaining promotions.
- [ ] All five approved map sprites render, with no missing atlas images.
- [ ] Save and reload preserve promotions, mana improvements and spell statuses.
- [ ] Official Unciv `mod-ci` has no errors or warnings.

Source of truth: [ExtraModMod](https://github.com/bewlay/extramodmod) and [official Unciv uniques](https://github.com/yairm210/Unciv/blob/master/docs/Modders/uniques.md).
