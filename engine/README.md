# EMM-native Unciv engine track

**Status:** separate proof-of-concept engine build; not yet an Android-certified release.

## Where it lives

- Mod main branch and the frozen `magic-test-2026-10-24` branch remain unchanged.
- Engine work is isolated in `feature/emm-engine-2026-10-25`.
- The GitHub app can write branches and CI but cannot directly create a new repository/fork. Until a dedicated engine fork is created, the `engine/` directory carries an **overlay** against a PINNED upstream Unciv source revision, not a complete checked-in copy of Unciv.
- `engine/apply_overlay.py` validates upstream commit `b5c4bccd2b038f49183338811dc30efec81cb105` and exact source-code anchors, then adds a native Kotlin EMM executor plus registered action/unique.
- Workflow `.github/workflows/emm-engine.yml` checks out upstream, applies overlay, compiles core and builds an Android test APK.
- APK application ID `com.unciv.emm` is distinct from regular `com.unciv.app`. The first APK will use upstream's existing debug signing; production signing and long-term key custody remain TODO.
- The mod uses `Can cast EMM spell [Haste]` on Body I. This is an **engine-only** unique: **do not install this branch into stock Unciv**. Stock Unciv does not recognize it.

## Design principles

1. EMM's pinned `CIV4SpellInfos.xml`, `CIV4PromotionInfos.xml`, Python event code and current EMM gameplay remain source-of-truth; our 82-spell parity audit remains the regression backlog.
2. Spell eligibility, target enumeration, effects, AI eligibility, resistance and expiration belong to a single reusable engine framework, not unrelated self-buffs in JSON.
3. Preserve the source's numerical values and failure conditions whenever systems are equivalent; explain any adaptation to hex adjacency, non-stacking military units, combat damage model, promotions, religion or economic systems.
4. Use the spell action's native turn budget, not fake extra movement, for the EMM `bHasCasted` restriction. Later Spellstaff must raise the allowed cast count rather than simply restore movement.
5. Persist gameplay state so save/reload cannot reset cast limits or summon lifetimes. Unit status data already serializes in Unciv; the new `emmSpellsCastThisTurn` persists and resets on `startTurn()`.
6. No claiming perfect parity without tests on Android and checks for allied/enemy, living/non-living, city ownership, resistance, duration, cast cost, save/reload and multiplayer synchronization.
7. The separate Android package prevents overwriting the regular Unciv app and its private game data.

## First native spell: Haste (Body I)

EMM source `SPELL_HASTE` adds `PROMOTION_HASTED`, removes `PROMOTION_SLOW`, ignores neutral/enemy and non-living units and consumes the caster's normal spell cast. Hasted is +1 movement and expires at the source's 100% expiry check.

Current implementation:

- Grants the mod's Hasted status (+1 movement) to eligible friendly **living land military units**, excluding undead, constructs and civilians.
- Uses caster's hex and six adjacent hexes rather than same-tile stack members: a deliberate hex/one-military-unit-per-hex adaptation.
- Attempts to remove the future `Slowed` status from beneficiaries.
- Expires using Unciv's native serializable status counter; using a value of two covers the following friendly turn, since counters decrement at start of turn. Requires in-game confirmation against EMM lifecycle.
- Consumes the caster's current movement and one native spellcast budget. Further cast actions for the same unit remain unavailable until the next start of turn.
- Refuses unsupported spell names; no silent substitution.

**Known limitations:** current living/construct classification uses unit types and names as a provisional bridge until EMM creature categories are ported, the engine does not yet implement magic resistance, source random expiry, stacked unit targeting, AI casting or Spellstaff. The +1 movement may be usable mainly next turn because the caster spends its remaining movement.

## Follow-up engine modules

1. **Unit taxonomy and target registry:** living, undead, demon, angel, elemental, mechanical, recon, disciple, ranged; allies/enemies/neutral; city/tile filters. Migrate from name heuristics.
2. **Status lifecycle:** source expiry probability, per-unit dispel, source-defined removal conditions, status immunities, on-hit effects.
3. **Summoner links:** serialize `casterId`, `remainingTurns`, `permanent`, summon limit; destroy appropriately on turn tick or caster death.
4. **Combat damage spells:** original EMM damage caps, range/radius on hexes, elemental damage, saves/resistance and diplomacy consequences.
5. **Targeted conversion / resurrection:** legal target picker, resistance, hero graveyard and dead hero registry, replacement unit ownership and XP.
6. **Metamagic and global/world spells:** multiple spellcast budgets, dispelling, Rift links, map changes, faction worldspell once-per-game flags.
7. **Core gameplay adaptation registry:** explicit record for any Civ IV mechanic absent or materially different in Unciv; all differences documented before implementation.

## Build and test

CI: [EMM engine workflow](https://github.com/kd40000-dot/unciv-ffh/actions/workflows/emm-engine.yml). Build outputs, when successful, appear as the `unciv-emm-engine-debug` workflow artifact; this is not yet a published signed release.

Do not mix saves from the engine-backed branch with the older vanilla-mod branch during early development. New fields default safely, but migration and compatibility need testing.
