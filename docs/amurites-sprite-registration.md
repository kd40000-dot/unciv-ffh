# Amurites sprite atlas registration

Each Amurites sprite is packed as a standalone, single-page LibGDX atlas, following the working Goblin sprite registration.

The ten originally registered atlas regions are in `amuritesunit1.atlas`–`amuritesunit10.atlas`. New atlases `amuritesunit11.atlas`–`amuritesunit20.atlas` map to the following image keys:

- `amuritesunit11.atlas` → `TileSets/AbsoluteUnits/Units/Horseman-Amurites`
- `amuritesunit12.atlas` → `TileSets/AbsoluteUnits/Units/Horse Archer-Amurites`
- `amuritesunit13.atlas` → `TileSets/AbsoluteUnits/Units/Hunter-Amurites`
- `amuritesunit14.atlas` → `TileSets/AbsoluteUnits/Units/Immortal-Amurites`
- `amuritesunit15.atlas` → `TileSets/AbsoluteUnits/Units/Marksman-Amurites`
- `amuritesunit16.atlas` → `TileSets/AbsoluteUnits/Units/Phalanx-Amurites`
- `amuritesunit17.atlas` → `TileSets/AbsoluteUnits/Units/Ranger-Amurites`
- `amuritesunit18.atlas` → `TileSets/AbsoluteUnits/Units/Scout-Amurites`
- `amuritesunit19.atlas` → `TileSets/AbsoluteUnits/Units/Swordsman`
- `amuritesunit20.atlas` → `TileSets/AbsoluteUnits/Units/Wizard`

All atlas names are loaded by `Atlases.json`. Image dimensions are 95×81 and use nearest-neighbor filtering. Common units use the built-in `<Unit>-Amurites` civilization-specific lookup; `Swordsman` and `Wizard` are unique Amurites unit names. Govannon and Immortal need future unit definitions before they can appear as playable units.

The `unitset` setting is not overridden, and gameplay remains unchanged.
