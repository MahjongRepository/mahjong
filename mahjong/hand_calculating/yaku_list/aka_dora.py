# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class AkaDora(Yaku):
    """
    Red five
    """

    def __init__(self, yaku_id=None):
        super(AkaDora, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 54

        self.name = 'Aka Dora'
        self.english = 'Red Five'
        self.japanese = '赤ドラ'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return True

    def __str__(self):
        return 'Aka Dora {}'.format(self.han_closed)
