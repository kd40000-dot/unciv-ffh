# Erebus diplomacy flavor — Phase 3.5

**Status:** Written and integrated for all 19 playable leaders; gameplay verification pending. No gameplay balance changes.

## What was changed

The 19 playable nations now have seven unique dialogue fields each:

| Unciv field | When displayed |
| --- | --- |
| `introduction` | First contact / leader introduction |
| `neutralHello` | Regular neutral dialogue |
| `hateHello` | Hostile greeting |
| `declaringWar` | Leader declares war on the player |
| `attacked` | Leader reacts to being attacked |
| `defeated` | Leader is defeated |
| `tradeRequest` | Leader initiates trade |

All **133 lines** are distinct across the 19 leaders; existing roster, mechanics, leader selection, trait uniques and gameplay JSON data are unchanged apart from these text fields.

## Important source-provenance clarification

These are **new FfH-themed, lore-inspired lines authored for this port**, **not original verbatim dialogue from FfH2 or ExtraModMod Continued**. We searched the pinned [EMM Continued revision](https://github.com/bewlay/extramodmod/tree/60b0ec3740083162aaab7bf8491761a54a65a610). Its `XML/Text/CIV4DiplomacyText.xml` contains generic Civilization IV first-contact lines for standard BtS leaders (not the 19 selected Erebus leaders), and `XML/Text/CIV4GameText_FFH2.xml` is empty in the pinned snapshot. We cannot currently authenticate original bespoke FfH dialogue for this roster. We therefore **did not fabricate source attributions** or put unverified quotes in the mod.

The complete text, leader-to-civilization assignment, and source notes are preserved in [the machine-readable dialogue ledger](data/erebus-diplomacy-dialogue.json), allowing individual lines to be replaced with source-authentic quotes if recovered.

## Gameplay tests

1. Download the updated mod from `https://github.com/kd40000-dot/unciv-ffh`. Start a new game; meet a leader such as Perpentach or Alexis. Verify that the first-contact text is distinctive and not the previous `We greet you in the name of our people.`
2. Visit a neutral diplomatic relationship (new `neutralHello`), then hostile relationship (`hateHello`) and confirm the leader-specific text is visible and not clipped.
3. Test an AI declaration of war (`declaringWar`), a player declaration against an AI (`attacked`), defeat (`defeated`) and an AI-requested trade (`tradeRequest`). Some contexts may be difficult to trigger; mark each untested rather than assuming every UI field appears correctly.
4. Compare at least three widely different leaders, e.g. Perpentach (Balseraphs), Sabathiel (Bannor) and Falamar (Lanun). All should have separate voices.
5. Confirm this milestone has not changed starting units, traits, palaces, Khazad Vaults, Lanun Coves or any other game mechanics.

## Automated test

`python3 tools/verify_erebus_diplomacy.py` validates exactly 19 playable leaders, seven nonempty distinct fields apiece, no placeholder remnants, stable per-leader attribution and machine-readable provenance. The GitHub validation workflow includes the script.

**Deferred:** source-authentic quote replacements once verified source text is available; multiple leader choices for each civilization; leader portraits; nation emblems; localization into other languages.
