# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class SuuankouTanki(Yaku):

    def set_attributes(self):
        self.yaku_id = 41
        self.name = 'Suu ankou tanki'

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        return True
