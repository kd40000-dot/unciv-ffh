# Casting proof 02 — unit expiration on the next turn

## Verified starting point
- Proof 01 (`magic-casting-proof-01`) passed static JSON checks and the official Unciv ruleset validator.
- The user tested the first casting probe on Android and reported that **all checks worked**: the summon action appears, movement is spent, the summon appears and the action is available again after a turn. Placement was included in the test instructions, but detailed positions were not separately recorded.
- This proof is a **separate branch**. Main, the portrait installation and `playable-0.1a` are not changed.

## Original ExtraModMod behavior
Source: [bewlay/extramodmod/CvGameCoreDLL/CvUnit.cpp](https://github.com/bewlay/extramodmod/blob/60b0ec3740083162aaab7bf8491761a54a65a610/CvGameCoreDLL/CvUnit.cpp), in `CvUnit::castCreateUnit` and `CvUnit::doTurn`.

A temporary `SPECIALUNIT_SPELL` summon starts at duration 2; the casting routine immediately calls the summoned unit's `doTurn()`, decrementing duration to 1. On the next normal unit turn, duration decreases to 0 and the summon is killed. Thus a Fireball may be used in the casting turn but must not persist through the caster's next turn.

## Controlled change in proof 02
The existing `Skeleton` unit gains:
```
[This Unit] is destroyed <upon turn start>
```
This is intentional **test-only behavior**: it will affect all Skeletons in the test ruleset, not just newly summoned ones. A real Fireball will use its own named unit definition instead. Skeleton's appearance, combat values and summoning action remain otherwise unchanged.

The engine recognizes:
- `OneTimeUnitDestroyed("[unitTriggerTarget] is destroyed", UnitTriggerable)`
- `TriggerUponTurnStart("upon turn start", UnitTriggerCondition)`
- `UnitTurnManager.startTurn` triggers `TriggerUponTurnStart`.

**Risk to verify:** A destruction trigger executing in `startTurn()` could have unintended follow-on logic effects. Syntax validation cannot rule out an Android crash or UI ghost unit.

## Android test install
Separate prerelease ZIP:
`https://github.com/kd40000-dot/unciv-ffh/releases/download/casting-proof-02/unciv-ffh-casting-test-02.zip`

Install via Unciv's mod manager **Download mod from URL**. For the new test game choose the `unciv-ffh-casting-test-02` ruleset and retain your regular `unciv-ffh` mod. Research Sorcery and train a Mage (or Amurite Wizard).

## Expected manual checks
1. Cast the Skeleton action. Confirm the Skeleton appears and can be selected immediately.
2. Move or use the Skeleton during the current turn. The Skeleton should not vanish before you get control.
3. End your turn, let other civilizations take their turns, and start **your next turn**. The summoned Skeleton should disappear as the turn starts, without requiring a manual action.
4. Check that the caster still exists, is still movable, and can cast again after the turn changes.
5. Repeat after saving and reopening the game between summoning and next turn. Look for crashes or resurrected/ghost units.
6. If possible, check a summon adjacent to friendly city territory and away from city centers.

## Exit criteria
- Both ruleset validators pass on this branch.
- Android confirms the summoned unit lasts exactly through its cast turn, disappears safely on the next player's turn and leaves no broken UI.
- If start-turn deletion crashes, do not merge. Investigate an engine-owned lifespan counter instead.

## Next stage
After this passes, **proof 03** should establish explicit once-per-turn caster state even when movement is restored mid-turn; using `<once>` is invalid because Unciv counts lifetime uses. Then define a distinct Fireball and implement the original FFH2 fire combat, if necessary via engine extension.
