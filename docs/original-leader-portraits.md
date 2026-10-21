# Original FfH2 leader portraits — source mapping and import preparation

**Status: All 19 portraits imported and the missing Unciv runtime atlas now provided (`game.png`, `game.atlas`, `Atlases.json`). Android retest pending.**

## Verified Unciv asset format

Unciv loads leader portraits from `Images/LeaderIcons/<leaderName>.png`, with **exact** `leaderName` spelling and case from `jsons/Nations.json`. Its documentation recommends square images of approximately 100–256 pixels, with a transparent border. These images are used in first contact, diplomacy, Civilopedia and the nation picker.

Source: [Unciv official image documentation](https://github.com/yairm210/Unciv/blob/master/docs/Modders/Images-and-Audio.md#adding-leader-portraits).

## EMM source mappings

The [portrait manifest](data/emm-leader-portraits.json) maps each of the 19 current playable Unciv leaders to its original `ART_DEF_LEADER_*` entry and portrait DDS location in pinned EMM Continued's `XML/Art/CIV4ArtDefines_Leaderhead.xml`.

**The art defines are metadata, not the image files.** The pinned EMM GitHub repository does not contain the individual source DDS files in the referenced paths. The user supplied `LeaderPortraits.zip` containing 19 labeled WEBP portraits instead of DDS files, and these were converted to square RGBA PNG with transparent padding. The source DDS filenames remain in the manifest for traceability; **the supplied WEBP imagery has not been independently proven pixel-identical to the original DDS archives**. No replacement art was invented or generated.

### Imported portrait files

All 19 submitted WEBP files were converted into 256×256 RGBA PNGs with 10px padding, retaining their artwork without inventing missing pixels. Filenames match the exact `leaderName` in the Nation roster. The converted PNGs are committed under `Images/LeaderIcons/` and should be recognized in diplomacy, first contact, Civilopedia and nation selection.

### Reproducible import from original DDS archives

Once the **original FfH2 portrait DDS textures have been extracted from FPK**, place them in any local directory (with either their original path hierarchy or a flat list of DDS files), and run:

```bash
python3 -m pip install Pillow
python3 tools/import_ffh_leader_portraits.py /path/to/extracted/art
python3 tools/verify_leader_portraits.py --require-art
```

The import script creates 256×256 RGBA PNGs with a 10-pixel transparent border using each `NIF` portrait DDS (not the smaller `Button` icon). All 19 DDS source files are required by default before it writes anything. The `--allow-partial` flag enables deliberately importing fewer portraits. Existing PNGs are preserved unless `--overwrite` is supplied.

The automatic conversion supports DDS variants that the installed Pillow build can decode. An unusual DDS codec may require a separate DDS decoder; this will be reported rather than silently falling back to unrelated artwork.

The CI verifier checks names, manifest/source mappings and the installed PNG image dimensions. `--require-art` now passes when all 19 images are present.

## Important source and attribution details

Kael encouraged modding FfH, but some original FfH2 2D art was contributed by or borrowed from third-party artists. Preserve all accompanying original asset attribution and any applicable licenses when importing originals. The mapping is source-verified; the ownership/licensing status of each individual image has not been separately audited.

## After import

1. Confirm there are exactly 19 genuine PNG files in `Images/LeaderIcons/`.
2. Refresh the mod in Unciv on Android.
3. Meet at least three leaders (e.g., Perpentach, Alexis, Falamar); each leader should display the corresponding original art beside their new dialogue.
4. Check portrait display in the nation picker, diplomacy screen and Civilopedia. Verify transparent borders, image alignment, and that no leader uses another leader's artwork.
5. Confirm the game's normal effects (Khazad Vaults, Lanun Pirate Cove, diplomacy strings, etc.) are unchanged.

**Next dependency:** Android gameplay verification of the 19 installed images in first contact, diplomacy, Civilopedia and nation selection. If any portrait mismatches the intended leader or differs from the desired original DDS art, it can be replaced individually.

## Android portrait-loading fix — October 21, 2026

The user reported that portraits did not appear in nation selection, first contact or diplomacy after the first image-only commit. We traced this to **absent packed texture atlas files**, not the leader names. On Android, Unciv reads the mod's packed texture atlas, not the individual source PNGs; a desktop Unciv installation can generate the atlas, but Android cannot.

This repository now includes a `game.atlas` defining **19** `LeaderIcons/<leaderName>` regions, the accompanying `game.png` texture page and `Atlases.json` containing `["game"]`. A 1024×1024 RGBA page contains 19 160×160 sprites with padding; source images stay at 256×256 in `Images/LeaderIcons/`. The image identifiers match `Nation.leaderName` exactly and are loaded automatically by `ImageGetter.loadModAtlases()`.

To rebuild on a computer: `python3 -m pip install Pillow && python3 tools/pack_leader_atlas.py`. CI runs `python3 tools/verify_leader_atlas.py` to ensure the texture page is valid and all expected leader names occur in the atlas. **In-game success must still be confirmed after updating the mod.**
