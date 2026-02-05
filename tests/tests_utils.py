import pytest

from mahjong.constants import FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU, HAKU
from mahjong.tile import TilesConverter
from mahjong.utils import (
    _indicator_to_dora_34,
    build_dora_count_map,
    classify_hand_suits,
    contains_terminals,
    count_dora_for_hand,
    count_tiles_by_suits,
    find_isolated_tile_indices,
    has_pon_or_kan_of,
    is_aka_dora,
    is_chi,
    is_dora_indicator_for_terminal,
    is_kan,
    is_pair,
    is_pon,
    is_pon_or_kan,
    is_sangenpai,
    is_terminal,
    is_tile_strictly_isolated,
    plus_dora,
    simplify,
)
from tests.utils_for_tests import _string_to_34_tile, _string_to_34_tiles, _string_to_136_tile


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
        ("", "", "1", "", True),
        ("", "", "2", "", True),
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
    hand_34 = TilesConverter.string_to_34_array(sou="1369", pin="15678", man="45", honors="124")
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


@pytest.mark.parametrize(
    ("tile_136", "dora_indicators_136", "add_aka_dora", "expected"),
    [
        # aka dora: FIVE_RED_MAN counts as dora when add_aka_dora is enabled
        (FIVE_RED_MAN, [], True, 1),
        # aka dora disabled: FIVE_RED_MAN does not count as dora
        (FIVE_RED_MAN, [], False, 0),
        # 9m indicator wraps dora to 1m
        (_string_to_136_tile(man="1"), [_string_to_136_tile(man="9")], False, 1),
        # 9p indicator wraps dora to 1p
        (_string_to_136_tile(pin="1"), [_string_to_136_tile(pin="9")], False, 1),
        # 9s indicator wraps dora to 1s
        (_string_to_136_tile(sou="1"), [_string_to_136_tile(sou="9")], False, 1),
        # chun indicator wraps dora to haku
        (_string_to_136_tile(honors="5"), [_string_to_136_tile(honors="7")], False, 1),
        # north indicator wraps dora to east
        (_string_to_136_tile(honors="1"), [_string_to_136_tile(honors="4")], False, 1),
        # no match: tile=2m, indicator=9m => dora is 1m, not 2m
        (_string_to_136_tile(man="2"), [_string_to_136_tile(man="9")], False, 0),
    ],
)
def test_plus_dora(tile_136: int, dora_indicators_136: list[int], add_aka_dora: bool, expected: int) -> None:
    assert plus_dora(tile_136, dora_indicators_136, add_aka_dora=add_aka_dora) == expected


@pytest.mark.parametrize(
    ("tile_34", "expected"),
    [
        (_string_to_34_tile(honors="5"), True),
        (_string_to_34_tile(honors="6"), True),
        (_string_to_34_tile(honors="7"), True),
        (_string_to_34_tile(honors="4"), False),
        (_string_to_34_tile(honors="1"), False),
        (_string_to_34_tile(man="5"), False),
    ],
)
def test_is_sangenpai(tile_34: int, expected: bool) -> None:
    assert is_sangenpai(tile_34) == expected


@pytest.mark.parametrize(
    ("tile_34", "expected"),
    [
        (_string_to_34_tile(man="1"), True),
        (_string_to_34_tile(man="9"), True),
        (_string_to_34_tile(pin="1"), True),
        (_string_to_34_tile(pin="9"), True),
        (_string_to_34_tile(sou="1"), True),
        (_string_to_34_tile(sou="9"), True),
        (_string_to_34_tile(man="5"), False),
        (_string_to_34_tile(pin="5"), False),
        (_string_to_34_tile(sou="5"), False),
        (_string_to_34_tile(honors="1"), False),
    ],
)
def test_is_terminal(tile_34: int, expected: bool) -> None:
    assert is_terminal(tile_34) == expected


@pytest.mark.parametrize(
    ("hand_set", "expected"),
    [
        (_string_to_34_tiles(man="123"), True),  # contains 1m (terminal)
        (_string_to_34_tiles(man="789"), True),  # contains 9m (terminal)
        (_string_to_34_tiles(pin="19"), True),  # contains 1p and 9p
        (_string_to_34_tiles(sou="456"), False),  # no terminals
        (_string_to_34_tiles(man="234"), False),  # no terminals
        (_string_to_34_tiles(honors="11"), False),  # honors are not terminals
        (_string_to_34_tiles(sou="19"), True),  # contains 1s and 9s
    ],
)
def test_contains_terminals(hand_set: list[int], expected: bool) -> None:
    assert contains_terminals(hand_set) == expected


def test_count_tiles_by_suits() -> None:
    tiles_34 = TilesConverter.string_to_34_array(man="123", pin="456", sou="789", honors="1")
    result = count_tiles_by_suits(tiles_34)

    assert result[0]["name"] == "sou"
    assert result[0]["count"] == 3
    assert result[1]["name"] == "man"
    assert result[1]["count"] == 3
    assert result[2]["name"] == "pin"
    assert result[2]["count"] == 3
    assert result[3]["name"] == "honor"
    assert result[3]["count"] == 1


def test_count_tiles_by_suits_empty_hand() -> None:
    tiles_34 = TilesConverter.string_to_34_array()
    result = count_tiles_by_suits(tiles_34)

    assert result[0]["count"] == 0
    assert result[1]["count"] == 0
    assert result[2]["count"] == 0
    assert result[3]["count"] == 0


@pytest.mark.parametrize(
    ("indicator_34", "expected_dora_34"),
    [
        # regular suited tiles: indicator + 1 = dora (one per suit)
        (_string_to_34_tile(man="4"), _string_to_34_tile(man="5")),
        (_string_to_34_tile(pin="1"), _string_to_34_tile(pin="2")),
        (_string_to_34_tile(sou="1"), _string_to_34_tile(sou="2")),
        # suit wrapping: 9 -> 1
        (_string_to_34_tile(man="9"), _string_to_34_tile(man="1")),
        # wind wrapping: north -> east
        (_string_to_34_tile(honors="2"), _string_to_34_tile(honors="3")),
        (_string_to_34_tile(honors="4"), _string_to_34_tile(honors="1")),
        # dragon wrapping: chun -> haku
        (_string_to_34_tile(honors="5"), _string_to_34_tile(honors="6")),
        (_string_to_34_tile(honors="7"), _string_to_34_tile(honors="5")),
    ],
)
def test_indicator_to_dora_34(indicator_34: int, expected_dora_34: int) -> None:
    assert _indicator_to_dora_34(indicator_34) == expected_dora_34


def test_build_dora_count_map_duplicate_indicators() -> None:
    # two 1m indicators both produce dora 2m, so count is 2
    indicator_a = _string_to_136_tile(man="1")
    result = build_dora_count_map([indicator_a, indicator_a + 1])
    assert result == {_string_to_34_tile(man="2"): 2}


def test_build_dora_count_map_different_indicators() -> None:
    result = build_dora_count_map([_string_to_136_tile(man="1"), _string_to_136_tile(pin="1")])
    assert result == {_string_to_34_tile(man="2"): 1, _string_to_34_tile(pin="2"): 1}


def test_count_dora_for_hand_no_dora() -> None:
    tiles_34 = TilesConverter.string_to_34_array(man="123", pin="456", sou="789", honors="11")
    dora_map = build_dora_count_map([_string_to_136_tile(man="5")])
    result = count_dora_for_hand(tiles_34, dora_map)
    assert result == 0


def test_count_dora_for_hand_multiple_dora_tiles() -> None:
    tiles_34 = TilesConverter.string_to_34_array(man="133", pin="456", sou="789", honors="11")
    dora_map = build_dora_count_map([_string_to_136_tile(man="2")])
    result = count_dora_for_hand(tiles_34, dora_map)
    assert result == 2


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        (_string_to_34_tiles(man="11"), True),
        (_string_to_34_tiles(man="111"), False),
        (_string_to_34_tiles(man="1111"), False),
        (_string_to_34_tiles(man="123"), False),
    ],
)
def test_is_pair(item: list[int], expected: bool) -> None:
    assert is_pair(item) == expected


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        (_string_to_34_tiles(man="123"), True),  # chi
        (_string_to_34_tiles(pin="456"), True),  # chi
        (_string_to_34_tiles(sou="789"), True),  # chi
        (_string_to_34_tiles(man="111"), False),  # pon
        (_string_to_34_tiles(man="11"), False),  # pair
        (_string_to_34_tiles(man="1111"), False),  # kan
        (_string_to_34_tiles(man="124"), False),  # not consecutive
    ],
)
def test_is_chi(item: list[int], expected: bool) -> None:
    assert is_chi(item) == expected


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        (_string_to_34_tiles(man="111"), True),  # pon
        (_string_to_34_tiles(pin="555"), True),  # pon
        (_string_to_34_tiles(honors="111"), True),  # pon of honors
        (_string_to_34_tiles(man="123"), False),  # chi
        (_string_to_34_tiles(man="11"), False),  # pair
        (_string_to_34_tiles(man="1111"), False),  # kan
    ],
)
def test_is_pon(item: list[int], expected: bool) -> None:
    assert is_pon(item) == expected


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        (_string_to_34_tiles(man="1111"), True),  # kan
        (_string_to_34_tiles(pin="5555"), True),  # kan
        (_string_to_34_tiles(man="111"), False),  # pon
        (_string_to_34_tiles(man="123"), False),  # chi
        (_string_to_34_tiles(man="11"), False),  # pair
    ],
)
def test_is_kan(item: list[int], expected: bool) -> None:
    assert is_kan(item) == expected


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        (_string_to_34_tiles(man="111"), True),  # pon
        (_string_to_34_tiles(man="1111"), True),  # kan
        (_string_to_34_tiles(pin="555"), True),  # pon
        (_string_to_34_tiles(pin="5555"), True),  # kan
        (_string_to_34_tiles(man="123"), False),  # chi
        (_string_to_34_tiles(man="11"), False),  # pair
    ],
)
def test_is_pon_or_kan(item: list[int], expected: bool) -> None:
    assert is_pon_or_kan(item) == expected
