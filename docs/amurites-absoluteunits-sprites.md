# Amurites — Absolute Units sprite inventory

## Source and coverage

User-provided `amurites.zip` (2026-10-22) contains 20 individually named EMM screenshots plus one unlabeled screenshot. Ten named images were already processed and registered; the remaining ten are now converted and installed, giving **20 named sprites** in all. The extra unlabeled screenshot appears to be a different pose of a crossbow-wielding unit, but is not assigned a unit name or given a duplicate atlas entry.

Sprite conversion follows the existing Amurites approach: remove snowy screenshot backgrounds, crop the recognizable figures, resize proportionately to a **95×81 transparent Absolute Units canvas**, reduce the palette and use nearest-neighbor rendering. These are small pixel-art adaptations of the source screenshots, not screenshots displayed at full size.

## Original 10 installed

- Adept-Amurites
- Archer-Amurites
- Archmage-Amurites
- Beastmaster-Amurites
- Champion-Amurites
- Chanter
- Chariot-Amurites
- Crossbowman-Amurites
- Firebow
- Govannon

Previously registered through `amuritesunit1.atlas`–`amuritesunit10.atlas`.

## Added 10

- Horseman-Amurites — `Images/TileSets/AbsoluteUnits/Units/Horseman-Amurites.png`; `amuritesunit11.atlas`
- Horse Archer-Amurites — `Images/TileSets/AbsoluteUnits/Units/Horse Archer-Amurites.png`; `amuritesunit12.atlas`
- Hunter-Amurites — `Images/TileSets/AbsoluteUnits/Units/Hunter-Amurites.png`; `amuritesunit13.atlas`
- Immortal-Amurites — `Images/TileSets/AbsoluteUnits/Units/Immortal-Amurites.png`; `amuritesunit14.atlas`
- Marksman-Amurites — `Images/TileSets/AbsoluteUnits/Units/Marksman-Amurites.png`; `amuritesunit15.atlas`
- Phalanx-Amurites — `Images/TileSets/AbsoluteUnits/Units/Phalanx-Amurites.png`; `amuritesunit16.atlas`
- Ranger-Amurites — `Images/TileSets/AbsoluteUnits/Units/Ranger-Amurites.png`; `amuritesunit17.atlas`
- Scout-Amurites — `Images/TileSets/AbsoluteUnits/Units/Scout-Amurites.png`; `amuritesunit18.atlas`
- Swordsman — `Images/TileSets/AbsoluteUnits/Units/Swordsman.png`; `amuritesunit19.atlas`
- Wizard — `Images/TileSets/AbsoluteUnits/Units/Wizard.png`; `amuritesunit20.atlas`

All 20 atlas names are present in `Atlases.json`. Standard shared units are registered with `-Amurites` to avoid replacing artwork for other civilizations; the Amurites-exclusive `Swordsman`, `Wizard`, `Chanter` and `Firebow` use their exact ruleset names.

## Gameplay and other scope

- The `Immortal-Amurites` sprite is stored and registered for future use, but `Immortal` is **not yet defined** in `jsons/Units.json`, so it will not appear in gameplay.
- `Govannon` is also only an art reservation until his hero unit is implemented.
- No unit stats, unlocks, promotions, AI, or faction-specific mechanics changed.
- `jsons/ModOptions.json` is unchanged; the game can still use user-selected **Absolute Units** or another unit set.
- All other civilization art, including Clan of Embers sprites, is untouched.

Actual in-game display has not been verified here.
