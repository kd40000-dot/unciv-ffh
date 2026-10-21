# Erebus civilization emblems — original FfH2 flags

**Status (October 21, 2026):** The 19 original FfH2 team-color flag symbols have been converted to clean, transparent Unciv `NationIcons`, with Android-ready texture atlas files. **Gameplay test of this new version pending.** The preceding round-badge version was visually accepted by the user and remains available in Git history.

## Original asset provenance

Source: user-provided `assets.zip` extracted from `pak0.fpk`, specifically the 19 files `art/interface/teamcolor/<civ>flag.dds`. These paths correspond to the source FfH/EMM civilization art definitions. The 19 original DDS files (128×128) are mapped by exact filename and SHA-256 in [the asset provenance ledger](data/erebus-civilization-emblems.json). The archive is not included in the GitHub repository because it is large (approximately 145 MB). This archive is a user-supplied extract, so exact byte-for-byte identity to the pinned EMM Continued release's source assets has not been separately verified.

## Why `NationIcons` instead of `NationPortraits`

The original icons were 64×64 WebP copies of Civ4 faction **buttons**, which contain backgrounds and borders. Unciv's `NationPortraits` bypasses faction tinting and therefore preserved the old colored discs. The new images are taken from the original Civ4 **flags**, which are white symbols with transparent alpha masks: `Images.Emblems/NationIcons/<exact nation>.png`. Unciv automatically tints `NationIcons` by a faction's inner color and supplies the familiar circular faction-colored backing. This removes the extra button background and frame altogether without altering any nation color or game rules.

Each symbol is extracted from a 128×128 source DDS, cropped to its nontransparent content, fit into a 120×120 rectangle without changing its aspect ratio, and centered in a 128×128 RGBA PNG. It has transparent corners and no embedded icon border or colored disc. Three special original-alpha cases were corrected without guessing colors:

- **Calabim** and **Illians**: original DDS uses an inverse alpha mask (opaque background); alpha is inverted to recover the symbol.
- **Elohim**: the source has unwanted opaque top and bottom strips (rows 0–15 and 112–127); they are removed.

All 19 files are packed into `emblems.png` (1024×512 RGBA), described by `emblems.atlas` using `NationIcons/<exact nation>` region names. Root `Atlases.json` includes both `game` (the already gameplay-verified 19 leader portraits) and `emblems`. The old `Images.Emblems/NationPortraits/` source PNGs are deleted, preventing future asset rebuilds from resurrecting the older round badges. `game.png`, `game.atlas` and all gameplay data are unchanged.

## Regeneration and checks

On desktop with Pillow installed:

```sh
python3 -m pip install Pillow
python3 tools/pack_original_civ_emblems.py /path/to/assets.zip
python3 tools/verify_civilization_emblems.py
```

CI runs the verification script (standard-library only) and checks all 19 exact nation names, PNG dimensions/CRC, the packed atlas regions, non-overlapping region bounds, the absence of old `NationPortraits`, and the continued registration of the leader atlas. The original asset ZIP is required **only to regenerate** the art; CI can verify the already committed PNGs without it.

## Android test plan

Update the mod from GitHub, reopen the nation selection screen and inspect several factions (especially Calabim, Elohim and Illians). Each should show **only its native Unciv colored circle and the large clean faction symbol**, without the extra colored disc, square badge or accidental bars. Confirm leader portraits still display correctly. This is a graphics-only update; game mechanics, names, and diplomacy have not changed.

The earlier circular-button version was confirmed working by the user on October 21, 2026, but the new original-flag artwork is still pending Android confirmation.
