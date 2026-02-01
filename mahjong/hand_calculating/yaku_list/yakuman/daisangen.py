from collections.abc import Collection, Sequence

from mahjong.constants import DRAGONS
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class Daisangen(Yaku):
    """
    The hand contains three sets of dragons
    """

    yaku_id = 103
    name = "Daisangen"
    han_open = 13
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        count_of_dragon_pon_sets = 0
        for item in hand:
            if is_pon_or_kan(item) and item[0] in DRAGONS:
                count_of_dragon_pon_sets += 1
        return count_of_dragon_pon_sets == 3
