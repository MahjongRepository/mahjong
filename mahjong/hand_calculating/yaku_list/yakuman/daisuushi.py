from collections.abc import Collection, Sequence

from mahjong.constants import WINDS
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class DaiSuushii(Yaku):
    """
    The hand contains four sets of winds
    """

    yaku_id = 111
    name = "Dai Suushii"
    han_open = 26
    han_closed = 26
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        count_wind_sets = 0

        for item in hand:
            if item[0] not in WINDS:
                continue

            if is_pon_or_kan(item):
                count_wind_sets += 1

        return count_wind_sets == 4
