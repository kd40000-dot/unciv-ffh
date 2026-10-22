# Arena implementation (2026-10-22)

Source: ExtraModMod Continued pinned commit `60b0ec3740083162aaab7bf8491761a54a65a610`.

- `python/entrypoints/CvSpellInterface.py`: `reqArenaBattle` and `spellArenaBattle`.
- `XML/Units/CIV4SpellInfos.xml`: `SPELL_ARENA_BATTLE` requires `BUILDING_ARENA` and location in city; consumes the caster's ability for the turn.
- `XML/Text/Buildings.xml`: `TXT_KEY_BUILDING_ARENA` exists but **no exact `TXT_KEY_BUILDING_ARENA_PEDIA` entry** in this source file. Do not claim the Civilopedia narrative in this mod is an original verbatim EMM entry.

## Original EMM gameplay

Balseraph Arena replaces Training Yard. Player-controlled melee or recon units and slaves can participate in Arena Battle in an Arena city. Each battle extends the city's happiness timer by 3. The unit has 50% chance of victory: on victory gets uniformly randomized 1–6 XP and is **set to 25 damage** (not necessarily 25 additional damage). On loss the unit is killed. A winning slave converts into a Warrior. AI only uses the spell on units below level 4 with Weak promotion.

## Current Unciv JSON implementation

- Preserve existing Arena's +2 starting XP for Sword units.
- Add a concise *city-screen* `Comment` unique documenting Arena Battle and its risk.
- Sword and Scout unit types gain a local Arena Battle action via a trigger unique conditioned on being in a city with an Arena; it consumes all movement to use.
- This action grants a temporary `Arena Battle` promotion; the promotion instant effects randomly add the temporary `Arena Victory` status with 50% chance; while status is present, grant +3 XP and take 25 damage; without the status, destroy the unit. Status cleaned up afterwards. Both promotions are implementation-only; the fight event is invoked when the player chooses the action.
- Initial source parity is **approximate, not exact**: +3 XP fixed instead of randomized 1–6 XP; 25 **additional** damage rather than setting damage to 25; no city happiness timer; no slave implementation (the current mod has no Slave unit); AI criteria not reproduced.

## Test cases / questions

1. Confirm an eligible Balseraph Sword or Scout unit physically standing in a city with an Arena has an **Arena Battle** action. Check the action has a readable name/icon, doesn't obscure other actions, and consumes movement.
2. Confirm another civilization, or a unit outside an Arena city, has no Arena Battle action.
3. Confirm one random outcome per click; surviving units gain exactly 3 XP and take 25 additional damage. Losing units die. Watch for accidental second rerolls or promotion retention/repeatability.
4. Confirm the promotion-side immediate effect order and status condition evaluation occur as expected in the installed Unciv version.
5. Confirm unit actions added to UnitTypes do not cause validation errors, and `<in cities with a [Arena]>` resolves the unit's present city.
6. Find an engine-independent way to replicate 1–6 XP roll, damage **set** to 25, 3-turn city happiness timer, conversion for slave winners, and AI restrictions. Keep these in the fidelity backlog.

**Important:** The changes are source-derived and structurally valid JSON, but not yet in-game tested. Unlike Warrens, failure to evaluate conditions in the expected order could produce incorrect or lethal effects; try in a disposable test save first.
