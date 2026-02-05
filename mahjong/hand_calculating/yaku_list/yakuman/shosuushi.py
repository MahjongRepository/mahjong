from collections.abc import Collection, Sequence

from mahjong.constants import WINDS
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pair, is_pon_or_kan


class Shousuushii(Yaku):
    """
    The hand contains three sets of winds and a pair of the remaining wind
    """

    yaku_id = 104
    name = "Shousuushii"
    han_open = 13
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        count_of_wind_sets = 0
        wind_pair = 0

        for item in hand:
            first = item[0]
            if first not in WINDS:
                continue

            if is_pair(item):
                wind_pair += 1
            elif is_pon_or_kan(item):
                count_of_wind_sets += 1

        return count_of_wind_sets == 3 and wind_pair == 1
