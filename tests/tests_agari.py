import pytest

from mahjong.agari import Agari
from mahjong.tile import TilesConverter
from tests.utils_for_tests import _string_to_open_34_set


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("123456789", "123", "33", ""),
        ("123456789", "11123", "", ""),
        ("123456789", "", "", "11777"),
        ("12345556778899", "", "", ""),
        ("11123456788999", "", "", ""),
        ("233334", "789", "345", "55"),
    ],
)
def test_is_agari(sou: str, pin: str, man: str, honors: str) -> None:
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert agari.is_agari(tiles)


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("123456789", "12345", "", ""),
        ("111222444", "11145", "", ""),
        ("11122233356888", "", "", ""),
    ],
)
def test_is_not_agari(sou: str, pin: str, man: str, honors: str) -> None:
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert not agari.is_agari(tiles)


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("1133557799", "1199", "", ""),
        ("2244", "1199", "11", "2277"),
        ("", "", "11223344556677", ""),
    ],
)
def test_is_chitoitsu_agari(sou: str, pin: str, man: str, honors: str) -> None:
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert agari.is_agari(tiles)


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("19", "19", "199", "1234567"),
        ("19", "19", "19", "11234567"),
        ("19", "19", "19", "12345677"),
    ],
)
def test_is_kokushi_musou_agari(sou: str, pin: str, man: str, honors: str) -> None:
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert agari.is_agari(tiles)


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("129", "19", "19", "1234567"),
        ("19", "19", "19", "11134567"),
    ],
)
def test_is_not_kokushi_musou_agari(sou: str, pin: str, man: str, honors: str) -> None:
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert not agari.is_agari(tiles)


def test_is_agari_and_open_hand() -> None:
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou="23455567", pin="222", man="345")
    melds = [
        _string_to_open_34_set(man="345"),
        _string_to_open_34_set(sou="555"),
    ]
    assert not agari.is_agari(tiles, melds)


def test_is_agari_can_call_as_static_method() -> None:
    tiles = TilesConverter.string_to_34_array(sou="123456789", pin="123", man="33")
    assert Agari.is_agari(tiles)


def test_open_sets_break_when_isolated_tiles_exhausted() -> None:
    tiles = TilesConverter.string_to_34_array(man="123456789", pin="123456789", sou="123456789", honors="1234567")
    open_sets = [
        _string_to_open_34_set(man="123"),
        _string_to_open_34_set(pin="123"),
    ]
    assert Agari.is_agari(tiles, open_sets) is False


@pytest.mark.parametrize(
    "tiles_34",
    [
        pytest.param(
            TilesConverter.string_to_34_array(honors="55555"),
            id="honor_count_5",
        ),
        pytest.param(
            TilesConverter.string_to_34_array(honors="1111"),
            id="honor_count_4",
        ),
    ],
)
def test_honor_tile_overflow_returns_false(tiles_34: list[int]) -> None:
    assert Agari.is_agari(tiles_34) is False


def test_pin_suit_mod3_equals_1_returns_false() -> None:
    # 1 tile in pin suit: sum = 1, 1 % 3 = 1
    tiles = TilesConverter.string_to_34_array(pin="1")
    assert Agari.is_agari(tiles) is False


def test_sou_suit_mod3_equals_1_returns_false() -> None:
    # 1 tile in sou suit: sum = 1, 1 % 3 = 1
    tiles = TilesConverter.string_to_34_array(sou="1")
    assert Agari.is_agari(tiles) is False


@pytest.mark.parametrize(
    "tiles_34",
    [
        pytest.param(
            TilesConverter.string_to_34_array(man="11", pin="11"),
            id="two_suit_pairs",
        ),
        pytest.param(
            TilesConverter.string_to_34_array(man="111"),
            id="zero_pairs",
        ),
    ],
)
def test_wrong_pair_count_returns_false(tiles_34: list[int]) -> None:
    assert Agari.is_agari(tiles_34) is False


def test_no_valid_decomposition_returns_false() -> None:
    # east wind pair triggers j & 4 branch;
    # man 1-4-7 are non-adjacent isolated tiles that can't form valid mentsu
    tiles = TilesConverter.string_to_34_array(man="147", honors="11")
    assert Agari.is_agari(tiles) is False


def test_is_mentsu_negative_a_returns_false() -> None:
    # east wind pair triggers j & 4 branch;
    # 1m count=2 implies 2 sequences, but 2m count=0 gives a = 0 - 2 = -2 < 0
    tiles = TilesConverter.string_to_34_array(man="114", honors="11")
    assert Agari.is_agari(tiles) is False
