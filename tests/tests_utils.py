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


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "expected"),
    [
        ("1", "", "", "", False),
        ("2", "", "", "", False),
        ("3", "", "", "", False),
        ("4", "", "", "", False),
        ("5", "", "", "", False),
        ("6", "", "", "", False),
        ("7", "", "", "", False),
        ("8", "", "", "", False),
        ("9", "", "", "", False),
        ("", "1", "", "", False),
        ("", "2", "", "", False),
        ("", "3", "", "", True),
        ("", "4", "", "", False),
        ("", "5", "", "", False),
        ("", "6", "", "", False),
        ("", "7", "", "", False),
        ("", "8", "", "", False),
        ("", "9", "", "", False),
        ("", "", "1", "", False),
        ("", "", "2", "", False),
        ("", "", "3", "", False),
        ("", "", "4", "", False),
        ("", "", "5", "", False),
        ("", "", "6", "", False),
        ("", "", "7", "", True),
        ("", "", "8", "", True),
        ("", "", "9", "", True),
        ("", "", "", "1", False),
        ("", "", "", "2", False),
        ("", "", "", "3", True),
        ("", "", "", "4", False),
        ("", "", "", "5", True),
        ("", "", "", "6", True),
        ("", "", "", "7", True),
    ],
)
def test_find_isolated_tiles(sou: str, pin: str, man: str, honors: str, expected: bool) -> None:
    hand_34 = TilesConverter.string_to_34_array(sou="1369", pin="15678", man="25", honors="124")
    isolated_tiles = find_isolated_tile_indices(hand_34)

    tile_34 = _string_to_34_tile(sou=sou, pin=pin, man=man, honors=honors)
    assert (tile_34 in isolated_tiles) == expected


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "expected"),
    [
        ("1", "", "", "", False),
        ("2", "", "", "", False),
        ("3", "", "", "", False),
        ("4", "", "", "", False),
        ("5", "", "", "", False),
        ("6", "", "", "", True),
        ("7", "", "", "", False),
        ("8", "", "", "", False),
        ("9", "", "", "", False),
        ("", "1", "", "", True),
        ("", "2", "", "", False),
        ("", "3", "", "", False),
        ("", "4", "", "", False),
        ("", "5", "", "", False),
        ("", "6", "", "", False),
        ("", "7", "", "", False),
        ("", "8", "", "", False),
        ("", "9", "", "", False),
        ("", "", "1", "", False),
        ("", "", "2", "", True),
        ("", "", "3", "", False),
        ("", "", "4", "", False),
        ("", "", "5", "", True),
        ("", "", "6", "", False),
        ("", "", "7", "", False),
        ("", "", "8", "", True),
        ("", "", "9", "", True),
        ("", "", "", "1", True),
        ("", "", "", "2", False),
        ("", "", "", "3", True),
        ("", "", "", "4", True),
        ("", "", "", "5", True),
        ("", "", "", "6", True),
        ("", "", "", "7", True),
    ],
)
def test_is_strictly_isolated_tile(sou: str, pin: str, man: str, honors: str, expected: bool) -> None:
    hand_34 = TilesConverter.string_to_34_array(sou="1399", pin="1567", man="25", honors="1224")
    tile_34 = _string_to_34_tile(sou=sou, pin=pin, man=man, honors=honors)
    assert is_tile_strictly_isolated(hand_34, tile_34) == expected


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "expected"),
    [
        ("1", "", "", "", False),
        ("2", "", "", "", False),
        ("3", "", "", "", False),
        ("4", "", "", "", False),
        ("5", "", "", "", False),
        ("6", "", "", "", False),
        ("7", "", "", "", False),
        ("8", "", "", "", True),
        ("9", "", "", "", True),
        ("", "1", "", "", False),
        ("", "2", "", "", False),
        ("", "3", "", "", False),
        ("", "4", "", "", False),
        ("", "5", "", "", False),
        ("", "6", "", "", False),
        ("", "7", "", "", False),
        ("", "8", "", "", True),
        ("", "9", "", "", True),
        ("", "", "1", "", False),
        ("", "", "2", "", False),
        ("", "", "3", "", False),
        ("", "", "4", "", False),
        ("", "", "5", "", False),
        ("", "", "6", "", False),
        ("", "", "7", "", False),
        ("", "", "8", "", True),
        ("", "", "9", "", True),
        ("", "", "", "1", False),
        ("", "", "", "2", False),
        ("", "", "", "3", False),
        ("", "", "", "4", False),
        ("", "", "", "5", False),
        ("", "", "", "6", False),
        ("", "", "", "7", False),
    ],
)
def test_is_dora_indicator_for_terminal(sou: str, pin: str, man: str, honors: str, expected: bool) -> None:
    tile_34 = _string_to_34_tile(sou=sou, pin=pin, man=man, honors=honors)
    assert is_dora_indicator_for_terminal(tile_34) == expected


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "simplified"),
    [
        ("1", "", "", "", 0),
        ("2", "", "", "", 1),
        ("3", "", "", "", 2),
        ("4", "", "", "", 3),
        ("5", "", "", "", 4),
        ("6", "", "", "", 5),
        ("7", "", "", "", 6),
        ("8", "", "", "", 7),
        ("9", "", "", "", 8),
        ("", "1", "", "", 0),
        ("", "2", "", "", 1),
        ("", "3", "", "", 2),
        ("", "4", "", "", 3),
        ("", "5", "", "", 4),
        ("", "6", "", "", 5),
        ("", "7", "", "", 6),
        ("", "8", "", "", 7),
        ("", "9", "", "", 8),
        ("", "", "1", "", 0),
        ("", "", "2", "", 1),
        ("", "", "3", "", 2),
        ("", "", "4", "", 3),
        ("", "", "5", "", 4),
        ("", "", "6", "", 5),
        ("", "", "7", "", 6),
        ("", "", "8", "", 7),
        ("", "", "9", "", 8),
        ("", "", "", "1", 0),
        ("", "", "", "2", 1),
        ("", "", "", "3", 2),
        ("", "", "", "4", 3),
        ("", "", "", "5", 4),
        ("", "", "", "6", 5),
        ("", "", "", "7", 6),
    ],
)
def test_simplify(sou: str, pin: str, man: str, honors: str, simplified: int) -> None:
    tile_34 = _string_to_34_tile(sou=sou, pin=pin, man=man, honors=honors)
    assert simplify(tile_34) == simplified
