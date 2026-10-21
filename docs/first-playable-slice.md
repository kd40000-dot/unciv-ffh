# First early-game ruleset slice

This standalone Unciv **base ruleset** is an early **unplaytested gameplay candidate**, not a completed EMM Continued port.

## Included

- 4 EMM nations: Amurites, Bannor, Clan of Embers, Ljosalfar. Leaders and ordered English city names sourced from EMM XML.
- 13 early EMM technologies, retaining source names and research costs. **OR prerequisite groups** are reduced to the first supported alternative for Unciv's AND-only tech tree.
- 12 prototype units, 12 prototype buildings, 13 resources, 13 improvements, and 29 Unciv terrain entries for map generation.
- Domination victory and early exploration ruins.

Unit and building combat/economic statistics and unique faction substitutions are **prototypes, not source-faithful EMM conversions**. Initial Adept has a ranged placeholder attack and **no spellcasting**.

## Install and test

1. Open Unciv → **Mods** → **Download mod from URL**.
2. Enter `https://github.com/kd40000-dot/unciv-ffh`.
3. Start a new game with the `unciv ffh` base ruleset and choose one of the four nations.
4. Test generated maps, settler founding, research, worker improvements, recruitment, combat, turn progression and victory.
5. Run **Options → Locate mod errors**, and report any engine validator errors.

**Important:** Programmatic JSON syntax and reference checks have been run, but full Unciv engine validation and Android playtesting have not yet been completed.

## Provenance and licensing

- EMM Continued data: [bewlay/extramodmod](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610), `CIV4CivilizationInfos.xml`, `CIV4TechInfos.xml`, and `XML/Text/Civilizations.xml`.
- Temporary map resource/terrain/improvement and barbarian scaffolding adapted from [Unciv Civ V - Vanilla](https://github.com/yairm210/Unciv/tree/master/android/assets/jsons/Civ%20V%20-%20Vanilla), [MPL-2.0](https://github.com/yairm210/Unciv/blob/master/LICENSE).
- No original EMM art, binaries, or audio redistributed.

## Missing

Religions, alignment, world spells, mana nodes, mage spell effects, heroes, lairs, armageddon, civics, and full unique civilization abilities are not implemented. Android validation, gameplay balance, and AI behavior remain untested.
