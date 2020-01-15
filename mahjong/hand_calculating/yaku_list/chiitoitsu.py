# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class Chiitoitsu(Yaku):
    """
    Hand contains only pairs
    """

    def __init__(self, yaku_id=None):
        super(Chiitoitsu, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 22

        self.name = 'Chiitoitsu'
        self.english = 'Seven Pairs'
        self.japanese = '七対子'

        self.han_open = None
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return len(hand) == 7
