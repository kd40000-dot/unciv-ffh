# Goblin sprite in Absolute Units

The Goblin is a Clan of Embers replacement for Scout. Unciv searches the active unit set for `TileSets/AbsoluteUnits/Units/Goblin`, then falls back to `Scout` when the region is missing.

**A PNG by itself is insufficient on Android.** Unciv loads image keys from packed `.atlas` files listed in `Atlases.json`. A loose PNG under `Images/TileSets/AbsoluteUnits/Units/` is not registered as a sprite.

For this unit, `goblin.atlas` maps the existing transparent 48×48 source `Images/TileSets/AbsoluteUnits/Units/Goblin.png` directly to the region name `TileSets/AbsoluteUnits/Units/Goblin`. `Atlases.json` lists `goblin` so Unciv loads the atlas alongside the existing portraits, emblems and tech artwork. This avoids repacking unrelated artwork.

Do **not** set `unitset` in `jsons/ModOptions.json`—that would override the user's unit-set choice.

Code references:
- `TileSetStrings.kt`: `unitsLocation = "TileSets/$unitSet/Units/"`; falls back to the replacement unit only when the Goblin region is missing.
- `ImageGetter.kt`: `loadModAtlases` loads only the atlases named in `Atlases.json`.

After installing the updated mod, restart Unciv with Absolute Units selected and pixel units enabled. This fix is source-validated but not yet game-tested.
