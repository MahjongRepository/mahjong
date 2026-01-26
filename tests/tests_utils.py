from mahjong.tile import TilesConverter
from mahjong.utils import (
    find_isolated_tile_indices,
    is_dora_indicator_for_terminal,
    is_tile_strictly_isolated,
    simplify,
)
from tests.utils_for_tests import _string_to_34_tile


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
