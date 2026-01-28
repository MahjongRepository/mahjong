import pytest

from mahjong.constants import FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU, HAKU
from mahjong.tile import TilesConverter
from mahjong.utils import (
    classify_hand_suits,
    find_isolated_tile_indices,
    has_pon_or_kan_of,
    is_aka_dora,
    is_dora_indicator_for_terminal,
    is_tile_strictly_isolated,
    simplify,
)
from tests.utils_for_tests import _string_to_34_tile, _string_to_34_tiles


@pytest.mark.parametrize(
    ("tile_136", "expected"),
    [
        (FIVE_RED_MAN, True),
        (FIVE_RED_PIN, True),
        (FIVE_RED_SOU, True),
        (FIVE_RED_MAN + 1, False),
        (FIVE_RED_PIN + 1, False),
        (FIVE_RED_SOU + 1, False),
        (HAKU, False),
    ],
)
def test_is_aka_dora_with_aka_enabled(tile_136: int, expected: bool) -> None:
    assert is_aka_dora(tile_136, aka_enabled=True) == expected


@pytest.mark.parametrize(
    "tile_136",
    [
        FIVE_RED_MAN,
        FIVE_RED_PIN,
        FIVE_RED_SOU,
    ],
)
def test_is_aka_dora_with_aka_disabled(tile_136: int) -> None:
    assert is_aka_dora(tile_136, aka_enabled=False) is False


@pytest.mark.parametrize(
    ("hand", "tile", "expected"),
    [
        ([_string_to_34_tiles(man="111")], _string_to_34_tile(man="1"), True),  # pon
        ([_string_to_34_tiles(man="1111")], _string_to_34_tile(man="1"), True),  # kan
        ([_string_to_34_tiles(man="123")], _string_to_34_tile(man="1"), False),  # chi
        ([_string_to_34_tiles(man="11")], _string_to_34_tile(man="1"), False),  # pair
    ],
)
def test_has_pon_or_kan_of(hand: list[list[int]], tile: int, expected: bool) -> None:
    assert has_pon_or_kan_of(hand, tile) == expected


@pytest.mark.parametrize(
    ("hand", "expected"),
    [
        ([_string_to_34_tiles(man="111")], (4, 0)),  # pon of man
        ([_string_to_34_tiles(pin="111")], (2, 0)),  # pon of pin
        ([_string_to_34_tiles(sou="111")], (1, 0)),  # pon of sou
        ([_string_to_34_tiles(honors="111")], (0, 1)),  # pon of east
        ([_string_to_34_tiles(man="123"), _string_to_34_tiles(pin="123")], (6, 0)),  # chi of man + chi of pin
        (
            [_string_to_34_tiles(sou="123"), _string_to_34_tiles(honors="111"), _string_to_34_tiles(honors="55")],
            (1, 2),
        ),  # sou chi + 2 honor groups
    ],
)
def test_classify_hand_suits(hand: list[list[int]], expected: tuple[int, int]) -> None:
    assert classify_hand_suits(hand) == expected


def test_find_isolated_tiles() -> None:
    hand_34 = TilesConverter.string_to_34_array(sou="1369", pin="15678", man="25", honors="124")
    isolated_tiles = find_isolated_tile_indices(hand_34)

    assert (_string_to_34_tile(sou="1") in isolated_tiles) is False
    assert (_string_to_34_tile(sou="2") in isolated_tiles) is False
    assert (_string_to_34_tile(sou="3") in isolated_tiles) is False
    assert (_string_to_34_tile(sou="4") in isolated_tiles) is False
    assert (_string_to_34_tile(sou="5") in isolated_tiles) is False
    assert (_string_to_34_tile(sou="6") in isolated_tiles) is False
    assert (_string_to_34_tile(sou="7") in isolated_tiles) is False
    assert (_string_to_34_tile(sou="8") in isolated_tiles) is False
    assert (_string_to_34_tile(sou="9") in isolated_tiles) is False
    assert (_string_to_34_tile(pin="1") in isolated_tiles) is False
    assert (_string_to_34_tile(pin="2") in isolated_tiles) is False
    assert (_string_to_34_tile(pin="3") in isolated_tiles) is True
    assert (_string_to_34_tile(pin="4") in isolated_tiles) is False
    assert (_string_to_34_tile(pin="5") in isolated_tiles) is False
    assert (_string_to_34_tile(pin="6") in isolated_tiles) is False
    assert (_string_to_34_tile(pin="7") in isolated_tiles) is False
    assert (_string_to_34_tile(pin="8") in isolated_tiles) is False
    assert (_string_to_34_tile(pin="9") in isolated_tiles) is False
    assert (_string_to_34_tile(man="1") in isolated_tiles) is False
    assert (_string_to_34_tile(man="2") in isolated_tiles) is False
    assert (_string_to_34_tile(man="3") in isolated_tiles) is False
    assert (_string_to_34_tile(man="4") in isolated_tiles) is False
    assert (_string_to_34_tile(man="5") in isolated_tiles) is False
    assert (_string_to_34_tile(man="6") in isolated_tiles) is False
    assert (_string_to_34_tile(man="7") in isolated_tiles) is True
    assert (_string_to_34_tile(man="8") in isolated_tiles) is True
    assert (_string_to_34_tile(man="9") in isolated_tiles) is True
    assert (_string_to_34_tile(honors="1") in isolated_tiles) is False
    assert (_string_to_34_tile(honors="2") in isolated_tiles) is False
    assert (_string_to_34_tile(honors="3") in isolated_tiles) is True
    assert (_string_to_34_tile(honors="4") in isolated_tiles) is False
    assert (_string_to_34_tile(honors="5") in isolated_tiles) is True
    assert (_string_to_34_tile(honors="6") in isolated_tiles) is True
    assert (_string_to_34_tile(honors="7") in isolated_tiles) is True


def test_is_strictly_isolated_tile() -> None:
    hand_34 = TilesConverter.string_to_34_array(sou="1399", pin="1567", man="25", honors="1224")

    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(sou="1")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(sou="2")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(sou="3")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(sou="4")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(sou="5")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(sou="6")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(sou="7")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(sou="8")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(sou="9")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(pin="1")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(pin="2")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(pin="3")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(pin="4")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(pin="5")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(pin="6")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(pin="7")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(pin="8")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(pin="9")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(man="1")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(man="2")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(man="3")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(man="4")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(man="5")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(man="6")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(man="7")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(man="8")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(man="9")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(honors="1")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(honors="2")) is False
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(honors="3")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(honors="4")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(honors="5")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(honors="6")) is True
    assert is_tile_strictly_isolated(hand_34, _string_to_34_tile(honors="7")) is True


def test_is_dora_indicator_for_terminal() -> None:
    assert not is_dora_indicator_for_terminal(_string_to_34_tile(man="1"))
    assert not is_dora_indicator_for_terminal(_string_to_34_tile(man="7"))
    assert is_dora_indicator_for_terminal(_string_to_34_tile(man="8"))
    assert is_dora_indicator_for_terminal(_string_to_34_tile(man="9"))
    assert not is_dora_indicator_for_terminal(_string_to_34_tile(pin="1"))
    assert not is_dora_indicator_for_terminal(_string_to_34_tile(pin="7"))
    assert is_dora_indicator_for_terminal(_string_to_34_tile(pin="8"))
    assert is_dora_indicator_for_terminal(_string_to_34_tile(pin="9"))
    assert not is_dora_indicator_for_terminal(_string_to_34_tile(sou="1"))
    assert not is_dora_indicator_for_terminal(_string_to_34_tile(sou="7"))
    assert is_dora_indicator_for_terminal(_string_to_34_tile(sou="8"))
    assert is_dora_indicator_for_terminal(_string_to_34_tile(sou="9"))
    assert not is_dora_indicator_for_terminal(_string_to_34_tile(honors="1"))
    assert not is_dora_indicator_for_terminal(_string_to_34_tile(honors="7"))


def test_simplify() -> None:
    assert simplify(_string_to_34_tile(sou="1")) == 0
    assert simplify(_string_to_34_tile(sou="2")) == 1
    assert simplify(_string_to_34_tile(sou="3")) == 2
    assert simplify(_string_to_34_tile(sou="4")) == 3
    assert simplify(_string_to_34_tile(sou="5")) == 4
    assert simplify(_string_to_34_tile(sou="6")) == 5
    assert simplify(_string_to_34_tile(sou="7")) == 6
    assert simplify(_string_to_34_tile(sou="8")) == 7
    assert simplify(_string_to_34_tile(sou="9")) == 8
    assert simplify(_string_to_34_tile(pin="1")) == 0
    assert simplify(_string_to_34_tile(pin="2")) == 1
    assert simplify(_string_to_34_tile(pin="3")) == 2
    assert simplify(_string_to_34_tile(pin="4")) == 3
    assert simplify(_string_to_34_tile(pin="5")) == 4
    assert simplify(_string_to_34_tile(pin="6")) == 5
    assert simplify(_string_to_34_tile(pin="7")) == 6
    assert simplify(_string_to_34_tile(pin="8")) == 7
    assert simplify(_string_to_34_tile(pin="9")) == 8
    assert simplify(_string_to_34_tile(man="1")) == 0
    assert simplify(_string_to_34_tile(man="2")) == 1
    assert simplify(_string_to_34_tile(man="3")) == 2
    assert simplify(_string_to_34_tile(man="4")) == 3
    assert simplify(_string_to_34_tile(man="5")) == 4
    assert simplify(_string_to_34_tile(man="6")) == 5
    assert simplify(_string_to_34_tile(man="7")) == 6
    assert simplify(_string_to_34_tile(man="8")) == 7
    assert simplify(_string_to_34_tile(man="9")) == 8
    assert simplify(_string_to_34_tile(honors="1")) == 0
    assert simplify(_string_to_34_tile(honors="2")) == 1
    assert simplify(_string_to_34_tile(honors="3")) == 2
    assert simplify(_string_to_34_tile(honors="4")) == 3
    assert simplify(_string_to_34_tile(honors="5")) == 4
    assert simplify(_string_to_34_tile(honors="6")) == 5
    assert simplify(_string_to_34_tile(honors="7")) == 6
