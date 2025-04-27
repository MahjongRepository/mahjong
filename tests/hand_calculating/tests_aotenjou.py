from tile import TilesConverter
from utils_for_tests import _make_hand_config, _make_meld, _string_to_136_tile

from mahjong.constants import EAST
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.scores import Aotenjou
from mahjong.meld import Meld


def test_aotenjou_hands():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="119", man="19", pin="19", honors="1234567")
    win_tile = _string_to_136_tile(sou="1")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(player_wind=EAST, round_wind=EAST, disable_double_yakuman=True),
    )
    assert result.error is None
    assert result.han == 13
    assert result.fu == 40
    assert len(result.yaku) == 1
    assert result.cost["main"] == 7864400

    tiles = TilesConverter.string_to_136_array(man="234", honors="11122233344")
    win_tile = _string_to_136_tile(man="2")
    melds = [
        _make_meld(Meld.PON, honors="111"),
        _make_meld(Meld.PON, honors="333"),
    ]

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 17
    assert result.fu == 40
    assert len(result.yaku) == 4
    assert result.cost["main"] + result.cost["additional"] == 83886200

    tiles = TilesConverter.string_to_136_array(honors="11122233444777")
    win_tile = _string_to_136_tile(honors="2")
    melds = [
        _make_meld(Meld.PON, honors="444"),
    ]

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 31
    assert result.fu == 50
    assert len(result.yaku) == 6
    assert result.cost["main"] + result.cost["additional"] == 1717986918400

    # monster hand for fun

    tiles = TilesConverter.string_to_136_array(honors="111133555566667777")
    win_tile = _string_to_136_tile(honors="3")

    melds = [
        _make_meld(Meld.KAN, honors="1111", is_open=False),
        _make_meld(Meld.KAN, honors="5555", is_open=False),
        _make_meld(Meld.KAN, honors="6666", is_open=False),
        _make_meld(Meld.KAN, honors="7777", is_open=False),
    ]

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        dora_indicators=TilesConverter.string_to_136_array(honors="22224444"),
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(
            is_riichi=True, is_tsumo=True, is_ippatsu=True, is_haitei=True, player_wind=EAST, round_wind=EAST
        ),
    )
    assert result.error is None
    assert result.han == 95
    assert result.fu == 160
    assert len(result.yaku) == 11
    assert result.cost["main"] + result.cost["additional"] == 101412048018258352119736256430200


def test_daisangen():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="11123", honors="555666777")
    win_tile = _string_to_136_tile(sou="1")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.fu == 60
    assert result.han == 20
    assert len(result.yaku) == 4
    assert result.cost["main"] == 1509949500


def test_shousuushii():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123", honors="11122233444")
    win_tile = _string_to_136_tile(honors="2")
    melds = [
        _make_meld(Meld.PON, honors="444"),
    ]

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 18
    assert result.fu == 50
    assert len(result.yaku) == 5
    assert result.cost["main"] + result.cost["additional"] == 209715200


def test_daisuushii():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="11", honors="111222333444")
    win_tile = _string_to_136_tile(honors="2")
    melds = [
        _make_meld(Meld.PON, honors="444"),
    ]

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 34
    assert result.fu == 50
    assert len(result.yaku) == 6
    assert result.cost["main"] + result.cost["additional"] == 13743895347200


def test_tsuuiisou():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(honors="11133344455566")
    win_tile = _string_to_136_tile(honors="6")
    melds = [
        _make_meld(Meld.PON, honors="444"),
    ]

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 18
    assert result.fu == 60
    assert len(result.yaku) == 5
    assert result.cost["main"] + result.cost["additional"] == 251658400


def test_suuankou():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="11133355566688")
    win_tile = _string_to_136_tile(man="8")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 33
    assert result.fu == 50
    assert len(result.yaku) == 3
    assert result.cost["main"] + result.cost["additional"] == 6871947673600


def test_chinroutou():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="111999", sou="11999", pin="111")
    win_tile = _string_to_136_tile(sou="9")
    melds = [
        _make_meld(Meld.PON, pin="111"),
    ]

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 15
    assert result.fu == 50
    assert len(result.yaku) == 2
    assert result.cost["main"] + result.cost["additional"] == 26214400


def test_chuuren_poutou():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="11112345678999")
    win_tile = _string_to_136_tile(man="1")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 29
    assert result.fu == 30
    assert len(result.yaku) == 3
    assert result.cost["main"] + result.cost["additional"] == 257698037800


def test_chuuren_poutou_inner():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="11123455678999")
    win_tile = _string_to_136_tile(man="5")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 27
    assert result.fu == 40
    assert len(result.yaku) == 2
    assert result.cost["main"] + result.cost["additional"] == 85899346000


def test_suukantsu():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="1111", sou="4444", pin="9999", honors="333322")
    win_tile = _string_to_136_tile(honors="2")

    melds = [
        _make_meld(Meld.KAN, man="1111"),
        _make_meld(Meld.KAN, sou="4444"),
        _make_meld(Meld.KAN, pin="9999"),
        _make_meld(Meld.KAN, honors="3333"),
    ]

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST),
    )
    assert result.error is None
    assert result.han == 13
    assert result.fu == 80
    assert len(result.yaku) == 1
    assert result.cost["main"] + result.cost["additional"] == 10485800


def test_daisharin():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(pin="22334455667788")
    win_tile = _string_to_136_tile(pin="7")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST, allow_daisharin=True),
    )
    assert result.error is None
    assert result.han == 14
    assert result.fu == 30
    assert len(result.yaku) == 2
    assert result.cost["main"] + result.cost["additional"] == 7864400


def test_ryuisou():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="223344666888", honors="66")
    win_tile = _string_to_136_tile(sou="8")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        scores_calculator_factory=Aotenjou,
        config=_make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST, allow_daisharin=True),
    )
    assert result.error is None
    assert result.han == 15
    assert result.fu == 40
    assert len(result.yaku) == 3
    assert result.cost["main"] + result.cost["additional"] == 20971600
