import pytest

from mahjong.tile import TilesConverter
from mahjong.utils import (
    find_isolated_tile_indices,
    is_dora_indicator_for_terminal,
    is_tile_strictly_isolated,
    simplify,
)
from tests.utils_for_tests import _string_to_34_tile


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
