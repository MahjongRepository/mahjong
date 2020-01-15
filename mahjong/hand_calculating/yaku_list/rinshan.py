# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Rinshan(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id=None):
        super(Rinshan, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 4

        self.name = 'Rinshan Kaihou'
        self.english = 'Dead Wall Draw'
        self.japanese = '嶺上開花'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
