# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Renhou(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id=None):
        super(Renhou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 36

        self.name = 'Renhou'
        self.english = 'Hand Of Man'
        self.japanese = '人和'

        self.han_open = None
        self.han_closed = 5

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
