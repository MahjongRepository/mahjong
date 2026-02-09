from collections.abc import Sequence
from functools import cached_property

from mahjong.tile import TilesConverter


class Meld:
    CHI = "chi"
    PON = "pon"
    KAN = "kan"
    SHOUMINKAN = "shouminkan"
    NUKI = "nuki"

    type: str | None
    tiles: tuple[int]
    # we need it to distinguish opened and closed kan
    opened: bool
    called_tile: int | None
    who: int | None
    from_who: int | None

    def __init__(
        self,
        meld_type: str | None = None,
        tiles: Sequence[int] | None = None,
        opened: bool = True,
        called_tile: int | None = None,
        who: int | None = None,
        from_who: int | None = None,
    ) -> None:
        self.type = meld_type
        self.tiles = tuple(tiles) if tiles else ()
        self.opened = opened
        self.called_tile = called_tile
        self.who = who
        self.from_who = from_who

    def __setattr__(self, name: str, value: object) -> None:
        super().__setattr__(name, value)
        if name == "tiles" and "tiles_34" in self.__dict__:
            del self.__dict__["tiles_34"]

    def __str__(self) -> str:
        return f"Type: {self.type}, Tiles: {TilesConverter.to_one_line_string(self.tiles)} {self.tiles}"

    # for calls in array
    def __repr__(self) -> str:
        return self.__str__()

    @cached_property
    def tiles_34(self) -> list[int]:
        return [x // 4 for x in self.tiles]
