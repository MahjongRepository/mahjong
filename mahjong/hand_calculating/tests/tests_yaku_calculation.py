from utils_for_tests import _hand, _make_hand_config, _make_meld, _string_to_136_tile

from mahjong.constants import EAST, FIVE_RED_SOU, NORTH, SOUTH, WEST
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.hand_calculating.yaku_config import YakuConfig
from mahjong.meld import Meld
from mahjong.tile import TilesConverter


def test_hands_calculation():
    """
    Group of hands that were not properly calculated on tenhou replays
    I did fixes and leave hands in tests, to be sure that bugs were fixed.
    """

    hand = HandCalculator()
    player_wind = EAST

    tiles = TilesConverter.string_to_136_array(pin="112233999", honors="11177")
    win_tile = _string_to_136_tile(pin="9")
    melds = [
        _make_meld(Meld.PON, honors="111"),
        _make_meld(Meld.CHI, pin="123"),
        _make_meld(Meld.CHI, pin="123"),
    ]

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.fu == 30

    # we had a bug with multiple dora indicators and honor sets
    # this test is working with this situation
    tiles = TilesConverter.string_to_136_array(pin="22244456799", honors="4444")
    win_tile = _string_to_136_tile(pin="2")
    dora_indicators = [_string_to_136_tile(sou="3"), _string_to_136_tile(honors="3")]
    melds = [_make_meld(Meld.KAN, honors="4444")]
    result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators, melds=melds)
    assert result.error is None
    assert result.han == 6
    assert result.fu == 50
    assert len(result.yaku) == 2

    # if we can't add pinfu to the hand
    # we can add 2 fu to make hand more expensive
    tiles = TilesConverter.string_to_136_array(sou="678", man="11", pin="123345", honors="666")
    win_tile = _string_to_136_tile(pin="3")
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True))
    assert result.fu == 40

    tiles = TilesConverter.string_to_136_array(man="234789", pin="12345666")
    win_tile = _string_to_136_tile(pin="6")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.fu == 30

    tiles = TilesConverter.string_to_136_array(sou="678", pin="34555789", honors="555")
    win_tile = _string_to_136_tile(pin="5")
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True))
    assert result.fu == 40

    tiles = TilesConverter.string_to_136_array(sou="123345678", man="678", pin="88")
    win_tile = _string_to_136_tile(sou="3")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1

    tiles = TilesConverter.string_to_136_array(sou="12399", man="123456", pin="456")
    win_tile = _string_to_136_tile(sou="1")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1

    tiles = TilesConverter.string_to_136_array(sou="111123666789", honors="11")
    win_tile = _string_to_136_tile(sou="1")
    melds = [_make_meld(Meld.PON, sou="666")]
    dora_indicators = [_string_to_136_tile(honors="4")]
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        dora_indicators=dora_indicators,
        config=_make_hand_config(player_wind=player_wind),
    )
    assert result.fu == 40
    assert result.han == 4

    tiles = TilesConverter.string_to_136_array(pin="12333", sou="567", honors="666777")
    win_tile = _string_to_136_tile(pin="3")
    melds = [_make_meld(Meld.PON, honors="666"), _make_meld(Meld.PON, honors="777")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.fu == 30
    assert result.han == 2

    tiles = TilesConverter.string_to_136_array(pin="12367778", sou="678", man="456")
    win_tile = _string_to_136_tile(pin="7")
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_riichi=True))
    assert result.fu == 40
    assert result.han == 1

    tiles = TilesConverter.string_to_136_array(man="11156677899", honors="7777")
    win_tile = _string_to_136_tile(man="7")
    melds = [
        _make_meld(Meld.KAN, honors="7777"),
        _make_meld(Meld.PON, man="111"),
        _make_meld(Meld.CHI, man="678"),
    ]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.fu == 40
    assert result.han == 3

    tiles = TilesConverter.string_to_136_array(man="122223777888", honors="66")
    win_tile = _string_to_136_tile(man="2")
    melds = [_make_meld(Meld.CHI, man="123"), _make_meld(Meld.PON, man="777")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.fu == 30
    assert result.han == 2

    tiles = TilesConverter.string_to_136_array(pin="11144678888", honors="444")
    win_tile = _string_to_136_tile(pin="8")
    melds = [
        _make_meld(Meld.PON, honors="444"),
        _make_meld(Meld.PON, pin="111"),
        _make_meld(Meld.PON, pin="888"),
    ]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.fu == 30
    assert result.han == 2

    tiles = TilesConverter.string_to_136_array(sou="67778", man="345", pin="999", honors="222")
    win_tile = _string_to_136_tile(sou="7")
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True))
    assert result.fu == 40
    assert result.han == 1

    tiles = TilesConverter.string_to_136_array(sou="33445577789", man="345")
    win_tile = _string_to_136_tile(sou="7")
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True))
    assert result.fu == 30
    assert result.han == 2

    tiles = TilesConverter.string_to_136_array(pin="112233667788", honors="22")
    win_tile = _string_to_136_tile(pin="3")
    melds = [_make_meld(Meld.CHI, pin="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.fu == 30
    assert result.han == 2

    tiles = TilesConverter.string_to_136_array(sou="345", man="12333456789")
    win_tile = _string_to_136_tile(man="3")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.fu == 40
    assert result.han == 2

    tiles = TilesConverter.string_to_136_array(sou="11123456777888")
    melds = [
        _make_meld(Meld.CHI, sou="123"),
        _make_meld(Meld.PON, sou="777"),
        _make_meld(Meld.PON, sou="888"),
    ]
    win_tile = _string_to_136_tile(sou="4")
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=True))
    assert result.fu == 30
    assert result.han == 5

    tiles = TilesConverter.string_to_136_array(sou="112233789", honors="55777")
    melds = [_make_meld(Meld.CHI, sou="123")]
    win_tile = _string_to_136_tile(sou="2")
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.fu == 40
    assert result.han == 4

    tiles = TilesConverter.string_to_136_array(pin="234777888999", honors="22")
    melds = [_make_meld(Meld.CHI, pin="234"), _make_meld(Meld.CHI, pin="789")]
    win_tile = _string_to_136_tile(pin="9")
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.fu == 30
    assert result.han == 2

    tiles = TilesConverter.string_to_136_array(pin="77888899", honors="777", man="444")
    melds = [_make_meld(Meld.PON, honors="777"), _make_meld(Meld.PON, man="444")]
    win_tile = _string_to_136_tile(pin="8")
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=True))
    assert result.fu == 30
    assert result.han == 1

    tiles = TilesConverter.string_to_136_array(pin="12333345", honors="555", man="567")
    win_tile = _string_to_136_tile(pin="3")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.fu == 40
    assert result.han == 1

    tiles = TilesConverter.string_to_136_array(pin="34567777889", honors="555")
    win_tile = _string_to_136_tile(pin="7")
    melds = [_make_meld(Meld.CHI, pin="345")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.fu == 30
    assert result.han == 3

    tiles = TilesConverter.string_to_136_array(pin="567", sou="3334444555", honors="77")
    win_tile = _string_to_136_tile(sou="3")
    melds = [_make_meld(Meld.KAN, is_open=False, sou="4444")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=_make_hand_config(is_riichi=True))
    assert result.fu == 60
    assert result.han == 1


def test_is_riichi():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_riichi=True))
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_tsumo():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True))
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1

    # with open hand tsumo not giving yaku
    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=True))
    assert result.error is not None


def test_is_ippatsu():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_riichi=True, is_ippatsu=True))
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 2


def test_is_rinshan():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="1234444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    # closed kan: rinshan & tsumo
    melds = [_make_meld(Meld.KAN, is_open=False, sou="4444")]
    result = hand.estimate_hand_value(
        tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=True, is_rinshan=True)
    )
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 2

    # open kan: rinshan only
    melds = [_make_meld(Meld.KAN, sou="4444")]
    result = hand.estimate_hand_value(
        tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=True, is_rinshan=True)
    )
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_chankan():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_chankan=True))
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_haitei():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    # menzen tsumo & haitei
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_haitei=True))
    assert result.error is None
    assert result.han == 2
    assert result.fu == 30
    assert len(result.yaku) == 2

    # haitei only
    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(
        tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=True, is_haitei=True)
    )
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_houtei():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_houtei=True))
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_renhou():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_renhou=True))
    assert result.error is None
    assert result.han == 5
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_daburu_riichi():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_daburu_riichi=True, is_riichi=True))
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_open_riichi():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_riichi=True, is_open_riichi=True))
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_daburu_open_riichi():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(is_daburu_riichi=True, is_riichi=True, is_open_riichi=True)
    )
    assert result.error is None
    assert result.han == 3
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_nagashi_mangan():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="13579", man="234456", pin="66")

    result = hand.estimate_hand_value(tiles, None, config=_make_hand_config(is_nagashi_mangan=True))
    assert result.error is None
    assert result.han == 5
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_chitoitsu_hand():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="113355", man="113355", pin="11")
    assert config.chiitoitsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="2299", man="2299", pin="1199", honors="44")
    assert config.chiitoitsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="113355", man="113355", pin="11")
    win_tile = _string_to_136_tile(pin="1")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 25
    assert len(result.yaku) == 1


def test_is_chitoitsu_hand_and_identical_pairs():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="11335555", man="1133", pin="11")
    win_tile = _string_to_136_tile(pin="1")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error == HandCalculator.ERR_HAND_NOT_WINNING


def test_is_tanyao():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="234567", man="234567", pin="22")
    assert config.tanyao.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="123456", man="234567", pin="22")
    assert not config.tanyao.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="234567", man="234567", honors="22")
    assert not config.tanyao.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="234567", man="234567", pin="22")
    win_tile = _string_to_136_tile(man="7")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_riichi=True))
    assert result.error is None
    assert result.han == 3
    assert result.fu == 30
    assert len(result.yaku) == 3

    tiles = TilesConverter.string_to_136_array(sou="234567", man="234567", pin="22")
    win_tile = _string_to_136_tile(man="7")
    melds = [_make_meld(Meld.CHI, sou="234")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=_make_hand_config(has_open_tanyao=True))
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1

    tiles = TilesConverter.string_to_136_array(sou="234567", man="234567", pin="22")
    win_tile = _string_to_136_tile(man="7")
    melds = [_make_meld(Meld.CHI, sou="234")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=_make_hand_config(has_open_tanyao=False))
    assert result.error is not None


def test_is_pinfu_hand():
    player_wind, round_wind = EAST, WEST
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123456", man="123456", pin="55")
    win_tile = _string_to_136_tile(man="6")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1

    # waiting in two pairs
    tiles = TilesConverter.string_to_136_array(sou="123456", man="123555", pin="55")
    win_tile = _string_to_136_tile(man="5")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is not None

    # contains pon or kan
    tiles = TilesConverter.string_to_136_array(sou="111456", man="123456", pin="55")
    win_tile = _string_to_136_tile(man="6")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is not None

    # penchan waiting
    tiles = TilesConverter.string_to_136_array(sou="123456", man="123456", pin="55")
    win_tile = _string_to_136_tile(sou="3")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is not None

    # kanchan waiting
    tiles = TilesConverter.string_to_136_array(sou="123567", man="123456", pin="55")
    win_tile = _string_to_136_tile(sou="6")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is not None

    # tanki waiting
    tiles = TilesConverter.string_to_136_array(man="22456678", pin="123678")
    win_tile = _string_to_136_tile(man="2")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is not None

    # valued pair
    tiles = TilesConverter.string_to_136_array(sou="123678", man="123456", honors="11")
    win_tile = _string_to_136_tile(sou="6")
    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(player_wind=player_wind, round_wind=round_wind)
    )
    assert result.error is not None

    # not valued pair
    tiles = TilesConverter.string_to_136_array(sou="123678", man="123456", honors="22")
    win_tile = _string_to_136_tile(sou="6")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1

    # open hand
    tiles = TilesConverter.string_to_136_array(sou="12399", man="123456", pin="456")
    win_tile = _string_to_136_tile(man="1")
    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is not None


def test_is_iipeiko():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="112233", man="123", pin="23444")
    assert config.iipeiko.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="112233", man="333", pin="12344")
    win_tile = _string_to_136_tile(man="3")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is not None


def test_is_ryanpeiko():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="112233", man="22", pin="223344")
    assert config.ryanpeiko.is_condition_met(_hand(tiles, 1))

    tiles = TilesConverter.string_to_34_array(sou="111122223333", man="22")
    assert config.ryanpeiko.is_condition_met(_hand(tiles, 1))

    tiles = TilesConverter.string_to_34_array(sou="112233", man="123", pin="23444")
    assert not config.ryanpeiko.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="112233", man="33", pin="223344")
    win_tile = _string_to_136_tile(pin="3")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 3
    assert result.fu == 40
    assert len(result.yaku) == 1

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is not None


def test_is_sanshoku():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="123", man="123", pin="12345677")
    assert config.sanshoku.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="123456", man="23455", pin="123")
    assert not config.sanshoku.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="123456", man="12399", pin="123")
    win_tile = _string_to_136_tile(man="2")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_sanshoku_douko():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="111", man="111", pin="11145677")
    assert config.sanshoku_douko.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="111", man="222", pin="33344455")
    assert not config.sanshoku_douko.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="222", man="222", pin="22245699")
    melds = [_make_meld(Meld.CHI, sou="222")]
    win_tile = _string_to_136_tile(pin="9")

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_sanshoku_douko_and_kan_in_hand():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="2222", man="222", pin="22245699")
    melds = [_make_meld(Meld.KAN, sou="2222")]
    win_tile = _string_to_136_tile(pin="9")

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_toitoi():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="111333", man="333", pin="44555")
    assert config.toitoi.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="777", pin="777888999", honors="44")
    assert config.toitoi.is_condition_met(_hand(tiles, 0))

    tiles = TilesConverter.string_to_136_array(sou="111333", man="333", pin="44555")
    melds = [_make_meld(Meld.PON, sou="111"), _make_meld(Meld.PON, sou="333")]
    win_tile = _string_to_136_tile(pin="5")

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1

    tiles = TilesConverter.string_to_136_array(sou="777", pin="777888999", honors="44")
    melds = [_make_meld(Meld.PON, sou="777")]
    win_tile = _string_to_136_tile(pin="9")

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_sankantsu():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_136_array(sou="11113333", man="123", pin="446666")

    melds = [
        _make_meld(Meld.KAN, sou="1111"),
        _make_meld(Meld.KAN, sou="3333"),
        _make_meld(Meld.KAN, pin="6666"),
    ]
    assert config.sankantsu.is_condition_met(hand, melds)

    melds = [
        _make_meld(Meld.SHOUMINKAN, sou="1111"),
        _make_meld(Meld.KAN, sou="3333"),
        _make_meld(Meld.KAN, pin="6666"),
    ]
    win_tile = _string_to_136_tile(man="3")

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 60
    assert len(result.yaku) == 1


def test_is_honroto():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="111999", man="111", honors="11222")
    assert config.honroto.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(pin="11", honors="22334466", man="1199")
    assert config.honroto.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="111999", man="111", honors="11222")
    win_tile = _string_to_136_tile(honors="2")
    melds = [_make_meld(Meld.PON, sou="111")]

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 4
    assert result.fu == 50
    assert len(result.yaku) == 2

    tiles = TilesConverter.string_to_136_array(pin="11", honors="22334466", man="1199")
    win_tile = _string_to_136_tile(man="1")
    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.fu == 25
    assert result.han == 4


def test_is_sanankou():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="111444", man="333", pin="44555")
    win_tile = _string_to_136_tile(sou="4")

    melds = [_make_meld(Meld.PON, sou="444"), _make_meld(Meld.PON, sou="111")]
    assert not config.sanankou.is_condition_met(_hand(tiles), win_tile, melds, False)

    melds = [_make_meld(Meld.PON, sou="111")]
    assert not config.sanankou.is_condition_met(_hand(tiles), win_tile, melds, False)
    assert config.sanankou.is_condition_met(_hand(tiles), win_tile, melds, True)

    tiles = TilesConverter.string_to_34_array(pin="444789999", honors="22333")
    win_tile = _string_to_136_tile(pin="9")
    assert config.sanankou.is_condition_met(_hand(tiles), win_tile, [], False)

    melds = [_make_meld(Meld.CHI, pin="456")]
    tiles = TilesConverter.string_to_34_array(pin="222456666777", honors="77")
    win_tile = _string_to_136_tile(pin="6")
    assert not config.sanankou.is_condition_met(_hand(tiles), win_tile, melds, False)

    tiles = TilesConverter.string_to_136_array(sou="123444", man="333", pin="44555")
    melds = [_make_meld(Meld.CHI, sou="123")]
    win_tile = _string_to_136_tile(pin="5")

    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=True))
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_shosangen():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="123", man="345", honors="55666777")
    assert config.shosangen.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="123", man="345", honors="55666777")
    win_tile = _string_to_136_tile(honors="7")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 4
    assert result.fu == 50
    assert len(result.yaku) == 3


def test_is_chanta():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="123", man="123789", honors="22333")
    assert config.chantai.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="111", man="111999", honors="22333")
    assert not config.chantai.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="111999", man="111999", pin="11999")
    assert not config.chantai.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="123", man="123789", honors="22333")
    win_tile = _string_to_136_tile(honors="3")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_junchan():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="789", man="123789", pin="12399")
    assert config.junchan.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="111", man="111999", honors="22333")
    assert not config.junchan.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(sou="111999", man="111999", pin="11999")
    assert not config.junchan.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="789", man="123789", pin="12399")
    win_tile = _string_to_136_tile(man="2")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 3
    assert result.fu == 40
    assert len(result.yaku) == 1

    melds = [_make_meld(Meld.CHI, sou="789")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_honitsu():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(man="123456789", honors="11122")
    assert config.honitsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(man="123456789", pin="123", honors="22")
    assert not config.honitsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(man="12345666778899")
    assert not config.honitsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(man="123455667", honors="11122")
    win_tile = _string_to_136_tile(honors="2")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 3
    assert result.fu == 40
    assert len(result.yaku) == 1

    melds = [_make_meld(Meld.CHI, man="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_chinitsu():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(man="12345666778899")
    assert config.chinitsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(man="123456778899", honors="22")
    assert not config.chinitsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(man="11234567677889")
    win_tile = _string_to_136_tile(man="1")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 6
    assert result.fu == 40
    assert len(result.yaku) == 1

    melds = [_make_meld(Meld.CHI, man="678")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 5
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_ittsu():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(man="123456789", sou="123", honors="22")
    assert config.ittsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(man="112233456789", honors="22")
    assert config.ittsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_34_array(man="122334567789", honors="11")
    assert not config.ittsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(man="123456789", sou="123", honors="22")
    win_tile = _string_to_136_tile(sou="3")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 1

    melds = [_make_meld(Meld.CHI, man="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error is None
    assert result.han == 1
    assert result.fu == 30
    assert len(result.yaku) == 1


def test_is_haku():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="234567", man="23422", honors="555")
    assert config.haku.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="234567", man="23422", honors="555")
    win_tile = _string_to_136_tile(honors="5")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_riichi=False))
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_hatsu():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="234567", man="23422", honors="666")
    assert config.hatsu.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="234567", man="23422", honors="666")
    win_tile = _string_to_136_tile(honors="6")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_riichi=False))
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_chun():
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="234567", man="23422", honors="777")
    assert config.chun.is_condition_met(_hand(tiles))

    tiles = TilesConverter.string_to_136_array(sou="234567", man="23422", honors="777")
    win_tile = _string_to_136_tile(honors="7")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_riichi=False))
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1


def test_is_east():
    player_wind, round_wind = EAST, WEST
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="234567", man="23422", honors="111")
    assert config.east.is_condition_met(_hand(tiles), player_wind, round_wind)

    tiles = TilesConverter.string_to_136_array(sou="234567", man="23422", honors="111")
    win_tile = _string_to_136_tile(honors="1")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_riichi=False, player_wind=player_wind, round_wind=round_wind),
    )
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1

    round_wind = EAST
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_riichi=False, player_wind=player_wind, round_wind=round_wind),
    )
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 2


def test_is_south():
    player_wind, round_wind = SOUTH, EAST
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="234567", man="23422", honors="222")
    assert config.south.is_condition_met(_hand(tiles), player_wind, round_wind)

    tiles = TilesConverter.string_to_136_array(sou="234567", man="23422", honors="222")
    win_tile = _string_to_136_tile(honors="2")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_riichi=False, player_wind=player_wind, round_wind=round_wind),
    )
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1

    round_wind = SOUTH
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_riichi=False, player_wind=player_wind, round_wind=round_wind),
    )
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 2


def test_is_west():
    player_wind, round_wind = WEST, EAST
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="234567", man="23422", honors="333")
    assert config.west.is_condition_met(_hand(tiles), player_wind, round_wind)

    tiles = TilesConverter.string_to_136_array(sou="234567", man="23422", honors="333")
    win_tile = _string_to_136_tile(honors="3")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_riichi=False, player_wind=player_wind, round_wind=round_wind),
    )
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1

    round_wind = WEST
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_riichi=False, player_wind=player_wind, round_wind=round_wind),
    )
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 2


def test_is_north():
    player_wind, round_wind = NORTH, EAST
    hand = HandCalculator()
    config = YakuConfig()

    tiles = TilesConverter.string_to_34_array(sou="234567", man="23422", honors="444")
    assert config.north.is_condition_met(_hand(tiles), player_wind, round_wind)

    tiles = TilesConverter.string_to_136_array(sou="234567", man="23422", honors="444")
    win_tile = _string_to_136_tile(honors="4")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_riichi=False, player_wind=player_wind, round_wind=round_wind),
    )
    assert result.error is None
    assert result.han == 1
    assert result.fu == 40
    assert len(result.yaku) == 1

    round_wind = NORTH
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_riichi=False, player_wind=player_wind, round_wind=round_wind),
    )
    assert result.error is None
    assert result.han == 2
    assert result.fu == 40
    assert len(result.yaku) == 2


def test_dora_in_hand():
    hand = HandCalculator()

    # hand without yaku, but with dora should be consider as invalid
    tiles = TilesConverter.string_to_136_array(sou="345678", man="456789", honors="55")
    win_tile = _string_to_136_tile(sou="5")
    dora_indicators = [_string_to_136_tile(sou="5")]
    melds = [_make_meld(Meld.CHI, sou="678")]

    result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators, melds=melds)
    assert result.error is not None

    tiles = TilesConverter.string_to_136_array(sou="123456", man="123456", pin="33")
    win_tile = _string_to_136_tile(man="6")
    dora_indicators = [_string_to_136_tile(pin="2")]

    result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators)
    assert result.error is None
    assert result.han == 3
    assert result.fu == 30
    assert len(result.yaku) == 2

    tiles = TilesConverter.string_to_136_array(man="22456678", pin="123678")
    win_tile = _string_to_136_tile(man="2")
    dora_indicators = [_string_to_136_tile(man="1"), _string_to_136_tile(pin="2")]
    result = hand.estimate_hand_value(
        tiles, win_tile, dora_indicators=dora_indicators, config=_make_hand_config(is_tsumo=True)
    )
    assert result.error is None
    assert result.han == 4
    assert result.fu == 30
    assert len(result.yaku) == 2

    # double dora
    tiles = TilesConverter.string_to_136_array(man="678", pin="34577", sou="123345")
    win_tile = _string_to_136_tile(pin="7")
    dora_indicators = [_string_to_136_tile(sou="4"), _string_to_136_tile(sou="4")]
    result = hand.estimate_hand_value(
        tiles, win_tile, dora_indicators=dora_indicators, config=_make_hand_config(is_tsumo=True)
    )
    assert result.error is None
    assert result.han == 3
    assert result.fu == 30
    assert len(result.yaku) == 2

    # double dora and honor tiles
    tiles = TilesConverter.string_to_136_array(man="678", pin="345", sou="123345", honors="66")
    win_tile = _string_to_136_tile(pin="5")
    dora_indicators = [_string_to_136_tile(honors="5"), _string_to_136_tile(honors="5")]
    result = hand.estimate_hand_value(
        tiles, win_tile, dora_indicators=dora_indicators, config=_make_hand_config(is_riichi=True)
    )
    assert result.error is None
    assert result.han == 5
    assert result.fu == 40
    assert len(result.yaku) == 2

    # double dora indicators and red fives
    tiles = TilesConverter.string_to_136_array(sou="12346", man="123678", pin="44")
    win_tile = _string_to_136_tile(pin="4")
    tiles.append(FIVE_RED_SOU)
    dora_indicators = [_string_to_136_tile(pin="2"), _string_to_136_tile(pin="2")]
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        dora_indicators=dora_indicators,
        config=_make_hand_config(is_tsumo=True, has_aka_dora=True),
    )
    assert result.error is None
    assert result.han == 2
    assert result.fu == 30
    assert len(result.yaku) == 2

    # dora in kan
    tiles = TilesConverter.string_to_136_array(man="7777", pin="34577", sou="123345")
    win_tile = _string_to_136_tile(pin="7")
    melds = [_make_meld(Meld.KAN, is_open=False, man="7777")]

    dora_indicators = [_string_to_136_tile(man="6")]
    result = hand.estimate_hand_value(
        tiles, win_tile, dora_indicators=dora_indicators, melds=melds, config=_make_hand_config(is_tsumo=True)
    )
    assert result.error is None
    assert result.han == 5
    assert result.fu == 40
    assert len(result.yaku) == 2


def test_is_agari_and_closed_kan():
    """
    There were a bug when we don't count closed kan set for agari
    and calculator though that hand was agari (but it doesn't)
    :return:
    """
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="45666777", pin="111", honors="222")
    win_tile = _string_to_136_tile(man="4")
    melds = [
        _make_meld(Meld.PON, pin="111"),
        _make_meld(Meld.KAN, man="6666", is_open=False),
        _make_meld(Meld.PON, man="777"),
    ]

    result = hand.estimate_hand_value(tiles, win_tile, melds)
    # error is correct answer
    assert result.error is not None


def test_kazoe_settings():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="222244466677788")
    win_tile = _string_to_136_tile(man="7")
    melds = [
        _make_meld(Meld.KAN, man="2222", is_open=False),
    ]

    dora_indicators = [
        _string_to_136_tile(man="1"),
        _string_to_136_tile(man="1"),
        _string_to_136_tile(man="1"),
        _string_to_136_tile(man="1"),
    ]

    config = HandConfig(is_riichi=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_LIMITED))
    result = hand.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
    assert result.han == 28
    assert result.cost["main"] == 32000

    config = HandConfig(is_riichi=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_SANBAIMAN))
    result = hand.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
    assert result.han == 28
    assert result.cost["main"] == 24000

    config = HandConfig(is_riichi=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))
    result = hand.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
    assert result.han == 28
    assert result.cost["main"] == 64000


def test_open_hand_without_additional_fu():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="234678", man="234567", pin="22")
    win_tile = _string_to_136_tile(sou="6")
    melds = [_make_meld(Meld.CHI, sou="234")]

    config = HandConfig(options=OptionalRules(has_open_tanyao=True, fu_for_open_pinfu=False))
    result = hand.estimate_hand_value(tiles, win_tile, melds, config=config)
    assert result.han == 1
    assert result.fu == 20
    assert result.cost["main"] == 700


def test_aka_dora():
    hand_calculator = HandCalculator()
    win_tile = TilesConverter.string_to_136_array(man="9")[0]

    hand_config = HandConfig(is_tsumo=True, options=OptionalRules(has_aka_dora=True))

    # three red old style, but not that useful
    tiles = TilesConverter.string_to_136_array(sou="345", pin="456", man="12355599", has_aka_dora=False)
    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
    assert hand_calculation.error is None
    assert hand_calculation.han == 4

    # zero red
    tiles = TilesConverter.string_to_136_array(sou="345", pin="456", man="12355599", has_aka_dora=True)
    win_tile = TilesConverter.string_to_136_array(man="9")[0]

    hand_config = HandConfig(is_tsumo=True, options=OptionalRules(has_aka_dora=True))

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
    assert hand_calculation.error is None
    assert hand_calculation.han == 1

    # one red
    tiles = TilesConverter.string_to_136_array(sou="34r", pin="456", man="12355599", has_aka_dora=True)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
    assert hand_calculation.error is None
    assert hand_calculation.han == 2

    # two red
    tiles = TilesConverter.string_to_136_array(sou="34r", pin="4r6", man="12355599", has_aka_dora=True)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
    assert hand_calculation.error is None
    assert hand_calculation.han == 3

    # three red
    tiles = TilesConverter.string_to_136_array(sou="34r", pin="4r6", man="123r5599", has_aka_dora=True)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
    assert hand_calculation.error is None
    assert hand_calculation.han == 4

    # four red
    tiles = TilesConverter.string_to_136_array(sou="34r", pin="4r6", man="123rr599", has_aka_dora=True)
    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
    assert hand_calculation.error is None
    assert hand_calculation.han == 5

    # five+ red (technically not legal in mahjong but not the fault of evaluator, really)
    tiles = TilesConverter.string_to_136_array(sou="34r", pin="4r6", man="123rrr99", has_aka_dora=True)

    hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
    assert hand_calculation.error is None
    assert hand_calculation.han == 6
