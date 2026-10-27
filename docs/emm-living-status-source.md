# EMM exact living-status source audit (2026-10-27)

Pinned upstream: `bewlay/extramodmod` commit
`60b0ec3740083162aaab7bf8491761a54a65a610`.

## Authoritative engine behavior

In `CvGameCoreDLL/CvUnit.cpp`, `CvUnit::isAlive()` returns
`m_iAlive == 0`. During initialization, `CvUnit::init` calls
`changeAlive(1)` if the unit's `CvUnitInfo::isMechUnit()` is set
(`bMechanized` in `XML/Units/CIV4UnitInfos.xml`). The
`setHasPromotion` code changes the counter by the promotion's
`bNotAlive` value, using +1 on acquire and -1 on removal.
Thus eligibility must be reevaluated from the unit's **current**
promotions, not cached at unit creation, and multiple simultaneous
nonliving promotions can stack.

Exactly nine pinned `CIV4PromotionInfos.xml` entries have
`bNotAlive=1`: ANGEL, AVATAR, DEMON, ELEMENTAL, GOLEM, ILLUSION,
PUPPET, RIFT, UNDEAD. A derived unit classifier has been added to
`tools/patch_emm_epidemic_damage.py` using these labels and the
pinned mechanized unit identities.

## Remaining integration gaps

- Not all nine source promotions currently exist as ruleset promotions,
  so units lacking their EMM racial promotion can be misclassified
  until those promotion sources and application rules are implemented.
- Unit names need one-to-one audit against each EMM mechanized source
  unit; renaming and civilization replacements must keep source identity.
- Exact EMM Death-type resistance and `doDamageNoCaster` effects are
  separate from the living-status classifier and still unimplemented.
- No gameplay QA yet; static assertions and build verification remain
  the next technical gates.
