import pytest

from mahjong.constants import EAST, SOUTH
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_response import HandResponse
from mahjong.meld import Meld
from mahjong.tile import TilesConverter
from tests.utils_for_tests import _make_hand_config, _make_meld, _string_to_136_tile


def test_no_winning_tile() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="9")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_riichi=True))
    assert result.error == HandCalculator.ERR_NO_WINNING_TILE


def test_open_hand_riichi() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=_make_hand_config(is_riichi=True))
    assert result.error == HandCalculator.ERR_OPEN_HAND_RIICHI


def test_open_hand_daburi() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        config=_make_hand_config(is_riichi=True, is_daburu_riichi=True),
    )
    assert result.error == HandCalculator.ERR_OPEN_HAND_DABURI


def test_ippatsu_without_riichi() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_ippatsu=True))
    assert result.error == HandCalculator.ERR_IPPATSU_WITHOUT_RIICHI


def test_hand_not_winning() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123344", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile)
    assert result.error == HandCalculator.ERR_HAND_NOT_WINNING


def test_no_yaku() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    melds = [_make_meld(Meld.CHI, sou="123")]
    result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
    assert result.error == HandCalculator.ERR_NO_YAKU


def test_no_yaku_hand_does_not_count_dora() -> None:
    hand = HandCalculator()

    # hand with no yaku but with dora and aka dora
    tiles = TilesConverter.one_line_string_to_136_array("123m234p340678s22z", has_aka_dora=True)
    win_tile = TilesConverter.string_to_136_array(man="2")[0]
    dora_indicators = TilesConverter.string_to_136_array(man="1")
    config = _make_hand_config(has_aka_dora=True)

    result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators, config=config)

    assert result.error == HandCalculator.ERR_NO_YAKU
    assert result.han is None
    assert result.fu is None
    assert result.yaku is None
    assert result.cost is None


def test_chankan_with_tsumo() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_chankan=True))
    assert result.error == HandCalculator.ERR_CHANKAN_WITH_TSUMO


def test_rinshan_without_tsumo() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_rinshan=True))
    assert result.error == HandCalculator.ERR_RINSHAN_WITHOUT_TSUMO


def test_haitei_without_tsumo() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_haitei=True))
    assert result.error == HandCalculator.ERR_HAITEI_WITHOUT_TSUMO


def test_houtei_with_tsumo() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_houtei=True))
    assert result.error == HandCalculator.ERR_HOUTEI_WITH_TSUMO


def test_haitei_with_rinshan() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=True, is_rinshan=True, is_haitei=True),
    )
    assert result.error == HandCalculator.ERR_HAITEI_WITH_RINSHAN


def test_houtei_with_chankan() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_chankan=True, is_houtei=True),
    )
    assert result.error == HandCalculator.ERR_HOUTEI_WITH_CHANKAN


def test_tenhou_not_as_dealer() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    # no error when player wind is *not* specified
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_tenhou=True))
    assert result.error is None

    # raise error when player wind is specified and *not* EAST
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=True, is_tenhou=True, player_wind=SOUTH),
    )
    assert result.error == HandCalculator.ERR_TENHOU_NOT_AS_DEALER


def test_tenhou_without_tsumo() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_tenhou=True))
    assert result.error == HandCalculator.ERR_TENHOU_WITHOUT_TSUMO


def test_tenhou_with_meld() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="1234444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    melds = [_make_meld(Meld.KAN, is_open=False, sou="4444")]
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        config=_make_hand_config(is_tsumo=True, is_rinshan=True, is_tenhou=True),
    )
    assert result.error == HandCalculator.ERR_TENHOU_WITH_MELD


def test_chiihou_as_dealer() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    # no error when player wind is *not* specified
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_chiihou=True))
    assert result.error is None

    # raise error when player wind is specified EAST
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=True, is_chiihou=True, player_wind=EAST),
    )
    assert result.error == HandCalculator.ERR_CHIIHOU_AS_DEALER


def test_chiihou_without_tsumo() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_chiihou=True))
    assert result.error == HandCalculator.ERR_CHIIHOU_WITHOUT_TSUMO


def test_chiihou_with_meld() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="1234444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    melds = [_make_meld(Meld.KAN, is_open=False, sou="4444")]
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        config=_make_hand_config(is_tsumo=True, is_rinshan=True, is_chiihou=True),
    )
    assert result.error == HandCalculator.ERR_CHIIHOU_WITH_MELD


def test_renhou_as_dealer() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    # no error when player wind is *not* specified
    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=False, is_renhou=True))
    assert result.error is None

    # raise error when player wind is specified EAST
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        config=_make_hand_config(is_tsumo=False, is_renhou=True, player_wind=EAST),
    )
    assert result.error == HandCalculator.ERR_RENHOU_AS_DEALER


def test_renhou_with_tsumo() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_tsumo=True, is_renhou=True))
    assert result.error == HandCalculator.ERR_RENHOU_WITH_TSUMO


def test_renhou_with_meld() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="1234444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="1")

    melds = [_make_meld(Meld.KAN, is_open=False, sou="4444")]
    result = hand.estimate_hand_value(
        tiles,
        win_tile,
        melds=melds,
        config=_make_hand_config(is_tsumo=False, is_renhou=True),
    )
    assert result.error == HandCalculator.ERR_RENHOU_WITH_MELD


def test_win_tile_only_in_opened_meld() -> None:
    """
    Verify that a hand where the win tile exists only in an opened meld
    returns hand_not_correct instead of crashing.
    """
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="111234", pin="456", sou="789", honors="11")
    win_tile = tiles[0]

    meld = Meld(meld_type=Meld.PON, tiles=tiles[0:3], opened=True, called_tile=tiles[0], who=0)
    result = hand.estimate_hand_value(tiles, win_tile, melds=[meld])
    assert result.error == HandCalculator.ERR_HAND_NOT_WINNING


@pytest.mark.parametrize(
    "error_string",
    [
        HandCalculator.ERR_HAND_NOT_WINNING,
        HandCalculator.ERR_NO_YAKU,
        HandCalculator.ERR_NO_WINNING_TILE,
    ],
)
def test_str_returns_error_when_error_is_set(error_string: str) -> None:
    result = HandResponse(error=error_string)
    assert str(result) == error_string


def test_str_returns_han_and_fu_for_valid_hand() -> None:
    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="123444", man="234456", pin="66")
    win_tile = _string_to_136_tile(sou="4")

    result = hand.estimate_hand_value(tiles, win_tile, config=_make_hand_config(is_riichi=True))
    assert result.error is None
    assert str(result) == f"{result.han} han, {result.fu} fu"
