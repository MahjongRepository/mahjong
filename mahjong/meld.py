from collections.abc import Sequence
from typing import Optional

from mahjong.tile import TilesConverter


class Meld:
    CHI = "chi"
    PON = "pon"
    KAN = "kan"
    SHOUMINKAN = "shouminkan"
    NUKI = "nuki"

    who = None
    tiles = None
    type = None
    from_who = None
    called_tile = None
    # we need it to distinguish opened and closed kan
    opened = True

    def __init__(
        self,
        meld_type: Optional[str] = None,
        tiles: Optional[Sequence[int]] = None,
        opened: bool = True,
        called_tile: Optional[int] = None,
        who: Optional[int] = None,
        from_who: Optional[int] = None,
    ) -> None:
        self.type = meld_type
        self.tiles = list(tiles) if tiles else []
        self.opened = opened
        self.called_tile = called_tile
        self.who = who
        self.from_who = from_who

    def __str__(self) -> str:
        return "Type: {}, Tiles: {} {}".format(self.type, TilesConverter.to_one_line_string(self.tiles), self.tiles)

    # for calls in array
    def __repr__(self) -> str:
        return self.__str__()

    @property
    def tiles_34(self) -> list[int]:
        return [x // 4 for x in self.tiles]
