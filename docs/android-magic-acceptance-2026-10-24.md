# Android magic acceptance matrix — October 24, 2026

This is an **in-game checklist**, not a claim that any remaining item passes. Test on the user's working Unciv APK and the current `main` mod. **No engine changes.**

## Already confirmed by player
- [x] Raw Mana → Fire Node → one Fire Mana.
- [x] Retune a Mana Node into another type.
- [x] Adept, Wizard, Mage and Archmage can construct Mana Nodes.
- [x] Fire I can create Smoke on permitted tiles; caster survives.
- [x] Body I → Haste was successfully exercised.
- [x] Enchanted Blade Aura and Nature I Treetop Tactics show their combat bonuses.

## Next: actual spell regression checks

### Water I / Spring (Elementalism)
- [ ] Construct Water Node and verify 1 Water Mana.
- [ ] Learn Water I on Channeling I Adept.
- [ ] On **owned unimproved Desert without Flood plains**, check **Turn tile into Plains** action appears.
- [ ] Cast. Confirm terrain becomes Plains, casting spends all movement, Adept survives.
- [ ] Verify action unavailable on owned Plains, Desert with Flood plains, improved Desert and foreign Desert.
- [ ] Have Fire I caster create Smoke on owned Forest; verify Water I caster may remove Smoke and the forest remains. Check range/position: effect should operate on caster's tile, not a distant tile.

### Mind I / Inspiration (Divination)
- [ ] Construct Mind Node and verify 1 Mind Mana.
- [ ] Learn Mind I; station caster **on an owned City center**.
- [ ] Record current accumulated research/science and science-per-turn **before** casting; distinguish the city's ordinary yields from bonus science.
- [ ] Cast Inspiration and end turns; test whether 2 Science is actually added at turn start on each eligible turn. If it does not appear, report *exactly* what changed: science stockpile, science-per-turn readout, or nothing.
- [ ] Check expiration after 2-turn status and ensure repeated casting refreshes rather than stacks.
- [ ] Check inability to cast from an ordinary tile, and unavailable promotion with no Mind Mana.

### Enchantment I and Nature I regression
- [ ] Verify bonuses cease after temporary status expiration, not just when stepping out of range.
- [ ] Save/load during active status, then verify expiry.
- [ ] Verify no unexpected stacking with repeated casting.

### Mana resource/ownership
- [ ] Pillage node → mana supply stops and new promotions needing that mana disappear.
- [ ] Restore node → supply returns.
- [ ] Retune occupied Fire Node to Water Node → one old resource disappears, one new resource appears, no double count.
- [ ] Capture/lose the tile → resource ownership updates.

## Failure report template
Write down: spell, exact tile terrain/improvement and ownership, owned Mana amounts, caster type and promotions, action label (or missing action), movement before/after, observed result, whether save/load changes behavior. Attach one screenshot if combat preview or city science display disagrees.

## Later implementation priorities
1. Fix any failing existing spell **before** adding more sphere I promotions.
2. Implement another sphere spell only after checking the pinned EMM spell semantics and validating native Unciv unique support.
3. Add appropriate caster rank/XP restrictions, group effects and temporary summons only if stock Unciv supports their gameplay accurately, otherwise document proxy/engine limitation.
