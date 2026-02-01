from collections.abc import Collection, Sequence

from mahjong.constants import EAST, NORTH, SOUTH, WEST
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
        """
        The hand contains four sets of winds
        :param hand: list of hand's sets
        :return: boolean
        """
        pon_sets = [x for x in hand if is_pon_or_kan(x)]
        if len(pon_sets) != 4:
            return False

        count_wind_sets = 0
        winds = [EAST, SOUTH, WEST, NORTH]
        for item in pon_sets:
            if is_pon_or_kan(item) and item[0] in winds:
                count_wind_sets += 1

        return count_wind_sets == 4
