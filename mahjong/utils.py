from collections.abc import Callable, Collection, Sequence
from typing import TypedDict

from mahjong.constants import AKA_DORAS, EAST, HAKU, NORTH, TERMINAL_INDICES


def is_aka_dora(tile_136: int, aka_enabled: bool) -> bool:
    """
    Check if tile is aka dora
    """
    if not aka_enabled:
        return False

    return tile_136 in AKA_DORAS


def plus_dora(tile_136: int, dora_indicators_136: Collection[int], add_aka_dora: bool = False) -> int:
    """
    Calculate the number of dora for the tile
    """
    tile_index = tile_136 // 4
    dora_count = 0

    if add_aka_dora and is_aka_dora(tile_136, aka_enabled=True):
        dora_count += 1

    for dora_indicator in dora_indicators_136:
        dora = dora_indicator // 4

        # sou, pin, man
        if tile_index < EAST:
            # with indicator 9, dora will be 1
            if dora == 8:
                dora = -1
            elif dora == 17:
                dora = 8
            elif dora == 26:
                dora = 17

            if tile_index == dora + 1:
                dora_count += 1
        else:
            if dora < EAST:
                continue

            dora -= 9 * 3
            tile_index_temp = tile_index - 9 * 3

            # dora indicator is north
            if dora == 3:
                dora = -1

            # dora indicator is hatsu
            if dora == 6:
                dora = 3

            if tile_index_temp == dora + 1:
                dora_count += 1

    return dora_count


def _indicator_to_dora_34(indicator_34: int) -> int:
    """
    Convert a dora indicator (34-format) to the actual dora tile (34-format)
    """
    # suited tiles wrap within each suit of 9
    if indicator_34 < EAST:
        suit_base = (indicator_34 // 9) * 9
        return suit_base + (indicator_34 - suit_base + 1) % 9

    # winds (27-30) wrap within group of 4
    if indicator_34 <= NORTH:
        return EAST + (indicator_34 - EAST + 1) % 4

    # dragons (31-33) wrap within group of 3
    return HAKU + (indicator_34 - HAKU + 1) % 3


def build_dora_count_map(dora_indicators_136: Collection[int]) -> dict[int, int]:
    """
    Build a mapping from tile_34 index to dora count for the given indicators
    """
    dora_map: dict[int, int] = {}
    for indicator in dora_indicators_136:
        dora_34 = _indicator_to_dora_34(indicator // 4)
        dora_map[dora_34] = dora_map.get(dora_34, 0) + 1
    return dora_map


def count_dora_for_hand(tiles_34: Sequence[int], dora_count_map: dict[int, int]) -> int:
    """
    Count total dora in a hand using a precomputed dora count map
    """
    total = 0
    for tile_34, dora_count in dora_count_map.items():
        total += tiles_34[tile_34] * dora_count
    return total


def is_chi(item: Sequence[int]) -> bool:
    """
    :param item: array of tile 34 indices
    :return: boolean
    """
    if len(item) != 3:
        return False
    return item[0] + 1 == item[1] and item[1] + 1 == item[2]


def is_pon(item: Sequence[int]) -> bool:
    """
    :param item: array of tile 34 indices
    :return: boolean
    """
    if len(item) != 3:
        return False
    return item[0] == item[1] == item[2]


def is_kan(item: Sequence[int]) -> bool:
    return len(item) == 4


def is_pon_or_kan(item: Sequence[int]) -> bool:
    length = len(item)
    if length == 4:
        return True
    if length == 3:
        return item[0] == item[1] == item[2]
    return False


def is_pair(item: Sequence[int]) -> bool:
    """
    :param item: array of tile 34 indices
    :return: boolean
    """
    return len(item) == 2


def has_pon_or_kan_of(hand: Collection[Sequence[int]], tile: int) -> bool:
    """
    Check if hand contains a pon or kan of the specified tile
    """
    for item in hand:
        if item[0] != tile:
            continue
        length = len(item)
        if length == 4 or (length == 3 and item[1] == tile):
            return True
    return False


def classify_hand_suits(hand: Collection[Sequence[int]]) -> tuple[int, int]:
    """
    Classify hand by suits using bitmask.
    Returns (suit_mask, honor_count) where suit_mask: 1=sou, 2=pin, 4=man
    """
    suit_mask = 0
    honor_count = 0
    for item in hand:
        first = item[0]
        if first >= 27:
            honor_count += 1
        elif first >= 18:
            suit_mask |= 1
        elif first >= 9:
            suit_mask |= 2
        else:
            suit_mask |= 4
    return suit_mask, honor_count


def is_man(tile: int) -> bool:
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return tile <= 8


def is_pin(tile: int) -> bool:
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return 8 < tile <= 17


def is_sou(tile: int) -> bool:
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return 17 < tile <= 26


def is_honor(tile: int) -> bool:
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return tile >= 27


def is_sangenpai(tile_34: int) -> bool:
    return tile_34 >= 31


def is_terminal(tile: int) -> bool:
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return tile in TERMINAL_INDICES


def is_dora_indicator_for_terminal(tile: int) -> bool:
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return tile in {7, 8, 16, 17, 25, 26}


def contains_terminals(hand_set: Collection[int]) -> bool:
    """
    :param hand_set: array of 34 tiles
    :return: boolean
    """
    return any(x in TERMINAL_INDICES for x in hand_set)


def simplify(tile: int) -> int:
    """
    :param tile: 34 tile format
    :return: tile: 0-8 presentation
    """
    return tile % 9


def find_isolated_tile_indices(hand_34: Sequence[int]) -> list[int]:
    """
    Tiles that don't have -1, 0 and +1 neighbors
    :param hand_34: array of tiles in 34 tile format
    :return: array of isolated tiles indices
    """
    isolated_indices = []

    # check suited tiles (man: 0-8, pin: 9-17, sou: 18-26) in groups of 9
    for suit_start in (0, 9, 18):
        for i in range(9):
            x = suit_start + i
            if hand_34[x] != 0:
                continue
            # 1 suit tile (index 0): check only right neighbor
            if i == 0:
                if hand_34[x + 1] == 0:
                    isolated_indices.append(x)
            # 9 suit tile (index 8): check only left neighbor
            elif i == 8:
                if hand_34[x - 1] == 0:
                    isolated_indices.append(x)
            # 2-8 tiles: check both neighbors
            elif hand_34[x - 1] == 0 and hand_34[x + 1] == 0:
                isolated_indices.append(x)

    # honor tiles (27-33) - no neighbor check needed
    isolated_indices.extend(x for x in range(27, 34) if hand_34[x] == 0)

    return isolated_indices


def is_tile_strictly_isolated(hand_34: Sequence[int], tile_34: int) -> bool:
    """
    Tile is strictly isolated if it doesn't have -2, -1, 0, +1, +2 neighbors
    :param hand_34: array of tiles in 34 tile format
    :param tile_34: int
    :return: bool
    """
    # honor tiles have no neighbors to check
    if is_honor(tile_34):
        return hand_34[tile_34] <= 1

    simplified = simplify(tile_34)

    # the tile itself should have at most 1 (the one we're checking)
    if hand_34[tile_34] > 1:
        return False

    # 1 suit tile: check +1, +2
    if simplified == 0:
        return hand_34[tile_34 + 1] == 0 and hand_34[tile_34 + 2] == 0
    # 2 suit tile: check -1, +1, +2
    if simplified == 1:
        return hand_34[tile_34 - 1] == 0 and hand_34[tile_34 + 1] == 0 and hand_34[tile_34 + 2] == 0
    # 8 suit tile: check -2, -1, +1
    if simplified == 7:
        return hand_34[tile_34 - 2] == 0 and hand_34[tile_34 - 1] == 0 and hand_34[tile_34 + 1] == 0
    # 9 suit tile: check -2, -1
    if simplified == 8:
        return hand_34[tile_34 - 2] == 0 and hand_34[tile_34 - 1] == 0
    # 3-7 tiles: check -2, -1, +1, +2
    return (
        hand_34[tile_34 - 2] == 0
        and hand_34[tile_34 - 1] == 0
        and hand_34[tile_34 + 1] == 0
        and hand_34[tile_34 + 2] == 0
    )


class SuitCount(TypedDict):
    count: int
    name: str
    function: Callable[[int], bool]


def count_tiles_by_suits(tiles_34: Sequence[int]) -> list[SuitCount]:
    """
    Separate tiles by suits and count them
    :param tiles_34: array of tiles to count
    :return: list[SuitCount]
    """
    suits = [
        SuitCount(count=0, name="sou", function=is_sou),
        SuitCount(count=0, name="man", function=is_man),
        SuitCount(count=0, name="pin", function=is_pin),
        SuitCount(count=0, name="honor", function=is_honor),
    ]

    for x in range(34):
        tile = tiles_34[x]
        if not tile:
            continue

        for item in suits:
            if item["function"](x):
                item["count"] += tile

    return suits
