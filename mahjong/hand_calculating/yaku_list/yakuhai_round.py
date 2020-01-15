# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class YakuhaiOfRound(Yaku):

    def __init__(self, yaku_id=None):
        super(YakuhaiOfRound, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 11

        self.name = 'Yakuhai (wind of round)'
        self.english = 'Value Tiles (Round)'
        self.japanese = '場風'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return True
