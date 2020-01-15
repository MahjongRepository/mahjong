# -*- coding: utf-8 -*-
from mahjong.constants import WEST
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon


class YakuhaiWest(Yaku):
    """
    Pon of west winds
    """

    def __init__(self, yaku_id=None):
        super(YakuhaiWest, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 10

        self.name = 'Yakuhai (west)'
        self.english = 'West Round/Seat'
        self.japanese = '役牌(西)'

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand, player_wind, round_wind, *args):
        if len([x for x in hand if is_pon(x) and x[0] == player_wind]) == 1 and player_wind == WEST:
            return True

        if len([x for x in hand if is_pon(x) and x[0] == round_wind]) == 1 and round_wind == WEST:
            return True

        return False
