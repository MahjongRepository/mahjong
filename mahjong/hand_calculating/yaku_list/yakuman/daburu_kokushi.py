# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class DaburuKokushiMusou(Yaku):

    def __init__(self, yaku_id=None):
        super(DaburuKokushiMusou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 48

        self.name = 'Kokushi Musou Juusanmen Matchi'
        self.english = 'Thirteen Orphans 13-way wait'
        self.japanese = '国士無双十三面待ち'

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
