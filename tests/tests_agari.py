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
    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert Agari.is_agari(tiles) is True


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("123456789", "12345", "", ""),
        ("111222444", "11145", "", ""),
        ("11122233356888", "", "", ""),
    ],
)
def test_is_not_agari(sou: str, pin: str, man: str, honors: str) -> None:
    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert Agari.is_agari(tiles) is False


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("1133557799", "1199", "", ""),
        ("2244", "1199", "11", "2277"),
        ("", "", "11223344556677", ""),
    ],
)
def test_is_chitoitsu_agari(sou: str, pin: str, man: str, honors: str) -> None:
    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert Agari.is_agari(tiles) is True


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("19", "19", "199", "1234567"),
        ("19", "19", "19", "11234567"),
        ("19", "19", "19", "12345677"),
    ],
)
def test_is_kokushi_musou_agari(sou: str, pin: str, man: str, honors: str) -> None:
    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert Agari.is_agari(tiles) is True


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("129", "19", "19", "1234567"),
        ("19", "19", "19", "11134567"),
    ],
)
def test_is_not_kokushi_musou_agari(sou: str, pin: str, man: str, honors: str) -> None:
    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert Agari.is_agari(tiles) is False


def test_is_agari_and_open_hand() -> None:
    tiles = TilesConverter.string_to_34_array(sou="23455567", pin="222", man="345")
    melds = [
        _string_to_open_34_set(man="345"),
        _string_to_open_34_set(sou="555"),
    ]
    assert Agari.is_agari(tiles, melds) is False


def test_open_hand_with_many_melds_returns_false() -> None:
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


@pytest.mark.parametrize(
    ("man", "pin", "sou"),
    [
        pytest.param("1", "", "", id="man"),
        pytest.param("", "1", "", id="pin"),
        pytest.param("", "", "1", id="sou"),
    ],
)
def test_single_tile_in_suit_returns_false(man: str, pin: str, sou: str) -> None:
    # a single tile in any suit can't form a valid group (tile count % 3 == 1)
    tiles = TilesConverter.string_to_34_array(man=man, pin=pin, sou=sou)
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


def test_open_hand_with_kan_meld() -> None:
    # 4-tile kan meld exercises the len(meld) > 3 branch
    tiles = TilesConverter.string_to_34_array(man="1111", pin="123456789", sou="22")
    kan_of_1m = [0, 0, 0, 0]
    assert Agari.is_agari(tiles, [kan_of_1m]) is True


@pytest.mark.parametrize(
    ("man", "pin"),
    [
        pytest.param("66", "111222333444"),
        pytest.param("99", "111222333444"),
        pytest.param("22", "111222333444"),
        pytest.param("44", "111222333444"),
        pytest.param("77", "111222333444"),
    ],
)
def test_atama_mentsu_pair_positions(man: str, pin: str) -> None:
    # each case places the pair at a different position within the man suit,
    # exercising distinct branches in _is_atama_mentsu
    tiles = TilesConverter.string_to_34_array(man=man, pin=pin)
    assert Agari.is_agari(tiles) is True
