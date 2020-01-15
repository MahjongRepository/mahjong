# -*- coding: utf-8 -*-
from functools import reduce

from mahjong.constants import TERMINAL_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Chinroutou(Yaku):

    def __init__(self, yaku_id=None):
        super(Chinroutou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 44

        self.name = 'Chinroutou'
        self.english = 'All Terminals'
        self.japanese = '清老頭'

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
