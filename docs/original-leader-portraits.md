# Original FfH2 leader portraits — source mapping and import preparation

**Status: Source references mapped for all 19 playable leaders; actual portrait PNG artwork NOT YET IMPORTED.** This milestone is **not ready for gameplay verification** until the source art binaries are obtained.

## Verified Unciv asset format

Unciv loads leader portraits from `Images/LeaderIcons/<leaderName>.png`, with **exact** `leaderName` spelling and case from `jsons/Nations.json`. Its documentation recommends square images of approximately 100–256 pixels, with a transparent border. These images are used in first contact, diplomacy, Civilopedia and the nation picker.

Source: [Unciv official image documentation](https://github.com/yairm210/Unciv/blob/master/docs/Modders/Images-and-Audio.md#adding-leader-portraits).

## EMM source mappings

The [portrait manifest](data/emm-leader-portraits.json) maps each of the 19 current playable Unciv leaders to its original `ART_DEF_LEADER_*` entry and portrait DDS location in pinned EMM Continued's `XML/Art/CIV4ArtDefines_Leaderhead.xml`.

**The art defines are metadata, not the image files.** The pinned EMM GitHub repository does not contain the individual source DDS files in the referenced paths. In the original FfH2 distribution, standard art is packaged within FPK archives, so the corresponding asset archives (or their pre-extracted DDS contents) are needed. **No artwork has been invented, generated, or silently replaced.**

### Reproducible import

Once the **original FfH2 portrait DDS textures have been extracted from FPK**, place them in any local directory (with either their original path hierarchy or a flat list of DDS files), and run:

```bash
python3 -m pip install Pillow
python3 tools/import_ffh_leader_portraits.py /path/to/extracted/art
python3 tools/verify_leader_portraits.py --require-art
```

The import script creates 256×256 RGBA PNGs with a 10-pixel transparent border using each `NIF` portrait DDS (not the smaller `Button` icon). All 19 DDS source files are required by default before it writes anything. The `--allow-partial` flag enables deliberately importing fewer portraits. Existing PNGs are preserved unless `--overwrite` is supplied.

The automatic conversion supports DDS variants that the installed Pillow build can decode. An unusual DDS codec may require a separate DDS decoder; this will be reported rather than silently falling back to unrelated artwork.

The CI verifier checks names and manifest/source mappings now; once images are present, it validates their square PNG dimensions. `--require-art` fails if any source image is missing.

## Important source and attribution details

Kael encouraged modding FfH, but some original FfH2 2D art was contributed by or borrowed from third-party artists. Preserve all accompanying original asset attribution and any applicable licenses when importing originals. The mapping is source-verified; the ownership/licensing status of each individual image has not been separately audited.

## After import

1. Confirm there are exactly 19 genuine PNG files in `Images/LeaderIcons/`.
2. Refresh the mod in Unciv on Android.
3. Meet at least three leaders (e.g., Perpentach, Alexis, Falamar); each leader should display the corresponding original art beside their new dialogue.
4. Check portrait display in the nation picker, diplomacy screen and Civilopedia. Verify transparent borders, image alignment, and that no leader uses another leader's artwork.
5. Confirm the game's normal effects (Khazad Vaults, Lanun Pirate Cove, diplomacy strings, etc.) are unchanged.

**Next dependency:** Obtain the actual **original FfH2 FPK art archive or extracted source DDS textures**. The GitHub XML source alone cannot supply portrait image pixels.
