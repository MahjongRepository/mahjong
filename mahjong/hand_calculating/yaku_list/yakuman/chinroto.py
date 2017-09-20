# -*- coding: utf-8 -*-
from functools import reduce

from mahjong.constants import TERMINAL_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Chinroutou(Yaku):

    def set_attributes(self):
        self.yaku_id = 44
        self.name = 'Chinroutou'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        """
        Hand composed entirely of terminal tiles.
        :param hand: list of hand's sets
        :return: boolean
        """
        indices = reduce(lambda z, y: z + y, hand)
        return all(x in TERMINAL_INDICES for x in indices)
