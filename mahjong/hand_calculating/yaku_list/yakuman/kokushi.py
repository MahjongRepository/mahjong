# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku


class KokushiMusou(Yaku):
    """
    A hand composed of one of each of the terminals and honour tiles plus
    any tile that matches anything else in the hand.
    """

    def __init__(self, yaku_id=None):
        super(KokushiMusou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 47

        self.name = 'Kokushi Musou'
        self.english = 'Thirteen Orphans'
        self.japanese = '国士無双'

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, tiles_34, *args):
        if (tiles_34[0] * tiles_34[8] * tiles_34[9] * tiles_34[17] * tiles_34[18] *
                tiles_34[26] * tiles_34[27] * tiles_34[28] * tiles_34[29] * tiles_34[30] *
                tiles_34[31] * tiles_34[32] * tiles_34[33] == 2):
            return True
