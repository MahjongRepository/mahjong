from mahjong.meld import Meld
from mahjong.tile import TilesConverter


def test_meld_str() -> None:
    tiles = TilesConverter.string_to_136_array(man="123")
    meld = Meld(meld_type=Meld.CHI, tiles=tiles)
    assert str(meld) == f"Type: chi, Tiles: 123m {tuple(tiles)}"


def test_meld_repr() -> None:
    tiles = TilesConverter.string_to_136_array(man="111")
    meld = Meld(meld_type=Meld.PON, tiles=tiles)
    assert repr(meld) == str(meld)


def test_tiles_34_updates_on_tiles_reassignment() -> None:
    tiles = TilesConverter.string_to_136_array(man="111")
    meld = Meld(meld_type=Meld.PON, tiles=tiles)
    assert meld.tiles_34 == [0, 0, 0]

    new_tiles = TilesConverter.string_to_136_array(man="1111")
    meld.tiles = tuple(new_tiles)
    assert meld.tiles_34 == [0, 0, 0, 0]
