# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon, is_sou, is_pin, is_man, simplify


class SanshokuDoukou(Yaku):
    """
    Three pon sets consisting of the same numbers in all three suits
    """

    def __init__(self, yaku_id=None):
        super(SanshokuDoukou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 26

        self.name = 'Sanshoku Doukou'
        self.english = 'Three Colored Triplets'
        self.japanese = '三色同刻'

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        pon_sets = [i for i in hand if is_pon(i)]
        if len(pon_sets) < 3:
            return False

        sou_pon = []
        pin_pon = []
        man_pon = []
        for item in pon_sets:
            if is_sou(item[0]):
                sou_pon.append(item)
            elif is_pin(item[0]):
                pin_pon.append(item)
            elif is_man(item[0]):
                man_pon.append(item)

        for sou_item in sou_pon:
            for pin_item in pin_pon:
                for man_item in man_pon:
                    # cast tile indices to 1..9 representation
                    sou_item = [simplify(x) for x in sou_item]
                    pin_item = [simplify(x) for x in pin_item]
                    man_item = [simplify(x) for x in man_item]
                    if sou_item == pin_item == man_item:
                        return True
        return False
