# -*- coding: utf-8 -*-

import math

from mahjong.constants import TERMINAL_INDICES, HONOR_INDICES
from mahjong.meld import Meld
from mahjong.utils import is_pair, is_pon, simplify, contains_terminals


class HandFuCalculator(object):
    BASE = 'base'
    PENCHAN = 'penchan'
    KANCHAN = 'kanchan'
    VALUED_PAIR = 'valued_pair'
    PAIR_WAIT = 'pair_wait'
    TSUMO = 'tsumo'
    HAND_WITHOUT_FU = 'hand_without_fu'

    CLOSED_PON = 'closed_pon'
    OPEN_PON = 'open_pon'

    CLOSED_TERMINAL_PON = 'closed_terminal_pon'
    OPEN_TERMINAL_PON = 'open_terminal_pon'

    CLOSED_KAN = 'closed_kan'
    OPEN_KAN = 'open_kan'

    CLOSED_TERMINAL_KAN = 'closed_terminal_kan'
    OPEN_TERMINAL_KAN = 'open_terminal_kan'

    def calculate_fu(self,
                     hand,
                     win_tile,
                     win_group,
                     is_tsumo=False,
                     valued_tiles=None,
                     melds=None):
        """
        Calculate hand fu with explanations
        :param hand:
        :param win_tile: 136 tile format
        :param win_group: one set where win tile exists
        :param is_tsumo:
        :param valued_tiles: dragons, player wind, round wind
        :param melds: opened sets
        :return:
        """

        win_tile_34 = win_tile // 4

        if not valued_tiles:
            valued_tiles = []

        if not melds:
            melds = []

        fu_details = []

        if len(hand) == 7:
            return [{'fu': 25, 'reason': HandFuCalculator.BASE}], 25

        pair = [x for x in hand if is_pair(x)][0]
        pon_sets = [x for x in hand if is_pon(x)]

        copied_opened_melds = [x.tiles_34 for x in melds if x.type == Meld.CHI]
        closed_chi_sets = []
        for x in hand:
            if x not in copied_opened_melds:
                closed_chi_sets.append(x)
            else:
                copied_opened_melds.remove(x)

        is_open_hand = any([x.opened for x in melds])

        if win_group in closed_chi_sets:
            tile_index = simplify(win_tile_34)

            # penchan
            if contains_terminals(win_group):
                # 1-2-... wait
                if tile_index == 2 and win_group.index(win_tile_34) == 2:
                    fu_details.append({'fu': 2, 'reason': HandFuCalculator.PENCHAN})
                # 8-9-... wait
                elif tile_index == 6 and win_group.index(win_tile_34) == 0:
                    fu_details.append({'fu': 2, 'reason': HandFuCalculator.PENCHAN})

            # kanchan waiting 5-...-7
            if win_group.index(win_tile_34) == 1:
                fu_details.append({'fu': 2, 'reason': HandFuCalculator.KANCHAN})

        # valued pair
        count_of_valued_pairs = valued_tiles.count(pair[0])
        if count_of_valued_pairs == 1:
            fu_details.append({'fu': 2, 'reason': HandFuCalculator.VALUED_PAIR})

        # east-east pair when you are on east gave double fu
        if count_of_valued_pairs == 2:
            fu_details.append({'fu': 2, 'reason': HandFuCalculator.VALUED_PAIR})
            fu_details.append({'fu': 2, 'reason': HandFuCalculator.VALUED_PAIR})

        # pair wait
        if is_pair(win_group):
            fu_details.append({'fu': 2, 'reason': HandFuCalculator.PAIR_WAIT})

        for set_item in pon_sets:
            open_meld = [x for x in melds if set_item == x.tiles_34]
            open_meld = open_meld and open_meld[0] or None

            set_was_open = open_meld and open_meld.opened or False
            is_kan = (open_meld and (open_meld.type == Meld.KAN or open_meld.type == Meld.CHANKAN)) or False
            is_honor = set_item[0] in TERMINAL_INDICES + HONOR_INDICES

            # we win by ron on the third pon tile, our pon will be count as open
            if not is_tsumo and set_item == win_group:
                set_was_open = True

            if is_honor:
                if is_kan:
                    if set_was_open:
                        fu_details.append({'fu': 16, 'reason': HandFuCalculator.OPEN_TERMINAL_KAN})
                    else:
                        fu_details.append({'fu': 32, 'reason': HandFuCalculator.CLOSED_TERMINAL_KAN})
                else:
                    if set_was_open:
                        fu_details.append({'fu': 4, 'reason': HandFuCalculator.OPEN_TERMINAL_PON})
                    else:
                        fu_details.append({'fu': 8, 'reason': HandFuCalculator.CLOSED_TERMINAL_PON})
            else:
                if is_kan:
                    if set_was_open:
                        fu_details.append({'fu': 8, 'reason': HandFuCalculator.OPEN_KAN})
                    else:
                        fu_details.append({'fu': 16, 'reason': HandFuCalculator.CLOSED_KAN})
                else:
                    if set_was_open:
                        fu_details.append({'fu': 2, 'reason': HandFuCalculator.OPEN_PON})
                    else:
                        fu_details.append({'fu': 4, 'reason': HandFuCalculator.CLOSED_PON})

        if is_tsumo and len(fu_details):
            # 2 additional fu for tsumo (but not for pinfu)
            fu_details.append({'fu': 2, 'reason': HandFuCalculator.TSUMO})

        if is_open_hand and not len(fu_details):
            # there is no 1-20 hands, so we had to add additional fu
            fu_details.append({'fu': 2, 'reason': HandFuCalculator.HAND_WITHOUT_FU})

        if is_open_hand or is_tsumo:
            fu_details.append({'fu': 20, 'reason': HandFuCalculator.BASE})
        else:
            fu_details.append({'fu': 30, 'reason': HandFuCalculator.BASE})

        return fu_details, self.round_fu(fu_details)

    def round_fu(self, fu_details):
        # 22 -> 30 and etc.
        fu = sum([x['fu'] for x in fu_details])
        return int(math.ceil(fu / 10.0)) * 10
