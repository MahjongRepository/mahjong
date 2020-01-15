# -*- coding: utf-8 -*-
from mahjong.constants import HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_sou, is_pin, is_man


class Honitsu(Yaku):
    """
    The hand contains tiles from a single suit plus honours
    """

    def __init__(self, yaku_id=None):
        super(Honitsu, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 34
        self.name = 'Honitsu'
        self.english = 'Half Flush'
        self.japanese = '混一色'

        self.han_open = 2
        self.han_closed = 3

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        honor_sets = 0
        sou_sets = 0
        pin_sets = 0
        man_sets = 0
        for item in hand:
            if item[0] in HONOR_INDICES:
                honor_sets += 1

            if is_sou(item[0]):
                sou_sets += 1
            elif is_pin(item[0]):
                pin_sets += 1
            elif is_man(item[0]):
                man_sets += 1

        sets = [sou_sets, pin_sets, man_sets]
        only_one_suit = len([x for x in sets if x != 0]) == 1

        return only_one_suit and honor_sets != 0
