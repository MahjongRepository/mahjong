from mahjong.constants import EAST
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.scores import Aotenjou
from mahjong.hand_calculating.yaku import Yaku
from mahjong.tile import TilesConverter
from tests.utils_for_tests import _make_hand_config, _string_to_136_tile


def _snapshot(yaku_list: list[Yaku]) -> list[tuple[int, str, int, int]]:
    return [(yaku.yaku_id, str(yaku), yaku.han_open, yaku.han_closed) for yaku in yaku_list]


def test_dora_of_earlier_result_is_unchanged() -> None:
    tiles = TilesConverter.string_to_136_array(man="234", pin="234567", sou="23488")
    win_tile = _string_to_136_tile(sou="4")
    config = _make_hand_config(is_riichi=True)

    first = HandCalculator.estimate_hand_value(
        tiles,
        win_tile,
        dora_indicators=TilesConverter.string_to_136_array(man="1"),
        config=config,
    )
    first_yaku = _snapshot(first.yaku)
    assert first_yaku[-1] == (120, "Dora 1", 1, 1)

    second = HandCalculator.estimate_hand_value(
        tiles,
        win_tile,
        dora_indicators=TilesConverter.string_to_136_array(man="1", sou="7"),
        config=config,
    )
    assert _snapshot(second.yaku)[-1] == (120, "Dora 3", 3, 3)
    assert _snapshot(first.yaku) == first_yaku
    assert config.yaku.dora.han_closed == 1


def test_double_yakuman_follows_option_on_reused_config() -> None:
    tiles = TilesConverter.string_to_136_array(sou="119", man="19", pin="19", honors="1234567")
    win_tile = _string_to_136_tile(sou="1")
    config = _make_hand_config(disable_double_yakuman=True)

    result = HandCalculator.estimate_hand_value(tiles, win_tile, config=config)
    assert result.han == 13

    config.options.has_double_yakuman = True
    result = HandCalculator.estimate_hand_value(tiles, win_tile, config=config)
    assert result.han == 26


def test_aotenjou_removes_precursors_of_renamed_daisharin() -> None:
    tiles = TilesConverter.string_to_136_array(sou="22334455667788")
    win_tile = _string_to_136_tile(sou="7")
    config = _make_hand_config(
        is_tsumo=True,
        player_wind=EAST,
        round_wind=EAST,
        allow_daisharin=True,
        allow_daisharin_other_suits=True,
    )

    result = HandCalculator.estimate_hand_value(tiles, win_tile, scores_calculator_factory=Aotenjou, config=config)
    assert result.han == 14
    assert _snapshot(result.yaku) == [(0, "Menzen Tsumo", 0, 1), (109, "Daichikurin", 0, 13)]
    assert config.yaku.daisharin.name == "Daisharin"
