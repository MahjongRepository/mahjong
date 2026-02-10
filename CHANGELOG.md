Releases History
================

2.0.0 (TBD)
-------------------

## New features

### Ura dora support
`HandCalculator.estimate_hand_value()` now accepts an `ura_dora_indicators` parameter and calculates ura dora accordingly when the hand won after riichi.

### Separate yakuhai yaku for each seat wind and round wind
Wind yakuhai are now represented as individual yaku classes per direction: `SeatWindEast`, `SeatWindSouth`, `SeatWindWest`, `SeatWindNorth` for seat winds, and `RoundWindEast`, `RoundWindSouth`, `RoundWindWest`, `RoundWindNorth` for round winds.

## Improvements

### Faster hand calculation
A redesigned hand division algorithm and a more streamlined yaku detection process have reduced the overall hand calculation time to roughly 1/3 of the previous version.

#### Benchmark
(TODO)

### Major methods converted to `staticmethod`
The following methods are now available as static methods:
- `HandDivider.divide_hand()`
- `FuCalculator.calculate_fu()`
- `HandCalculator.estimate_hand_value()`
- `ScoresCalculator.calculate_scores()`
- `Aotenjou.calculate_scores()`
- `Aotenjou.aotenjou_filter_yaku()`
- `Agari.is_agari()`
- `Shanten.calculate_shanten()`
- `Shanten.calculate_shanten_for_chiitoitsu_hand()`
- `Shanten.calculate_shanten_for_kokushi_hand()`
- `Shanten.calculate_shanten_for_regular_hand()`

## Breaking changes
- Dropped support for Python 3.9 (because it is EOL). Python 3.10 or later is required.
- The following constants in `constants.py` have been converted from lists to frozensets for O(1) lookup performance. Code using list-specific operations (such as indexing or concatenation) will need updates.
  - `TERMINAL_INDICES`
  - `WINDS`
  - `HONOR_INDICES`
  - `AKA_DORA_LIST` (now `AKA_DORAS`)
- `AKA_DORA_LIST` has been renamed to `AKA_DORAS`. Update all imports and references.
- Removed deprecated `Meld.CHANKAN`. Use `Meld.SHOUMINKAN` instead.
- The `use_cache` parameter of `HandDivider.divide_hand()` has been removed following the introduction of `functools.lru_cache`.
- The `use_hand_divider_cache` parameter of `HandCalculator.estimate_hand_value()` has been removed following the introduction of `functools.lru_cache`.
- The following methods have been removed due to algorithm changes.
  - `HandDivider.find_pairs()`
  - `HandDivider.find_valid_combinations()`
  - `HandDivider.clear_cache()`
  - `FuCalculator.round_fu()`
- The following class and instance attributes have been removed as part of internal cleanup related to the transition of several methods to staticmethods. These attributes were not intended for public use.
  - `HandDivider.divider_cache`
  - `HandDivider.cache_key`
  - `HandCalculator.config`
  - `HandCalculator.divider`
  - `Shanten.tiles`
  - `Shanten.number_melds`
  - `Shanten.number_tatsu`
  - `Shanten.number_pairs`
  - `Shanten.number_jidahai`
  - `Shanten.number_characters`
  - `Shanten.number_isolated_tiles`
  - `Shanten.min_shanten`
- The following methods now invoke other methods via the class rather than `self`. This affects code that relies on subclass overrides, instance attribute assignments, or instance method replacements.
  - `HandDivider.divide_hand()`
  - `FuCalculator.calculate_fu()`
  - `HandCalculator.estimate_hand_value()`
  - `Agari.is_agari()`
  - `Shanten.calculate_shanten()`
  - `Shanten.calculate_shanten_for_regular_hand()`
- In the following classes, some instance variables were incorrectly declared as class variables. They are now defined as type annotations. These variables are overwritten in `__init__()`, so this has no effect on typical usage, but it does affect code that accesses them as class variables.
  - `OptionalRules`
  - `HandConfig`
  - `HandResponse`
  - `Yaku`
  - `Meld`
  - `Tile`
- `HandDivider.divide_hand()` now only succeeds when the tiles can be divided into exactly five blocks. Previous implementation succeeded even when the tiles could be divided into six or more blocks. This change also affects `HandCalculator.estimate_hand_value()`, which internally relies on `HandDivider.divide_hand()`.
- `Yaku` class has been redesigned:
  - `Yaku` is now an abstract base class (`abc.ABC`). Only `is_condition_met()` is decorated with `@abstractmethod`. Directly instantiating `Yaku` or an incomplete subclass now raises `TypeError` instead of `NotImplementedError`.
  - Removed `Yaku.set_attributes()` and `Yaku.__init__()`. All yaku attributes (`yaku_id`, `name`, `han_open`, `han_closed`, `is_yakuman`) are now class-level attributes on each subclass. Subclasses that override `set_attributes()` must convert to class-level attributes.
  - Removed deprecated `Yaku.english` and `Yaku.japanese`. Use `Yaku.name` instead.
  - Removed `Yaku.tenhou_id`. Use the `YAKU_ID_TO_TENHOU_ID` mapping from `mahjong.hand_calculating.yaku_config` instead.
  - `yaku_id` values have been reassigned. Each `Yaku` subclass now defines its own fixed `yaku_id` as a class attribute. Code that relies on specific `yaku_id` values (e.g., for serialization or lookup) must be updated.
- Wind yakuhai classes have been renamed and restructured:
  - `YakuhaiEast` → `SeatWindEast`, `YakuhaiSouth` → `SeatWindSouth`, `YakuhaiWest` → `SeatWindWest`, `YakuhaiNorth` → `SeatWindNorth`.
  - `YakuhaiOfPlace` and `YakuhaiOfRound` have been removed and replaced by per-direction round wind classes: `RoundWindEast`, `RoundWindSouth`, `RoundWindWest`, `RoundWindNorth`.
  - `YakuConfig` attributes renamed: `east` → `seat_wind_east`, `south` → `seat_wind_south`, `west` → `seat_wind_west`, `north` → `seat_wind_north`. `yakuhai_place` and `yakuhai_round` replaced by `round_wind_east`, `round_wind_south`, `round_wind_west`, `round_wind_north`.
  - Seat wind `is_condition_met` now accepts `(hand, player_wind)` and round wind accepts `(hand, round_wind)` instead of both accepting `(hand, player_wind, round_wind)`.
- `han_open` and `han_closed` are now `int` (default `0`) instead of `int | None` (default `None`). A value of `0` means the yaku is not available in the respective hand type.
- Yaku calculation order has changed: chinitsu/honitsu are now mutually exclusive, and tsuisou/honroto/chinroto checks now require no chi sets. Users manually overwriting `config.yaku` fields may be affected.
- Yakuhai detection (hatsu, haku, chun, winds) now uses `has_pon_or_kan_of()` instead of counting triplets. Behavior changes for invalid hands with two or more identical triplets of the same tile.
- Fixed an issue where `KokushiMusou.is_condition_met()` would return `None` if the condition was not met. It now consistently returns a `bool` value. Remove any `None` checks in the code that relied on the previous behavior.
- `Shanten.calculate_shanten()` and `Shanten.calculate_shanten_for_regular_hand()` now raises `ValueError` instead of `assert` when the number of tiles is 15 or more.
- `HandDivider.divide_hand()` now determines block type from `Meld.type` instead of inferring it from `Meld.tiles`. Behavior may differ for invalid `Meld.tiles` or inconsistent `Meld.type` and `Meld.tiles` combinations.
- Removed `HandCalculator.ERR_HAND_NOT_CORRECT`. Hands that previously returned `ERR_HAND_NOT_CORRECT` now return `ERR_HAND_NOT_WINNING` instead.
- `Meld.tiles` is now a `tuple[int, ...]` instead of `list[int]`. Code that mutates `Meld.tiles` in place (e.g., `append()`, `sort()`, item assignment) must be updated.

## What's Changed
- Placeholder. It would be filled on release automatically

1.4.0 (Oct 20, 2025)
-------------------

## What's Changed
* chore: Update astral-sh/setup-uv action
* chore: Update actions/checkout action
* chore: Add Python 3.14 support
* feat: Deprecate `Shanten.number_characters` and `Shanten.number_isolated_tiles`
* feat: Deprecate internal state properties of Shanten
* docs: Apply markdownlint rules to README
* docs: Add badges
* docs: Change `uv venv` to `uv sync` for accurate setup and dependency installation via `pyproject.toml`

1.3.0 (May 17, 2025)
-------------------

## Breaking Changes
* dropped support for Python 3.7 and 3.8
 
## Bug fixes
* fix: Correct miscalculation of shanten number for Seven Pairs (chiitoitsu, 七対子)
* fix: Correct miscalculation of shanten number for general form

## Other changes
* migrate the project to a modern Python stack: uv and ruff
* other minor improvements and optimizations along the way
* add support for Python 3.13

1.2.1 (Sep 8, 2023)
-------------------

## Features
* Adjust warning configs

## Chores
* Remove Python 3.6 support
* Fix typo in the test name
* Move wiki files to md files for easier diffs

1.2.0 (May 22, 2022)
-------------------

This release contains many improvements and bug fixes. The new version was tested over millions of real hanchans and many bugs were fixed.

## Incompatibility highlight:
* Python 2 support was dropped
* Changes in interfaces, please refer `doc/example.py` for usage examples. For example now all four tiles should be in hand tiles when you have kan melds.

1.1.11 (Oct 28, 2020)
-------------------

* Speed up performance a bit
* Add support for Python 3.9

1.1.10 (May 11, 2020)
-------------------

* Add japanese yaku names
* Fix an issue with not correct ryuuiisou detection
* Allow to print aka dora in TilesConverter.to_one_line_string()
  method ("0" symbol)
* Add support for Python 3.8

1.1.9 (Jul 29, 2019)
------------------

* Add TilesConverter.one_line_string_to_136_array() and TilesConverter.one_line_string_to_34_array() methods

1.1.8 (Jul 25, 2019)
------------------

* Fix an issue with incorrect daburu chuuren poutou calculations
* Allow passing '0' as a red five to tiles converter

1.1.7 (Apr 9, 2019)
------------------

* Introduce OptionalRules hand configuration

1.1.6 (Feb 10, 2019)
------------------

* Fix a bug when hatsu yaku was added to the hand instead of chun
* Fix a bug where kokushi wasn't combined with tenhou/renhou/chihou
* Add English names to all yaku
* Add support of python 2.7
* Add a way to pass aka dora to tile converter

1.1.5 (Sep 4, 2018)
------------------

* Allow to disable chiitoitsu or kokushi in shanten calculator

1.1.4 (Aug 31, 2018)
------------------

* Add is_terminal() and is_dora_indicator_for_terminal()
  functions to the utils.py

1.1.3 (Aug 22, 2018)
------------------

* Add is_tile_strictly_isolated() function to the utils.py

1.1.2 (Oct 14, 2017)
------------------

* Add settings for different kazoe yakuman calculation (it kan be an yakuman or a sanbaiman)
* Support up to sextuple yakuman scores
* Support kiriage mangan
* Allow to disable +2 fu in open hand
* Allow to disable tsumo pinfu (add 2 additional fu for hand like that)

1.1.1 (Oct 7, 2017)
------------------

* Fix a bug with not correct agari state determination and closed kan in the hand

1.1.0 (Oct 7, 2017)
------------------

## Breaking changes:

* Interface of hand calculator was changed. New interface will allow to easy support different game rules

## Additional fixes:

* Refactor hand divider. Allow to pass melds objects instead of arrays
* Add file with usage examples
* Minor project refactoring

1.0.5 (Sep 25, 2017)
------------------

* Improve installation script

1.0.4 (Sep 25, 2017)
------------------

Bug fixes:

* Fix refactoring regressions with kan sets and dora calculations
* Fix regression with sankantsusuukantsu and called chankan
* Closed kan can't be used in chuuren poutou
* Fix yaku ids (some of them had incorrect numbers)

Features:

* Allow to disable double yakuman (like suuanko tanki)
* Remove float calculations from scores and fu
* Add travis build status
* Add usage examples to the readme

1.0.3 (Sep 23, 2017)
------------------

* Hand calculation code was moved from mahjong bot package
  <https://github.com/MahjongRepository/tenhou-python-bot>
* This library can calculate hand cost (han, fu with details, yaku and scores) for riichi mahjong (japanese version)
