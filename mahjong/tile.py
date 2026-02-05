from collections.abc import Collection, Sequence
from typing import Any

from mahjong.constants import FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU


class Tile:
    value: Any
    is_tsumogiri: Any

    def __init__(self, value: Any, is_tsumogiri: Any) -> None:  # noqa: ANN401
        self.value = value
        self.is_tsumogiri = is_tsumogiri


class TilesConverter:
    @staticmethod
    def to_one_line_string(tiles: Collection[int], print_aka_dora: bool = False) -> str:
        """
        Convert 136 tiles array to the one line string
        Example of output with print_aka_dora=False: 1244579m3p57z
        Example of output with print_aka_dora=True:  1244079m3p57z
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
        Convert 136 array to the 34 tiles array
        """
        results = [0] * 34
        for tile in tiles:
            results[tile // 4] += 1
        return results

    @staticmethod
    def to_136_array(tiles: Sequence[int]) -> list[int]:
        """
        Convert 34 array to the 136 tiles array
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

        data: list[int] = []
        seen: set[int] = set()
        counts: dict[int, int] = {}

        explicit_aka = {"r", "0"}
        for ch in string:
            # explicit aka markers
            if red is not None and ch in explicit_aka:
                data.append(red)
                seen.add(red)
                # explicit aka does not increment the regular tile count
                continue

            tile = offset + (int(ch) - 1) * 4

            # numeric '5' should not map to aka id when aka support is present
            if red is not None and tile == red:
                tile += 1

            if tile in seen:
                count_of_tiles = counts.get(tile, 0)
                new_tile = tile + count_of_tiles
                data.append(new_tile)
                seen.add(new_tile)
                counts[tile] = count_of_tiles + 1
            else:
                data.append(tile)
                seen.add(tile)
                counts[tile] = counts.get(tile, 0) + 1

        return data

    @staticmethod
    def string_to_136_array(
        sou: str | None = None,
        pin: str | None = None,
        man: str | None = None,
        honors: str | None = None,
        has_aka_dora: bool = False,
    ) -> list[int]:
        """
        Method to convert one line string tiles format to the 136 array.
        You can pass r or 0 instead of 5 for it to become a red five from
        that suit. To prevent old usage without red,
        has_aka_dora has to be True for this to do that.
        We need it to increase readability of our tests
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
        Method to convert one line string tiles format to the 34 array
        We need it to increase readability of our tests
        """
        results = TilesConverter.string_to_136_array(sou, pin, man, honors)
        return TilesConverter.to_34_array(results)

    @staticmethod
    def find_34_tile_in_136_array(tile34: int | None, tiles: Collection[int]) -> int | None:
        """
        Our shanten calculator will operate with 34 tiles format,
        after calculations we need to find calculated 34 tile
        in player's 136 tiles.

        For example we had 0 tile from 34 array
        in 136 array it can be present as 0, 1, 2, 3
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
        Method to convert one line string tiles format to the 136 array, like
        "123s456p789m11222z". 's' stands for sou, 'p' stands for pin,
        'm' stands for man and 'z' or 'h' stands for honor.
        You can pass r or 0 instead of 5 for it to become a red five from
        that suit. To prevent old usage without red,
        has_aka_dora has to be True for this to do that.
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
        Method to convert one line string tiles format to the 34 array, like
        "123s456p789m11222z". 's' stands for sou, 'p' stands for pin,
        'm' stands for man and 'z' or 'h' stands for honor.
        You can pass r or 0 instead of 5 for it to become a red five from
        that suit. To prevent old usage without red,
        has_aka_dora has to be True for this to do that.
        """
        results = TilesConverter.one_line_string_to_136_array(string, has_aka_dora)
        return TilesConverter.to_34_array(results)
