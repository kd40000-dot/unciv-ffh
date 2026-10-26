# EMM epidemic source audit

Pinned EMM `python/entrypoints/CvRandomEventInterface.py` at `60b0ec3740083162aaab7bf8491761a54a65a610` confirms that both `doArmageddonBlight` and `doArmageddonPestilence` apply `doDamageNoCaster(25, 100, DAMAGE_DEATH, False)` to each living unit. Infernal exclusion applies to cities' sickness counters, not automatically to living units. Exact `isAlive` classification and typed Death damage need an engine implementation and regression testing.

Blight city counter: only positive `rand(15) + population + badFeatureHealth - goodFeatureHealth - totalGoodBuildingHealth`. Pestilence city counter: signed `rand(9) + floor(population/4) - totalGoodBuildingHealth`. The current patched dispatcher handles city counters but omits both unit-damage passes.
