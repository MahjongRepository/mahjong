# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Pinfu(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id=None):
        super(Pinfu, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 7

        self.name = 'Pinfu'
        self.english = 'All Sequences'
        self.japanese = '平和'

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return True
