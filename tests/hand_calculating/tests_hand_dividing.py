import pytest

from mahjong.hand_calculating.divider import HandDivider, _Block, _BlockType
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.meld import Meld
from mahjong.tile import TilesConverter
from tests.utils_for_tests import _make_meld, _string_to_34_tile, _string_to_136_tile


def _string(hand: list[list[int]]) -> list[str]:
    return [TilesConverter.to_one_line_string([x * 4 for x in set_item]) for set_item in hand]


def test_simple_hand_dividing() -> None:
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="234567", sou="23455", honors="777")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 1
    assert _string(result[0]) == ["234m", "567m", "234s", "55s", "777z"]


def test_second_simple_hand_dividing() -> None:
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="123", pin="123", sou="123", honors="11222")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 1
    assert _string(result[0]) == ["123m", "123p", "123s", "11z", "222z"]


def test_hand_with_pairs_dividing() -> None:
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="23444", pin="344556", sou="333")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 1
    assert _string(result[0]) == ["234m", "44m", "345p", "456p", "333s"]


def test_one_suit_hand_dividing() -> None:
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="11122233388899")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 2
    assert _string(result[0]) == ["111m", "222m", "333m", "888m", "99m"]
    assert _string(result[1]) == ["123m", "123m", "123m", "888m", "99m"]


def test_second_one_suit_hand_dividing() -> None:
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(sou="111123666789", honors="11")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 1
    assert _string(result[0]) == ["111s", "123s", "666s", "789s", "11z"]


def test_third_one_suit_hand_dividing() -> None:
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(pin="234777888999", honors="22")
    melds = [
        _make_meld(Meld.CHI, pin="789"),
        _make_meld(Meld.CHI, pin="234"),
    ]
    result = hand.divide_hand(tiles_34, melds)
    assert len(result) == 1
    assert _string(result[0]) == ["234p", "789p", "789p", "789p", "22z"]


def test_chitoitsu_like_hand_dividing() -> None:
    hand = HandDivider()

    tiles_34 = TilesConverter.string_to_34_array(man="112233", pin="99", sou="445566")
    result = hand.divide_hand(tiles_34)
    assert len(result) == 2
    assert _string(result[0]) == ["11m", "22m", "33m", "99p", "44s", "55s", "66s"]
    assert _string(result[1]) == ["123m", "123m", "99p", "456s", "456s"]


def test_fix_not_correct_kan_handling() -> None:
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


@pytest.mark.parametrize(
    "other",
    [42, "string", 3.14, None],
    ids=["int", "str", "float", "None"],
)
def test_block_eq_with_non_block_returns_not_implemented(other: object) -> None:
    block = _Block(tile_34=_string_to_34_tile(man="1"), ty=_BlockType.TRIPLET)
    assert block.__eq__(other) is NotImplemented


@pytest.mark.parametrize(
    "other",
    [42, "string", 3.14, None],
    ids=["int", "str", "float", "None"],
)
def test_block_lt_with_non_block_returns_not_implemented(other: object) -> None:
    block = _Block(tile_34=_string_to_34_tile(man="1"), ty=_BlockType.TRIPLET)
    assert block.__lt__(other) is NotImplemented


def test_block_from_meld_with_invalid_meld_type_raises_runtime_error() -> None:
    # nuki meld has a single tile, which fails is_chi (len != 3),
    # is_pon (len != 3), and is_kan (len != 4)
    meld = Meld(meld_type=Meld.NUKI, tiles=TilesConverter.string_to_136_array(man="1"))
    with pytest.raises(RuntimeError, match="invalid meld type"):
        _Block.from_meld(meld)


def test_divide_hand_skips_combinations_with_wrong_block_count() -> None:
    # 5 melds + 1 pair = 6 blocks, which != 5
    tiles_34 = TilesConverter.string_to_34_array(man="123789", pin="123789", sou="111", honors="11")
    result = HandDivider.divide_hand(tiles_34)
    assert result == []


def test_decompose_honors_hand_rejects_invalid_tile_count() -> None:
    # honor tile with count 5 is invalid and must be rejected.
    # without the guard, the invalid count is silently skipped,
    # allowing other honors to form blocks that pass validation.
    tiles_34 = TilesConverter.string_to_34_array(man="111", pin="111", sou="111", honors="22233")
    tiles_34[_string_to_34_tile(honors="1")] = 5
    result = HandDivider.divide_hand(tiles_34)
    assert result == []


def test_decompose_chiitoitsu_rejects_hand_with_melds() -> None:
    tiles_34 = TilesConverter.string_to_34_array(man="2288", pin="2288", sou="22", honors="2244")
    melds = [Meld(meld_type=Meld.PON, tiles=TilesConverter.string_to_136_array(man="111"))]
    result = HandDivider.divide_hand(tiles_34, melds)
    assert result == []


def test_decompose_chiitoitsu_rejects_hand_with_too_many_tiles() -> None:
    tiles_34 = TilesConverter.string_to_34_array(man="2288", pin="2288", sou="228", honors="2244")
    result = HandDivider.divide_hand(tiles_34)
    assert result == []


def test_decompose_chiitoitsu_rejects_hand_with_too_many_pairs() -> None:
    tiles_34 = TilesConverter.string_to_34_array(man="2288", pin="2288", sou="2288", honors="2244")
    result = HandDivider.divide_hand(tiles_34)
    assert result == []
