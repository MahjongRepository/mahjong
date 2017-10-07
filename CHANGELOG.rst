Releases History
================

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
