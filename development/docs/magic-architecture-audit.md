# Magic architecture audit — verified sources and implementation gates (2026-10-20)

## Safe baseline
- The working mod on `main` retains the four user-tested leader portraits and the existing Arcane Circle / Blooming Grove magic *prototypes*.
- `playable-0.1a` remains the independent rollback.
- Failed typed-mana and Fireball experiments survive on `backup-pre-magic-reset-20261020` only.
- This document changes **no gameplay**. New mechanics require an isolated proof branch before being merged.

## Original ExtraModMod mechanics — checked against source

Reference repository: [bewlay/extramodmod](https://github.com/bewlay/extramodmod), reference revision `60b0ec3740083162aaab7bf8491761a54a65a610`.

- [XML/Units/CIV4SpellInfos.xml](https://github.com/bewlay/extramodmod/blob/60b0ec3740083162aaab7bf8491761a54a65a610/XML/Units/CIV4SpellInfos.xml): `SPELL_FIREBALL` needs `PROMOTION_FIRE2`, creates `UNIT_FIREBALL` quantity 1, and has `bHasCasted=1`. There is no custom `PyRequirement` or `PyResult` for this spell.
- [XML/Units/CIV4PromotionInfos.xml](https://github.com/bewlay/extramodmod/blob/60b0ec3740083162aaab7bf8491761a54a65a610/XML/Units/CIV4PromotionInfos.xml): `PROMOTION_FIRE2` requires `PROMOTION_FIRE1` and `PROMOTION_CHANNELING2`. `PROMOTION_FIRE1` requires Fire mana and Channeling I.
- [XML/Units/CIV4UnitInfos.xml](https://github.com/bewlay/extramodmod/blob/60b0ec3740083162aaab7bf8491761a54a65a610/XML/Units/CIV4UnitInfos.xml): Fireball is not trainable (`iCost=-1`), moves 1, has 0 ordinary strength and 4 fire-type strength, suicide attacks, cannot capture, is first-strike immune, ignores terrain movement cost, carries Flying/Elemental/Fire Immunity, causes up to 30% damage on at most 4 collateral targets, and has 10% bombardment. The XML also gives `iCollateralDamage=50`.
- [CvGameCoreDLL/CvUnit.cpp](https://github.com/bewlay/extramodmod/blob/60b0ec3740083162aaab7bf8491761a54a65a610/CvGameCoreDLL/CvUnit.cpp): summons have a duration counter decremented in the unit's turn routine, and are killed when it reaches zero. The `SPELL_FIREBALL` XML creates a summon; confirm the precise initial duration in the spell-creation DLL logic before implementing expiration.

## Unciv implementation audit — from current engine source

Engine repository: [yairm210/Unciv](https://github.com/yairm210/Unciv).

- [UniqueType.kt](https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/UniqueType.kt) defines `Free [unit] appears` as a triggerable and `<for all movement>` as a unit-action modifier.
- [UnitActionsFromUniques.kt](https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/map/mapunit/actions/UnitActionsFromUniques.kt) converts a triggerable unique with a UnitActionModifier into a selectable unit action and passes the caster's tile to the trigger.
- [UniqueTriggerActivation.kt](https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/models/ruleset/unique/UniqueTriggerActivation.kt) places `Free [unit] appears` **at a city** when the caster's tile belongs to a city; only outside city territory does it use `placeUnitNearTile`. This conflicts with FFH2 summoning next to the caster.
- [UnitActionModifiers.kt](https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/map/mapunit/actions/UnitActionModifiers.kt) handles movement consumption and limits. `<once>` is lifetime-limited through `abilityToTimesUsed`, **not** once per turn; do not apply it to repeatable spells.
- [UnitTurnManager.kt](https://github.com/yairm210/Unciv/blob/master/core/src/com/unciv/logic/map/mapunit/UnitTurnManager.kt) executes unit triggers at turn start and turn end. `[This Unit] is destroyed <upon turn start>` is a potential expiration mechanism, but invoking destruction from turn processing must be tested before adoption.
- Standard Unciv JSON does not currently represent FFH2's separate fire-damage strength, capped collateral damage to 4 nearby units, or exact damage-type resistances. Do not silently claim a normal ranged attack is equivalent.

## Proof gates (in order)

1. **Unit action**: Isolate one `Free [Skeleton] appears <for all movement>` action on a development branch. Verify button availability and movement consumption with Mage/Wizard.
2. **Placement**: Test in open terrain, inside friendly city territory, and on a city tile. The current engine's city-placement behavior is a known blocker to an exact summon.
3. **Caster action budget**: Identify and prove a genuine once-per-turn limit; the `<once>` modifier is not valid for this.
4. **Expiration**: Verify a safe temporary-unit removal trigger, preferably one turn after summoning, and whether newly created units may act immediately.
5. **Combat**: Determine whether engine extension is required for melee Fireball behavior, ranged bombard/collateral, fire-type damage and damage cap. Record approximations explicitly.
6. **Only then integrate**: Complete mana nodes/typed mana, palace mana and promotion prerequisites before unlocking Fire II casting.

The official Unciv `mod-ci` validator checks structural/ruleset compatibility, **not** live action behavior. Android gameplay test remains mandatory.

## Status
- Verified: original Fireball's XML definition, basic Unciv trigger-action mechanism, lifetime meaning of `<once>`, and city-placement limitation.
- Pending: proof-branch static validation and Android testing, exact EMM summon-duration mechanics, true per-turn casting, temporary unit management and combat fidelity.
- Main's gameplay data is unchanged.
