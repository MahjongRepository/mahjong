# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Ippatsu(Yaku):
    """
    Yaku situation
    """

    def set_attributes(self):
        self.yaku_id = 2
        self.name = 'Ippatsu'

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
