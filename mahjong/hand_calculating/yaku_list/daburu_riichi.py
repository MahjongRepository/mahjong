# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class DaburuRiichi(Yaku):
    """
    Yaku situation
    """

    def set_attributes(self):
        self.yaku_id = 21
        self.name = 'Double Riichi'

        self.han_open = None
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
