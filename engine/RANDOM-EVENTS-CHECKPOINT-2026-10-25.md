# EMM random events: initial native runtime checkpoint

Source EMM pinned commit: `60b0ec3740083162aaab7bf8491761a54a65a610`.

## Implemented on this branch
- Persistent per-city event turn records (`City.emmEventLastTurn`) and last-checked-turn gating (`City.emmEventCheckedTurn`), serialized into saved games.
- Executable turn-start event roll using each city's computed `CityStats.emmCrimeModifier`, which includes the Dungeon's −10 crime modifier.
- Basic city-size prerequisite, probability clamp, event cooldown, and gold consequence.
- Dungeon and other building crime modifiers affect incident probability rather than simply existing as inert Civilopedia text.

## Important — this is an experimental runtime, not EMM event parity
The current executable **Crime Incident** is an Unciv-specific temporary test event: eligible city population >=3; roll chance clamp(5 + crime, 0, 30)% each turn; cooldown 15 turns; penalty 10 Gold. **These constants and the event itself are NOT claimed to originate in EMM.** They exercise the event scheduler and demonstrate that Dungeon's crime modifier is connected to gameplay. They must be replaced with actual `CIV4EventTriggerInfos` and `CIV4EventInfos` definitions before fidelity acceptance.

Source-confirmed EMM Python example: `python/entrypoints/CvRandomEventInterface.py::canApplyOrderVsVeil4` allows one religious conflict event option only when the city has a Dungeon. This is **not** an automatic Dungeon crime event and must not be approximated as one. The port needs event trigger prerequisites (religion/state religion, city building, event option), player choice UI, consequences and saved event states.

## Missing EMM event services
- Source XML trigger and result import, `bRecurring`, prerequisite tech/civic/religion/unit/building, event chance/weight and cooldown rules
- Human selection popups and AI event-option selection; current prototype resolves automatically and has no UI
- Crime-level semantics from full EMM events, global game options, unique city/civ/race and leader modifiers
- City/unit/plot target selection, chained events, delayed effects, Python handlers, scripted quests
- Notifications, event history and reload-safe random-state parity
- Original EMM event probabilities, outcomes, graphics/text and localization

## Test checklist
1. Test only in a newly built `com.unciv.emm` APK, NOT standard Unciv.
2. Save a game with a size >=3 city, record Gold and built buildings, observe repeated turns.
3. With neutral crime, the prototype may eventually deduct 10 Gold on an event. This is stochastic: a few turns without an event do not prove failure.
4. Construct a Dungeon: city crime modifier -10 should reduce prototype 5% base risk to 0%; no incident should fire while only that modifier applies.
5. Add +5 crime Market or Inn: risk increases, subject to Dungeon offset and clamp.
6. Verify at most one event roll per city per turn and 15-turn minimum gap after an incident.
7. Save and reload: `emmEventLastTurn` and `emmEventCheckedTurn` persist; no duplicate incident on same turn.
8. Compare cities with independent event state; crime modifiers only affect the owning city.

**Current status:** implementation committed but Python patcher, Kotlin compilation and Android gameplay not yet verified for this branch.

## Source XML inventory importer

`engine/import_emm_events.py` parses pinned EMM `XML/Events/CIV4EventTriggerInfos.xml` and `XML/Events/CIV4EventInfos.xml`, recording trigger weights, city and population prerequisites, recurring flags, world-counter thresholds, building/religion prerequisites, and option IDs; event options record fixed effects and Python callback names.

Usage on a checkout of the pinned EMM source:

```sh
python3 engine/import_emm_events.py \
  /path/to/extramodmod/XML/Events/CIV4EventTriggerInfos.xml \
  /path/to/extramodmod/XML/Events/CIV4EventInfos.xml \
  engine/emm-event-source-catalog.json
```

This is an audit/import tool, not proof that every source event is playable. In particular, the source's `EVENTTRIGGER_ORDER_VS_VEIL` requires both The Order and Ashen Veil and a sufficiently high world counter, while `EVENT_ORDER_VS_VEIL_4` specifically requires a Dungeon. Those conditions cannot be replaced with a generic crime incident without changing EMM gameplay.
