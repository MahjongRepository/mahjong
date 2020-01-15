# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class SuuankouTanki(Yaku):

    def __init__(self, yaku_id=None):
        super(SuuankouTanki, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 40

        self.name = 'Suu ankou tanki'
        self.english = 'Four Concealed Triplets Single Wait'
        self.japanese = '四暗刻単騎待ち'

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        return True
