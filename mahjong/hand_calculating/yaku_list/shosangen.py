# -*- coding: utf-8 -*-
from mahjong.constants import CHUN, HAKU, HATSU
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon, is_pair


class Shosangen(Yaku):
    """
    Hand with two dragon pon sets and one dragon pair
    """

    def __init__(self, yaku_id=None):
        super(Shosangen, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 30

        self.name = 'Shou Sangen'
        self.english = 'Small Three Dragons'
        self.japanese = '小三元'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        dragons = [CHUN, HAKU, HATSU]
        count_of_conditions = 0
        for item in hand:
            # dragon pon or pair
            if (is_pair(item) or is_pon(item)) and item[0] in dragons:
                count_of_conditions += 1

        return count_of_conditions == 3
