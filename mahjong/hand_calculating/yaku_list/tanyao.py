# -*- coding: utf-8 -*-
from functools import reduce

from mahjong.constants import TERMINAL_INDICES, HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Tanyao(Yaku):
    """
    Hand without 1, 9, dragons and winds
    """

    def __init__(self, yaku_id=None):
        super(Tanyao, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 8

        self.name = 'Tanyao'
        self.english = 'All Simples'
        self.japanese = '断么九'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        indices = reduce(lambda z, y: z + y, hand)
        result = TERMINAL_INDICES + HONOR_INDICES
        return not any(x in result for x in indices)
