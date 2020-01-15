# -*- coding: utf-8 -*-
from mahjong.constants import HAKU
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon


class Haku(Yaku):
    """
    Pon of white dragons
    """

    def __init__(self, yaku_id=None):
        super(Haku, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 18

        self.name = 'Yakuhai (haku)'
        self.english = 'White Dragon'
        self.japanese = '役牌(白)'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return len([x for x in hand if is_pon(x) and x[0] == HAKU]) == 1
