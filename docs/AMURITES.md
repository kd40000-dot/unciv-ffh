# Amurites — source-verified faction checklist

**Theme:** civilization built around arcane specialists, a mana economy and spells taught by its hero, not merely stronger generic units.

## Manual reference: printed pages 4–5 of *Fall from Heaven II 0.30 Manual*

- Starts with **Body, Fire and Mind mana**.
- Valledia the Even: **Neutral**, **Organized** (civic upkeep reduction and building production bonuses) and **Arcane** (Arcane promotion and faster Mage Guilds). Preferred civic **Apprenticeship**.
- **Wizard** replaces Mage, starts with **Spellstaff**, and is an experienced arcane upgrade.
- **Firebow** replaces Longbowman, with ranged combat, Fire I and Channeling II.
- **Chanter** replaces Assassin; Dimensional I and unusual recon/poison combat.
- **Govannon** is a hero who can teach a group of spells to non-casters after learning them (Blaze, Blur, Dance of Blades, Escape, Haste, Raise Skeleton).
- **Cave of Ancestors**: cost 120 in the manual; +1 experience to trained Arcane units **per mana resource accessible to that city**, not a flat bonus.
- **Arcane Lacuna**: grants arcane-unit XP based on improved mana nodes worldwide and reverts mana nodes to raw mana.

**Illustration guide:** manual p. 4 shows Firebow as an earthy-toned bowman and Govannon as a dark-hooded mage holding a staff emitting green light; p. 5 shows the Cave building and Valledia's original painted portrait. Match recognizable silhouettes and color/weapon cues without using low-resolution source art as a substitute for a true game sprite. For the new sprite concepts, the user separately supplied original Firebow and Govannon icon references.

## Differences between the early manual and ExtraModMod

| Field | FFH2 0.30 manual | ExtraModMod XML | Implementation decision |
| --- | --- | --- | --- |
| Wizard technology | Arcane Lore | `TECH_SORCERY` | Use EMM Sorcery |
| Govannon technology | Sorcery | `TECH_ARCANE_LORE` | Use EMM Arcane Lore |
| Firebow technology | Machinery and Bowyer | `TECH_BOWYERS`; `BUILDINGCLASS_ARCHERY_RANGE` prerequisite | Use EMM Bowyers; add proper Archery Range prerequisite when available |
| Chanter free promotions | Channeling I, Dimensional I, Sorcery listed | `PROMOTION_MARKSMAN` and `PROMOTION_DIMENSIONAL1` in `UNIT_CHANTER` | Use EMM; do not invent Channeling I |
| Wizard free promotions | Channeling I–II, Sorcery, Spellstaff | Channeling I–II, Spellstaff (casting type defined separately) | Use EMM promotion list |
| Govannon free promotions | Channeling I–III, Hero, Sorcery listed | Channeling I–III, Hero (casting type separately defined) | Use EMM promotion list |

XML data for the above: [ExtraModMod CIV4UnitInfos.xml](https://github.com/bewlay/extramodmod/blob/master/XML/Units/CIV4UnitInfos.xml) and [civilization replacement list](https://github.com/bewlay/extramodmod/blob/master/XML/Civilizations/CIV4CivilizationInfos.xml).

## Current development branch: `amurites-first-playable-01`

### Added in ruleset, pending Android playtest
- Amurite-exclusive Wizard `replaces: Mage`, Firebow `replaces: Longbowman`, Govannon, shared arcane unit type and advancement technologies.
- Stated original promotions are represented, but Channeling/Fire I/Spellstaff do **not yet cast working spells**.
- `Limited to [1] per Civilization` implements a unit-count cap for Govannon, **not** FFH2 irreversible one-time hero construction after death.
- Firebow standard ranged attack **does not simulate** EMM first strikes, defensive strikes or separate elemental fire damage.
- A `Mage Guild` foundation exists, but unit prerequisite behavior and Cave of Ancestors mechanics are still pending.

### Still required for a genuine Amurite experience
1. Implement Chanter + generic Assassin, source-correct promotions and poison/dimensional effects.
2. Complete the early mana resource and node economy, including the three Amurite starting mana resources.
3. Add the real **Cave of Ancestors** rule with mana-count–scaled training XP: do not replace it with a flat bonus and call it done.
4. Enforce tiered Arcane promotions, casting actions and Spellstaff in the *mod*; prove behaviors in-game rather than inferring from JSON validation.
5. Implement Govannon's teachable spells, once-per-game hero status, and Arcane Lacuna.
6. Recreate Valledia's Organized/Arcane effects using native Unciv uniques and full prerequisite buildings/civics.
7. Supply separate unit icons + map sprites for Wizard, Firebow and Govannon, atlas-pack them for Android; ideally also create a Chanter sprite. Use the user's approved Valledia portrait.
8. Pass official `mod-ci`, then test unit replacements, costs, image rendering, unlocking, upgrades and save/reload on Android.

**Status caution:** This is a staged integration, not a full playable Amurite simulation until the remaining mechanics pass the tests.
