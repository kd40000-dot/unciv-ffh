# Native EMM engine framework — 25 October 2026

**Development branch:** `feature/emm-engine-framework-2026-10-25`. Derived from the working native-engine prototype branch, which in turn derives from expanded-magic data. **Do not merge to main or install as a standard Unciv mod.** The regular playable mod and rollback checkpoint remain untouched.

## Engine architecture

The build pins upstream Unciv `b5c4bccd2b038f49183338811dc30efec81cb105`; `engine/apply_overlay.py` patches a clean upstream checkout and copies the Kotlin classes in `engine/overlay/`. It fails closed when source anchors differ. `.github/workflows/emm-engine.yml` compiles core and builds a separate `com.unciv.emm` Android debug APK.

* `EMMSpell.kt` is loaded from `jsons/EMMSpells.json` into `Ruleset.emmSpells` and merged with other rulesets. All fields are save-independent game rules, not ephemeral UI data.
* `Can cast EMM spell [X]` registers an EMM-native action on a promotion. Unregistered names cannot execute. Eligible actions use the existing worldscreen unit-action UI, and are revalidated immediately before execution.
* `EmmSpellEngine.kt` implements explicit target/allegiance filters (self, allies, war enemies), radius-based selection, living/nonliving restrictions, status delivery/removal, direct healing, direct damage with EMM accumulated-damage caps, and unit creation.
* The existing serializable `statusMap` stores buff lifetime. New persisted `emmSpellsCastThisTurn`, `emmSummonTurnsLeft`, and `emmSummonerId` fields maintain cast budgets and summon state across saves and unit cloning. Cast budget resets at unit start-of-turn; temporary summoned units are removed when their owner-turn counter expires.
* `Courage (Spell)` now modifies the recipient's own ordinary healing calculation (+10) rather than leaking an adjacent-unit aura from the caster. Inapplicable healing still returns zero.

## First engine-backed spells

| Spell | EMM source | Native implementation | Difference/gap |
|---|---|---|---|
| Haste — Body I | SPELL_HASTE | Hasted status (+1 Movement) and removes Slowed on eligible friendly living land units, radius 1, cast once per turn | Civ IV same-plot stack → caster hex plus 6 neighbors. No source random expiration, creature taxonomy provisional |
| Courage — Spirit I | SPELL_COURAGE | Individual two-turn recipient Courage status, +10 ordinary healing to eligible friendly living units, radius 1 | Source fear immunity, exploration result bonus, same-plot targeting and expiration probability pending |
| Maelstrom — Air II | SPELL_MAELSTROM | Direct damage 15 to war enemies within distance 2, accumulating no more than 30 HP damage | Original lightning resistance and automatic war declaration for neutral targets not implemented |
| Summon Fire Elemental — Fire III | SPELL_SUMMON_FIRE_ELEMENTAL | Creates a fire elemental with summoner ID and automatic expiry after one owner-turn start | Summoner/elemental mechanics, summoning cap, default EMM lifespan and combat modifiers still require source validation |
| Raise Skeleton — Death I | SPELL_RAISE_SKELETON | Creates permanent skeleton (does not expire) with summoner provenance | Source Python `spellRaiseSkeleton` cap and immobile-on-creation require separate port |

The rule registry and implementation are extensions of the already-committed engine prototype, not a claim that the remaining EMM spells are implemented.

## Android / engine acceptance gates

- [ ] Native Android workflow builds successfully on the *framework* branch.
- [ ] APK installs as `com.unciv.emm` alongside regular Unciv.
- [ ] Framework mod loads with `EMMSpells.json` and displays the five cast actions.
- [ ] Each action is gated by corresponding sphere promotion and movement, and at most one cast per turn.
- [ ] Haste affects the eligible adjacent allied units, not neutral/enemy units; removes Slowed and expires as expected.
- [ ] Courage provides exactly +10 natural healing for each recipient, never affects unrelated units, and expires after the configured turns.
- [ ] Maelstrom correctly enforces range 2, causes 15 damage initially, never takes enemies under 70 health from the spell alone, never harms non-war units (neutral-war handling not yet added).
- [ ] Fire Elemental appears near the caster and automatically expires; Skeleton persists.
- [ ] Summoner ID, spell count, status remaining turns and summon expiry survive save/load.
- [ ] Check game/CI logs and `Locate mod errors`, replay against the old JSON branch to identify regressions.

## Remaining EMM engine modules

Creature-taxonomy tags; damage-type and spell resistance; spell-specific targeting and immunities; target picker; source probabilistic promotion expiration; caster death and summon caps; world-spell once-per-game state; city spell buildings and removal; hell terrain/Armageddon counter; religions, mana channeling, heroes and resurrection; transformations and equipment; diplomacy and AI casting; multiplayer-deterministic RNG; Rust/Enchanted Blade as permanent individual equipment; map/lair event engine; and the full 355-record inventory audit.

Do not treat these as completed simply because `mod-ci` passes or an APK compiles. Detailed records: `docs/emm-full-spell-inventory.md` and `docs/emm-all-355-android-checklist.md`.
