from mahjong.constants import EAST, NORTH, SOUTH, WEST
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pair, is_pon_or_kan


class Shousuushii(Yaku):
    """
    The hand contains three sets of winds and a pair of the remaining wind
    """

    def __init__(self, yaku_id=None):
        super(Shousuushii, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 50

        self.name = "Shousuushii"

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        pon_sets = [x for x in hand if is_pon_or_kan(x)]
        if len(pon_sets) < 3:
            return False

        count_of_wind_sets = 0
        wind_pair = 0
        winds = [EAST, SOUTH, WEST, NORTH]
        for item in hand:
            if is_pon_or_kan(item) and item[0] in winds:
                count_of_wind_sets += 1

            if is_pair(item) and item[0] in winds:
                wind_pair += 1

        return count_of_wind_sets == 3 and wind_pair == 1
