from typing import List

from mahjong.constants import CHUN, EAST, FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU, TERMINAL_INDICES


def is_aka_dora(tile_136: int, aka_enabled: bool) -> bool:
    """
    Check if tile is aka dora
    """
    if not aka_enabled:
        return False

    if tile_136 in [FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU]:
        return True

    return False


def plus_dora(tile_136: int, dora_indicators_136: List[int], add_aka_dora: bool = False) -> int:
    """
    Calculate the number of dora for the tile
    """
    tile_index = tile_136 // 4
    dora_count = 0

    if add_aka_dora and is_aka_dora(tile_136, aka_enabled=True):
        dora_count += 1

    for dora in dora_indicators_136:
        dora //= 4

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


def is_chi(item):
    """
    :param item: array of tile 34 indices
    :return: boolean
    """
    if len(item) != 3:
        return False

    return item[0] == item[1] - 1 == item[2] - 2


def is_pon(item):
    """
    :param item: array of tile 34 indices
    :return: boolean
    """
    if len(item) != 3:
        return False

    return item[0] == item[1] == item[2]


def is_kan(item: List[int]) -> bool:
    return len(item) == 4


def is_pon_or_kan(item: List[int]) -> bool:
    return is_pon(item) or is_kan(item)


def is_pair(item):
    """
    :param item: array of tile 34 indices
    :return: boolean
    """
    return len(item) == 2


def is_man(tile):
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return tile <= 8


def is_pin(tile):
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return 8 < tile <= 17


def is_sou(tile):
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return 17 < tile <= 26


def is_honor(tile):
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return tile >= 27


def is_sangenpai(tile_34: int) -> bool:
    return tile_34 >= 31


def is_terminal(tile):
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return tile in TERMINAL_INDICES


def is_dora_indicator_for_terminal(tile):
    """
    :param tile: 34 tile format
    :return: boolean
    """
    return tile == 7 or tile == 8 or tile == 16 or tile == 17 or tile == 25 or tile == 26


def contains_terminals(hand_set):
    """
    :param hand_set: array of 34 tiles
    :return: boolean
    """
    return any([x in TERMINAL_INDICES for x in hand_set])


def simplify(tile):
    """
    :param tile: 34 tile format
    :return: tile: 0-8 presentation
    """
    return tile - 9 * (tile // 9)


def find_isolated_tile_indices(hand_34):
    """
    Tiles that don't have -1, 0 and +1 neighbors
    :param hand_34: array of tiles in 34 tile format
    :return: array of isolated tiles indices
    """
    isolated_indices = []

    for x in range(0, CHUN + 1):
        # for honor tiles we don't need to check nearby tiles
        if is_honor(x) and hand_34[x] == 0:
            isolated_indices.append(x)
        else:
            simplified = simplify(x)

            # 1 suit tile
            if simplified == 0:
                if hand_34[x] == 0 and hand_34[x + 1] == 0:
                    isolated_indices.append(x)
            # 9 suit tile
            elif simplified == 8:
                if hand_34[x] == 0 and hand_34[x - 1] == 0:
                    isolated_indices.append(x)
            # 2-8 tiles tiles
            else:
                if hand_34[x] == 0 and hand_34[x - 1] == 0 and hand_34[x + 1] == 0:
                    isolated_indices.append(x)

    return isolated_indices


def is_tile_strictly_isolated(hand_34, tile_34):
    """
    Tile is strictly isolated if it doesn't have -2, -1, 0, +1, +2 neighbors
    :param hand_34: array of tiles in 34 tile format
    :param tile_34: int
    :return: bool
    """

    if is_honor(tile_34):
        return hand_34[tile_34] - 1 <= 0

    simplified = simplify(tile_34)

    # 1 suit tile
    if simplified == 0:
        indices = [tile_34, tile_34 + 1, tile_34 + 2]
    # 2 suit tile
    elif simplified == 1:
        indices = [tile_34 - 1, tile_34, tile_34 + 1, tile_34 + 2]
    # 8 suit tile
    elif simplified == 7:
        indices = [tile_34 - 2, tile_34 - 1, tile_34, tile_34 + 1]
    # 9 suit tile
    elif simplified == 8:
        indices = [tile_34 - 2, tile_34 - 1, tile_34]
    # 3-7 tiles tiles
    else:
        indices = [tile_34 - 2, tile_34 - 1, tile_34, tile_34 + 1, tile_34 + 2]

    isolated = True
    for tile_index in indices:
        # we don't want to count our tile as it is in hand already
        if tile_index == tile_34:
            isolated &= hand_34[tile_index] - 1 <= 0
        else:
            isolated &= hand_34[tile_index] == 0

    return isolated


def count_tiles_by_suits(tiles_34):
    """
    Separate tiles by suits and count them
    :param tiles_34: array of tiles to count
    :return: dict
    """
    suits = [
        {"count": 0, "name": "sou", "function": is_sou},
        {"count": 0, "name": "man", "function": is_man},
        {"count": 0, "name": "pin", "function": is_pin},
        {"count": 0, "name": "honor", "function": is_honor},
    ]

    for x in range(0, 34):
        tile = tiles_34[x]
        if not tile:
            continue

        for item in suits:
            if item["function"](x):
                item["count"] += tile

    return suits
