from mahjong.constants import EAST, NORTH, SOUTH, WEST
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class DaiSuushii(Yaku):
    """
    The hand contains four sets of winds
    """

    def __init__(self, yaku_id=None):
        super(DaiSuushii, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 49

        self.name = "Dai Suushii"

        self.han_open = 26
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
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
