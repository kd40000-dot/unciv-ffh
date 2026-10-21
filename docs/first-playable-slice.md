# First early-game ruleset slice

This standalone Unciv **base ruleset** is an early **unplaytested gameplay candidate**, not a completed EMM Continued port.

## Included

- 4 EMM nations: Amurites, Bannor, Clan of Embers, Ljosalfar. Leaders and ordered English city names sourced from EMM XML.
- 82 EMM researchable technologies, source-derived costs and original tree positions; see [technology conversion](technology-tree.md).
- 50 source-derived units and 40 buildings; see [conversion report](units-and-buildings.md).
- Domination victory and early exploration ruins.

Unit and building research prerequisites, production costs, movement and basic combat values now come from EMM XML. Combat promotions, upgrades and selected strategic resource requirements are now implemented, with documented limits. Spells and many unique effects are still unimplemented.

## Install and test

1. Open Unciv → **Mods** → **Download mod from URL**.
2. Enter `https://github.com/kd40000-dot/unciv-ffh`.
3. Start a new game with the `unciv ffh` base ruleset and choose one of the four nations.
4. Test generated maps, settler founding, research, worker improvements, recruitment, combat, turn progression and victory.
5. Run **Options → Locate mod errors**, and report any engine validator errors.

**Validation:** JSON syntax, source-fidelity scripts, and Unciv's official `mod-ci` ruleset validator passed without gameplay-definition warnings. **Android gameplay and multi-turn AI testing remain outstanding**.

## Provenance and licensing

- EMM Continued data: [bewlay/extramodmod](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610), `CIV4CivilizationInfos.xml`, `CIV4TechInfos.xml`, `CIV4UnitInfos.xml`, `CIV4BuildingInfos.xml`, relevant class XML, and `XML/Text/Civilizations.xml`.
- Temporary map resource/terrain/improvement and barbarian scaffolding adapted from [Unciv Civ V - Vanilla](https://github.com/yairm210/Unciv/tree/master/android/assets/jsons/Civ%20V%20-%20Vanilla), [MPL-2.0](https://github.com/yairm210/Unciv/blob/master/LICENSE).
- No original EMM art, binaries, or audio redistributed.

## Engine validation

Unciv `mod-ci` initially reported missing promotion and ruin references; these are now defined explicitly. An automated Unciv engine check runs on every push at [GitHub Actions](https://github.com/kd40000-dot/unciv-ffh/actions).

## Missing

Religions, alignment, world spells, mana nodes, mage spell effects, heroes, lairs, armageddon, civics, and full unique civilization abilities are not implemented. Android validation, gameplay balance, and AI behavior remain untested.
