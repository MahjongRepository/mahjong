# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon


class Suuankou(Yaku):
    """
    Four closed pon sets
    """

    def __init__(self, yaku_id=None):
        super(Suuankou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 41

        self.name = 'Suu ankou'
        self.english = 'Four Concealed Triplets'
        self.japanese = '四暗刻'

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, win_tile, is_tsumo):
        win_tile //= 4
        closed_hand = []
        for item in hand:
            # if we do the ron on syanpon wait our pon will be consider as open
            if is_pon(item) and win_tile in item and not is_tsumo:
                continue

            closed_hand.append(item)

        count_of_pon = len([i for i in closed_hand if is_pon(i)])
        return count_of_pon == 4
