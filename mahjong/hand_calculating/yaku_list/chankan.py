# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Chankan(Yaku):
    """
    Yaku situation
    """

    def set_attributes(self):
        self.yaku_id = 3
        self.name = 'Chankan'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
