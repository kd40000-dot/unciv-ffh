# Original Fall from Heaven technology icons

Imported **52 of 82** playable technologies directly from original DDS images in the user-provided `assets.zip` archive (extracted from `pak0.fpk`). These are 64×64 RGBA buttons, packed as `TechPortraits/<exact Unciv technology name>` into the separate `techart.png` / `techart.atlas` Android-compatible LibGDX atlas. Registered through `Atlases.json` alongside the existing leader and civilization emblem atlases.

Three original DDS names are deliberately mapped to their Unciv technology names: `leaves.dds` → **Way of the Forests**, `runes.dds` → **Way of the Earthmother**, and `overlords.dds` → **Message from the Deep**. All other 49 names match directly after case, spaces and punctuation normalization.

The other **30 technologies** do not have corresponding files in the source archive's `techtree` directory. We do not invent matches or replace them with unrelated art. Unciv will use its own available default tech icons where applicable. Their names are listed in [the mapping manifest](data/ffh-technology-icons.json).

This milestone changes only graphics/metadata, not technology rules or dependencies. Test the research tree and technology details on Android, including Ancient Chants, Knowledge of the Ether, Way of the Forests, and Way of the Earthmother. Existing leader portraits and civilization emblems should remain visible. In-game verification is pending.

## Contrast fix — October 21, 2026

The first Android gameplay screenshot showed the Mithril Weapons icon extremely dark, despite the original DDS being brightly colored. Unciv's `PortraitTech` applies a darkened era-color tint to `TechIcons`, which is appropriate for monochrome vector icons but destroys the legibility of imported full-color DDS artwork. The `Portrait` loader does **not** tint `TechPortraits`. Accordingly, the 52 atlas region names have been changed from `TechIcons/<name>` to `TechPortraits/<name>`, retaining the same `techart.png` pixels, atlas coordinates, and tech rules. Unciv continues to render these images in its circular tech UI, using the existing portrait sizing logic. Android confirmation of corrected contrast is pending.
