# Original Fall from Heaven technology icons

Imported **52 of 82** playable technologies directly from original DDS images in the user-provided `assets.zip` archive (extracted from `pak0.fpk`). These are 64×64 RGBA buttons, packed as `TechIcons/<exact Unciv technology name>` into the separate `techart.png` / `techart.atlas` Android-compatible LibGDX atlas. Registered through `Atlases.json` alongside the existing leader and civilization emblem atlases.

Three original DDS names are deliberately mapped to their Unciv technology names: `leaves.dds` → **Way of the Forests**, `runes.dds` → **Way of the Earthmother**, and `overlords.dds` → **Message from the Deep**. All other 49 names match directly after case, spaces and punctuation normalization.

The other **30 technologies** do not have corresponding files in the source archive's `techtree` directory. We do not invent matches or replace them with unrelated art. Unciv will use its own available default tech icons where applicable. Their names are listed in [the mapping manifest](data/ffh-technology-icons.json).

This milestone changes only graphics/metadata, not technology rules or dependencies. Test the research tree and technology details on Android, including Ancient Chants, Knowledge of the Ether, Way of the Forests, and Way of the Earthmother. Existing leader portraits and civilization emblems should remain visible. In-game verification is pending.
