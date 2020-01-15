# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi, is_sou, is_pin, is_man, simplify


class Sanshoku(Yaku):
    """
    The same chi in three suits
    """

    def __init__(self, yaku_id=None):
        super(Sanshoku, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 25

        self.name = 'Sanshoku Doujun'
        self.english = 'Three Colored Triplets'
        self.japanese = '三色同順'

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

        for sou_item in sou_chi:
            for pin_item in pin_chi:
                for man_item in man_chi:
                    # cast tile indices to 0..8 representation
                    sou_item = [simplify(x) for x in sou_item]
                    pin_item = [simplify(x) for x in pin_item]
                    man_item = [simplify(x) for x in man_item]
                    if sou_item == pin_item == man_item:
                        return True
        return False
