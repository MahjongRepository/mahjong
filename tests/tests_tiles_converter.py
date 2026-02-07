import pytest

from mahjong.constants import FIVE_RED_PIN
from mahjong.tile import Tile, TilesConverter
from tests.utils_for_tests import _string_to_34_tile, _string_to_136_tile


def test_convert_to_one_line_string() -> None:
    tiles = TilesConverter.string_to_136_array(man="1199", pin="1199", sou="1199", honors="1177")
    result = TilesConverter.to_one_line_string(tiles)
    assert result == "1199m1199p1199s1177z"


@pytest.mark.parametrize(
    ("print_aka_dora", "expected"),
    [
        (False, "1244579m3p57z"),
        (True, "1244079m3p57z"),
    ],
)
def test_convert_to_one_line_string_with_aka_dora(print_aka_dora: bool, expected: str) -> None:
    tiles = TilesConverter.string_to_136_array(man="1244079", pin="3", honors="57", has_aka_dora=True)
    result = TilesConverter.to_one_line_string(tiles, print_aka_dora=print_aka_dora)
    assert result == expected


def test_convert_to_34_array() -> None:
    tiles = TilesConverter.string_to_136_array(man="199", pin="1199", sou="1199", honors="117")
    result = TilesConverter.to_34_array(tiles)
    assert result == [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2,  # man: 1m=1, 9m=2
        2,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2,  # pin: 1p=2, 9p=2
        2,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2,  # sou: 1s=2, 9s=2
        2,
        0,
        0,
        0,
        0,
        0,
        1,  # honors: 1z=2, 7z=1
    ]


def test_convert_to_136_array() -> None:
    tiles = TilesConverter.string_to_136_array(man="199", pin="1199", sou="1199", honors="117")
    result = TilesConverter.to_34_array(tiles)
    result = TilesConverter.to_136_array(result)
    assert result == tiles


def test_convert_string_to_136_array() -> None:
    tiles = TilesConverter.string_to_136_array(sou="19", pin="19", man="19", honors="1234567")

    assert tiles == [0, 32, 36, 68, 72, 104, 108, 112, 116, 120, 124, 128, 132]


@pytest.mark.parametrize(
    ("tile_34", "tiles_136", "expected"),
    [
        pytest.param(
            _string_to_34_tile(man="1"),
            TilesConverter.string_to_136_array(man="1222"),
            _string_to_136_tile(man="1"),
            id="finds_first_match",
        ),
        pytest.param(
            _string_to_34_tile(honors="7"),
            TilesConverter.string_to_136_array(man="1", honors="77"),
            _string_to_136_tile(honors="7"),
            id="finds_honor_tile",
        ),
        pytest.param(
            _string_to_34_tile(sou="3"),
            TilesConverter.string_to_136_array(man="1", honors="77"),
            None,
            id="returns_none_for_missing_tile",
        ),
        pytest.param(
            34,
            TilesConverter.string_to_136_array(man="1111"),
            None,
            id="returns_none_for_out_of_range_tile",
        ),
    ],
)
def test_find_34_tile_in_136_array(tile_34: int, tiles_136: list[int], expected: int | None) -> None:
    result = TilesConverter.find_34_tile_in_136_array(tile_34, tiles_136)
    assert result == expected


def test_convert_string_with_aka_dora_to_136_array() -> None:
    tiles = TilesConverter.string_to_136_array(man="22444", pin="333r67", sou="444", has_aka_dora=True)
    assert FIVE_RED_PIN in tiles


def test_convert_string_with_aka_dora_as_zero_to_136_array() -> None:
    tiles = TilesConverter.string_to_136_array(man="22444", pin="333067", sou="444", has_aka_dora=True)
    assert FIVE_RED_PIN in tiles


def test_one_line_string_to_136_array() -> None:
    initial_string = "789m456p555s11222z"
    tiles = TilesConverter.one_line_string_to_136_array(initial_string)
    new_string = TilesConverter.to_one_line_string(tiles)
    assert initial_string == new_string


def test_one_line_string_to_34_array() -> None:
    initial_string = "789m456p555s11222z"
    tiles = TilesConverter.one_line_string_to_34_array(initial_string)
    tiles = TilesConverter.to_136_array(tiles)
    new_string = TilesConverter.to_one_line_string(tiles)
    assert initial_string == new_string


def test_tile_instantiation() -> None:
    tile_value = _string_to_136_tile(man="1")
    tile = Tile(value=tile_value, is_tsumogiri=False)
    assert tile.value == tile_value
    assert tile.is_tsumogiri is False
