# -*- coding: utf-8 -*-
from mahjong.constants import HATSU
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon


class Hatsu(Yaku):
    """
    Pon of green dragons
    """

    def set_attributes(self):
        self.yaku_id = 19
        self.name = 'Yakuhai (hatsu)'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return len([x for x in hand if is_pon(x) and x[0] == HATSU]) == 1
