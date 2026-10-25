# Spell wiring continuation — October 25, 2026

Branch: `checkpoint/emm-spell-wiring-inventory-2026-10-25`. This branch inherits the 29-action native prototype and preserves the playable `main` branch.

## Saved checkpoints
- `444359e`: all 355 pinned EMM XML action identifiers have a source-to-native coverage record.
- `43aa18c`: fail-closed coverage validator checks source IDs, definitions, promotion grants.
- `bd4bac1`: include the validator in the experimental Android workflow.
- `29bfd3a` / `6be23e3`: migrate Enchanted Blade from caster aura to recipient status using valid native unique syntax.
- `f351ac3`: native Enchanted Blade definition.
- `d27c19c`: mark the linked source action in the coverage manifest.
- `522f87a`: assertions for Enchanted Blade recipient behavior.

## Currently registered: 32 of 355

**This is NOT 355 playable EMM spells.** The remainder need explicit source reviews and effect implementations.

### Enchanted Blade (SPELL_ENCHANTED_BLADE)
- Enchantment I caster, one cast each turn, one-hex friendly Sword recipients (Civ IV same-plot substitute).
- Individual persistent `Enchanted Blade (Spell)` status, with an Unciv +20% Strength proxy; tries to clear `Rusted (Spell)` status on recipient.
- Source fidelity gaps: precise Enchanted Blade damage calculations and type interactions, range/stack mapping, equipment lifecycle, and correct separation of innate versus granted weapon effects.
- Runtime concern: legacy Rusted effect is implemented as an adjacent aura promotion, not necessarily a literal status. Removing that status does not remove enemy auras in range.
- Android acceptance: adjacent friendly sword gets status and bonuses; non-Sword and hostile units do not; existing status persists after caster moves; duplicate casting is gated; Rust removal when Rust is represented as unit status; normal Unciv untouched.

## Validation
A connector-side read of the committed branch confirmed 355 source records, 31 native spell definitions, and 31 corresponding promotion grants without missing names. The new Python assertions and Android workflow have been committed, **not yet run to successful completion**. Kotlin compilation and actual gameplay are outstanding.

## Next engine work
Implement first-class effects for terrain/feature/improvement manipulation, city-targeted spells, equipment mutations, promotion cleansing with explicit status taxonomy, target selection and diplomacy, then world-spell persistence. Do not promote a catalog entry to `native-registered` without executable effect and grant.

## Continuation: native Rust (SPELL_RUST)

- Migrated Entropy I from a caster self-aura to the EMM native cast action.
- Eligible adjacent war-enemy Sword recipients receive a persistent `Rusted (Spell)` status (-10% Strength proxy). `Enchanted Blade (Spell)` is removed before applying Rust.
- Native registry, source catalog, and regression assertions were updated in consecutive GitHub commits.
- **Fidelity remains unverified:** EMM Rust's exact valid targets, defense modifiers, dispel conditions, magic resistance, and Civ IV stack targeting need source examination and gameplay verification. An enemy at peace will not be targeted by this adaptation.
- Connector-based consistency check after commits: 355 records, 31 definitions, 31 promotion grants, no mismatches. GitHub Actions compile and Android gameplay tests have not been verified in this continuation.

## Continuation: native status-cleansing executor and Dispel Magic

- The engine now supports a `CLEANSE` effect with explicitly declared `removeStatuses`, only offering a cast where at least one recipient has a removable status.
- `SPELL_DISPEL_MAGIC` is registered on Metamagic II with a one-hex friendly-unit cleanse of `Withered (Spell)` and `Rusted (Spell)`. Existing mana-node-clearing action remains separately available.
- This is **partial EMM functionality**, not full dispelling: original source effects on enemy beneficial promotions, mana nodes, summons and wider ranges still need faithful implementation, where applicable.
- All 355 source entries still tracked; 32 have native effect definitions and promotion grants, 323 remain. Static registry consistency was checked through GitHub connector, but compilation and Android tests are not yet confirmed.
- Negative status names not declared in `UnitPromotions.json` must not be inserted in `removeStatuses`; the schema validator now enforces this.
