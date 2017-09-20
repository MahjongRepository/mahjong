# -*- coding: utf-8 -*-
from functools import reduce

from mahjong.constants import HATSU
from mahjong.hand_calculating.yaku import Yaku


class Ryuuiisou(Yaku):
    """
    Hand composed entirely of green tiles. Green tiles are: green dragons and 2, 3, 4, 6 and 8 of sou.
    """

    def set_attributes(self):
        self.yaku_id = 43
        self.name = 'Ryuuiisou'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        green_indices = [19, 20, 21, 23, 25, HATSU]
        indices = reduce(lambda z, y: z + y, hand)
        return all(x in green_indices for x in indices)
