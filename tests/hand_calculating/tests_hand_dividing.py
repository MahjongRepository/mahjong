from tile import TilesConverter
from utils_for_tests import _make_meld, _string_to_136_tile

from mahjong.hand_calculating.divider import HandDivider
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.meld import Meld


def _string(hand):
    results = []
    for set_item in hand:
        results.append(TilesConverter.to_one_line_string([x * 4 for x in set_item]))
    return results


def test_simple_hand_dividing():
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="234567", sou="23455", honors="777")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 1
    assert _string(result[0]) == ["234m", "567m", "234s", "55s", "777z"]


def test_second_simple_hand_dividing():
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="123", pin="123", sou="123", honors="11222")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 1
    assert _string(result[0]) == ["123m", "123p", "123s", "11z", "222z"]


def test_hand_with_pairs_dividing():
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="23444", pin="344556", sou="333")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 1
    assert _string(result[0]) == ["234m", "44m", "345p", "456p", "333s"]


def test_one_suit_hand_dividing():
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="11122233388899")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 2
    assert _string(result[0]) == ["111m", "222m", "333m", "888m", "99m"]
    assert _string(result[1]) == ["123m", "123m", "123m", "888m", "99m"]


def test_second_one_suit_hand_dividing():
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(sou="111123666789", honors="11")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 1
    assert _string(result[0]) == ["111s", "123s", "666s", "789s", "11z"]


def test_third_one_suit_hand_dividing():
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(pin="234777888999", honors="22")
    melds = [
        _make_meld(Meld.CHI, pin="789"),
        _make_meld(Meld.CHI, pin="234"),
    ]
    result = hand.divide_hand(tiles_34, melds)
    assert len(result) == 1
    assert _string(result[0]) == ["234p", "789p", "789p", "789p", "22z"]


def test_chitoitsu_like_hand_dividing():
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="112233", pin="99", sou="445566")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 2
    assert _string(result[0]) == ["11m", "22m", "33m", "99p", "44s", "55s", "66s"]
    assert _string(result[1]) == ["123m", "123m", "99p", "456s", "456s"]


def test_fix_not_correct_kan_handling():
    # Hand calculator crashed because it wasn't able to split hand

    hand = HandCalculator()

    tiles = TilesConverter.string_to_136_array(man="55666777", pin="111", honors="222")
    win_tile = _string_to_136_tile(man="5")
    melds = [
        _make_meld(Meld.KAN, man="6666", is_open=False),
        _make_meld(Meld.PON, pin="111"),
        _make_meld(Meld.PON, man="777"),
    ]

    hand.estimate_hand_value(tiles, win_tile, melds=melds)
