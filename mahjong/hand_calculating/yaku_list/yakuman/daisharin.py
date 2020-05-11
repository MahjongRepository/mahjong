# -*- coding: utf-8 -*-
from functools import reduce

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_sou, is_pin, is_man, simplify


class Daisharin(Yaku):
    """
    Optional yakuman

    The hand contains 2-2 3-3 4-4 5-5 6-6 7-7 8-8 of one pin suit

    Optionally can be of any suit
    """

    def __init__(self, yaku_id=None):
        super(Daisharin, self).__init__(yaku_id)

    def set_attributes(self):
        self.set_pin()

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def set_pin(self):
        self.name = 'Daisharin'
        self.english = 'Big wheels'
        self.japanese = '大車輪'

    def set_sou(self):
        self.name = 'Daisuurin'
        self.english = 'Bamboo forest'
        self.japanese = '大数隣'

    def set_man(self):
        self.name = 'Daichikurin'
        self.english = 'Numerous numbers'
        self.japanese = '大竹林'

    def rename(self, hand):
        # rename this yakuman depending on tiles used
        if is_sou(hand[0][0]):
            self.set_sou()
        elif is_pin(hand[0][0]):
            self.set_pin()
        else:
            self.set_man()

    def is_condition_met(self, hand, allow_other_sets, *args):
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

        if not allow_other_sets and pin_sets == 0:
            # if we are not allowing other sets than pins
            return False

        indices = reduce(lambda z, y: z + y, hand)
        # cast tile indices to 0..8 representation
        indices = [simplify(x) for x in indices]

        # check for pairs
        for x in range(1, 8):
            if len([y for y in indices if y == x]) != 2:
                return False

        return True
