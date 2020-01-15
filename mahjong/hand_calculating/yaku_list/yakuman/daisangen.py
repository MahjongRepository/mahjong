# -*- coding: utf-8 -*-
from mahjong.constants import CHUN, HAKU, HATSU
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon


class Daisangen(Yaku):
    """
    The hand contains three sets of dragons
    """

    def __init__(self, yaku_id=None):
        super(Daisangen, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 39

        self.name = 'Daisangen'
        self.english = 'Big Three Dragons'
        self.japanese = '大三元'

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        count_of_dragon_pon_sets = 0
        for item in hand:
            if is_pon(item) and item[0] in [CHUN, HAKU, HATSU]:
                count_of_dragon_pon_sets += 1
        return count_of_dragon_pon_sets == 3
