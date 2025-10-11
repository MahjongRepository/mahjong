from typing import Optional

import pytest

from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "shanten_number"),
    [
        ("4566677", "1367", "8", "12", 2),
        ("14", "3356", "3678", "2567", 4),
        (None, None, "1111222235555", "1", 0),
    ],
)
def test_calculate_shanten(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
    shanten_number: int,
) -> None:
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert shanten.calculate_shanten(tiles) == shanten_number


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "shanten_number"),
    [
        ("111234567", "11", "567", None, -1),
        ("111345677", "11", "567", None, 0),
        ("111345677", "15", "567", None, 1),
        ("11134567", "15", "1578", None, 2),
        ("113456", "1358", "1358", None, 3),
        ("1589", "13588", "1358", "1", 4),
        ("159", "13588", "1358", "12", 5),
        ("1589", "258", "1358", "123", 6),
        ("11123456788999", None, None, None, -1),
        ("11122245679999", None, None, None, 0),
        ("159", "17", "359", "123567", 7),
        (None, None, None, "11112222333444", 1),
        (None, None, "11", "111122223333", 2),
        (None, None, "23", "111122223333", 2),
    ],
)
def test_calculate_shanten_for_regular_hand(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
    shanten_number: int,
) -> None:
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert shanten.calculate_shanten_for_regular_hand(tiles) == shanten_number


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "shanten_number"),
    [
        ("111345677", "1", "567", None, 1),
        ("111345677", None, "567", None, 1),
        ("111345677", None, "56", None, 0),
        (None, None, "123456789", "1111", 1),
        ("112233", "123", "1111", None, 1),
        (None, None, None, "1111222333444", 1),
        (None, None, "11", "11112222333", 2),
        (None, None, "23", "11112222333", 2),
        (None, None, None, "1111222233334", 3),
    ],
)
def test_calculate_shanten_for_regular_hand_for_not_completed_hand(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
    shanten_number: int,
) -> None:
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert shanten.calculate_shanten_for_regular_hand(tiles) == shanten_number


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "shanten_number"),
    [
        ("114477", "114477", "77", None, -1),
        ("114477", "114477", "76", None, 0),
        ("114477", "114479", "76", None, 1),
        ("114477", "14479", "76", "1", 2),
        ("114477", "13479", "76", "1", 3),
        ("114467", "13479", "76", "1", 4),
        ("114367", "13479", "76", "1", 5),
        ("124367", "13479", "76", "1", 6),
        ("66677888", "55", "2255", None, 1),
    ],
)
def test_calculate_shanten_for_chiitoitsu_hand(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
    shanten_number: int,
) -> None:
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == shanten_number


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "shanten_number"),
    [
        ("19", "19", "19", "12345677", -1),
        ("129", "19", "19", "1234567", 0),
        ("129", "129", "19", "123456", 1),
        ("129", "129", "129", "12345", 2),
        ("1239", "129", "129", "2345", 3),
        ("1239", "1239", "129", "345", 4),
        ("1239", "1239", "1239", "45", 5),
        ("12349", "1239", "1239", "5", 6),
        ("12349", "12349", "1239", None, 7),
    ],
)
def test_calculate_shanten_for_kokushi_hand(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
    shanten_number: int,
) -> None:
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == shanten_number


@pytest.mark.parametrize(
    ("sou", "pin", "man", "honors", "shanten_number"),
    [
        ("44467778", "222567", None, None, -1),
        ("44468", "222567", None, None, 0),
        ("68", "222567", None, None, 0),
        ("68", "567", None, None, 0),
        ("68", None, None, None, 0),
        ("88", None, None, None, -1),
    ],
)
def test_calculate_shanten_with_open_sets(
    sou: Optional[str],
    pin: Optional[str],
    man: Optional[str],
    honors: Optional[str],
    shanten_number: int,
) -> None:
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)
    assert shanten.calculate_shanten(tiles) == shanten_number


def test_calculate_shanten_can_call_as_static_method() -> None:
    tiles = TilesConverter.string_to_34_array(sou="4566677", pin="1367", man="8", honors="12")
    assert Shanten.calculate_shanten(tiles) == 2


def test_calculate_shanten_for_regular_hand_can_call_as_static_method() -> None:
    tiles = TilesConverter.string_to_34_array(sou="111234567", pin="11", man="567")
    assert Shanten.calculate_shanten_for_regular_hand(tiles) == Shanten.AGARI_STATE


def test_calculate_shanten_for_chiitoitsu_hand_can_call_as_static_method() -> None:
    tiles = TilesConverter.string_to_34_array(sou="114477", pin="114477", man="77")
    assert Shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == Shanten.AGARI_STATE


def test_calculate_shanten_for_kokushi_hand_can_call_as_static_method() -> None:
    tiles = TilesConverter.string_to_34_array(sou="19", pin="19", man="19", honors="12345677")
    assert Shanten.calculate_shanten_for_kokushi_hand(tiles) == Shanten.AGARI_STATE
