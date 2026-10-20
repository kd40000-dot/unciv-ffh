# FFH2/ExtraModMod — civilization-first mod roadmap

## Goal

A **complete, faithful, playable base-ruleset mod** for stock Unciv on Android and desktop. The player should *feel* the distinctive strategic choices of each civilization, not just recognize its units' names or colors. Every native JSON mechanism is considered before any game-engine extension. A missing engine feature is logged, not silently substituted with an unrelated bonus.

## Phase 0 — New standalone mod foundation (this commit)

- Independent mod-only repository tree, `isBaseRuleset: true`, no Unciv engine sources, no inherited prototype art or JSON.
- Two initial civilization identities: Amurites (Valledia) and Bannor (Sabathiel).
- An intentionally small neutral world, economy, and military scaffold; **not a recreation of FFH gameplay yet**.
- CI verifies JSON and invokes official Unciv `mod-ci`.
- Archive branches remain available for recovery, not as gameplay dependencies.

## Phase 1 — Civilizations as integrated game systems

Work through the original EMM definitions and connected mechanisms before treating a civilization as completed.

### Amurites
- Civilization-specific starting technologies and palace effects.
- Wizard, Firebow, Chanter, and other documented unit replacements.
- Cave of Ancestors, magic-oriented production/training, mana interactions and promotions.
- Govannon and the mechanics that let the Amurites spread arcane training.
- Arcane Lacuna (only when a proper global spell action exists).
- Leaders' traits, art and Civilopedia once source-verified and rights-cleared.

### Bannor
- Starting technology, palace, and Guardsman civilization trait.
- Donal Lugh, defensive institutions, and historical Bannor troop roster.
- Fanaticism → Crusade civic, its **benefits and restrictions**, conscription/recruitment, and ending Crusade.
- Rally world spell and its precise requirements and results.
- Leaders' traits, art, Civilopedia and AI incentives.

Each feature receives: EMM source path(s) → intended gameplay behavior → Unciv native unique(s) or blocking constraint → validator/test result → player-observable acceptance check.

## Phase 2 — Expand to all original major civilizations

Implement the actual defining mechanics, assets, units, buildings, and faction asymmetries of each civ: Ljosalfar, Clan of Embers, and the remaining original EMM roster. Do not insert empty nation placeholders just to increase a counter. Introduce shared mechanics when the currently targeted civ needs them.

## Phase 3 — Connected Erebus systems

Complete the shared FFH2 technology tree, civics, religion/alignment, mana node improvements and sphere resources, promotion trees, heroes, rituals, world spells, unique terrain/resources, event system, global counters/Armageddon, diplomacy and AI behavior. This is ongoing alongside civ slices, not isolated prototype work.

## Phase 4 — Graphics, audio, scenario compatibility and release

Import properly sourced, license-compatible FFH2/EMM assets where permission allows. Build transparent attribution and Android texture atlases. Test a variety of maps and games, all implemented factions, and no ruleset warnings. Publish stable installable releases with clear change logs.

## Milestone acceptance policy

- Native JSON rules first; test edge cases (ownership, turn timing, stacking, UI, AI and saves).
- Do not describe a placeholder effect as canonical FFH2.
- No custom Unciv APK, Kotlin fork or game patch while modding paths remain viable.
- Record blocked mechanics in `docs/MODDING_BOUNDARY.md`; evaluate engine changes **only** if a significant gameplay requirement cannot be built or convincingly expressed using supported mod rules.
- Preserve a known-working release before any substantial mechanics or artwork changes.
