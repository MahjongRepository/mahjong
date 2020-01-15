# -*- coding: utf-8 -*-
from functools import reduce

from mahjong.constants import HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Tsuuiisou(Yaku):
    """
    Hand composed entirely of honour tiles
    """

    def __init__(self, yaku_id=None):
        super(Tsuuiisou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 42

        self.name = 'Tsuu iisou'
        self.english = 'All Honors'
        self.japanese = '字一色'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        """
        Hand composed entirely of honour tiles.
        :param hand: list of hand's sets
        :return: boolean
        """
        indices = reduce(lambda z, y: z + y, hand)
        return all(x in HONOR_INDICES for x in indices)
