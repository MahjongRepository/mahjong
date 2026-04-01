Releases History
================

2.0.0
-------------------

## New features

### Ura dora support
`HandCalculator.estimate_hand_value()` now accepts an `ura_dora_indicators` parameter and calculates ura dora accordingly when the hand won after riichi.

### Separate yakuhai yaku for each seat wind and round wind
Wind yakuhai are now represented as individual yaku classes per direction: `SeatWindEast`, `SeatWindSouth`, `SeatWindWest`, `SeatWindNorth` for seat winds, and `RoundWindEast`, `RoundWindSouth`, `RoundWindWest`, `RoundWindNorth` for round winds.

## Improvements

### Faster hand calculation
A redesigned hand division algorithm (roughly 3x faster), more streamlined yaku detection, and more efficient data structures make the overall hand calculation roughly 6x faster than the previous version.

#### Benchmark
Benchmark for hand calculation (han, fu, yaku scores) was run 5 times to calculate median, with 500,000 hands per iteration.

For `1.4.0` version:
- Throughput: 5925 hands/sec (based on median)
- Avg per hand: 0.169ms (based on median)

For `2.0.0` version:
- Throughput: 35364 hands/sec (based on median)
- Avg per hand: 0.028ms (based on median)

### TypedDict return types for scores, fu, and hand calculations
Plain `dict` return types have been replaced with `TypedDict` classes for improved type safety and IDE auto-completion:
- `ScoresResult` — returned by `ScoresCalculator.calculate_scores()` and `Aotenjou.calculate_scores()`
- `FuDetail` — returned (as list elements) by `FuCalculator.calculate_fu()`
- `SuitCount` — returned (as list elements) by `count_tiles_by_suits()`

`HandResponse.cost` is now typed as `ScoresResult | None` and `HandResponse.fu_details` as `list[FuDetail] | None`.

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
- `Shanten.calculate_shanten()` and `Shanten.calculate_shanten_for_regular_hand()` now raises `ValueError` for tile counts divisible by 3 (0, 3, 6, 9, 12). These counts never occur in real riichi mahjong gameplay. Valid tile counts are 1, 2, 4, 5, 7, 8, 10, 11, 13, 14.
- `Shanten.calculate_shanten()` now ignores chiitoitsu and kokushi calculations when the hand contains melds (i.e., the number of tiles is less than 13), preventing invalid shanten results from being considered.
- `HandDivider.divide_hand()` now determines block type from `Meld.type` instead of inferring it from `Meld.tiles`. Behavior may differ for invalid `Meld.tiles` or inconsistent `Meld.type` and `Meld.tiles` combinations.
- Removed `HandCalculator.ERR_HAND_NOT_CORRECT`. Hands that previously returned `ERR_HAND_NOT_CORRECT` now return `ERR_HAND_NOT_WINNING` instead.
- `Meld.tiles` is now a `tuple[int, ...]` instead of `list[int]`. Code that mutates `Meld.tiles` in place (e.g., `append()`, `sort()`, item assignment) must be updated.
- `Aotenjou.calculate_scores()` now returns a full `ScoresResult` with all keys (`main`, `additional`, `main_bonus`, `additional_bonus`, `kyoutaku_bonus`, `total`, `yaku_level`) instead of a minimal dict with only `main` and `additional`. Code that relies on the absence of these keys (e.g., catching `KeyError`) must be updated.
- Hands without yaku no longer count dora. `HandResponse` now returns only `error` with all other fields as `None`, instead of returning `han`, `fu`, and dora yaku alongside the error.

## What's Changed
* refactor: Simplify to_136_array implementation by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/93
* feat: Change instance methods to static methods by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/92
* feat: Rewrite `HandDivider.divide_hand()` with a backtracking-based algorithm and caching improvements by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/94
* feat: Remove deprecated `Meld.CHANKAN` property by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/95
* feat: Remove deprecated `Yaku.english` and `Yaku.japanese` properties by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/96
* refactor: Eliminate an unnecessary generator expression by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/97
* refactor: Use list comprehension in `_decompose_chiitoitsu` by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/98
* fix: Fix type hint for `fu_details` parameter of `HandResponse.__init__()` by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/100
* feat: Migrate class variables to type annotations by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/99
* refactor: Simplify `TilesConverter.to_one_line_string()` implementation by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/101
* fix: Fix type hint for `valued_tiles` parameter of `FuCalculator.calculate_fu()` by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/102
* refactor: Simplify `is_dora_indicator_for_terminal()` implementation by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/106
* refactor: Simplify `simplify()` implementation by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/107
* test: Split agari multi‑assert tests into parameterized tests by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/123
* test: Split shanten multi‑assert tests into parameterized tests by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/124
* test: Split utils multi‑assert tests into parameterized tests by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/126
* feat: Add `Shanten.TENPAI_STATE` by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/127
* refactor!: Improve performance across the project by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/128
* refactor!: drop support for Python 3.9 by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/131
* chore: Update Ruff Configuration to `select = ["ALL"]` by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/132
* refactor: Fix lint print-empty-string (FURB105) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/133
* docs: Update CHANGELOG.md by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/130
* chore: improve tests coverage by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/134
* fix: Check that no melds are present when decomposing chiitoitsu by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/135
* refactor: Use match statement in _decompose_honors_hand() by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/136
* refactor: Streamline the determination of ChuurenPoutou by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/138
* feat: Add DRAGONS by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/139
* refactor: Fix lint yoda-conditions (SIM300) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/143
* refactor! redo yaku_id system by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/137
* refactor! refactor yaku class further by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/144
* refactor: Fix lint implicit-return-value (RET502) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/145
* refactor: Fix lint utf8-encoding-declaration (UP009) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/146
* refactor: Fix lint repeated-equality-comparison (PLR1714) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/148
* feat: add ura dora yaku by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/147
* refactor: Fix lint reimplemented-builtin (SIM110) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/149
* refactor: Fix lint len-test (PLC1802) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/150
* refactor: Fix lint unnecessary-range-start (PIE808) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/151
* refactor: Fix lint parenthesize-chained-operators (RUF021) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/153
* feat: improve yakuhai yaku by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/152
* refactor: Fix lint collection-literal-concatenation (RUF005) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/155
* chore: Update actions/checkout by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/156
* refactor!: improve performance of fu calculations by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/157
* chore: Add maintainers by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/154
* chore: Install only the packages required by CI by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/158
* refactor: Fix lint invalid-assert-message-literal-argument (RUF040) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/159
* refactor: Fix lint unnecessary-iterable-allocation-for-first-element (RUF015) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/160
* refactor: Fix lint unnecessary-assign (RET504) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/161
* refactor: Fix lint superfluous-else-return (RET505) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/162
* fix: Fix reutrn value of KokushiMusou.is_condition_met() by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/163
* refactor: Fix lint implicit-return (RET503) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/164
* refactor: Fix lint unused-unpacked-variable (RUF059) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/165
* refactor: Fix lint manual-list-comprehension (PERF401) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/166
* refactor: Fix lint if-stmt-min-max (PLR1730) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/167
* refactor: Fix lint f-string (UP032) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/168
* refactor: improve dora calculations performance by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/169
* refactor: improve Agari.is_agari performace by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/170
* refactor: Fix lint collapsible-else-if (PLR5501) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/172
* refactor: Fix lint collapsible-if (SIM102) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/173
* chore: publish wiki from source code by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/174
* refactor: Fix lint if-else-block-instead-of-if-exp (SIM108) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/175
* refactor: Fix lint eq-without-hash (PLW1641) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/176
* refactor: Fix lint blanket-type-ignore (PGH003) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/177
* refactor: Fix lint unused-static-method-argument (ARG004) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/178
* chore: Ignore lint unused-method-argument (ARG002) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/180
* refactor: Fix lint redefined-loop-name (PLW2901) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/181
* chore: Update Ruff by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/182
* style: Fix lint missing-trailing-comma (COM812) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/183
* feat!: Replace assert with `ValueError` for tile count validation in `Shanten.calculate_shanten_for_regular_hand()` by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/184
* chore: add wiki v2 pages by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/179
* refactor: Simplify `TilesConverter.string_to_136_array()` implementation by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/186
* refactor: improve hand divider performance a bit by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/185
* docs: Add Japanese wiki by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/188
* refactor: optimize performance for hand calculations by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/189
* chore: Add wiki URL to `[project.urls]` by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/191
* fix: Add validation for hand decomposition by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/190
* chore: Ignore lint missing-trailing-comma (COM812) by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/194
* refactor: improve performance for hand calculations further by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/192
* docs: Add trailing commas to code examples on the wiki by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/196
* docs: Split the examples into separate files by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/197
* test: add parametrize for some pytest tests by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/193
* refactor: rename aka doras const by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/201
* refactor: change meld tiles from list to tuple by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/200
* fix: Fix type error of Meld.tiles by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/202
* refactor: replace dict responses with typed dicts by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/203
* fix: Allow round and seat wind parameters to be optional in condition checks by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/204
* bug: hands without yaku but with dora should be rejected by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/206
* docs: Fix description for kazoe_limit parameter in Wiki by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/208
* chore: Add ty to dev dependencies by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/209
* chore: Limit the type checking to only the library by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/211
* docs: Align the explanation of daichisei in the Chinese version of the Wiki with the English and Japanese versions by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/212
* chore: Add type checking to make commands and CI by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/213
* chore: Add format check to lint command by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/214
* docs: Translate `Output` in Japanese Wiki by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/215
* docs: add v2 version link for v1 pages by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/216
* docs: fix license copyright by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/218
* chore: add codeowners file by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/217
* chore: Add ruff settings for docstring by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/220
* chore: Update MANIFEST.in by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/221
* docs: add agari section to wiki, extend shanten section by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/219
* docs: Update examples by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/222
* docs: add validation results by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/223
* docs: add doc for agari class by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/224
* docs: add shanten doc by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/225
* docs: Introduce Sphinx by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/226
* feat: Add each yaku to `__all__` in `__init__.py` by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/227
* docs: Add API documentation by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/228
* docs: add meld doc by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/229
* docs: Add the description for tile representations to the pacakege docstring by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/230
* chore: Improve sphinx options by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/231
* docs: Fix the package docstring by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/232
* docs: add doc for constants by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/233
* docs: Update documentation links in README by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/234
* docs: add tiles documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/235
* docs: Add a license section to README by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/237
* docs: add utils documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/236
* docs: Unify tile representation by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/238
* docs: Match the nuances of the Chinese and Japanese wikis to the English version by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/240
* docs: add fu doc by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/239
* bug: stabilize shanten input validation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/242
* docs: add hand divider documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/243
* refactor: Avoid creating instances of `Yaku` for `yaku_id` references by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/247
* docs: add hand config documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/244
* docs: add hand response documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/248
* docs: add scores documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/250
* docs: add hand documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/249
* chore: Tweak pyproject.toml settings by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/251
* docs: add init modules documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/254
* docs: add yaku config documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/252
* docs: add yaku abstract class documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/253
* chore: Update actions/deploy-pages by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/255
* chore: Specify ruff ignore for each individual yaku by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/256
* docs: Add the hand_calculating module docstring by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/257
* docs: Simplify docstring by inlining mpsz-notation example by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/258
* docs: add yaku and yakuman documentation by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/259
* docs: Normalize terminology in Japanese wiki by replacing "断幺九" with the standard mahjong notation "断么九" by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/260
* docs: Correct "pon/kan" to "pon or kan" by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/261
* docs: add missed doc strings by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/262
* docs: Clarify shanten calculation details and target hand structure in docstring by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/263
* docs: add missed doc strings by @Nihisil in https://github.com/MahjongRepository/mahjong/pull/264
* docs: Improve README by @Apricot-S in https://github.com/MahjongRepository/mahjong/pull/265

**Full Changelog**: https://github.com/MahjongRepository/mahjong/compare/v1.4.0...v2.0.0

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
