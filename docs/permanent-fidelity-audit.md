# EMM → Unciv permanent gameplay fidelity audit

**Baseline:** 2026-10-26. **Target:** [ExtraModMod Continued](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610) at `60b0ec3740083162aaab7bf8491761a54a65a610`.

**Canonical data:** [25-system fidelity-scorecard.json](data/fidelity-scorecard.json). This page is the human-readable governance and history document; the JSON supplies the exact scores, evidence, remaining differences and source-file starting points for each system.

## Baseline scorecard

| ID | EMM system | Fidelity estimate |
|---|---|---:|
| F01 | Civilization-specific mechanics | 25% |
| F02 | Magic and mana | 15% |
| F03 | Religions | 5% |
| F04 | Alignment | 0% |
| F05 | Heroes and world units | 10% |
| F06 | World spells | 0% |
| F07 | Civics and government | 0% |
| F08 | Combat system | 30% |
| F09 | Promotions and experience | 20% |
| F10 | Equipment and weapon metals | 20% |
| F11 | Summoning and transformations | 5% |
| F12 | Stealth and covert operations | 5% |
| F13 | City health and disease | 0% |
| F14 | Happiness and war weariness | 15% |
| F15 | City economy and maintenance | 25% |
| F16 | Population, specialists and slavery | 15% |
| F17 | Culture and territory | 30% |
| F18 | Resources and improvements | 35% |
| F19 | Armageddon Counter | 0% |
| F20 | Hell terrain and transformation | 5% |
| F21 | Wilderness and barbarian factions | 5% |
| F22 | Lairs, dungeons and exploration | 5% |
| F23 | Diplomacy, councils and vassalage | 10% |
| F24 | Advanced tactics, forts and revolutions | 5% |
| F25 | Victory conditions | 10% |
| | **Equal-weight mean** | **11.8%** |

**Correction:** The earlier conversational ~14% overall estimate was an arithmetic error. The exact simple average of its 25 proposed percentages is 11.8%, which is the immutable initial baseline unless a later audit explicitly revises it with documented evidence.

## Evidence standards and definitions

- **Missing:** the required EMM gameplay behavior is not present; cosmetic names, descriptions or JSON stubs do not count.
- **Early:** small functional slices or substantial proxies, far from a faithful system.
- **Partial:** significant working mechanics, but incomplete roster, formulas, timing or interactions.
- **Needs QA:** implementation appears present but lacks specific in-game confirmation. This is a verification flag, not proof of correctness.
- **Faithful:** source-defined mechanic, inputs, output, limitations, lifecycle and AI path verified to match EMM within explicitly disclosed and justified deviations.
- **In-game confirmed:** only an explicit player test or reproducible game execution, with date, build and expected/observed result; a CI pass is **not** gameplay confirmation.
- **Source paths** in the JSON are an audit search map to the pinned EMM tree, not assertions that every listed path was independently checked field-by-field. For formulas and script behavior, inspect referenced EMM XML **and Python/C++** and add exact symbol/line/commit details on the relevant implementation change.
- **Percent** is an evidence-backed but subjective estimate of EMM behavioral fidelity, **not** a count of source XML entries or engineering hours. Give major behavior more weight than scaffolding. Never increase it merely because code was written.
- **Scope:** these 25 mechanics exclude traditional BtS espionage, artwork and audio; these are a **gameplay** scorecard, not total-project completion. EMM stealth/covert rules remain in scope.
- When older living notes conflict with newer feature documentation, record the conflict. The JSON references the most relevant local documentation; stale historical notes must not be silently treated as current.

## Mandatory completion protocol for every gameplay task

1. Before touching code, identify impacted F01–F25 systems and inspect their current score, source paths, confirmed tests and `remainingDifferences`. Cite the pinned EMM XML/Python/C++ definition for the task.
2. Implement in the mod/engine; check mod loading, formulas, AI usage, and unintended regressions. List intentional deviations; distinguish proxies clearly.
3. In **the same change as the gameplay implementation**, update affected objects in `docs/data/fidelity-scorecard.json`: `status`, `percent` (only with justification), `portEvidence`, `gameplayConfirmed` (only for actual tests), `remainingDifferences`, `verification`, `lastReviewed`, and `updatedBy`.
4. Recalculate the 25-system equal-weight average using `python3 scripts/check_fidelity_audit.py` or `python3 scripts/check_fidelity_audit.py --summary`. Update this page's **Current scorecard** snapshot in the same commit when any score changes; do not erase baseline rows.
5. Add a one-paragraph dated entry to the history below identifying commit/PR, affected systems, old → new scores, evidence, tests performed, failed/untested cases, and new gaps.
6. For substantial features include an Android acceptance checklist; record **tested** vs **needs test** separately.
7. Do not close an item without testing all required input/output and lifecycle edge cases. Unverified edge cases remain gaps even when the UI appears correct.

CI rejects gameplay-file changes without an updated audit data file when the workflow can see the triggering commit. CI also verifies all 25 rows, unique IDs, 0–100 bounds, required fields and documentation synchronization.

## Current scorecard

The current scores are those in [fidelity-scorecard.json](data/fidelity-scorecard.json); baseline is **11.8% equal-weight**. On each score-changing task, regenerate the table with `python3 scripts/check_fidelity_audit.py --summary` and paste the output here, preserving the baseline above.

## Change history

### 2026-10-26 — Initial audit
- Baseline `F01`–`F25` created from the October 26 gameplay audit and repository's source ledgers.
- Approximately 11.8% average estimated fidelity (25 systems, equal weights).
- Confirmed user tests have been recorded separately from static validations; all other mechanics remain unverified until explicit test evidence.
- Historic gaps in `docs/open-fidelity-gaps.md` may be stale relative to the October 23–24 magic documentation. Do not interpret historic omissions as current.

