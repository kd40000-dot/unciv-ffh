# Amurites unit sprite atlas registration

The original ten-page `amuritesunits.atlas` is no longer loaded. The ten 95×81 PNGs remain unchanged. Each is now registered through its own single-page LibGDX atlas, matching the working Goblin and Warrior sprite layout.

- `amuritesunit1.atlas` → `TileSets/AbsoluteUnits/Units/Adept-Amurites`
- `amuritesunit2.atlas` → `TileSets/AbsoluteUnits/Units/Archer-Amurites`
- `amuritesunit3.atlas` → `TileSets/AbsoluteUnits/Units/Archmage-Amurites`
- `amuritesunit4.atlas` → `TileSets/AbsoluteUnits/Units/Beastmaster-Amurites`
- `amuritesunit5.atlas` → `TileSets/AbsoluteUnits/Units/Champion-Amurites`
- `amuritesunit6.atlas` → `TileSets/AbsoluteUnits/Units/Chanter`
- `amuritesunit7.atlas` → `TileSets/AbsoluteUnits/Units/Chariot-Amurites`
- `amuritesunit8.atlas` → `TileSets/AbsoluteUnits/Units/Crossbowman-Amurites`
- `amuritesunit9.atlas` → `TileSets/AbsoluteUnits/Units/Firebow`
- `amuritesunit10.atlas` → `TileSets/AbsoluteUnits/Units/Govannon`

Image lookup for standard units is civilization-specific by `<Unit>-Amurites`; the unique `Chanter` and `Firebow` units use their own exact names. `Govannon` artwork is registered but its ruleset unit remains unimplemented.

No gameplay changes, and no forced unit set. In-game verification pending.
