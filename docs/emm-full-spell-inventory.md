# EMM Continued spell source inventory

Pinned source: `bewlay/extramodmod` commit `60b0ec3740083162aaab7bf8491761a54a65a610`, `XML/Units/CIV4SpellInfos.xml`.

**Important:** The source defines 355 XML SpellInfo entries, including non-arcane unit abilities, item transfers, faction rituals and internal effects. Not all are caster spells, and not all can be expressed in stock Unciv. `not implemented / not evaluated` is deliberate, not a gameplay claim. Spell `PyResult` or `PyRequirement` flags require review of EMM Python behavior before implementation. This ledger is a source inventory, **not an implementation or completed QA report**.

| EMM identifier | Promotion 1 | Promotion 2 | Tech | Python logic | Declared effect | Status |
|---|---|---|---|---|---|---|
| SPELL_ADD_TO_CITY | — | — | — | no | review XML | not implemented / not evaluated |
| SPELL_ADD_TO_FLESH_GOLEM | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ADD_TO_FREAK_SHOW_DARK_ELF | PROMOTION_DARK_ELF | — | — | no | building | not implemented / not evaluated |
| SPELL_ADD_TO_FREAK_SHOW_DWARF | PROMOTION_DWARF | — | — | no | building | not implemented / not evaluated |
| SPELL_ADD_TO_FREAK_SHOW_ELF | PROMOTION_ELF | — | — | no | building | not implemented / not evaluated |
| SPELL_ADD_TO_FREAK_SHOW_HUMAN | — | — | — | yes | building | not implemented / not evaluated |
| SPELL_ADD_TO_FREAK_SHOW_ORC | PROMOTION_ORC | — | — | no | building | not implemented / not evaluated |
| SPELL_ADD_TO_WOLF_PACK | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ANIMATE_FROSTLINGS | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ARCANE_LACUNA | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ARDOR | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ARENA_BATTLE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_BLAZE | PROMOTION_FIRE1 | PROMOTION_CHANNELING1 | — | yes | improvement | partial: Fire I Smoke |
| SPELL_BLESS | PROMOTION_CHANNELING2 | PROMOTION_DIVINE | — | no | buff | not implemented / not evaluated |
| SPELL_BLESSING | PROMOTION_CREATION3 | — | — | no | building | not implemented / not evaluated |
| SPELL_BLINDING_LIGHT | PROMOTION_SUN2 | — | — | no | buff | not implemented / not evaluated |
| SPELL_BLOOM | PROMOTION_CHANNELING2 | PROMOTION_DIVINE | — | no | review XML | not implemented / not evaluated |
| SPELL_BLUR | PROMOTION_SHADOW1 | PROMOTION_CHANNELING1 | — | no | buff | not implemented / not evaluated |
| SPELL_BREATH_FIRE | PROMOTION_DRAGON | PROMOTION_FEAR | — | no | summon | not implemented / not evaluated |
| SPELL_BURNING_BLOOD | — | — | — | no | buff | not implemented / not evaluated |
| SPELL_CALL_BLIZZARD | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_CALL_BLIZZARD_HIGH_PRIEST | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_CALL_FORM | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_CALL_OF_THE_GRAVE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_CHARM_PERSON | PROMOTION_MIND2 | — | — | no | buff | not implemented / not evaluated |
| SPELL_CONSUME_SOUL | — | — | — | no | review XML | not implemented / not evaluated |
| SPELL_CONTAGION | — | — | — | no | buff | not implemented / not evaluated |
| SPELL_CONVERT_CITY_BASIUM | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_CONVERT_CITY_RANTINE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_COURAGE | PROMOTION_SPIRIT1 | PROMOTION_CHANNELING1 | — | no | buff | not implemented / not evaluated |
| SPELL_CREATE_BATTERING_RAM | — | — | TECH_ENGINEERING | yes | summon | not implemented / not evaluated |
| SPELL_CREATE_PUPPET | — | — | — | no | summon | not implemented / not evaluated |
| SPELL_CREATE_PUPPET_LOKI | — | — | — | no | summon | not implemented / not evaluated |
| SPELL_CREW_BUCCANEERS | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_CREW_LONGSHOREMEN | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_CREW_NORMAL_CREW | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_CREW_SKELETON_CREW | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_CROWN_OF_BRILLANCE | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_CROWN_OF_BRILLANCE_CHALID | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_CRUSH | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_CURE_DISEASE | PROMOTION_MEDIC2 | — | — | no | review XML | not implemented / not evaluated |
| SPELL_DANCE_OF_BLADES | PROMOTION_CHAOS1 | PROMOTION_CHANNELING1 | — | no | buff | not implemented / not evaluated |
| SPELL_DECIUS_JOIN | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DECIUS_SPLIT | PROMOTION_DECIUS | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_DECLARE_WAR_BARBS | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_DECLARE_NATIONALITY | PROMOTION_HIDDEN_NATIONALITY | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_DESTROY_UNDEAD | PROMOTION_LIFE2 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_DISPEL_MAGIC | PROMOTION_METAMAGIC2 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_DISRUPT | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_DIVINE_RETRIBUTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_DOMINATION | PROMOTION_MIND3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_DROP_ATHAME_ITEM | PROMOTION_ATHAME | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_BLACK_MIRROR_ITEM | PROMOTION_BLACK_MIRROR | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_CROWN_OF_AKHARIEN | PROMOTION_CROWN_OF_AKHARIEN | — | — | no | building | not implemented / not evaluated |
| SPELL_DROP_CROWN_OF_AKHARIEN_ITEM | PROMOTION_CROWN_OF_AKHARIEN | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_CROWN_OF_COMMAND_ITEM | PROMOTION_CROWN_OF_COMMAND | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_DRAGONS_HORDE | PROMOTION_DRAGONS_HORDE | — | — | no | building | not implemented / not evaluated |
| SPELL_DROP_DRAGONS_HORDE_ITEM | PROMOTION_DRAGONS_HORDE | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_EMPTY_BIER_ITEM | PROMOTION_EMPTY_BIER | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_GELA_ITEM | PROMOTION_GELA | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_GOLDEN_HAMMER_ITEM | PROMOTION_GOLDEN_HAMMER | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_HEALING_SALVE_ITEM | PROMOTION_HEALING_SALVE | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_INFERNAL_GRIMOIRE_ITEM | PROMOTION_INFERNAL_GRIMOIRE | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_JADE_TORC_ITEM | PROMOTION_JADE_TORC | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_NETHER_BLADE_ITEM | PROMOTION_NETHER_BLADE | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_ORTHUSS_AXE_ITEM | PROMOTION_ORTHUSS_AXE | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_PIECES_OF_BARNAXUS_ITEM | PROMOTION_PIECES_OF_BARNAXUS | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_POTION_OF_INVISIBILITY_ITEM | PROMOTION_POTION_OF_INVISIBILITY | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_POTION_OF_RESTORATION_ITEM | PROMOTION_POTION_OF_RESTORATION | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_ROD_OF_WINDS_ITEM | PROMOTION_ROD_OF_WINDS | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_SCORCHED_STAFF_ITEM | PROMOTION_SCORCHED_STAFF | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_STAFF_OF_SOULS_ITEM | PROMOTION_STAFF_OF_SOULS | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_SYLIVENS_PERFECT_LYRE | PROMOTION_SYLIVENS_PERFECT_LYRE | — | — | no | building | not implemented / not evaluated |
| SPELL_DROP_SYLIVENS_PERFECT_LYRE_ITEM | PROMOTION_SYLIVENS_PERFECT_LYRE | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_TIMOR_MASK_ITEM | PROMOTION_TIMOR_MASK | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_GODSLAYER_ITEM | PROMOTION_GODSLAYER | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROP_WAR_ITEM | PROMOTION_WAR | — | — | yes | summon | not implemented / not evaluated |
| SPELL_DROWN | — | — | — | no | review XML | not implemented / not evaluated |
| SPELL_EARTHQUAKE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ENCHANT_SPELLSTAFF | PROMOTION_ENCHANTMENT3 | — | — | no | buff | not implemented / not evaluated |
| SPELL_ENCHANTED_BLADE | PROMOTION_ENCHANTMENT1 | PROMOTION_CHANNELING1 | — | no | buff | partial: temporary proximity aura |
| SPELL_ENTANGLE | — | — | — | no | review XML | not implemented / not evaluated |
| SPELL_ENTER_PORTAL | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ENTERTAIN | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ESCAPE | PROMOTION_DIMENSIONAL1 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_AIFON_ISLE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_BARROW | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_BAIR_OF_LACUNA | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_BRADELINES_WELL | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_BROKEN_SEPULCHER | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_DUNGEON | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_GOBLIN_FORT | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_PALUS | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_PYRE_OF_THE_SERAPHIC | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_RUINS | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_EXPLORE_LAIR_SHIP_WRECK | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_FAIR_WINDS | PROMOTION_AIR1 | PROMOTION_CHANNELING1 | — | no | buff | not implemented / not evaluated |
| SPELL_FEAST | PROMOTION_VAMPIRE | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_FEED | PROMOTION_VAMPIRE | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_FERTILITY | PROMOTION_CREATION2 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_FIREBALL | PROMOTION_FIRE2 | — | — | no | summon | not implemented / not evaluated |
| SPELL_FLAMING_ARROWS | PROMOTION_ENCHANTMENT2 | — | — | no | buff | not implemented / not evaluated |
| SPELL_FLOATING_EYE | PROMOTION_METAMAGIC1 | — | — | no | summon | not implemented / not evaluated |
| SPELL_FOR_THE_HORDE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_FORM_WOLF_PACK | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_FOUND_TEMPLE_OF_KILMORPH | — | — | — | no | building | not implemented / not evaluated |
| SPELL_FOUND_TEMPLE_OF_LEAVES | — | — | — | no | building | not implemented / not evaluated |
| SPELL_FOUND_TEMPLE_OF_THE_EMPYREAN | — | — | — | no | building | not implemented / not evaluated |
| SPELL_FOUND_TEMPLE_OF_THE_ORDER | — | — | — | no | building | not implemented / not evaluated |
| SPELL_FOUND_TEMPLE_OF_THE_OVERLORDS | — | — | — | no | building | not implemented / not evaluated |
| SPELL_FOUND_TEMPLE_OF_THE_VEIL | — | — | — | no | building | not implemented / not evaluated |
| SPELL_GIFT_VAMPIRISM | PROMOTION_VAMPIRE | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_GIFTS_OF_NANTOSUELTA | — | — | TECH_MASONRY | yes | review XML | not implemented / not evaluated |
| SPELL_GIVE_HAMMER_TO_CRAFTSMAN | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_GRAFT_FLESH | PROMOTION_BODY3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_GROWTH | PROMOTION_CREATION1 | — | — | no | building | not implemented / not evaluated |
| SPELL_HASTE | PROMOTION_BODY1 | PROMOTION_CHANNELING1 | — | no | buff | partial: Body I self-Haste |
| SPELL_HASTURS_RAZOR | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_HEAL | PROMOTION_MEDIC3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ESUS_BLUR | PROMOTION_ESUS_AGENT | — | — | no | buff | not implemented / not evaluated |
| SPELL_ESUS_HASTE | PROMOTION_ESUS_AGENT | — | — | no | buff | not implemented / not evaluated |
| SPELL_ESUS_POISONED_BLADE | PROMOTION_ESUS_AGENT | — | TECH_POISONS | no | buff | not implemented / not evaluated |
| SPELL_ESUS_REGENERATION | PROMOTION_ESUS_AGENT | — | — | no | buff | not implemented / not evaluated |
| SPELL_ESUS_SHADOWWALK | PROMOTION_ESUS_AGENT | — | — | no | buff | not implemented / not evaluated |
| SPELL_EXTORT | PROMOTION_ESUS_AGENT | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_HEALING_SALVE | PROMOTION_HEALING_SALVE | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_HELLFIRE | — | — | — | yes | improvement | not implemented / not evaluated |
| SPELL_HERALDS_CALL | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_HIDE | PROMOTION_STEALTH | — | — | yes | buff | not implemented / not evaluated |
| SPELL_ESUS_HIDE | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_HIRE_ARCHER | — | — | TECH_ARCHERY | yes | review XML | not implemented / not evaluated |
| SPELL_HIRE_CHARIOT | — | — | TECH_TRADE | yes | review XML | not implemented / not evaluated |
| SPELL_HIRE_GOBLIN | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_HIRE_UNITS | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_HIRE_WOLF_RIDER | — | — | TECH_HORSEBACK_RIDING | yes | review XML | not implemented / not evaluated |
| SPELL_HOPE | PROMOTION_SPIRIT2 | — | — | no | building | not implemented / not evaluated |
| SPELL_HYBOREMS_WHISPER | — | — | TECH_MALEVOLENT_DESIGNS | yes | review XML | not implemented / not evaluated |
| SPELL_IMPERSONATE_LEADER | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_INQUISITION | PROMOTION_INQUISITOR | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_INSPIRATION | PROMOTION_MIND1 | PROMOTION_CHANNELING1 | — | no | building | partial: Mind I temporary Science |
| SPELL_ILLUMINATION | PROMOTION_SPIRIT3 | PROMOTION_CHANNELING3 | — | no | building | not implemented / not evaluated |
| SPELL_INTO_THE_MIST | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_IRA_UNLEASHED | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_KIDNAP | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_LABYRINTH | PROMOTION_DIMENSIONAL2 | — | — | no | review XML | not implemented / not evaluated |
| SPELL_LEGENDS | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_LICHDOM | PROMOTION_DEATH3 | — | TECH_DIVINE_ESSENCE | yes | buff | not implemented / not evaluated |
| SPELL_LOYALTY | PROMOTION_LAW1 | PROMOTION_CHANNELING1 | — | no | buff | not implemented / not evaluated |
| SPELL_MAELSTROM | PROMOTION_AIR2 | — | — | no | review XML | not implemented / not evaluated |
| SPELL_MAGIC_MISSILE | PROMOTION_FORCE2 | — | — | no | summon | not implemented / not evaluated |
| SPELL_MARCH_OF_THE_TREES | — | — | TECH_WAY_OF_THE_FORESTS | yes | review XML | not implemented / not evaluated |
| SPELL_MASK | — | — | TECH_DECEPTION | yes | buff | not implemented / not evaluated |
| SPELL_MEZMERIZE_ANIMAL | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_MIRROR | PROMOTION_BLACK_MIRROR | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_MORALE | — | — | — | no | buff | not implemented / not evaluated |
| SPELL_MOTHER_LODE | — | — | TECH_MINING | yes | review XML | not implemented / not evaluated |
| SPELL_MUTATION | PROMOTION_CHAOS2 | — | — | no | buff | not implemented / not evaluated |
| SPELL_OPEN_CHEST | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_PEACE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_PEACE_SEVEN_PINES | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_PILLAR_OF_FIRE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_PILLAR_OF_FIRE_CHALID | — | — | TECH_RIGHTEOUSNESS | yes | review XML | not implemented / not evaluated |
| SPELL_PIRATE_COVE | — | — | — | yes | improvement | not implemented / not evaluated |
| SPELL_POISONED_BLADE | PROMOTION_NATURE2 | — | — | no | buff | not implemented / not evaluated |
| SPELL_POTION_OF_INVISIBILITY | PROMOTION_POTION_OF_INVISIBILITY | — | — | no | buff | not implemented / not evaluated |
| SPELL_POTION_OF_RESTORATION | PROMOTION_POTION_OF_RESTORATION | — | — | no | review XML | not implemented / not evaluated |
| SPELL_PROMOTE_SETTLEMENT | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RAGE | — | — | — | no | buff | not implemented / not evaluated |
| SPELL_RAGING_SEAS | — | — | TECH_OPTICS | yes | review XML | not implemented / not evaluated |
| SPELL_RAISE_SKELETON | PROMOTION_DEATH1 | PROMOTION_CHANNELING1 | — | yes | summon | not implemented / not evaluated |
| SPELL_RALLY | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_READ_THE_GRIMOIRE | PROMOTION_INFERNAL_GRIMOIRE | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_REBUILD_BARNAXUS | PROMOTION_PIECES_OF_BARNAXUS | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RECRUIT | PROMOTION_RECRUITER | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RECRUIT_MERCENARY | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RECRUIT_NIGHTWATCH | — | — | TECH_BOWYERS | yes | review XML | not implemented / not evaluated |
| SPELL_REGENERATION | PROMOTION_BODY2 | — | — | no | buff | not implemented / not evaluated |
| SPELL_RELEASE_FROM_CAGE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RELIGIOUS_FERVOR | — | — | TECH_PRIESTHOOD | yes | review XML | not implemented / not evaluated |
| SPELL_REPAIR | PROMOTION_ENCHANTMENT1 | PROMOTION_DWARF | — | yes | review XML | not implemented / not evaluated |
| SPELL_RESSURECTION | PROMOTION_LIFE3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RESSURECTION_GRAVEYARD | PROMOTION_LIFE3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_REVEAL | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_REVELATION | PROMOTION_CHANNELING2 | PROMOTION_DIVINE | — | yes | review XML | not implemented / not evaluated |
| SPELL_REVELRY | — | — | TECH_FESTIVALS | yes | review XML | not implemented / not evaluated |
| SPELL_RIFT_CREATE | PROMOTION_DIMENSIONAL3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RIFT_CROSS | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RIFT_OPEN | PROMOTION_DIMENSIONAL3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RING_OF_FLAMES | PROMOTION_CHANNELING2 | PROMOTION_DIVINE | — | yes | review XML | not implemented / not evaluated |
| SPELL_RIVER_OF_BLOOD | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_ROAR | PROMOTION_DRAGON | PROMOTION_FEAR | — | yes | review XML | not implemented / not evaluated |
| SPELL_ROB_GRAVE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_RUST | PROMOTION_ENTROPY1 | PROMOTION_CHANNELING1 | — | no | buff | not implemented / not evaluated |
| SPELL_SACRIFICE_ALTAR | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SACRIFICE_PYRE | PROMOTION_ANGEL | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SANCTIFY | PROMOTION_LIFE1 | PROMOTION_CHANNELING1 | — | yes | review XML | not implemented / not evaluated |
| SPELL_SANCTUARY | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SCORCH | PROMOTION_SUN1 | PROMOTION_CHANNELING1 | — | yes | review XML | not implemented / not evaluated |
| SPELL_SEVER | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SHADOWWALK | PROMOTION_SHADOW2 | — | — | no | buff | not implemented / not evaluated |
| SPELL_SHIELD_OF_FAITH | PROMOTION_CHANNELING2 | PROMOTION_DIVINE | — | no | buff | not implemented / not evaluated |
| SPELL_SING | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SIRONAS_TOUCH | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SLAVE_TRADE_BUY | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SLAVE_TRADE_SELL | — | — | — | no | review XML | not implemented / not evaluated |
| SPELL_SLOW | PROMOTION_ICE1 | PROMOTION_CHANNELING1 | — | no | buff | not implemented / not evaluated |
| SPELL_SLOW_GREATER | — | — | — | no | buff | not implemented / not evaluated |
| SPELL_SNOWFALL | PROMOTION_ICE3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SNOWFALL_GREATER | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SPELLSTAFF | PROMOTION_SPELLSTAFF | — | — | no | review XML | not implemented / not evaluated |
| SPELL_SPORES | — | — | — | no | review XML | not implemented / not evaluated |
| SPELL_SPREAD_THE_COUNCIL_OF_ESUS | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_SPRING | PROMOTION_WATER1 | PROMOTION_CHANNELING1 | — | yes | review XML | partial: Water I terrain/smoke |
| SPELL_SPRINT | PROMOTION_CENTAUR | — | — | yes | buff | not implemented / not evaluated |
| SPELL_STASIS | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_STEAL | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_STONESKIN | PROMOTION_EARTH2 | — | — | no | buff | not implemented / not evaluated |
| SPELL_SUMMON_AIR_ELEMENTAL | PROMOTION_AIR3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_AUREALIS | PROMOTION_SUN3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_BALOR | — | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_DJINN | PROMOTION_METAMAGIC3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_EARTH_ELEMENTAL | PROMOTION_EARTH3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_EINHERJAR | PROMOTION_LAW2 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_FIRE_ELEMENTAL | PROMOTION_FIRE3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_ICE_ELEMENTAL | PROMOTION_ICE2 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_KRAKEN | — | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_MISTFORM | PROMOTION_SHADOW3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_PIT_BEAST | PROMOTION_ENTROPY2 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_RUNEWYN | PROMOTION_FORCE3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_SAND_LION | PROMOTION_CHANNELING2 | — | — | yes | summon | not implemented / not evaluated |
| SPELL_SUMMON_SPECTRE | PROMOTION_DEATH2 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_TIGER | PROMOTION_CHANNELING2 | PROMOTION_DIVINE | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_TREANT | — | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_WATER_ELEMENTAL | PROMOTION_WATER3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_SUMMON_WRAITH | PROMOTION_DEATH3 | — | — | no | summon | not implemented / not evaluated |
| SPELL_TAKE_ATHAME_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_ATHAME_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_BLACK_MIRROR_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_BLACK_MIRROR_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_CROWN_OF_AKHARIEN_BUILDING | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_CROWN_OF_AKHARIEN_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_CROWN_OF_AKHARIEN_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_CROWN_OF_COMMAND_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_CROWN_OF_COMMAND_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_DRAGONS_HORDE_BUILDING | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_DRAGONS_HORDE_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_DRAGONS_HORDE_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_EMPTY_BIER_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_EMPTY_BIER_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_GELA_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_GELA_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_GOLDEN_HAMMER_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_GOLDEN_HAMMER_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_GOLDEN_HAMMER_UNIT_NEW | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_HEALING_SALVE_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_HEALING_SALVE_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_INFERNAL_GRIMOIRE_BUILDING | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_INFERNAL_GRIMOIRE_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_INFERNAL_GRIMOIRE_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_JADE_TORC_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_JADE_TORC_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_NETHER_BLADE_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_NETHER_BLADE_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_ORTHUSS_AXE_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_ORTHUSS_AXE_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_PIECES_OF_BARNAXUS_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_PIECES_OF_BARNAXUS_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_POTION_OF_INVISIBILITY_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_POTION_OF_INVISIBILITY_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_POTION_OF_RESTORATION_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_POTION_OF_RESTORATION_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_ROD_OF_WINDS_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_ROD_OF_WINDS_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_SCORCHED_STAFF_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_SCORCHED_STAFF_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_STAFF_OF_SOULS_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_STAFF_OF_SOULS_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_SYLIVENS_PERFECT_LYRE_BUILDING | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_SYLIVENS_PERFECT_LYRE_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_SYLIVENS_PERFECT_LYRE_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_TIMOR_MASK_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_TIMOR_MASK_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_GODSLAYER_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_GODSLAYER_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_WAR_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_WAR_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAUNT | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TEACH_SPELLCASTING | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TEMPERANCE | PROMOTION_FORCE1 | — | — | no | buff | not implemented / not evaluated |
| SPELL_TREETOP_TACTICS | PROMOTION_NATURE1 | PROMOTION_CHANNELING1 | — | no | buff | partial: Nature I forest bonus |
| SPELL_TRUST | PROMOTION_SPIRIT3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TSUNAMI | PROMOTION_CHANNELING2 | PROMOTION_DIVINE | — | yes | review XML | not implemented / not evaluated |
| SPELL_UNYIELDING_ORDER | — | — | — | yes | building | not implemented / not evaluated |
| SPELL_UNYIELDING_ORDER_SPHENER | — | — | — | yes | building | not implemented / not evaluated |
| SPELL_UPGRADE_DOVIELLO_AXEMAN | — | — | TECH_BRONZE_WORKING | no | review XML | not implemented / not evaluated |
| SPELL_UPGRADE_DOVIELLO_AXEMAN_LUCIAN | — | — | TECH_BRONZE_WORKING | yes | review XML | not implemented / not evaluated |
| SPELL_UPGRADE_DOVIELLO_BATTLEMASTER | — | — | TECH_IRON_WORKING | no | review XML | not implemented / not evaluated |
| SPELL_UPGRADE_DOVIELLO_CHAMPION | — | — | TECH_IRON_WORKING | no | review XML | not implemented / not evaluated |
| SPELL_UPGRADE_DOVIELLO_WARRIOR | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_UPGRADE_DOVIELLO_WARRIOR_SLAVE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_UPGRADE_SPECTRE | — | — | TECH_SORCERY | no | review XML | not implemented / not evaluated |
| SPELL_VALOR | PROMOTION_LAW3 | — | — | no | buff | not implemented / not evaluated |
| SPELL_VEIL_OF_NIGHT | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_VITALIZE | PROMOTION_NATURE3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_WALL_OF_STONE | PROMOTION_EARTH1 | PROMOTION_CHANNELING1 | — | no | building | not implemented / not evaluated |
| SPELL_WANE | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_WARCRY | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_WHITEOUT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_WILD_HUNT | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_WITHER | PROMOTION_ENTROPY3 | — | — | no | buff | not implemented / not evaluated |
| SPELL_WONDER | PROMOTION_CHAOS3 | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_WORLDBREAK | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_GREAT_GENERAL_JOIN | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_GREAT_GENERAL_SPLIT | PROMOTION_GREAT_GENERAL | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TARGET_WEAK | PROMOTION_MARKSMAN_DISABLED | — | — | no | buff | not implemented / not evaluated |
| SPELL_TARGET_STRONG | PROMOTION_MARKSMAN | — | — | no | buff | not implemented / not evaluated |
| SPELL_DROP_PIKE_OF_TEARS_ITEM | PROMOTION_PIKE_OF_TEARS | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_PIKE_OF_TEARS_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_PIKE_OF_TEARS_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_FROZEN_FLAME | PROMOTION_FROZEN_FLAME | — | — | no | building | not implemented / not evaluated |
| SPELL_TAKE_FROZEN_FLAME_BUILDING | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_TAKE_FROZEN_FLAME_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_FROZEN_FLAME_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_SOL_ITEM | PROMOTION_SOL | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_SOL_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_SOL_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_SELL_ANIMAL | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_DROP_AMULET_SEAS_ITEM | PROMOTION_AMULET_SEAS | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_AMULET_SEAS_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_AMULET_SEAS_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_ANCIENT_BOW_ITEM | PROMOTION_ANCIENT_BOW | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_ANCIENT_BOW_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_ANCIENT_BOW_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_COMPELLING_JEWEL_ITEM | PROMOTION_COMPELLING_JEWEL | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_COMPELLING_JEWEL_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_COMPELLING_JEWEL_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_HEART_AMULET_ITEM | PROMOTION_HEART_AMULET | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_HEART_AMULET_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_HEART_AMULET_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_MENACING_HELM_ITEM | PROMOTION_MENACING_HELM | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_MENACING_HELM_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_MENACING_HELM_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_HAUBERK_OF_ABJURATION_ITEM | PROMOTION_HAUBERK_OF_ABJURATION | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_HAUBERK_OF_ABJURATION_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_HAUBERK_OF_ABJURATION_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_PATRIAN_ARTIFACT | PROMOTION_PATRIAN_ARTIFACT | — | — | no | building | not implemented / not evaluated |
| SPELL_DROP_OBSIDIAN_SPEAR_ITEM | PROMOTION_OBSIDIAN_SPEAR | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_OBSIDIAN_SPEAR_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_OBSIDIAN_SPEAR_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_RADIANT_AMULET_ITEM | PROMOTION_RADIANT_AMULET | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_RADIANT_AMULET_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_RADIANT_AMULET_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
| SPELL_DROP_WYRMSLAYER_ITEM | PROMOTION_WYRMSLAYER | — | — | yes | summon | not implemented / not evaluated |
| SPELL_TAKE_WYRMSLAYER_PROMOTION | — | — | — | yes | review XML | not implemented / not evaluated |
| SPELL_TAKE_WYRMSLAYER_UNIT | — | — | — | yes | buff | not implemented / not evaluated |
