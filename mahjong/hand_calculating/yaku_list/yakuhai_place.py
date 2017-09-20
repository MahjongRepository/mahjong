# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class YakuhaiOfPlace(Yaku):

    def set_attributes(self):
        self.yaku_id = 10
        self.name = 'Yakuhai (wind of place)'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return True
