from functools import reduce

from mahjong.constants import HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Daichisei(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id):
        super(Daichisei, self).__init__(yaku_id)

    def set_attributes(self):
        self.name = "Daichisei"

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        indices = reduce(lambda z, y: z + y, hand)
        return all(x in HONOR_INDICES for x in indices) and len(hand) == 7
