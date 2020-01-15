# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku
from mahjong.meld import Meld


class SanKantsu(Yaku):
    """
    The hand with three kan sets
    """

    def __init__(self, yaku_id=None):
        super(SanKantsu, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 27

        self.name = 'San Kantsu'
        self.english = 'Three Kans'
        self.japanese = '三槓子'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, melds, *args):
        kan_sets = [x for x in melds if x.type == Meld.KAN or x.type == Meld.CHANKAN]
        return len(kan_sets) == 3
