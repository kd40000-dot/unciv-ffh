# Building Civilopedia source-text audit — 2026-10-22

Source: ExtraModMod Continued at pinned commit `60b0ec3740083162aaab7bf8491761a54a65a610`, `XML/Text/Buildings.xml`.

**Goal:** Building/construction screen shows concise *mechanical effects* only (stats, cost, maintenance and visible uniques). The Civilopedia contains the source EMM background/history, not a new invented lore paragraph. Hidden implementation uniques stay hidden.

**Applied:** 25 exact-name `TXT_KEY_BUILDING_..._PEDIA` entries copied *verbatim in wording* from EMM English XML (with XML entity decoding and `[PARAGRAPH:1]` / `[TAB]` display controls converted to line breaks/spacing). Original gameplay effects in the mod were not altered. Warrens retains an additional adaptation note about building-versus-city maintenance; in-city tooltip still shows one concise `Comment` effect for duplication plus the real +10% building-upkeep unique and its 1-Gold cost.

## Buildings with original EMM Civilopedia background restored

Alchemy Lab, Aqueduct, Archery Range, Carnival, Command Post, Courthouse, Dungeon, Elder Council, Gambling House, Harbor, Hunting Lodge, Infirmary, Inn, Lighthouse, Mage Guild, Market, Monument, Pagan Temple, Shipyard, Smokehouse, Tavern, Theatre, Training Yard, Warrens, Sculptors Studio.

## Buildings without a confirmed exact PEDIA entry in the pinned XML/Text/Buildings.xml

Palace, Forge, Granary, Grove, Herbalist, Library, Moneychanger, Obsidian Gate, Palisade, Public Baths, Siege Workshop, Stable, Tax Office, Walls, Museum, Cave of Ancestors, Arena, Reliquary, Tavern Grigori, Forum, Grigori Museum, Temple Of The Hand, Dwarven Smithy, Harbor Lanun, Desert Shrine, Amurites Palace, Balseraphs Palace, Bannor Palace, Calabim Palace, Clan of Embers Palace, Doviello Palace, Elohim Palace, Grigori Palace, Hippus Palace, Illians Palace, Khazad Palace, Kuriotates Palace, Lanun Palace, Ljosalfar Palace, Luchuirp Palace, Malakim Palace, Sheaim Palace, Sidar Palace, Svartalfar Palace.

These currently retain their earlier Civilopedia text. They should be revisited for source aliases, other source XML files, or genuinely absent Pedia entries. **Do not describe these as verified EMM lore.** Generic nation palaces may have a shared source entry rather than separate national entries.

## Fidelity and UI caveats

- The EMM `_PEDIA` text is background/history, not a substitute for showing real gameplay effects. No generic descriptions have been added as visible city-screen comments except Warrens.
- Some buildings currently have unfinished EMM mechanics; city-screen stats/uniques reflect *current Unciv effects*, not ideal future EMM effects.
- For certain very long entries (Mage Guild, Monument, Pagan Temple, Theatre), the original full lore can be several thousand characters; test Civilopedia scroll/layout.
- The `Comment` unique placed on Warrens is only a display string; actual duplication continues to use 16 hidden one-time promotion triggers. The +10% building-maintenance effect is a workaround and does not equal EMM's total city-maintenance modifier.
- EMM source text may have other special game localization control tokens beyond `[PARAGRAPH:1]`, `[TAB]`, `[NEWLINE]`; review in-game formatting as necessary.

Rollback branch: `checkpoint/pre-emm-building-civilopedia-2026-10-22`.
