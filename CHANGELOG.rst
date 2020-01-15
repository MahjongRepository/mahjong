Releases History
================

1.1.9 (2019-07-29)
------------------
-  Add `TilesConverter.one_line_string_to_136_array()` and `TilesConverter.one_line_string_to_34_array()` methods

1.1.8 (2019-07-25)
------------------
- Fix an issue with incorrect daburu chuuren poutou calculations
- Allow passing '0' as a red five to tiles converter


1.1.7 (2019-04-09)
------------------
- Introduce OptionalRules hand configuration

1.1.6 (2019-02-10)
------------------
- Fix a bug when hatsu yaku was added to the hand instead of chun
- Fix a bug where kokushi wasn't combined with tenhou/renhou/chihou
- Add English names to all yaku
- Add support of python 2.7
- Add a way to pass aka dora to tile converter

1.1.5 (2018-09-04)
------------------

- Allow to disable chiitoitsu or kokushi in shanten calculator

1.1.4 (2018-08-31)
------------------

- Add is_terminal() and is_dora_indicator_for_terminal() functions to the utils.py

1.1.3 (2018-08-22)
------------------

- Add is_tile_strictly_isolated() function to the utils.py

1.1.2 (2017-10-14)
------------------

- Add settings for different kazoe yakuman calculation (it kan be an yakuman or a sanbaiman)
- Support up to sextuple yakuman scores
- Support kiriage mangan
- Allow to disable +2 fu in open hand
- Allow to disable tsumo pinfu (add 2 additional fu for hand like that)

1.1.1 (2017-10-07)
------------------

- Fix a bug with not correct agari state determination and closed kan in the hand

1.1.0 (2017-10-07)
------------------

Breaking changes:

- Interface of hand calculator was changed. New interface will allow to easy support different game rules

Additional fixes:

- Refactor hand divider. Allow to pass melds objects instead of arrays
- Add file with usage examples
- Minor project refactoring


1.0.5 (2017-09-25)
------------------

- Improve installation script


1.0.4 (2017-09-25)
------------------

Bug fixes:

- Fix refactoring regressions with kan sets and dora calculations
- Fix regression with sankantsu\suukantsu and called chankan
- Closed kan can't be used in chuuren poutou
- Fix yaku ids (some of them had incorrect numbers)

Features:

- Allow to disable double yakuman (like suuanko tanki)
- Remove float calculations from scores and fu
- Add travis build status
- Add usage examples to the readme


1.0.3 (2017-09-23)
------------------

- Hand calculation code was moved from mahjong bot package https://github.com/MahjongRepository/tenhou-python-bot
- This library can calculate hand cost (han, fu with details, yaku and scores) for riichi mahjong (japanese version)
