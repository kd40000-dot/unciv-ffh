# Fall from Heaven II / ExtraModMod for Unciv

A standalone **stock-Unciv-compatible base ruleset mod** bringing the civilizations, progression, mana, magic and strategic asymmetry of *Fall from Heaven II / ExtraModMod* to Unciv.

This GitHub repository is **mod data only**. It does not contain or require a customized Unciv APK or game-engine fork.

## Which version should I install?

- **Amurite Magic Foundation 0.2 (current gameplay test):** [download release](https://github.com/kd40000-dot/unciv-ffh/releases/tag/amurite-magic-foundation-02). Starts the actual mana economy and casting test.
- **Firebow Repair preview 1.2 (preserved artwork comparison):** [download release](https://github.com/kd40000-dot/unciv-ffh/releases/tag/firebow-repair-art-12). Its five units all cost 12 production for visual testing and it does **not** represent the actual progression.
- The `main` branch retains the earlier mod-only foundation. The rollback branch `playable-0.1a` has not been modified.

Install the gameplay ZIP in **Unciv → Mods → Download mod from URL**, and choose its base ruleset when **starting a new game**. Do not expect existing saves from artwork-preview rulesets to remain compatible.

## Magic Foundation 0.2 — what changed?

- Restore ExtraModMod unlocks/costs for Amurite **Adept, Wizard, Firebow, Chanter and Govannon** instead of easy-test unit production.
- Require **Knowledge of the Ether** and a **Mage Guild** for Adepts. Archery Range gates Firebows. Mage/Wizard are upgrade-focused rather than directly trainable.
- Amurites begin with **Body, Fire and Mind Mana**. Unciv can generate **Raw Mana** and Workers can build four types of attuned mana nodes.
- Sphere promotion choices (**Body I, Fire I, Mind I, Death I**) require their corresponding mana supply.
- **Body I grants a first experimental Haste unit action**, implemented as a temporary self-only movement status. This is **not** the original area spell and needs manual Android playtesting.
- The map sprites, icons, nation portrait and simple unit badges carry forward from the accepted artwork preview.

Read [Magic Foundation test scope, EMM source references and Android checklist](docs/MAGIC_0.2.md).

## Important limitations

This is an incremental mechanics test, not a finished Fall from Heaven port. The original sorcery technology OR-tree, exact level-four Mage/Wizard upgrade gate, Cave of Ancestors experience-per-mana, Spellstaff double-casting, Govannon teaching, Firebow's special fire effects, religions/alignment, world spells and global Armageddon effects are **not yet implemented**. The Mage Guild training XP is a deliberate playtest approximation.

Passing official Unciv `mod-ci` demonstrates ruleset consistency but **does not prove a spell action works in Android**. Please playtest and report which action buttons appear and whether the effects fire.

## References and project guidance

- [ExtraModMod original rules and implementation](https://github.com/bewlay/extramodmod)
- [Official Unciv modding guide](https://github.com/yairm210/Unciv/blob/master/docs/Modders/Mods.md) and [native uniques](https://github.com/yairm210/Unciv/blob/master/docs/Modders/uniques.md)
- [Project roadmap](docs/ROADMAP.md) and [native-mod-only architecture contract](docs/MODDING_BOUNDARY.md)
- [Amurite source audit](docs/AMURITES.md)
