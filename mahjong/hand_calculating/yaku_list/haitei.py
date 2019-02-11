# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Haitei(Yaku):
    """
    Yaku situation
    """
    
    def __init__(self, yaku_id):
        super(Haitei, self).__init__(yaku_id)

    def set_attributes(self):
        self.name = 'Haitei Raoyue'
        self.english = 'Win By Last Draw'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
