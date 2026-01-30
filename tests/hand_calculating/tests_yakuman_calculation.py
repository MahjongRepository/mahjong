import pytest

from mahjong.constants import EAST
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.hand_calculating.yaku_config import YakuConfig
from mahjong.meld import Meld
from mahjong.tile import TilesConverter
from tests.utils_for_tests import _hand, _make_hand_config, _make_meld, _string_to_136_tile


def test_is_tenhou() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_tenhou=True))
    assert result.error is None
    assert result.han == 13
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_chiihou() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_chiihou=True))
    assert result.error is None
    assert result.han == 13
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_daisangen() -> None:
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="123", man="22", honors="555666777")
    assert config.daisangen.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="123", man="22", honors="555666777")
    win_tile = _string_to_136_tile(honors="7")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 13
    assert result.fu == 50
    assert len(result.yaku) == 1


def test_is_shosuushi() -> None:
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="123", honors="11122233344")
    assert config.shosuushi.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="123", honors="11122233344")
    win_tile = _string_to_136_tile(honors="4")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 13
    assert result.fu == 60
    assert len(result.yaku) == 1


def test_is_daisuushi() -> None:
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="22", honors="111222333444")
    assert config.daisuushi.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="22", honors="111222333444")
    win_tile = _string_to_136_tile(honors="4")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 26
    assert result.fu == 60
    assert len(result.yaku) == 1


def test_is_tsuisou() -> None:
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(honors="11122233366677")
    assert config.tsuisou.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(honors="11223344556677")
    assert config.tsuisou.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(honors="1133445577", pin="88", sou="11")
    assert not config.tsuisou.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(honors="11223344556677")
    win_tile = _string_to_136_tile(honors="7")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 13
    assert result.fu == 25
    assert len(result.yaku) == 1


def test_is_tsuisou_and_daichisei() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(honors="11223344556677")
    win_tile = _string_to_136_tile(honors="7")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(has_daichisei=True))
    assert result.error is None
    assert result.han == 26
    assert len(result.yaku) == 2


def test_is_chinroto() -> None:
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="111999", man="111999", pin="99")
    assert config.chinroto.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="111222", man="111999", pin="99")
    win_tile = _string_to_136_tile(pin="9")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 26
    assert result.fu == 60
    assert len(result.yaku) == 1


def test_is_kokushi() -> None:
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="119", man="19", pin="19", honors="1234567")
    assert config.kokushi.is_condition_met(None, tiles)

    tiles = TilesConverter.string_to_136_array(sou="119", man="19", pin="19", honors="1234567")
    win_tile = _string_to_136_tile(sou="9")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 13
    assert result.fu == 0
    assert len(result.yaku) == 1

    tiles = TilesConverter.string_to_136_array(sou="119", man="19", pin="19", honors="1234567")
    win_tile = _string_to_136_tile(sou="1")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 26
    assert result.fu == 0
    assert len(result.yaku) == 1


def test_is_ryuisou() -> None:
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="22334466888", honors="666")
    assert config.ryuisou.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="22334466888", honors="666")
    win_tile = _string_to_136_tile(honors="6")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 13
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_suuankou() -> None:
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="111444", man="333", pin="44555")
    win_tile = _string_to_136_tile(sou="4")

    assert config.suuankou.is_condition_met(_hand(tiles), win_tile, True)
    assert not config.suuankou.is_condition_met(_hand(tiles), win_tile, False)

    tiles = TilesConverter.string_to_136_array(sou="111444", man="333", pin="44555")
    win_tile = _string_to_136_tile(pin="5")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True))
    assert result.error is None
    assert result.han == 13
    assert result.fu == 50
    assert len(result.yaku) == 1

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False))
    assert result.han != 13

    tiles = TilesConverter.string_to_136_array(sou="111444", man="333", pin="44455")
    win_tile = _string_to_136_tile(pin="5")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True))
    assert result.error is None
    assert result.han == 26
    assert result.fu == 50
    assert len(result.yaku) == 1

    tiles = TilesConverter.string_to_136_array(man="33344455577799")
    win_tile = _string_to_136_tile(man="9")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False))
    assert result.error is None
    assert result.han == 26
    assert result.fu == 50
    assert len(result.yaku) == 1


@pytest.mark.parametrize(
    "tiles",
    [
        TilesConverter.string_to_34_array(man="11112345678999"),
        TilesConverter.string_to_34_array(pin="11122345678999"),
        TilesConverter.string_to_34_array(sou="11123345678999"),
        TilesConverter.string_to_34_array(sou="11123445678999"),
        TilesConverter.string_to_34_array(sou="11123455678999"),
        TilesConverter.string_to_34_array(sou="11123456678999"),
        TilesConverter.string_to_34_array(sou="11123456778999"),
        TilesConverter.string_to_34_array(sou="11123456788999"),
        TilesConverter.string_to_34_array(sou="11123456789999"),
    ],
)
def test_is_chuuren_poutou(tiles: list[int]) -> None:
    config = YakuConfig()
    assert config.chuuren_poutou.is_condition_met(_hand(tiles))


@pytest.mark.parametrize(
    "tiles",
    [
        TilesConverter.string_to_34_array(man="11112233488999"),
        TilesConverter.string_to_34_array(pin="11123444678999"),
    ],
)
def test_is_not_chuuren_poutou(tiles: list[int]) -> None:
    config = YakuConfig()
    assert not config.chuuren_poutou.is_condition_met(_hand(tiles))


def test_chuuren_poutou_hand_value() -> None:
    hand = HandCalculator()
    tiles = TilesConverter.string_to_136_array(man="11123456789999")
    win_tile = _string_to_136_tile(man="1")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 13
    assert result.fu == 40
    assert len(result.yaku) == 1

    daburi = [
        ["11122345678999", "2"],
        ["11123456789999", "9"],
        ["11112345678999", "1"],
    ]
    for hand_tiles, win_tile in daburi:
        tiles = TilesConverter.string_to_136_array(man=hand_tiles)
        win_tile = _string_to_136_tile(man=win_tile)

        result = hand.estimate_hand_value(tiles, win_tile)
        assert result.error is None
        assert result.han == 26
        assert len(result.yaku) == 1

    tiles = TilesConverter.string_to_136_array(pin="111234566789999")
    win_tile = _string_to_136_tile(pin="3")
    melds = [_make_meld(Meld.KAN, pin="9999", is_open=False)]

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 6
    assert result.fu == 70
    assert len(result.yaku) == 1


def test_is_suukantsu() -> None:
    hand = HandCalculator()
    config = YakuConfig()

    melds = [
        _make_meld(Meld.KAN, sou="1111"),
        _make_meld(Meld.KAN, sou="3333"),
        _make_meld(Meld.KAN, pin="5555"),
        _make_meld(Meld.SHOUMINKAN, man="2222"),
    ]
    assert config.suukantsu.is_condition_met(None, melds)

    tiles = TilesConverter.string_to_136_array(sou="11113333", man="2222", pin="445555")
    win_tile = _string_to_136_tile(pin="4")
    melds = [
        _make_meld(Meld.KAN, sou="1111"),
        _make_meld(Meld.KAN, sou="3333"),
        _make_meld(Meld.KAN, pin="5555"),
        _make_meld(Meld.KAN, man="2222"),
    ]

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 13
    assert result.fu == 70
    assert len(result.yaku) == 1


def test_disabled_double_yakuman() -> None:
    hand = HandCalculator()

    # kokushi
    tiles = TilesConverter.string_to_136_array(sou="119", man="19", pin="19", honors="1234567")
    win_tile = _string_to_136_tile(sou="1")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(disable_double_yakuman=True))
    assert result.error is None
    assert result.han == 13
    assert result.fu == 0
    assert len(result.yaku) == 1

    # suanko tanki
    tiles = TilesConverter.string_to_136_array(sou="111444", man="333", pin="44455")
    win_tile = _string_to_136_tile(pin="5")

    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(is_tsumo=True, disable_double_yakuman=True)
    )
    assert result.error is None
    assert result.han == 13
    assert result.fu == 50
    assert len(result.yaku) == 1

    # chuuren poutou
    tiles = TilesConverter.string_to_136_array(man="11122345678999")
    win_tile = _string_to_136_tile(man="2")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(disable_double_yakuman=True))
    assert result.error is None
    assert result.han == 13
    assert result.fu == 50
    assert len(result.yaku) == 1

    # daisushi
    tiles = TilesConverter.string_to_136_array(sou="22", honors="111222333444")
    win_tile = _string_to_136_tile(honors="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(disable_double_yakuman=True))
    assert result.error is None
    assert result.han == 13
    assert result.fu == 60
    assert len(result.yaku) == 1


def test_sextuple_yakuman() -> None:
    hand = HandCalculator()

    # 1112223334445z 5z tenhou & tsuisou & daisushi & suuankou tanki
    tiles = TilesConverter.string_to_136_array(honors="11122233344455")
    win_tile = _string_to_136_tile(honors="5")

    config = _make_hand_config(is_tsumo=True, is_tenhou=True, disable_double_yakuman=False)

    result = hand.estimate_hand_value(tiles, win_tile, config=config)
    assert result.error is None
    assert result.han == 78
    assert result.cost["main"] == 96000
    assert result.cost["additional"] == 48000

    # 5z -11-z -22-z -33-z -44-z 5z suukantsu & tsuisou & daisushi & suuankou tanki
    tiles = TilesConverter.string_to_136_array(honors="111122223333444455")
    win_tile = _string_to_136_tile(honors="5")

    config = _make_hand_config(disable_double_yakuman=False)
    melds = [
        _make_meld(Meld.KAN, is_open=False, honors="1111"),
        _make_meld(Meld.KAN, is_open=False, honors="2222"),
        _make_meld(Meld.KAN, is_open=False, honors="3333"),
        _make_meld(Meld.KAN, is_open=False, honors="4444"),
    ]

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=config)
    assert result.error is None
    assert result.han == 78
    assert result.cost["main"] == 192000


def test_kokushi_musou_multiple_yakuman() -> None:
    hand_calculator = HandCalculator()

    # kokushi test

    tiles = TilesConverter.string_to_136_array(sou="19", pin="19", man="19", honors="12345677")
    win_tile = TilesConverter.string_to_136_array(honors="1")[0]

    hand_config = HandConfig(is_tsumo=True, is_tenhou=False, is_chiihou=False)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

    assert hand_calculation.error is None
    assert len(hand_calculation.yaku) == 1
    assert hand_config.yaku.kokushi in hand_calculation.yaku
    assert hand_config.yaku.daburu_kokushi not in hand_calculation.yaku
    assert hand_config.yaku.tenhou not in hand_calculation.yaku
    assert hand_config.yaku.chiihou not in hand_calculation.yaku
    assert hand_calculation.han == 13

    hand_config = HandConfig(is_tsumo=True, is_tenhou=True, is_chiihou=False)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

    assert hand_calculation.error is None
    assert len(hand_calculation.yaku) == 2
    assert hand_config.yaku.kokushi in hand_calculation.yaku
    assert hand_config.yaku.daburu_kokushi not in hand_calculation.yaku
    assert hand_config.yaku.tenhou in hand_calculation.yaku
    assert hand_config.yaku.chiihou not in hand_calculation.yaku
    assert hand_calculation.han == 26

    hand_config = HandConfig(is_tsumo=True, is_tenhou=False, is_chiihou=True)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

    assert hand_calculation.error is None
    assert len(hand_calculation.yaku) == 2
    assert hand_config.yaku.kokushi in hand_calculation.yaku
    assert hand_config.yaku.daburu_kokushi not in hand_calculation.yaku
    assert hand_config.yaku.tenhou not in hand_calculation.yaku
    assert hand_config.yaku.chiihou in hand_calculation.yaku
    assert hand_calculation.han == 26

    # double kokushi test

    tiles = TilesConverter.string_to_136_array(sou="19", pin="19", man="19", honors="12345677")
    win_tile = TilesConverter.string_to_136_array(honors="7")[0]

    hand_config = HandConfig(is_tsumo=True, is_tenhou=False, is_chiihou=False)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

    assert hand_calculation.error is None
    assert len(hand_calculation.yaku) == 1
    assert hand_config.yaku.kokushi not in hand_calculation.yaku
    assert hand_config.yaku.daburu_kokushi in hand_calculation.yaku
    assert hand_config.yaku.tenhou not in hand_calculation.yaku
    assert hand_config.yaku.chiihou not in hand_calculation.yaku
    assert hand_calculation.han == 26

    hand_config = HandConfig(is_tsumo=True, is_tenhou=True, is_chiihou=False)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

    assert hand_calculation.error is None
    assert len(hand_calculation.yaku) == 2
    assert hand_config.yaku.kokushi not in hand_calculation.yaku
    assert hand_config.yaku.daburu_kokushi in hand_calculation.yaku
    assert hand_config.yaku.tenhou in hand_calculation.yaku
    assert hand_config.yaku.chiihou not in hand_calculation.yaku
    assert hand_calculation.han == 39

    hand_config = HandConfig(is_tsumo=True, is_tenhou=False, is_chiihou=True)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

    assert hand_calculation.error is None
    assert len(hand_calculation.yaku) == 2
    assert hand_config.yaku.kokushi not in hand_calculation.yaku
    assert hand_config.yaku.daburu_kokushi in hand_calculation.yaku
    assert hand_config.yaku.tenhou not in hand_calculation.yaku
    assert hand_config.yaku.chiihou in hand_calculation.yaku
    assert hand_calculation.han == 39

    hand_config = HandConfig(is_tsumo=False, is_renhou=True, options=OptionalRules(renhou_as_yakuman=True))

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

    assert hand_calculation.error is None
    assert len(hand_calculation.yaku) == 2
    assert hand_config.yaku.kokushi not in hand_calculation.yaku
    assert hand_config.yaku.daburu_kokushi in hand_calculation.yaku
    assert hand_config.yaku.renhou_yakuman in hand_calculation.yaku
    assert hand_config.yaku.tenhou not in hand_calculation.yaku
    assert hand_config.yaku.chiihou not in hand_calculation.yaku
    assert hand_calculation.han == 39

    hand_config = HandConfig(
        is_tsumo=False,
        is_renhou=True,
        is_riichi=True,
        is_open_riichi=True,
        options=OptionalRules(renhou_as_yakuman=True, has_sashikomi_yakuman=True),
    )

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

    assert hand_calculation.error is None
    assert len(hand_calculation.yaku) == 3
    assert hand_config.yaku.kokushi not in hand_calculation.yaku
    assert hand_config.yaku.daburu_kokushi in hand_calculation.yaku
    assert hand_config.yaku.renhou_yakuman in hand_calculation.yaku
    assert hand_config.yaku.sashikomi in hand_calculation.yaku
    assert hand_config.yaku.tenhou not in hand_calculation.yaku
    assert hand_config.yaku.chiihou not in hand_calculation.yaku
    assert hand_calculation.han == 52


def test_is_renhou_yakuman() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_renhou=True, renhou_as_yakuman=True)
    )
    assert result.error is None
    assert result.han == 13
    assert len(result.yaku) == 1


def test_is_not_daisharin() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(pin="22334455667788")
    win_tile = _string_to_136_tile(pin="8")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config())
    assert result.error is None
    assert result.han == 11
    assert len(result.yaku) == 4


def test_is_daisharin() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(pin="22334455667788")
    win_tile = _string_to_136_tile(pin="8")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(allow_daisharin=True))
    assert result.error is None
    assert result.han == 13
    assert len(result.yaku) == 1
    assert result.yaku[0].name == "Daisharin"


def test_is_not_daichikurin() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="22334455667788")
    win_tile = _string_to_136_tile(sou="8")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(allow_daisharin=True))
    assert result.error is None
    assert result.han == 11
    assert len(result.yaku) == 4


def test_is_daichikurin() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="22334455667788")
    win_tile = _string_to_136_tile(sou="8")

    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(allow_daisharin=True, allow_daisharin_other_suits=True)
    )
    assert result.error is None
    assert result.han == 13
    assert len(result.yaku) == 1
    assert result.yaku[0].name == "Daichikurin"


def test_is_not_daisuurin() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="22334455667788")
    win_tile = _string_to_136_tile(man="8")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(allow_daisharin=True))
    assert result.error is None
    assert result.han == 11
    assert len(result.yaku) == 4


def test_is_daisuurin() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="22334455667788")
    win_tile = _string_to_136_tile(man="8")

    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(allow_daisharin=True, allow_daisharin_other_suits=True)
    )
    assert result.error is None
    assert result.han == 13
    assert len(result.yaku) == 1
    assert result.yaku[0].name == "Daisuurin"


def test_is_open_riichi_sashikomi() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_riichi=True, is_open_riichi=True, has_sashikomi_yakuman=True),
    )
    assert result.error is None
    assert result.han == 13
    assert len(result.yaku) == 1


def test_septuple_yakuman_disabled() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(honors="11122233344455")
    win_tile = _string_to_136_tile(honors="5")

    config = _make_hand_config(
        is_renhou=True, disable_double_yakuman=False, renhou_as_yakuman=True, has_sashikomi_yakuman=True
    )

    result = hand.estimate_hand_value(tiles, win_tile, config=config)
    assert result.error is None
    assert result.han == 78
    assert result.cost["main"] == 192000


def test_septuple_yakuman_enabled() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(honors="11122233344455")
    win_tile = _string_to_136_tile(honors="5")

    config = _make_hand_config(
        is_tsumo=False,
        is_riichi=True,
        is_open_riichi=True,
        is_renhou=True,
        disable_double_yakuman=False,
        renhou_as_yakuman=True,
        has_sashikomi_yakuman=True,
        limit_to_sextuple_yakuman=False,
    )

    result = hand.estimate_hand_value(tiles, win_tile, config=config)
    assert result.error is None
    assert result.han == 91
    assert result.cost["main"] == 224000


def test_paarenchan_no_yaku_disallowed() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(pin="12367778", sou="678", man="456")
    win_tile = _string_to_136_tile(pin="7")
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, paarenchan=1))
    assert result.error is not None, None


def test_paarenchan_no_yaku_allowed() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(pin="12367778", sou="678", man="456")
    win_tile = _string_to_136_tile(pin="7")
    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(is_tsumo=False, paarenchan=1, paarenchan_needs_yaku=False)
    )
    assert result.error is None, None
    assert result.han == 13


def test_paarenchan() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(pin="111222777", sou="44455")
    win_tile = _string_to_136_tile(pin="7")
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(paarenchan=1, is_tsumo=True))
    assert result.error is None, None
    assert result.han == 26

    tiles = TilesConverter.string_to_136_array(pin="111222777", sou="44455")
    win_tile = _string_to_136_tile(pin="7")
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(paarenchan=4, is_tsumo=True))
    assert result.error is None, None
    assert result.han == 65


def test_sextuple_yakuman_limit() -> None:
    """
    Verify that sextuple yakuman limit caps han at 78.
    Uses the septuple yakuman hand (renhou + tsuisou + daisuushi + suuankou_tanki + sashikomi)
    with limit_to_sextuple_yakuman=True (the default).
    """
    hand = HandCalculator()

    # same hand as test_septuple_yakuman_enabled but with default sextuple limit
    tiles = TilesConverter.string_to_136_array(honors="11122233344455")
    win_tile = _string_to_136_tile(honors="5")

    config = _make_hand_config(
        is_tsumo=False,
        is_riichi=True,
        is_open_riichi=True,
        is_renhou=True,
        disable_double_yakuman=False,
        renhou_as_yakuman=True,
        has_sashikomi_yakuman=True,
        limit_to_sextuple_yakuman=True,
    )

    result = hand.estimate_hand_value(tiles, win_tile, config=config)
    assert result.error is None
    assert result.han == 78


def test_kokushi_sashikomi_with_daburu_riichi_and_open_riichi() -> None:
    """
    Verify kokushi + sashikomi via daburu_riichi + open_riichi on ron.
    """
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="19", pin="19", man="19", honors="12345677")
    win_tile = _string_to_136_tile(honors="7")

    config = _make_hand_config(
        is_tsumo=False,
        is_daburu_riichi=True,
        is_open_riichi=True,
        player_wind=EAST,
        round_wind=EAST,
        has_sashikomi_yakuman=True,
    )

    result = hand.estimate_hand_value(tiles, win_tile, config=config)
    assert result.error is None
    assert config.yaku.daburu_kokushi in result.yaku
    assert config.yaku.sashikomi in result.yaku
    assert result.han == 39


def test_kokushi_with_paarenchan() -> None:
    """
    Verify kokushi hand combined with paarenchan yakuman.
    """
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="19", pin="19", man="19", honors="12345677")
    win_tile = _string_to_136_tile(honors="7")

    config = _make_hand_config(
        is_tsumo=False,
        paarenchan=1,
        player_wind=EAST,
        round_wind=EAST,
    )

    result = hand.estimate_hand_value(tiles, win_tile, config=config)
    assert result.error is None
    assert config.yaku.daburu_kokushi in result.yaku
    assert config.yaku.paarenchan in result.yaku
    assert result.han == 39
