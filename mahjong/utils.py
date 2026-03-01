"""
Utility functions for tile classification, dora counting, and hand structure analysis.

.. rubric:: Tile classification

Functions that identify suit membership and tile properties, all operating on the 34-format
tile index:

* :func:`is_man`, :func:`is_pin`, :func:`is_sou`, :func:`is_honor` - suit membership checks
* :func:`is_terminal` - whether a tile is a terminal (1 or 9 of any suit)
* :func:`is_dora_indicator_for_terminal` - whether a tile is a dora indicator that points to a terminal
* :func:`is_sangenpai` - whether a tile is a dragon (haku, hatsu, or chun)
* :func:`simplify` - reduce a tile index to its rank (0-8) within its suit

.. rubric:: Dora counting

Functions for calculating dora (bonus tiles) in a hand:

* :func:`is_aka_dora` - check if a specific 136-format tile is a red five
* :func:`plus_dora` - count dora for a single tile given dora indicators
* :func:`build_dora_count_map` - precompute a mapping from tile type to dora count
* :func:`count_dora_for_hand` - total dora in a hand using a precomputed map

.. rubric:: Hand structure analysis

Functions that inspect sets (melds) within a hand decomposition:

* :func:`is_chi`, :func:`is_pon`, :func:`is_kan`, :func:`is_pair` - classify a set by type
* :func:`is_pon_or_kan` - check for triplet or quad
* :func:`has_pon_or_kan_of` - search for a triplet/quad of a specific tile
* :func:`classify_hand_suits` - bitmask summary of suits present in the hand
* :func:`contains_terminals` - whether a set includes terminal tiles
* :func:`find_isolated_tile_indices` - find tiles with no adjacent neighbors
* :func:`is_tile_strictly_isolated` - strict isolation check (no +-2 neighbors)
* :func:`count_tiles_by_suits` - count tiles per suit
"""

from collections.abc import Callable, Collection, Sequence
from typing import TypedDict

from mahjong.constants import AKA_DORAS, EAST, HAKU, NORTH, TERMINAL_INDICES


def is_aka_dora(tile_136: int, aka_enabled: bool) -> bool:
    """
    Check if a tile is an aka dora (red five).

    >>> from mahjong.utils import is_aka_dora
    >>> is_aka_dora(16, aka_enabled=True)
    True

    >>> is_aka_dora(16, aka_enabled=False)
    False

    :param tile_136: tile index in 136-format
    :param aka_enabled: whether aka dora rules are active
    :return: True if the tile is a red five and aka dora is enabled
    """
    if not aka_enabled:
        return False

    return tile_136 in AKA_DORAS


def plus_dora(tile_136: int, dora_indicators_136: Collection[int], add_aka_dora: bool = False) -> int:
    """
    Calculate the number of dora for a single tile given dora indicators.

    Each dora indicator reveals which tile type is dora (the next tile in sequence).
    If the tile matches, the count increments once per matching indicator.
    Optionally includes aka dora (red five) as an additional bonus.

    Indicator 0 (1m) points to 2m as dora, so tile 4 (2m) scores one dora:

    >>> from mahjong.utils import plus_dora
    >>> plus_dora(4, [0])
    1

    Two indicators each pointing to 2m as dora:

    >>> plus_dora(4, [0, 1])
    2

    :param tile_136: tile index in 136-format
    :param dora_indicators_136: collection of dora indicator tile indices in 136-format
    :param add_aka_dora: include aka dora (red five) bonus in the count
    :return: total dora count for this tile
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
    """Convert a dora indicator (34-format) to the actual dora tile (34-format)."""
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
    Build a mapping from tile type (34-format) to dora count for the given indicators.

    Indicator 0 (first copy of 1m) points to dora 2m (index 1):

    >>> from mahjong.utils import build_dora_count_map
    >>> build_dora_count_map([0])
    {1: 1}

    Two indicators each pointing to the same dora:

    >>> build_dora_count_map([0, 1])
    {1: 2}

    :param dora_indicators_136: collection of dora indicator tile indices in 136-format
    :return: dictionary mapping 34-format tile index to dora count
    """
    dora_map: dict[int, int] = {}
    for indicator in dora_indicators_136:
        dora_34 = _indicator_to_dora_34(indicator // 4)
        dora_map[dora_34] = dora_map.get(dora_34, 0) + 1
    return dora_map


def count_dora_for_hand(tiles_34: Sequence[int], dora_count_map: dict[int, int]) -> int:
    """
    Count total dora in a hand using a precomputed dora count map.

    Three copies of 2m with one dora indicator pointing to 2m:

    >>> from mahjong.utils import count_dora_for_hand, build_dora_count_map
    >>> tiles_34 = [0] * 34
    >>> tiles_34[1] = 3
    >>> dora_map = build_dora_count_map([0])
    >>> count_dora_for_hand(tiles_34, dora_map)
    3

    :param tiles_34: hand in 34-format tile count array
    :param dora_count_map: mapping from 34-format tile index to dora count
    :return: total dora count for the hand
    """
    total = 0
    for tile_34, dora_count in dora_count_map.items():
        total += tiles_34[tile_34] * dora_count
    return total


def is_chi(item: Sequence[int]) -> bool:
    """
    Check if a set of tiles forms a chi (sequence of three consecutive tiles).

    The indices must be in ascending order.

    >>> from mahjong.utils import is_chi
    >>> is_chi([0, 1, 2])
    True

    >>> is_chi([0, 0, 0])
    False

    >>> is_chi([2, 1, 0])
    False

    :param item: array of tile indices in 34-format
    :return: True if the tiles form a chi
    """
    if len(item) != 3:
        return False
    return item[0] + 1 == item[1] and item[1] + 1 == item[2]


def is_pon(item: Sequence[int]) -> bool:
    """
    Check if a set of tiles forms a pon (triplet of identical tiles).

    >>> from mahjong.utils import is_pon
    >>> is_pon([0, 0, 0])
    True

    >>> is_pon([0, 1, 2])
    False

    :param item: array of tile indices in 34-format
    :return: True if the tiles form a pon
    """
    if len(item) != 3:
        return False
    return item[0] == item[1] == item[2]


def is_kan(item: Sequence[int]) -> bool:
    """
    Check if a set of tiles forms a kan (quad of identical tiles).

    >>> from mahjong.utils import is_kan
    >>> is_kan([0, 0, 0, 0])
    True

    >>> is_kan([0, 0, 0])
    False

    :param item: array of tile indices in 34-format
    :return: True if the tiles form a kan
    """
    return len(item) == 4


def is_pon_or_kan(item: Sequence[int]) -> bool:
    """
    Check if a set of tiles forms a pon (triplet) or a kan (quad).

    >>> from mahjong.utils import is_pon_or_kan
    >>> is_pon_or_kan([0, 0, 0])
    True

    >>> is_pon_or_kan([0, 0, 0, 0])
    True

    >>> is_pon_or_kan([0, 1, 2])
    False

    :param item: array of tile indices in 34-format
    :return: True if the tiles form a pon or kan
    """
    length = len(item)
    if length == 4:
        return True
    if length == 3:
        return item[0] == item[1] == item[2]
    return False


def is_pair(item: Sequence[int]) -> bool:
    """
    Check if a set of tiles forms a pair (two tiles).

    >>> from mahjong.utils import is_pair
    >>> is_pair([0, 0])
    True

    >>> is_pair([0, 0, 0])
    False

    :param item: array of tile indices in 34-format
    :return: True if the tiles form a pair
    """
    return len(item) == 2


def has_pon_or_kan_of(hand: Collection[Sequence[int]], tile: int) -> bool:
    """
    Check if hand contains a pon or kan of the specified tile.

    >>> from mahjong.utils import has_pon_or_kan_of
    >>> has_pon_or_kan_of([[0, 0, 0], [1, 2, 3]], 0)
    True

    >>> has_pon_or_kan_of([[0, 1, 2], [3, 3, 3]], 0)
    False

    :param hand: collection of tile sets, each a sequence of tile indices in 34-format
    :param tile: tile index in 34-format to search for
    :return: True if the hand contains a pon or kan of the given tile
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
    Classify the tile sets in a hand by suit, returning a bitmask and honor count.

    The bitmask bits are: ``1`` for sou, ``2`` for pin, ``4`` for man.

    >>> from mahjong.utils import classify_hand_suits
    >>> classify_hand_suits([[0, 1, 2], [27, 27, 27]])
    (4, 1)

    :param hand: collection of tile sets, each a sequence of tile indices in 34-format
    :return: tuple of (suit_mask, honor_count)
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
    Check if a tile belongs to the man (characters) suit.

    >>> from mahjong.utils import is_man
    >>> is_man(0)
    True

    >>> is_man(9)
    False

    :param tile: tile index in 34-format
    :return: True if the tile is a man tile (indices 0-8)
    """
    return tile <= 8


def is_pin(tile: int) -> bool:
    """
    Check if a tile belongs to the pin (circles) suit.

    >>> from mahjong.utils import is_pin
    >>> is_pin(9)
    True

    >>> is_pin(0)
    False

    :param tile: tile index in 34-format
    :return: True if the tile is a pin tile (indices 9-17)
    """
    return 8 < tile <= 17


def is_sou(tile: int) -> bool:
    """
    Check if a tile belongs to the sou (bamboo) suit.

    >>> from mahjong.utils import is_sou
    >>> is_sou(18)
    True

    >>> is_sou(0)
    False

    :param tile: tile index in 34-format
    :return: True if the tile is a sou tile (indices 18-26)
    """
    return 17 < tile <= 26


def is_honor(tile: int) -> bool:
    """
    Check if a tile is an honor tile (wind or dragon).

    >>> from mahjong.utils import is_honor
    >>> is_honor(27)
    True

    >>> is_honor(26)
    False

    :param tile: tile index in 34-format
    :return: True if the tile is an honor tile (indices 27-33)
    """
    return tile >= 27


def is_sangenpai(tile_34: int) -> bool:
    """
    Check if a tile is a dragon (sangenpai: haku, hatsu, or chun).

    >>> from mahjong.utils import is_sangenpai
    >>> is_sangenpai(31)
    True

    >>> is_sangenpai(27)
    False

    :param tile_34: tile index in 34-format
    :return: True if the tile is a dragon (indices 31-33)
    """
    return tile_34 >= 31


def is_terminal(tile: int) -> bool:
    """
    Check if a tile is a terminal (1 or 9 of any suited tile).

    >>> from mahjong.utils import is_terminal
    >>> is_terminal(0)
    True

    >>> is_terminal(8)
    True

    >>> is_terminal(1)
    False

    :param tile: tile index in 34-format
    :return: True if the tile is a terminal
    """
    return tile in TERMINAL_INDICES


def is_dora_indicator_for_terminal(tile: int) -> bool:
    """
    Check if a tile is a dora indicator that points to a terminal.

    The tiles with ranks 8 and 9 in each suit (indices 7, 8, 16, 17, 25, 26) are
    dora indicators for terminals: a rank-9 indicator wraps around to make rank 1 the dora,
    and a rank-8 indicator points to rank 9 as the dora.

    >>> from mahjong.utils import is_dora_indicator_for_terminal
    >>> is_dora_indicator_for_terminal(7)
    True

    >>> is_dora_indicator_for_terminal(0)
    False

    :param tile: tile index in 34-format
    :return: True if the tile is a dora indicator for a terminal
    """
    return tile in {7, 8, 16, 17, 25, 26}


def contains_terminals(hand_set: Collection[int]) -> bool:
    """
    Check if a set of tiles contains any terminal tiles.

    >>> from mahjong.utils import contains_terminals
    >>> contains_terminals([0, 1, 2])
    True

    >>> contains_terminals([1, 2, 3])
    False

    :param hand_set: collection of tile indices in 34-format
    :return: True if any tile in the set is a terminal
    """
    return any(x in TERMINAL_INDICES for x in hand_set)


def simplify(tile: int) -> int:
    """
    Reduce a tile index to its rank within its suit (0-8).

    >>> from mahjong.utils import simplify
    >>> simplify(0)
    0

    >>> simplify(9)
    0

    >>> simplify(20)
    2

    :param tile: tile index in 34-format
    :return: rank within the suit (0-8)
    """
    return tile % 9


def find_isolated_tile_indices(hand_34: Sequence[int]) -> list[int]:
    """
    Find tiles that are isolated (absent from the hand with no adjacent neighbors).

    A suited tile is isolated if neither the tile itself, its left neighbor (-1),
    nor its right neighbor (+1) is present in the hand.
    Honor tiles are isolated if they are simply not present.

    >>> from mahjong.utils import find_isolated_tile_indices
    >>> hand_34 = [4, 0, 0, 0, 0, 0, 0, 0, 0] + [0] * 25
    >>> 1 not in find_isolated_tile_indices(hand_34)
    True

    >>> 2 in find_isolated_tile_indices(hand_34)
    True

    :param hand_34: hand in 34-format tile count array
    :return: list of 34-format tile indices that are isolated
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
    Check if a tile is strictly isolated (no tiles within ±2 distance).

    A tile is strictly isolated if no copies (beyond the one being checked)
    and no neighbors at distances -2, -1, +1, +2 exist in the hand.
    Honor tiles only need to check for duplicates.

    >>> from mahjong.utils import is_tile_strictly_isolated
    >>> hand_34 = [1, 0, 0, 0, 0, 0, 0, 0, 0] + [0] * 25
    >>> is_tile_strictly_isolated(hand_34, 0)
    True

    >>> hand_34[2] = 1
    >>> is_tile_strictly_isolated(hand_34, 0)
    False

    :param hand_34: hand in 34-format tile count array
    :param tile_34: tile index in 34-format to check
    :return: True if the tile is strictly isolated
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
    """
    Per-suit tile count entry returned by :func:`count_tiles_by_suits`.

    :param count: number of tiles in this suit
    :param name: suit name (``"sou"``, ``"man"``, ``"pin"``, or ``"honor"``)
    :param function: predicate that tests whether a 34-format tile index belongs to this suit
    """

    count: int
    name: str
    function: Callable[[int], bool]


def count_tiles_by_suits(tiles_34: Sequence[int]) -> list[SuitCount]:
    """
    Separate tiles by suit and count them.

    >>> from mahjong.utils import count_tiles_by_suits
    >>> tiles_34 = [0] * 34
    >>> tiles_34[0] = 3
    >>> tiles_34[27] = 2
    >>> result = count_tiles_by_suits(tiles_34)
    >>> [(s["name"], s["count"]) for s in result]
    [('sou', 0), ('man', 3), ('pin', 0), ('honor', 2)]

    :param tiles_34: hand in 34-format tile count array
    :return: list of :class:`SuitCount` entries, one per suit
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
