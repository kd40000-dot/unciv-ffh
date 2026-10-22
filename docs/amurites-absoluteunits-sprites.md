# Amurites — High-detail Absolute Units artwork

The 21 civilization-specific unit sprites have been updated using individually generated high-detail full-body character illustrations. The source characters were derived from the user's ExtraModMod Continued Amurites in-game screenshots and `amurites.zip`, then rebuilt as standalone art, not copied from the earlier composite contact sheet.

## Sprite format

- `Images/TileSets/AbsoluteUnits/Units/<name>.png`: **95 × 81 transparent PNG**, original aspect ratio preserved, palette reduced at game scale, nearest-neighbor atlas filtering.
- Character feet, weapons and mounts fit inside the image canvas; all sprites align to the same approximate baseline.
- Existing `amuritesunit1.atlas`–`amuritesunit20.atlas` and `warrioramurites.atlas` continue to register these same image paths in `Atlases.json`.
- Common shared unit sprites use the `-Amurites` suffix, while Amurites' unique unit types `Chanter`, `Firebow`, `Swordsman` and `Wizard` use the exact unit name.
- `Govannon` and `Immortal-Amurites` have artwork registered, but those unit definitions remain outside the current mod's ruleset; this artwork update does **not** implement them.
- `jsons/ModOptions.json` remains unchanged, so Absolute Units is optional, not forced.
- No gameplay or stat changes were introduced.

## All 21 current art entries

- `Adept-Amurites`
- `Archer-Amurites`
- `Archmage-Amurites`
- `Beastmaster-Amurites`
- `Champion-Amurites`
- `Chanter`
- `Chariot-Amurites`
- `Crossbowman-Amurites`
- `Firebow`
- `Govannon`
- `Horse Archer-Amurites`
- `Horseman-Amurites`
- `Hunter-Amurites`
- `Immortal-Amurites`
- `Marksman-Amurites`
- `Phalanx-Amurites`
- `Ranger-Amurites`
- `Scout-Amurites`
- `Swordsman`
- `Warrior-Amurites`
- `Wizard`

The 21 PNGs and all existing atlas references were committed together. The image files were checksum-verified as identical to the processed source PNGs. In-game rendering of this revision still requires user confirmation.
