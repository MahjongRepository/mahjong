# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi, is_sou, is_pin, is_man, simplify


class Ittsu(Yaku):
    """
    Three sets of same suit: 1-2-3, 4-5-6, 7-8-9
    """

    def __init__(self, yaku_id=None):
        super(Ittsu, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 24

        self.name = 'Ittsu'
        self.english = 'Straight'
        self.japanese = '一気通貫'

        self.han_open = 1
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        chi_sets = [i for i in hand if is_chi(i)]
        if len(chi_sets) < 3:
            return False

        sou_chi = []
        pin_chi = []
        man_chi = []
        for item in chi_sets:
            if is_sou(item[0]):
                sou_chi.append(item)
            elif is_pin(item[0]):
                pin_chi.append(item)
            elif is_man(item[0]):
                man_chi.append(item)

        sets = [sou_chi, pin_chi, man_chi]

        for suit_item in sets:
            if len(suit_item) < 3:
                continue

            casted_sets = []

            for set_item in suit_item:
                # cast tiles indices to 0..8 representation
                casted_sets.append([simplify(set_item[0]),
                                    simplify(set_item[1]),
                                    simplify(set_item[2])])

            if [0, 1, 2] in casted_sets and [3, 4, 5] in casted_sets and [6, 7, 8] in casted_sets:
                return True

        return False
