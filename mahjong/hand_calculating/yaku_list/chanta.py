# -*- coding: utf-8 -*-
from mahjong.constants import TERMINAL_INDICES, HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi


class Chanta(Yaku):
    """
    Every set must have at least one terminal or honour tile, and the pair must be of
    a terminal or honour tile. Must contain at least one sequence (123 or 789)
    """

    def __init__(self, yaku_id=None):
        super(Chanta, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 23

        self.name = 'Chanta'
        self.english = 'Terminal Or Honor In Each Group'
        self.japanese = '混全帯么九'

        self.han_open = 1
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand, *args):
        def tile_in_indices(item_set, indices_array):
            for x in item_set:
                if x in indices_array:
                    return True
            return False

        honor_sets = 0
        terminal_sets = 0
        count_of_chi = 0
        for item in hand:
            if is_chi(item):
                count_of_chi += 1

            if tile_in_indices(item, TERMINAL_INDICES):
                terminal_sets += 1

            if tile_in_indices(item, HONOR_INDICES):
                honor_sets += 1

        if count_of_chi == 0:
            return False

        return terminal_sets + honor_sets == 5 and terminal_sets != 0 and honor_sets != 0
