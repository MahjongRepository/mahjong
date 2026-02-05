from collections.abc import Collection, Sequence

from mahjong.constants import DRAGONS
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pair, is_pon_or_kan


class Shosangen(Yaku):
    """
    Hand with two dragon pon sets and one dragon pair
    """

    yaku_id = 35
    name = "Shou Sangen"
    han_open = 2
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        count_of_conditions = 0
        for item in hand:
            if item[0] not in DRAGONS:
                continue

            if is_pair(item) or is_pon_or_kan(item):
                count_of_conditions += 1

        return count_of_conditions == 3
