# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class NagashiMangan(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id=None):
        super(NagashiMangan, self).__init__(yaku_id)

    def set_attributes(self):
        self.name = 'Nagashi Mangan'
        self.english = 'Nagashi Mangan'
        self.japanese = '流し満貫'

        self.han_open = 5
        self.han_closed = 5

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
