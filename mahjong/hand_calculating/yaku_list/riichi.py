# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Riichi(Yaku):

    def __init__(self, yaku_id=None):
        super(Riichi, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 1

        self.name = 'Riichi'
        self.english = 'Riichi'
        self.japanese = '立直'

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return True
