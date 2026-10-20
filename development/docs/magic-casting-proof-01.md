# Casting proof 01 — selectable summon action (DEVELOPMENT ONLY)

This branch deliberately **does not** implement Fireball. It tests the fundamental user action in a safe isolated environment.

## Changes limited to this branch
- New `Casting Probe` promotion, usable by the custom Mage unit type, prerequisite `Channeling II`.
- The promotion grants the Unciv-supported unit action: `Free [Skeleton] appears <for all movement>`.
- Newly created Mage and Amurite Wizard units receive the promotion for convenient testing.
- The pre-existing Skeleton unit already has a unit definition and image; no new projectile art or Fireball unit has been added.
- Original `Fire II`, mana nodes, leader portraits, and the playable `main` branch are not modified.

## Why this syntax
The current Unciv engine converts triggerables having UnitActionModifier conditionals into a selectable action:
- `UnitActionsFromUniques.getTriggerUniqueActions` checks `UniqueTarget.UnitActionModifier`, `unique.isTriggerable`, and movement.
- `UniqueTriggerActivation.getTriggerFunction` recognizes `Free [unit] appears`.
- `UnitActionModifiers.activateSideEffects` consumes movement for `<for all movement>`.

The modifier `<once>` is deliberately *absent*: it limits a unit's lifetime use, not once per turn.

## How to install without overwriting the working mod
Unciv's Mod Manager supports **Download mod from URL** with direct ZIP URLs, according to the official modding guide:
`https://github.com/yairm210/Unciv/blob/master/docs/Modders/Mods.md`.

Development branch ZIP:
`https://github.com/kd40000-dot/unciv-ffh/archive/refs/heads/magic-casting-proof-01.zip`

Use **Mods → Download mod from URL** and paste that URL. The downloaded branch should be installed separately; confirm it has a distinct name before enabling it. Do not uninstall the regular `unciv-ffh` mod.

## Manual acceptance checks
1. On a new test game with the branch variant, research `Sorcery`, make a Mage or Amurite Wizard.
2. Select the caster, open its actions, and verify the `Free Skeleton appears` action is offered.
3. Use it and check that a Skeleton appears, the caster loses all available movement and **the caster** remains.
4. Begin a new turn and see whether the action is usable again (repeatable). It must not become permanently exhausted.
5. Repeat with a caster **outside all city territory**. Record whether the unit appears beside the caster.
6. Repeat inside a friendly city's borders but **away from the city center**. The current Unciv source suggests the spawned unit may appear *in the city instead*. Record the actual tile.
7. Attempt to cast when there is no legal space for a new military unit. Record if the action remains available and whether movement is consumed on failed placement.

## Expected / intentionally untested
- The free-unit action's placement favors `addUnit(..., chosenCity)` when the caster's tile has a relevant city; exact Fireball placement is therefore **not yet solved**.
- This proof intentionally does not test duration, fire damage, collateral, city bombardment, Fire II access, mana gating or turn-based casting budgets.
- GitHub Actions `Validate Ruleset JSON` checks JSON and `mod-ci` syntax compatibility. It does **not** prove that the action works in play.

## Exit criteria
Only after action existence, repeated use and movement cost are observed in Android gameplay should this implementation be used as a building block. If city-border summoning deviates from FFH2, make a targeted engine patch rather than a location-dependent compromise.
