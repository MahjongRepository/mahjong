# -*- coding: utf-8 -*-
from mahjong.constants import CHUN
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon


class Chun(Yaku):
    """
    Pon of red dragons
    """

    def set_attributes(self):
        self.yaku_id = 20
        self.name = 'Yakuhai (chun)'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        return len([x for x in hand if is_pon(x) and x[0] == CHUN]) == 1
