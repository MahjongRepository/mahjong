# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class DaburuChuurenPoutou(Yaku):

    def __init__(self, yaku_id=None):
        super(DaburuChuurenPoutou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 46

        self.name = 'Daburu Chuuren Poutou'
        self.english = 'Pure Nine Gates'
        self.japanese = '純正九蓮宝燈'

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
