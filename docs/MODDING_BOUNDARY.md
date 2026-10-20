# Modding-first architecture contract

**Delivery target:** stock Unciv's mod manager. The repository is a base-ruleset mod, not the Unciv game.

## Allowed
- `jsons/` definitions for civilizations, cities, units, unit types, promotions, improvements, resources, technologies, eras, buildings, policies/civics and religions.
- Documented native Unciv `uniques`, including unit actions and trigger conditions, tested for actual gameplay behavior rather than just syntactic validation.
- `Images/`, texture atlases, audiovisual files and maps when properly sourced and built.
- Mod-only GitHub Actions for static validation and artwork processing.

## Not in scope unless all usable modding options are exhausted
- Editing Unciv Kotlin/Java engine or app UI.
- A custom Android APK or separate Unciv build for playing FFH.
- Forking the upstream game to add isolated spells.
- Unverified or invented unit action syntax masquerading as a working spell.

## Source-of-truth order
1. Exact original EMM XML/Python/DLL definitions (https://github.com/bewlay/extramodmod).
2. Earlier FFH2 definitions if EMM does not modify them.
3. Unciv's code and generated unique documentation (https://github.com/yairm210/Unciv).
4. Wiki descriptions only as supporting background.

## Capability audit workflow
For each mechanic, document whether it is (A) exact with JSON, (B) exact with supported native uniques and tested triggers, (C) an explicitly described approximation that preserves intended player decisions, or (D) blocked. Keep blocked mechanics on a centralized list. Only after testing multiple mod-side approaches and assessing gameplay importance should we *discuss* an engine extension.

## Current limitations
Phase 0 is a fresh structural scaffold. It deliberately does **not** claim working mana conversion, spellcasting, religion, Crusade, Arcane Lacuna, world spells, heroes, or FFH damage types. The two starting technology differences are drawn from EMM `XML/Civilizations/CIV4CivilizationInfos.xml`.
