Releases History
================

2.0.0 (TBD)
-------------------

## Highlights

### Faster hand calculation
A redesigned hand decomposition algorithm and a more streamlined yaku detection process have reduced the overall hand calculation time to roughly 1/3 of the previous version.

#### Benchmark
(TODO)

### Major methods converted to `staticmethod`
Several evaluation methods have been converted to staticmethods.

#### List of staticmethods

- `mahjong.hand_calculating.divider.HandDivider`
  - `divide_hand()`
- `mahjong.hand_calculating.fu.FuCalculator`
  - `calculate_fu()`
  - `round_fu()`
- `mahjong.hand_calculating.hand.HandCalculator`
  - `estimate_hand_value()`
- `mahjong.hand_calculating.scores.ScoresCalculator`
  - `calculate_scores()`
- `mahjong.hand_calculating.scores.Aotenjou`
  - `calculate_scores()`
  - `aotenjou_filter_yaku()`
- `mahjong.agari.Agari`
  - `is_agari()`
- `mahjong.shanten.Shanten`
  - `calculate_shanten()`
  - `calculate_shanten_for_chiitoitsu_hand()`
  - `calculate_shanten_for_kokushi_hand()`
  - `calculate_shanten_for_regular_hand()`

## Breaking changes

### Things that likely require your code changes
- Dropped support for Python 3.9 (because it is EOL). Python 3.10 or later is required.
- Constants in `constants.py` have been converted from lists to frozensets for O(1) lookup performance. This affects `TERMINAL_INDICES`, `HONOR_INDICES`, `WINDS` and `AKA_DORA_LIST`. Code using list-specific operations (indexing, concatenation) will need updates.
- Removed deprecated `Meld.CHANKAN`. Use `Meld.SHOUMINKAN` instead.

### Internal behavior changes that may affect you if you rely on specific implementation details
- Yaku calculation order has changed: chinitsu/honitsu are now mutually exclusive, and tsuisou/honroto/chinroto checks now require no chi sets. Users manually overwriting `config.yaku` fields may be affected.
- Yakuhai detection (hatsu, haku, chun, winds) now uses `has_pon_or_kan_of()` instead of counting triplets. Behavior changes for invalid hands with two or more identical triplets of the same tile.

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
