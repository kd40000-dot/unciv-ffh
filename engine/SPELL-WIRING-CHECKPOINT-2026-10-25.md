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

## Currently registered: 30 of 355

**This is NOT 355 playable EMM spells.** The remainder need explicit source reviews and effect implementations.

### Enchanted Blade (SPELL_ENCHANTED_BLADE)
- Enchantment I caster, one cast each turn, one-hex friendly Sword recipients (Civ IV same-plot substitute).
- Individual persistent `Enchanted Blade (Spell)` status, with an Unciv +20% Strength proxy; tries to clear `Rusted (Spell)` status on recipient.
- Source fidelity gaps: precise Enchanted Blade damage calculations and type interactions, range/stack mapping, equipment lifecycle, and correct separation of innate versus granted weapon effects.
- Runtime concern: legacy Rusted effect is implemented as an adjacent aura promotion, not necessarily a literal status. Removing that status does not remove enemy auras in range.
- Android acceptance: adjacent friendly sword gets status and bonuses; non-Sword and hostile units do not; existing status persists after caster moves; duplicate casting is gated; Rust removal when Rust is represented as unit status; normal Unciv untouched.

## Validation
A connector-side read of the committed branch confirmed 355 source records, 30 native spell definitions, and 30 corresponding promotion grants without missing names. The new Python assertions and Android workflow have been committed, **not yet run to successful completion**. Kotlin compilation and actual gameplay are outstanding.

## Next engine work
Implement first-class effects for terrain/feature/improvement manipulation, city-targeted spells, equipment mutations, promotion cleansing with explicit status taxonomy, target selection and diplomacy, then world-spell persistence. Do not promote a catalog entry to `native-registered` without executable effect and grant.
