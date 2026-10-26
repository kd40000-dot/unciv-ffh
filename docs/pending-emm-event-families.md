# Pending Armageddon-related random-event families (2026-10-26)

The pinned EMM catalog contains 23 families. The project's 2026-10-26
fidelity audit records ten playable families: Demonic Tome, Holy Child,
Sobs, War Games, Witch, Shrine of Camulos, Iron Orb, Strange Adept,
Necro-Cannibalism and Winds from Hell.

## Thirteen source-indexed families still requiring implementation

- Angelic Procession
- Elohim Hallowing
- Mystic Tree
- Orphanage Fire
- Sheaim Elegy
- Two-Headed Cow
- Lunatic — requires `canTriggerLunaticCity`
- Trapped Frostlings — requires `CanTriggerTrappedFrostlings`
- Demon Sign — requires `CanTriggerDemonSign`
- Ash Cough
- Dead Angel
- Depressed Toymaker
- Haunted Castle — requires `canTriggerPlotEmpty`

Source record: `docs/data/emm-armageddon-event-triggers.json` pinned to
EMM commit `60b0ec3740083162aaab7bf8491761a54a65a610`.

A trigger must only be enabled after all relevant XML effects, candidate
city/plot/unit eligibility, Python conditions, choice gating, AI handling,
and save/clone targets have complete runtime behavior. This ledger does
not claim the other choices in the ten active families are implemented.

## Epidemic build status

`tools/patch_emm_epidemic_damage.py` runs after the health patcher in
`.github/workflows/build-emm-epidemic.yml`. Its 25 HP raw damage is a
**temporary approximation** of EMM's typed Death damage and `isAlive()`.
Neither a successful workflow build nor gameplay acceptance was established
when this ledger was written. The 35% F13 fidelity estimate is unchanged.
