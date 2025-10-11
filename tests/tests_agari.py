from typing import Optional

import pytest

from mahjong.agari import Agari
from mahjong.tile import TilesConverter
from tests.utils_for_tests import _string_to_open_34_set


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("123456789", "123", "33", None),
        ("123456789", "11123", None, None),
        ("123456789", None, None, "11777"),
        ("12345556778899", None, None, None),
        ("11123456788999", None, None, None),
        ("233334", "789", "345", "55"),
    ],
)
def test_is_agari(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
) -> None:
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert agari.is_agari(tiles)


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("123456789", "12345", None, None),
        ("111222444", "11145", None, None),
        ("11122233356888", None, None, None),
    ],
)
def test_is_not_agari(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
) -> None:
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert not agari.is_agari(tiles)


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors"),
    [
        ("1133557799", "1199", None, None),
        ("2244", "1199", "11", "2277"),
        (None, None, "11223344556677", None),
    ],
)
def test_is_chitoitsu_agari(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
) -> None:
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
def test_is_kokushi_musou_agari(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
) -> None:
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
def test_is_not_kokushi_musou_agari(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
) -> None:
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
