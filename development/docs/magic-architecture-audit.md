# Magic implementation audit — phase 0 (2026-10-20)

## Baseline and safeguards

- Main starts at portrait-tested commit `23b9eef4cbe5740d6057c0a93f5ab915fe71ac62`.
- The unsuccessful typed-mana/Fireball experiments are retained on `backup-pre-magic-reset-20261020`, not merged into main.
- Keep `playable-0.1a` untouched.
- No speculative gameplay changes should be made until the action semantics are demonstrated and tested.

## What the current ruleset actually does

- `jsons/Units.json`: Adept, Shaman, Mage, Wizard have an instant `Arcane Circle` improvement action; Mage/Wizard have `Channeling II`, Adept/Shaman have `Channeling I`.
- `jsons/UnitPromotions.json`: `Nature I` adds instant `Blooming Grove`; `Fire II` adds `[+1] Range` and **does not summon Fireball**.
- `jsons/TileResources.json`: one generic strategic `Mana` resource, generated on maps; no sphere-specific mana resources.
- `jsons/TileImprovements.json`: `Node of Mana` improves generic Mana, but no conversion mechanism.
- `jsons/ModOptions.json`: `isBaseRuleset: true`, `Disable religion`; no engine code or custom casting UI is present.

## Source-of-truth audit still required

Original FFH2/ExtraModMod installations are not present in this GitHub repository. Before claiming spell fidelity, extract and compare:
- `Assets/XML/Units/CIV4SpellInfos.xml` (spell definitions, prerequisites, flags, durations and costs).
- Promotion, bonus/mana, unit, civilization, building and technology XML.
- Python spell requirement/result callbacks and DLL-side spell mechanics.
- Any ExtraModMod changes to Fireball and sphere prerequisites.

Record exact source-file paths and version identifiers. The wiki is secondary reference material only.

## Architecture questions and proof gates

1. Verify the actual Unciv version used on Android and the precise engine UniqueTypes and trigger syntax. Do not assume an undocumented summon string works.
2. Create a minimal isolated test ruleset (not the main mod) proving that a promotion can expose a player-selectable unit action which spawns a specified unit.
3. Verify unit placement, movement consumption, once-per-turn limits, projectile control, ranged attack, removal on attack, and expiration on end turn.
4. If any critical behavior cannot be expressed in vanilla Unciv JSON, identify the minimal engine change and its maintenance/Android implications before coding it.
5. Once proven, implement mana prerequisites and channeling progression, then Fireball against the original EMM specification.

## Acceptance criteria for Fireball

- Only an eligible caster with Fire II can cast.
- Casting is explicitly selectable and has a clear per-turn cost.
- The projectile appears legally, can be directed to a target, attacks at the intended range, and is consumed correctly.
- Lifetime and repeated casting obey verified original-game rules.
- Normal units cannot build Fireball in a city.
- Mod loads in Unciv with no ruleset errors; behavior is tested on Android.

## Current outcome

Audit of our mod is complete; verification against EMM source and a working engine-action proof is pending. **No Fireball implementation has been reintroduced.**
