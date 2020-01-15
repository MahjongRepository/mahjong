# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Ippatsu(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id=None):
        super(Ippatsu, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 2

        self.name = 'Ippatsu'
        self.english = 'One Shot'
        self.japanese = '一発'

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
