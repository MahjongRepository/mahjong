from tile import TilesConverter
from utils_for_tests import _make_hand_config, _make_meld, _string_to_136_tile

from mahjong.constants import EAST, SOUTH
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.meld import Meld


def test_no_winning_tile():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="9")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_riichi=True))
    assert result.error == "winning_tile_not_in_hand"


def test_open_hand_riichi():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=_make_hand_config(is_riichi=True))
    assert result.error == "open_hand_riichi_not_allowed"


def test_open_hand_daburi():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(
        tiles, win_tile, melds=melds, config=_make_hand_config(is_riichi=True, is_daburu_riichi=True)
    )
    assert result.error == "open_hand_daburi_not_allowed"


def test_ippatsu_without_riichi():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_ippatsu=True))
    assert result.error == "ippatsu_without_riichi_not_allowed"


def test_hand_not_winning():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123344", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error == "hand_not_winning"


def test_no_yaku():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error == "no_yaku"


def test_chankan_with_tsumo():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_chankan=True))
    assert result.error == "chankan_with_tsumo_not_allowed"


def test_rinshan_without_tsumo():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_rinshan=True))
    assert result.error == "rinshan_without_tsumo_not_allowed"


def test_haitei_without_tsumo():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_haitei=True))
    assert result.error == "haitei_without_tsumo_not_allowed"


def test_houtei_with_tsumo():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_houtei=True))
    assert result.error == "houtei_with_tsumo_not_allowed"


def test_haitei_with_rinshan():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_rinshan=True, is_haitei=True)
    )
    assert result.error == "haitei_with_rinshan_not_allowed"


def test_houtei_with_chankan():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_chankan=True, is_houtei=True)
    )
    assert result.error == "houtei_with_chankan_not_allowed"


def test_tenhou_not_as_dealer():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    # no error when player wind is *not* specified
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_tenhou=True))
    assert result.error is None

    # raise error when player wind is specified and *not* EAST
    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_tenhou=True, player_wind=SOUTH)
    )
    assert result.error == "tenhou_not_as_dealer_not_allowed"


def test_tenhou_without_tsumo():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_tenhou=True))
    assert result.error == "tenhou_without_tsumo_not_allowed"


def test_tenhou_with_meld():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="1234444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    melds = [_make_meld(Meld.KAN, is_open=False, sou="4444")]
    result = hand.estimate_hand_value(
        tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=True, is_rinshan=True, is_tenhou=True)
    )
    assert result.error == "tenhou_with_meld_not_allowed"


def test_chiihou_as_dealer():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    # no error when player wind is *not* specified
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_chiihou=True))
    assert result.error is None

    # raise error when player wind is specified EAST
    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_chiihou=True, player_wind=EAST)
    )
    assert result.error == "chiihou_as_dealer_not_allowed"


def test_chiihou_without_tsumo():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_chiihou=True))
    assert result.error == "chiihou_without_tsumo_not_allowed"


def test_chiihou_with_meld():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="1234444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    melds = [_make_meld(Meld.KAN, is_open=False, sou="4444")]
    result = hand.estimate_hand_value(
        tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=True, is_rinshan=True, is_chiihou=True)
    )
    assert result.error == "chiihou_with_meld_not_allowed"


def test_renhou_as_dealer():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    # no error when player wind is *not* specified
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_renhou=True))
    assert result.error is None

    # raise error when player wind is specified EAST
    result = hand.estimate_hand_value(
        tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_renhou=True, player_wind=EAST)
    )
    assert result.error == "renhou_as_dealer_not_allowed"


def test_renhou_with_tsumo():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_renhou=True))
    assert result.error == "renhou_with_tsumo_not_allowed"


def test_renhou_with_meld():
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="1234444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    melds = [_make_meld(Meld.KAN, is_open=False, sou="4444")]
    result = hand.estimate_hand_value(
        tiles, win_tile, melds=melds, config=_make_hand_config(is_tsumo=False, is_renhou=True)
    )
    assert result.error == "renhou_with_meld_not_allowed"
