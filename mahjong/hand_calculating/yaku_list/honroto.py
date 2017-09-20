# -*- coding: utf-8 -*-
from functools import reduce

from mahjong.constants import HONOR_INDICES, TERMINAL_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Honroto(Yaku):
    """
    All tiles are terminals or honours
    """

    def set_attributes(self):
        self.yaku_id = 31
        self.name = 'Honroutou'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        indices = reduce(lambda z, y: z + y, hand)
        result = HONOR_INDICES + TERMINAL_INDICES
        return all(x in result for x in indices)
