# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Chiitoitsu(Yaku):
    """
    Hand contains only pairs
    """

    def set_attributes(self):
        self.yaku_id = 22
        self.name = 'Chiitoitsu'

        self.han_open = None
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return len(hand) == 7
