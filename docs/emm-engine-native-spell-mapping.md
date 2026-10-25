# EMM engine-backed spell acceptance matrix

Generated from the actual `jsons/EMMSpells.json` definitions, branch `feature/emm-engine-framework-2026-10-25`.

**Status:** 21 actions are wired into the native Kotlin EMM executor. Neither build success nor JSON consistency establishes on-device spell correctness or full EMM parity. The remaining source EMM records are inventoried separately in `docs/emm-full-spell-inventory.md`.

The current engine has one cast per unit turn, explicit radius/relations, native timed statuses, damage caps and instant healing, and persistent summoned-unit lifetime. Hex adjacency substitutes for Civ IV's same-plot stack where indicated. Original damage type/resistance, random buff expiration, summons' full inheritance and most world abilities remain incomplete.

| Spell | EMM source | Implemented engine behavior | Gameplay validation |
|---|---|---|---|
| Haste | `SPELL_HASTE` | Hasted on friendly (range 1); 2 turns | Awaiting on-device QA |
| Courage | `SPELL_COURAGE` | Courage (Spell) on friendly (range 1); 2 turns | Awaiting on-device QA |
| Maelstrom | `SPELL_MAELSTROM` | 15 damage (cap 30) to enemy targets (range 2) | Awaiting on-device QA |
| Summon Fire Elemental | `SPELL_SUMMON_FIRE_ELEMENTAL` | Fire Elemental (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Raise Skeleton | `SPELL_RAISE_SKELETON` | Skeleton (Summoned); permanent; immobile on creation | Awaiting on-device QA |
| Repair | `SPELL_REPAIR` | +20 HP to friendly eligible targets (range 1) | Awaiting on-device QA |
| Fireball | `SPELL_FIREBALL` | Fireball (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Graft Flesh | `SPELL_GRAFT_FLESH` | Flesh Golem (Summoned); permanent; immobile on creation | Awaiting on-device QA |
| Magic Missile | `SPELL_MAGIC_MISSILE` | Magic Missile (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Air Elemental | `SPELL_SUMMON_AIR_ELEMENTAL` | Air Elemental (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Aurealis | `SPELL_SUMMON_AUREALIS` | Aurealis (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Djinn | `SPELL_SUMMON_DJINN` | Djinn (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Earth Elemental | `SPELL_SUMMON_EARTH_ELEMENTAL` | Earth Elemental (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Einherjar | `SPELL_SUMMON_EINHERJAR` | Einherjar (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Ice Elemental | `SPELL_SUMMON_ICE_ELEMENTAL` | Ice Elemental (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Mistform | `SPELL_SUMMON_MISTFORM` | Mistform (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Pit Beast | `SPELL_SUMMON_PIT_BEAST` | Pit Beast (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Runewyn | `SPELL_SUMMON_RUNEWYN` | Runewyn (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Spectre | `SPELL_SUMMON_SPECTRE` | Spectre (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Water Elemental | `SPELL_SUMMON_WATER_ELEMENTAL` | Water Elemental (Summoned); expires automatically (1 turn) | Awaiting on-device QA |
| Summon Wraith | `SPELL_SUMMON_WRAITH` | Wraith (Summoned); expires automatically (1 turn) | Awaiting on-device QA |

## On-device test sequence

- [ ] Install separately signed `com.unciv.emm` test APK. Confirm ordinary Unciv data and saves remain separate.
- [ ] Download the matching **framework branch** mod, not `main`. Confirm `Locate mod errors` is clean in the modified client. Do not test this mod branch in standard Unciv (it has engine-only spell uniques).
- [ ] Acquire Body, Spirit, Air, Enchantment, Death and Fire sphere promotions via Mana Nodes. Check actions unlocked for correct ranks and Channeling prerequisites.
- [ ] Put allied living military units next to Haste/Courage casters, and arrange nonliving/undead plus hostile units as controls.
- [ ] Measure turn-by-turn status bonuses and expiry, move the caster away and see whether recipient-specific status persists.
- [ ] Arrange damaged ships, siege engines, golems and ordinary melee units; verify that Dwarf caster Repair restores only eligible targets by up to 20 HP.
- [ ] Cast Maelstrom on enemies at distances 1, 2, 3 and after cumulative spell damage reaches 30. Verify non-war targets are not harmed.
- [ ] Summon Fireball/Spectre/Elemental and permanent Skeleton/Flesh Golem. Observe movement availability, turn expiry, per-caster limit and save/load persistence. Check graveyard and special promotion effects against EMM.
- [ ] Attempt two casts on one turn, reload the save before ending the turn, then verify the limit remains enforced.
- [ ] Check the original EMM behavior and log differences and screenshots for each specific case. No checkboxes are pre-checked.

## Known source-fidelity blockers

- Engine-native Courage still lacks EMM fear immunity and +5 exploration result bonus; status expiration is deterministic.
- Maelstrom ignores lightning resistance and `bCausesWar` for neutral targets.
- Raise Skeleton lacks the Python graveyard triple-cast behavior; source `bImmobileUnitCreate` is now honored.
- Same-plot targeting is adapted to adjacent hexes for EMM group spells and Repair.
- Summoned unit combat bonuses, summoned promotion expiry interaction, animation and source caster restrictions are not fully modeled.
- A spell can presently specify one status/heal/damage/summon effect. Multi-effect, world-spell and targeted-player choices require more executor actions and save-state structures.


## New native spell behaviors: October 25 continuation (awaiting Android playtest)

This section supersedes any earlier 21-spell count above. Registry now has **24** actions (21 preceding plus three newly wired), but **none of these are certified EMM-exact** merely because an engine build succeeds.

| Name | EMM XML | Engine implementation | Explicit fidelity gaps | Player QA |
|---|---|---|---|---|
| Snowfall (Ice III) | `SPELL_SNOWFALL`: `iRange=1`, `iDamage=40`, `iDamageLimit=70`, cold; `PyResult=spellSnowfall` | Damage to war enemies within one hex, maximum cumulative 70 damage | No `spellSnowfall` Python terrain/secondary effects, elemental cold resistance, neutral-provokes-war handling | [ ] |
| Wither (Entropy III) | `SPELL_WITHER`: range 1, Death 10 damage cap 40, resistable, `PROMOTION_WITHERED`, living enemy only | Individual living enemies within radius 1 take 10 damage, max cumulative 40, and receive temporary Withered debuff | Spell resistance, persistent source promotion and original promotion healing/XP modifiers not faithfully ported | [ ] |
| Regeneration (Body II) | `SPELL_REGENERATION`: `PROMOTION_REGENERATION`, no nonliving recipients | Apply regeneration individually to allied living units near caster, 2 turns | Same-plot Civ IV stacking adapted to radius 1, source promotion lifetime and actual recipient healing not fully verified | [ ] |

**Critical test:** A combat spell must never affect an out-of-war civilization simply because it is within radius. This is currently a limitation: EMM `bCausesWar` may declare war, while this framework only attacks existing war enemies. For Wither, EMM `bResistable` is still unimplemented. Summon duration is an Unciv owner-turn approximation, not a universal promise of Civ IV's EMM expiry timing.

Source reference: `bewlay/extramodmod` `XML/Units/CIV4SpellInfos.xml` pinned at `60b0ec3740083162aaab7bf8491761a54a65a610`.


## Recipient-targeted promotions (native action migration)

These five actions were converted from caster-only JSON proxies to individual recipient statuses. They **still do not reproduce every EMM promotion property**. All require Android gameplay testing.

| EMM spell | Source promotion | Native engine effect | Missing fidelity |
|---|---|---|---|
| Blur (Shadow I) | `PROMOTION_BLUR` | Apply `Blur (Spell)` to friendly units in caster's 1-hex radius | Existing status gives +20% defending Strength instead of exact immunity to first strikes; fixed timer and stack→adjacency |
| Dance of Blades (Chaos I) | `PROMOTION_DANCE_OF_BLADES` | Apply `Dance of Blades (Spell)` to friendly units within 1 hex | Existing status approximates one first strike with +15% attacking Strength |
| Stoneskin (Earth II) | `PROMOTION_STONESKIN` | Self-only `Stoneskin (Spell)` buff | Existing +2 defensive Strength approximation; source stoneskin mechanics, promotion expiry and damage absorption need review |
| Loyalty (Law I) | `PROMOTION_LOYALTY` | Apply `Loyalty (Spell)` to friendlies within 1 hex | `Uncapturable` proxy lacks source Loyalty and Burning Blood interplay |
| Flaming Arrows (Enchantment II) | `PROMOTION_FLAMING_ARROWS` | Give individual friendly Archery units `Flaming Arrows (Spell)`, rather than a caster aura | Current +20% Strength is not the source extra Fire damage |

**Registry coverage after this batch: 29 EMM source-backed native actions.** This means registered actions in the experimental engine; it is **not** a tally of verified faithful EMM spells. Several are explicitly limited proxies and the remaining source spell records remain unimplemented.
