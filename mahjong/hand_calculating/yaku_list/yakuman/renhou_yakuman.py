# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class RenhouYakuman(Yaku):
    """
    Yaku situation
    """

    def set_attributes(self):
        self.yaku_id = 36
        self.name = 'Renhou'
        self.english = 'Hand Of Man'

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
