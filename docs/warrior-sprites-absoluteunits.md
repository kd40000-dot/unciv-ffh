# Civilization-specific Warrior sprites — Absolute Units

Both warrior sprites are newly developed for this Unciv mod based on the original Fall from Heaven 2 / ExtraModMod Continued assets provided in `assets.zip`. They are **not direct cropped DDS textures**. They complement the working Goblin sprite and use the existing Absolute Units rendering approach.

## Clan of Embers

- Sprite: `Images/TileSets/AbsoluteUnits/Units/Warrior-Clan of Embers.png`
- Atlas: `warriorclan.atlas` registered as `TileSets/AbsoluteUnits/Units/Warrior-Clan of Embers`
- References from the FFH asset archive: `art/interface/buttons/units/warrior clan of embers.dds`; `art/units/civs/clan of embers/warrior/scout_128.dds`; `art/units/civs/clan of embers/warrior/woodstonespear.dds`
- Muted ashen-olive Orc warrior, stone-tipped spear, rough leather armor and weathered dark red shield.

## Amurites

- Sprite: `Images/TileSets/AbsoluteUnits/Units/Warrior-Amurites.png`
- Atlas: `warrioramurites.atlas` registered as `TileSets/AbsoluteUnits/Units/Warrior-Amurites`
- References from the FFH asset archive: `art/interface/buttons/units/warrior amurites.dds`; `art/units/civs/amurites/warrior/warrior_128.dds`; `art/units/civs/amurites/warrior/stone_axe.dds`
- Human warrior with weathered tan hide, brown hair and a stone axe.

## Scale, compatibility and scope

- Both sprites use **95×81-pixel transparent canvases**, with nearest-neighbor filtering and 36-color quantized opaque artwork, as in the Absolute Units native unit sprites.
- Clan warrior opaque bounds: x=64–88, y=14–60 (25×47).
- Amurites warrior opaque bounds: x=63–88, y=14–60 (26×47).
- Stock Warrior: x=58–85, y=15–59 (28×45); Goblin: x=55–88, y=14–60 (34×47). Differences accommodate the weapons and silhouettes.
- All atlas entries are in `Atlases.json`, including the existing Goblin. The image lookup uses the core Unciv civ-specific unit-image naming convention `Warrior-<civilization name>`, not a new gameplay unit or replacement.
- **No `unitset` is forced** in `jsons/ModOptions.json`. Original Warrior remains used for other civilizations, and users can switch between unit sets.
- Data paths and image dimensions are source-checked; the new sprites still require in-game validation.

