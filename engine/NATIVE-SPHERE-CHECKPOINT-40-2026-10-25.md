# Native spell wiring checkpoint: 40 actions (2026-10-25)

This is an experimental engine branch, not the standard mod. The playable `main` branch and earlier checkpoints are preserved.

## Changes in this batch
- Migrated Chaos II Mutation, Force I Temperance, Nature II Poisoned Blade, and Shadow II Shadowwalk from caster-local JSON proxy actions to native `Can cast EMM spell` registry entries.
- Created recipient-targeted definitions using explicit living, land and Sword filters. Poisoned Blade status now affects each recipient instead of radiating from the caster.
- Added source-catalog links and regression assertions for all four definitions.

## EMM fidelity warnings
These entries currently execute **approximations**, not fully faithful EMM behavior:
- Mutation: a fixed 2-turn +20% attacking / -20% defending Strength status; original randomized mutation effects are not implemented.
- Temperance: a fixed 2-turn +20% defending Strength proxy; source spell protection / restrictions require verification.
- Poisoned Blade: a fixed 2-turn +15% Strength status on nearby Sword units; original poisoned weapon damage type and appropriate lifetimes are unimplemented.
- Shadowwalk: a fixed 2-turn city-combat +20% Strength status to nearby land units; original stealth and movement rules are not implemented.

## Validation
Connector-side structural audit on committed files found 355 source entries, 40 native registry entries, and 40 matching promotion grants, with no orphaned records. Python regression assertions committed but no successful Actions run, Kotlin compilation, APK, or gameplay verification is claimed.

Next priority: accurate source-based duration, native terrain/city and equipment effects, target choice, resistance and status cleanup. Do not count these approximations as EMM-exact.
