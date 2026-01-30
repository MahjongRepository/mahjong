from mahjong.meld import Meld
from mahjong.tile import TilesConverter


def test_meld_str() -> None:
    tiles = TilesConverter.string_to_136_array(man="123")
    meld = Meld(meld_type=Meld.CHI, tiles=tiles)
    assert str(meld) == f"Type: chi, Tiles: 123m {tiles}"


def test_meld_repr() -> None:
    tiles = TilesConverter.string_to_136_array(man="111")
    meld = Meld(meld_type=Meld.PON, tiles=tiles)
    assert repr(meld) == str(meld)
