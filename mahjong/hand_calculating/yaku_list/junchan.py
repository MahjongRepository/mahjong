# -*- coding: utf-8 -*-
from mahjong.constants import TERMINAL_INDICES
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi


class Junchan(Yaku):
    """
    Every set must have at least one terminal, and the pair must be of
    a terminal tile. Must contain at least one sequence (123 or 789).
    Honours are not allowed
    """

    def __init__(self, yaku_id=None):
        super(Junchan, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 33

        self.name = 'Junchan'
        self.english = 'Terminal In Each Meld'
        self.japanese = '純全帯么九'

        self.han_open = 2
        self.han_closed = 3

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        def tile_in_indices(item_set, indices_array):
            for x in item_set:
                if x in indices_array:
                    return True
            return False

        terminal_sets = 0
        count_of_chi = 0
        for item in hand:
            if is_chi(item):
                count_of_chi += 1

            if tile_in_indices(item, TERMINAL_INDICES):
                terminal_sets += 1

        if count_of_chi == 0:
            return False

        return terminal_sets == 5
