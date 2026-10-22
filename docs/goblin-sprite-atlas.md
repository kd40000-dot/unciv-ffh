# Goblin sprite in Absolute Units

The Clan of Embers Goblin replaces Scout. Unciv looks up `TileSets/AbsoluteUnits/Units/Goblin` and uses the Scout art only if the Goblin atlas region is absent.

## New artwork

The Goblin now uses newly developed, original pixel sprite art informed by the Goblin button and texture references in the user-provided Fall from Heaven `assets.zip`, rather than directly displaying a DDS-derived Goblin button. It features green skin, pointed ears, spear, red shield and rough armor.

The file matches Unciv's stock **Absolute Units** layout:

- Transparent **95×81 pixel canvas**.
- Character footprint **34×47 pixels**, aligned x=55–88 and y=14–60. For comparison the stock Scout occupies x=62–85 and y=14–59 and Warrior occupies x=58–85 and y=15–59; the Goblin's wider footprint accommodates its spear, shield and ears.
- **37 opaque colors**, hard-edge transparency, nearest-neighbor pixel filtering.
- PNG path: `Images/TileSets/AbsoluteUnits/Units/Goblin.png`.
- `goblin.atlas` continues to register `TileSets/AbsoluteUnits/Units/Goblin`, now at **95×81**, and is loaded through the existing `Atlases.json` entry.

No gameplay/ruleset changes and no `unitset` override in `jsons/ModOptions.json`; the user can keep Absolute Units or select other unit sets. Dimensions, palette, alpha and atlas registration have been checked; in-game rendering of the revised art is not yet verified.
