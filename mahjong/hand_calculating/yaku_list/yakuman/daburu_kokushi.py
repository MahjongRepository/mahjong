# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class DaburuKokushiMusou(Yaku):

    def set_attributes(self):
        self.yaku_id = 48
        self.name = 'Daburu Kokushi Musou'

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
