# Amurites — unit roster integration 0.1

## Original ExtraModMod source

- [UnitInfos](https://github.com/bewlay/extramodmod/blob/master/XML/Units/CIV4UnitInfos.xml): `UNIT_FIREBOW`, `UNIT_WIZARD`, `UNIT_GOVANNON`, `UNIT_ADEPT`, `UNIT_MAGE`.
- [CivilizationInfos](https://github.com/bewlay/extramodmod/blob/master/XML/Civilizations/CIV4CivilizationInfos.xml): Mage → Wizard, Longbowman → Firebow, Assassin → Chanter; Amurite hero Govannon.
- [TechInfos](https://github.com/bewlay/extramodmod/blob/master/XML/Technologies/CIV4TechInfos.xml): Bowyers, Sorcery, Arcane Lore and their dependencies.

## Working in native Unciv

- Unique-to-Amurites Firebow and Wizard replacing Longbowman and Mage via `replaces`/ `uniqueTo`.
- Govannon appears only for the Amurites and is capped at one per civilization.
- Original promotions attached to each unit, names maintained as framework for spells; Hero's provisional combat XP is explicitly not native hero experience.
- A shared Adept, Mage, Longbowman and Mage Guild plus development-stage research path permit getting to the new roster.
- Assets include the previously approved Valledia image plus custom Firebow, Wizard and Govannon unit art and icon entries.

## Not working and not represented as complete

- Full FFH2 fire damage, defensive strikes, mage spells and mana spheres; Channeling I/II/III and Fire I have no mechanical effects until spells exist.
- Govannon's signature ability to teach tier-one spells; his automatic experience growth and spellcasting.
- Wizard spellstaff extra casting, level-4 promotion eligibility and exact mage-upgrade restrictions; Wizards are directly buildable for this milestone.
- Original Sorcery's `Writing AND one of Alteration/Divination/Elementalism/Necromancy` — temporarily routed through Writing and Divination only.
- Chanter (Assassin replacement), Cave of Ancestors and other Amurite-specific structures — intentionally not labeled completed.
- Overall Unciv one-tile vs original Civ4 movement scale, diplomatic traits, broader research economy balance.

## Acceptance checklist for Android

- [ ] Valledia portrait appears on nation picker and diplomacy screens
- [ ] Firebow's own unit icon and on-map sprite load and cannot be trained by Bannor
- [ ] Wizard has its own icon and on-map sprite, replaces Mage in Amurite city production
- [ ] Govannon has custom icon/on-map sprite, and cannot be produced more than once
- [ ] Base standard units, researching, settling and city production still work
- [ ] No missing atlas entries or invisible sprites with stock FantasyHex tileset
- [ ] Full mod-ci validator clean; manual Android test confirms game behavior
