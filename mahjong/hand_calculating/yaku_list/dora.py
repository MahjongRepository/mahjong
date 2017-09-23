# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Dora(Yaku):

    def set_attributes(self):
        self.yaku_id = 52
        self.name = 'Dora'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return True

    def __str__(self):
        return 'Dora {}'.format(self.han_closed)
