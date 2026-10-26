from collections.abc import Sequence
from functools import cached_property

from mahjong.constants import NORTH
from mahjong.tile import TilesConverter
from mahjong.utils import is_chi, is_honor, is_pon


class Meld:
    """
    Representation of a declared meld (called or concealed tile group).

    A meld is a set of tiles that a player has declared, either by calling another
    player's discard (open meld) or by declaring a concealed kan. Meld types follow
    standard Japanese mahjong terminology:

    - **Chi** — a sequence of three consecutive suited tiles, called from the player to the left.
    - **Pon** — a triplet of identical tiles, called from any player.
    - **Kan** — a quad of identical tiles (open, closed, or extended).
    - **Shouminkan** — an added kan (extending an existing pon with the fourth tile).
    - **Nuki** — a special declaration used in three-player mahjong (north wind extraction).

    Create an open chi meld:

    >>> from mahjong.meld import Meld
    >>> from mahjong.tile import TilesConverter
    >>> tiles = TilesConverter.string_to_136_array(man="123")
    >>> meld = Meld(meld_type=Meld.CHI, tiles=tiles)
    >>> meld.type
    'chi'
    >>> meld.tiles
    (0, 4, 8)

    Create a closed kan:

    >>> tiles = TilesConverter.string_to_136_array(man="1111")
    >>> meld = Meld(meld_type=Meld.KAN, tiles=tiles, opened=False)
    >>> meld.opened
    False

    :ivar type: one of the meld type constants (CHI, PON, KAN, SHOUMINKAN, NUKI)
    :vartype type: str | None
    :ivar tiles: tile indices in 136-format, stored as an immutable tuple
    :vartype tiles: tuple[int, ...]
    :ivar opened: True for open melds (called from another player), False for closed kan
    :vartype opened: bool
    :ivar called_tile: the specific tile index (136-format) that was called to form this meld
    :vartype called_tile: int | None
    :ivar who: seat index (0-3) of the player who declared the meld
    :vartype who: int | None
    :ivar from_who: seat index (0-3) of the player who discarded the called tile
    :vartype from_who: int | None
    """

    CHI = "chi"
    """Chi (sequence) meld type — three consecutive suited tiles."""

    PON = "pon"
    """Pon (triplet) meld type — three identical tiles."""

    KAN = "kan"
    """Kan (quad) meld type — four identical tiles."""

    SHOUMINKAN = "shouminkan"
    """Shouminkan (added kan) meld type — extending a pon with the fourth tile."""

    NUKI = "nuki"
    """Nuki (north wind extraction) meld type, at the moment is not used in the library."""

    type: str | None
    tiles: tuple[int, ...]
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
        """
        Initialize a meld.

        >>> from mahjong.meld import Meld
        >>> from mahjong.tile import TilesConverter
        >>> tiles = TilesConverter.string_to_136_array(man="111")
        >>> meld = Meld(meld_type=Meld.PON, tiles=tiles, who=0, from_who=2)
        >>> meld.type
        'pon'
        >>> meld.who
        0

        :param meld_type: one of the meld type constants (CHI, PON, KAN, SHOUMINKAN, NUKI)
        :param tiles: tile indices in 136-format
        :param opened: True for open melds (called from another player), False for closed kan
        :param called_tile: the specific tile index (136-format) that was called to form this meld
        :param who: seat index (0-3) of the player who declared the meld
        :param from_who: seat index (0-3) of the player who discarded the called tile
        """
        self.type = meld_type
        self.tiles = tuple(tiles) if tiles else ()
        self.opened = opened
        self.called_tile = called_tile
        self.who = who
        self.from_who = from_who

    def __setattr__(self, name: str, value: object) -> None:
        """Invalidate the tiles_34 cache when tiles are reassigned."""
        super().__setattr__(name, value)
        if name == "tiles" and "tiles_34" in self.__dict__:
            del self.__dict__["tiles_34"]

    def __str__(self) -> str:
        """
        Return a human-readable string with meld type and tiles.

        >>> from mahjong.meld import Meld
        >>> from mahjong.tile import TilesConverter
        >>> tiles = TilesConverter.string_to_136_array(man="123")
        >>> meld = Meld(meld_type=Meld.CHI, tiles=tiles)
        >>> str(meld)
        'Type: chi, Tiles: 123m (0, 4, 8)'
        """
        return f"Type: {self.type}, Tiles: {TilesConverter.to_one_line_string(self.tiles)} {self.tiles}"

    def __repr__(self) -> str:
        """Return the same representation as __str__."""
        return self.__str__()

    @cached_property
    def tiles_34(self) -> list[int]:
        """
        Convert the meld's 136-format tile indices to 34-format tile indices.

        >>> from mahjong.meld import Meld
        >>> from mahjong.tile import TilesConverter
        >>> tiles = TilesConverter.string_to_136_array(man="111")
        >>> meld = Meld(meld_type=Meld.PON, tiles=tiles)
        >>> meld.tiles_34
        [0, 0, 0]

        :return: list of tile indices in 34-format
        """
        return [x // 4 for x in self.tiles]

    def is_valid(self) -> bool:
        """
        Check that the meld tiles match its type and that only a kan is closed.

        A chi is three consecutive tiles of one suit, a pon is three identical tiles, a kan
        or shouminkan is four identical tiles, a nuki is one to four north winds. Chi, pon and
        shouminkan are always called, so only a kan or a nuki may be closed. Unknown types
        are not valid.

        >>> from mahjong.meld import Meld
        >>> from mahjong.tile import TilesConverter
        >>> Meld(meld_type=Meld.CHI, tiles=TilesConverter.string_to_136_array(man="123")).is_valid()
        True

        >>> Meld(meld_type=Meld.CHI, tiles=TilesConverter.string_to_136_array(man="89", pin="1")).is_valid()
        False

        >>> Meld(meld_type=Meld.PON, tiles=TilesConverter.string_to_136_array(man="111"), opened=False).is_valid()
        False

        :return: True if the meld is valid
        """
        tiles_34 = sorted(self.tiles_34)
        match self.type:
            case Meld.CHI:
                is_valid_shape = is_chi(tiles_34) and not is_honor(tiles_34[0]) and tiles_34[0] // 9 == tiles_34[2] // 9
            case Meld.PON:
                is_valid_shape = is_pon(tiles_34)
            case Meld.KAN | Meld.SHOUMINKAN:
                is_valid_shape = len(tiles_34) == 4 and len(set(tiles_34)) == 1
            case Meld.NUKI:
                is_valid_shape = 0 < len(tiles_34) <= 4 and all(tile == NORTH for tile in tiles_34)
            case _:
                return False

        return is_valid_shape and (self.opened or self.type in (Meld.KAN, Meld.NUKI))
