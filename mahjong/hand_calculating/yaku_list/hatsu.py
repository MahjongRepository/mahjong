# -*- coding: utf-8 -*-
from mahjong.constants import HATSU
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon


class Hatsu(Yaku):
    """
    Pon of green dragons
    """

    def __init__(self, yaku_id=None):
        super(Hatsu, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 19

        self.name = 'Yakuhai (hatsu)'
        self.english = 'Green Dragon'
        self.japanese = '役牌(發)'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return len([x for x in hand if is_pon(x) and x[0] == HATSU]) == 1
