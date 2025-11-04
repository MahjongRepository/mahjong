from collections.abc import Collection, Sequence
from typing import Any, Optional

from mahjong.constants import FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU


class Tile:
    value = None
    is_tsumogiri = None

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

        pin = [t for t in tiles if 36 <= t < 72]
        pin = [t - 36 for t in pin]

        sou = [t for t in tiles if 72 <= t < 108]
        sou = [t - 72 for t in sou]

        honors = [t for t in tiles if t >= 108]
        honors = [t - 108 for t in honors]

        def words(suits: list[int], red_five: int, suffix: str) -> str:
            return (
                suits
                and "".join(["0" if i == red_five and print_aka_dora else str((i // 4) + 1) for i in suits]) + suffix
                or ""
            )

        sou = words(sou, FIVE_RED_SOU - 72, "s")  # type: ignore
        pin = words(pin, FIVE_RED_PIN - 36, "p")  # type: ignore
        man = words(man, FIVE_RED_MAN, "m")  # type: ignore
        honors = words(honors, -1 - 108, "z")  # type: ignore

        return man + pin + sou + honors  # type: ignore

    @staticmethod
    def to_34_array(tiles: Collection[int]) -> list[int]:
        """
        Convert 136 array to the 34 tiles array
        """
        results = [0] * 34
        for tile in tiles:
            tile //= 4
            results[tile] += 1
        return results

    @staticmethod
    def to_136_array(tiles: Sequence[int]) -> list[int]:
        """
        Convert 34 array to the 136 tiles array
        """
        results: list[int] = []
        for index, count in enumerate(tiles):
            base_id = index * 4
            for i in range(count):
                results.append(base_id + i)
        return results

    @staticmethod
    def string_to_136_array(
        sou: Optional[str] = None,
        pin: Optional[str] = None,
        man: Optional[str] = None,
        honors: Optional[str] = None,
        has_aka_dora: bool = False,
    ) -> list[int]:
        """
        Method to convert one line string tiles format to the 136 array.
        You can pass r or 0 instead of 5 for it to become a red five from
        that suit. To prevent old usage without red,
        has_aka_dora has to be True for this to do that.
        We need it to increase readability of our tests
        """

        def _split_string(string: Optional[str], offset: int, red: Optional[int] = None) -> list[int]:
            data = []
            temp = []

            if not string:
                return []

            for i in string:
                if (i == "r" or i == "0") and has_aka_dora:
                    assert red is not None
                    temp.append(red)
                    data.append(red)
                else:
                    tile = offset + (int(i) - 1) * 4
                    if tile == red and has_aka_dora:
                        # prevent non reds to become red
                        tile += 1
                    if tile in data:
                        count_of_tiles = len([x for x in temp if x == tile])
                        new_tile = tile + count_of_tiles
                        data.append(new_tile)

                        temp.append(tile)
                    else:
                        data.append(tile)
                        temp.append(tile)

            return data

        results = _split_string(man, 0, FIVE_RED_MAN)
        results += _split_string(pin, 36, FIVE_RED_PIN)
        results += _split_string(sou, 72, FIVE_RED_SOU)
        results += _split_string(honors, 108)

        return results

    @staticmethod
    def string_to_34_array(
        sou: Optional[str] = None,
        pin: Optional[str] = None,
        man: Optional[str] = None,
        honors: Optional[str] = None,
    ) -> list[int]:
        """
        Method to convert one line string tiles format to the 34 array
        We need it to increase readability of our tests
        """
        results = TilesConverter.string_to_136_array(sou, pin, man, honors)
        results = TilesConverter.to_34_array(results)
        return results

    @staticmethod
    def find_34_tile_in_136_array(tile34: Optional[int], tiles: Collection[int]) -> Optional[int]:
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
            if i == "z" or i == "h":
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
        results = TilesConverter.to_34_array(results)
        return results
