# -*- coding: utf-8 -*-
from functools import reduce

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_sou, is_pin, is_man, simplify


class ChuurenPoutou(Yaku):
    """
    The hand contains 1-1-1-2-3-4-5-6-7-8-9-9-9 of one suit, plus any other tile of the same suit.
    """

    def __init__(self, yaku_id=None):
        super(ChuurenPoutou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 45

        self.name = 'Chuuren Poutou'
        self.english = 'Nine Gates'
        self.japanese = '九蓮宝燈'

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        sou_sets = 0
        pin_sets = 0
        man_sets = 0
        honor_sets = 0
        for item in hand:
            if is_sou(item[0]):
                sou_sets += 1
            elif is_pin(item[0]):
                pin_sets += 1
            elif is_man(item[0]):
                man_sets += 1
            else:
                honor_sets += 1

        sets = [sou_sets, pin_sets, man_sets]
        only_one_suit = len([x for x in sets if x != 0]) == 1
        if not only_one_suit or honor_sets > 0:
            return False

        indices = reduce(lambda z, y: z + y, hand)
        # cast tile indices to 0..8 representation
        indices = [simplify(x) for x in indices]

        # 1-1-1
        if len([x for x in indices if x == 0]) < 3:
            return False

        # 9-9-9
        if len([x for x in indices if x == 8]) < 3:
            return False

        # 1-2-3-4-5-6-7-8-9 and one tile to any of them
        indices.remove(0)
        indices.remove(0)
        indices.remove(8)
        indices.remove(8)
        for x in range(0, 9):
            if x in indices:
                indices.remove(x)

        if len(indices) == 1:
            return True

        return False
