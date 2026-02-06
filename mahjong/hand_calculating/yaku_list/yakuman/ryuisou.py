from collections.abc import Collection, Sequence

from mahjong.constants import HATSU
from mahjong.hand_calculating.yaku import Yaku

# green tiles: 2, 3, 4, 6, 8 of sou (indices 19, 20, 21, 23, 25) and green dragon (hatsu)
_GREEN_INDICES = frozenset([19, 20, 21, 23, 25, HATSU])


class Ryuuiisou(Yaku):
    """
    Hand composed entirely of green tiles. Green tiles are: green dragons and 2, 3, 4, 6 and 8 of sou.
    """

    yaku_id = 105
    name = "Ryuuiisou"
    han_open = 13
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return all(tile in _GREEN_INDICES for item in hand for tile in item)
