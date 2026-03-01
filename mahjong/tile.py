from collections import Counter
from collections.abc import Collection, Sequence
from typing import Any

from mahjong.constants import FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU


class Tile:
    """
    Container for a single discarded tile record.

    Not used internally by the library. Provided as a convenience data class
    for consumers that need to track discards with tsumogiri information.

    :ivar value: tile index (typically in 136-format)
    :ivar is_tsumogiri: True if the tile was discarded immediately after drawing it
    """

    value: Any
    is_tsumogiri: Any

    def __init__(self, value: Any, is_tsumogiri: Any) -> None:  # noqa: ANN401
        """
        Initialize a tile record.

        :param value: tile index (typically in 136-format)
        :param is_tsumogiri: True if the tile was discarded immediately after drawing it
        """
        self.value = value
        self.is_tsumogiri = is_tsumogiri


class TilesConverter:
    """
    Utility class for converting between tile representation formats.

    All methods are static — no instance is needed. The class supports conversion
    between mpsz-notation strings, 34-format arrays, and 136-format arrays.
    """

    @staticmethod
    def to_one_line_string(tiles: Collection[int], print_aka_dora: bool = False) -> str:
        """
        Convert a collection of 136-format tile indices to an mpsz-notation string.

        When ``print_aka_dora`` is False, red fives are printed as ``5``.
        When True, they are printed as ``0``.

        >>> TilesConverter.to_one_line_string([0, 4, 8, 12, 16, 24, 32])
        '1234579m'
        >>> TilesConverter.to_one_line_string([0, 4, 8, 12, 16, 24, 32], print_aka_dora=True)
        '1234079m'

        :param tiles: tile indices in 136-format
        :param print_aka_dora: render red fives as ``0`` instead of ``5``
        :return: mpsz-notation string representing the tiles
        """
        tiles = sorted(tiles)

        man = [t for t in tiles if t < 36]
        pin = [t - 36 for t in tiles if 36 <= t < 72]
        sou = [t - 72 for t in tiles if 72 <= t < 108]
        honors = [t - 108 for t in tiles if t >= 108]

        def words(suits: list[int], red_five: int, suffix: str) -> str:
            if not suits:
                return ""
            return "".join(["0" if i == red_five and print_aka_dora else str((i // 4) + 1) for i in suits]) + suffix

        man_words = words(man, FIVE_RED_MAN, "m")
        pin_words = words(pin, FIVE_RED_PIN - 36, "p")
        sou_words = words(sou, FIVE_RED_SOU - 72, "s")
        honors_words = words(honors, -1 - 108, "z")

        return man_words + pin_words + sou_words + honors_words

    @staticmethod
    def to_34_array(tiles: Collection[int]) -> list[int]:
        """
        Convert a collection of 136-format tile indices to a 34-format count array.

        Each element of the returned list holds the number of copies present
        for that tile type.

        >>> TilesConverter.to_34_array([0, 1, 2, 3])
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        :param tiles: tile indices in 136-format
        :return: list of length 34 with tile counts
        """
        results = [0] * 34
        for tile in tiles:
            results[tile // 4] += 1
        return results

    @staticmethod
    def to_136_array(tiles: Sequence[int]) -> list[int]:
        """
        Convert a 34-format count array to a list of 136-format tile indices.

        For each tile type with count *n*, the first *n* physical tile indices are
        selected (e.g., count 2 of 1m yields indices ``[0, 1]``).

        >>> tiles_34 = [2] + [0] * 33
        >>> TilesConverter.to_136_array(tiles_34)
        [0, 1]

        :param tiles: 34-format count array (length 34)
        :return: list of tile indices in 136-format
        """
        results: list[int] = []
        for index, count in enumerate(tiles):
            base_id = index * 4
            results.extend(base_id + i for i in range(count))
        return results

    @staticmethod
    def _split_string(string: str | None, offset: int, red: int | None = None) -> list[int]:
        if not string:
            return []

        counts: Counter[int] = Counter()
        result: list[int] = []

        explicit_aka = {"r", "0"}
        for ch in string:
            # explicit aka markers
            if ch in explicit_aka and red is not None:
                result.append(red)
                continue

            tile = offset + (int(ch) - 1) * 4
            # numeric '5' should not map to aka id when aka support is present
            if red is not None and tile == red:
                tile += 1

            count_of_tiles = counts[tile]
            result.append(tile + count_of_tiles)
            counts[tile] += 1

        return result

    @staticmethod
    def string_to_136_array(
        sou: str | None = None,
        pin: str | None = None,
        man: str | None = None,
        honors: str | None = None,
        has_aka_dora: bool = False,
    ) -> list[int]:
        """
        Convert per-suit digit strings to a list of 136-format tile indices.

        Each suit string contains digit characters representing tile ranks.
        When ``has_aka_dora`` is True, ``0`` or ``r`` in a suit string produces
        the red five for that suit.

        >>> TilesConverter.string_to_136_array(man="123")
        [0, 4, 8]
        >>> TilesConverter.string_to_136_array(man="0", has_aka_dora=True)
        [16]

        :param sou: souzu (bamboo) tile ranks
        :param pin: pinzu (circles) tile ranks
        :param man: manzu (characters) tile ranks
        :param honors: honor tile ranks (1-7 for East through Red dragon)
        :param has_aka_dora: enable red five handling (``0`` and ``r`` map to aka dora)
        :return: list of tile indices in 136-format
        """
        results = TilesConverter._split_string(man, 0, FIVE_RED_MAN if has_aka_dora else None)
        results += TilesConverter._split_string(pin, 36, FIVE_RED_PIN if has_aka_dora else None)
        results += TilesConverter._split_string(sou, 72, FIVE_RED_SOU if has_aka_dora else None)
        results += TilesConverter._split_string(honors, 108)
        return results

    @staticmethod
    def string_to_34_array(
        sou: str | None = None,
        pin: str | None = None,
        man: str | None = None,
        honors: str | None = None,
    ) -> list[int]:
        """
        Convert per-suit digit strings to a 34-format count array.

        Equivalent to calling :meth:`string_to_136_array` followed by :meth:`to_34_array`.

        >>> TilesConverter.string_to_34_array(man="111")
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        :param sou: souzu (bamboo) tile ranks
        :param pin: pinzu (circles) tile ranks
        :param man: manzu (characters) tile ranks
        :param honors: honor tile ranks (1-7 for East through Red dragon)
        :return: list of length 34 with tile counts
        """
        results = TilesConverter.string_to_136_array(sou, pin, man, honors)
        return TilesConverter.to_34_array(results)

    @staticmethod
    def find_34_tile_in_136_array(tile34: int | None, tiles: Collection[int]) -> int | None:
        """
        Find the first 136-format index that corresponds to a given 34-format tile type.

        A single 34-format index maps to four possible 136-format indices
        (e.g., tile type 0 maps to indices 0, 1, 2, 3). Return the first one
        present in *tiles*, or ``None`` if no match is found.

        >>> TilesConverter.find_34_tile_in_136_array(0, [1, 4, 8])
        1
        >>> TilesConverter.find_34_tile_in_136_array(0, [4, 8]) is None
        True

        :param tile34: tile type index in 34-format, or None
        :param tiles: collection of tile indices in 136-format to search
        :return: first matching 136-format index, or None
        """
        if tile34 is None or tile34 > 33:
            return None

        tile = tile34 * 4

        possible_tiles = [tile] + [tile + i for i in range(1, 4)]

        found_tile = None
        for possible_tile in possible_tiles:
            if possible_tile in tiles:
                found_tile = possible_tile
                break

        return found_tile

    @staticmethod
    def one_line_string_to_136_array(string: str, has_aka_dora: bool = False) -> list[int]:
        """
        Parse a combined mpsz-notation string into a list of 136-format tile indices.

        The string contains digit sequences terminated by suit letters:
        ``m`` (man), ``p`` (pin), ``s`` (sou), ``z`` or ``h`` (honors).
        For example, ``"123m456p789s11z"`` represents 1-2-3 man, 4-5-6 pin,
        7-8-9 sou, and a pair of East winds.

        When ``has_aka_dora`` is True, ``0`` or ``r`` in the string produces
        the red five for the corresponding suit.

        >>> TilesConverter.one_line_string_to_136_array("123m456s")
        [0, 4, 8, 84, 88, 92]
        >>> TilesConverter.one_line_string_to_136_array("0m", has_aka_dora=True)
        [16]

        :param string: mpsz-notation string (e.g., ``"123m456p789s11z"``)
        :param has_aka_dora: enable red five handling (``0`` and ``r`` map to aka dora)
        :return: list of tile indices in 136-format
        """
        sou = ""
        pin = ""
        man = ""
        honors = ""

        split_start = 0

        for index, i in enumerate(string):
            if i == "m":
                man += string[split_start:index]
                split_start = index + 1
            if i == "p":
                pin += string[split_start:index]
                split_start = index + 1
            if i == "s":
                sou += string[split_start:index]
                split_start = index + 1
            if i in {"z", "h"}:
                honors += string[split_start:index]
                split_start = index + 1

        return TilesConverter.string_to_136_array(sou, pin, man, honors, has_aka_dora)

    @staticmethod
    def one_line_string_to_34_array(string: str, has_aka_dora: bool = False) -> list[int]:
        """
        Parse a combined mpsz-notation string into a 34-format count array.

        Equivalent to calling :meth:`one_line_string_to_136_array` followed by
        :meth:`to_34_array`.

        >>> TilesConverter.one_line_string_to_34_array("111m")
        [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        :param string: mpsz-notation string (e.g., ``"123m456p789s11z"``)
        :param has_aka_dora: enable red five handling (``0`` and ``r`` map to aka dora)
        :return: list of length 34 with tile counts
        """
        results = TilesConverter.one_line_string_to_136_array(string, has_aka_dora)
        return TilesConverter.to_34_array(results)
