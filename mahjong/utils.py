from mahjong.constants import EAST, FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU, HONOR_INDICES, TERMINAL_INDICES


def is_aka_dora(tile):
    """
    :param tile: int 136 tiles format
    :return: boolean
    """

    if tile in [FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU]:
        return True

    return False


def plus_dora(tile, dora_indicators, count_aka_dora=True):
    """
    :param tile: int 136 tiles format
    :param dora_indicators: array of 136 tiles format
    :return: int count of dora
    """
    tile_index = tile // 4
    dora_count = 0

    if count_aka_dora and is_aka_dora(tile):
        dora_count += 1

    for dora in dora_indicators:
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
    :param hand_34: array of tiles in 34 tile format
    :return: array of isolated tiles indices
    """
    isolated_indices = []
    for x in range(1, 27):
        # TODO handle 1-9 tiles situation to have more isolated tiles
        if hand_34[x] == 0 and hand_34[x - 1] == 0 and hand_34[x + 1] == 0:
            isolated_indices.append(x)

    # for honor tiles we don't need to check nearby tiles
    for x in HONOR_INDICES:
        if hand_34[x] == 0:
            isolated_indices.append(x)

    return isolated_indices


def count_tiles_by_suits(tiles_34):
    """
    Separate tiles by suits and count them
    :param tiles_34: array of tiles to count
    :return: dict
    """
    suits = [
        {'count': 0, 'name': 'sou',   'function': is_sou},
        {'count': 0, 'name': 'man',   'function': is_man},
        {'count': 0, 'name': 'pin',   'function': is_pin},
        {'count': 0, 'name': 'honor', 'function': is_honor}
    ]

    for x in range(0, 34):
        tile = tiles_34[x]
        if not tile:
            continue

        for item in suits:
            if item['function'](x):
                item['count'] += tile

    return suits
