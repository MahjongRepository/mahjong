from collections.abc import Collection, Sequence
from typing import TypedDict

from mahjong.constants import TERMINAL_AND_HONOR_INDICES
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld


class FuDetail(TypedDict):
    fu: int
    reason: str


# terminal/honor membership lookup for tile_34 indices 0..33
_IS_TERMINAL_OR_HONOR = [i in TERMINAL_AND_HONOR_INDICES for i in range(34)]

# meld state bit flags
_OPENED = 1
_IS_KAN = 2


class FuCalculator:
    BASE = "base"
    PENCHAN = "penchan"
    KANCHAN = "kanchan"
    VALUED_PAIR = "valued_pair"
    DOUBLE_VALUED_PAIR = "double_valued_pair"
    PAIR_WAIT = "pair_wait"
    TSUMO = "tsumo"
    HAND_WITHOUT_FU = "hand_without_fu"

    CLOSED_PON = "closed_pon"
    OPEN_PON = "open_pon"

    CLOSED_TERMINAL_PON = "closed_terminal_pon"
    OPEN_TERMINAL_PON = "open_terminal_pon"

    CLOSED_KAN = "closed_kan"
    OPEN_KAN = "open_kan"

    CLOSED_TERMINAL_KAN = "closed_terminal_kan"
    OPEN_TERMINAL_KAN = "open_terminal_kan"

    # lookup table indexed by [is_terminal_or_honor][is_kan][is_open] -> (fu, reason)
    _PON_KAN_FU_TABLE = (
        (  # simple tiles
            ((4, CLOSED_PON), (2, OPEN_PON)),  # pon
            ((16, CLOSED_KAN), (8, OPEN_KAN)),  # kan
        ),
        (  # terminal or honor tiles
            ((8, CLOSED_TERMINAL_PON), (4, OPEN_TERMINAL_PON)),  # pon
            ((32, CLOSED_TERMINAL_KAN), (16, OPEN_TERMINAL_KAN)),  # kan
        ),
    )

    @staticmethod
    def calculate_fu(
        hand: Collection[Sequence[int]],
        win_tile: int,
        win_group: Sequence[int],
        config: HandConfig,
        valued_tiles: Sequence[int | None] | None = None,
        melds: Collection[Meld] | None = None,
    ) -> tuple[list[FuDetail], int]:
        """
        Calculate hand fu with explanations
        :param hand:
        :param win_tile: 136 tile format
        :param win_group: one set where win tile exists
        :param config: HandConfig object
        :param valued_tiles: dragons, player wind, round wind
        :param melds: opened sets
        :return:
        """
        # chiitoitsu: always 25 fu
        if len(hand) == 7:
            return [FuDetail(fu=25, reason=FuCalculator.BASE)], 25

        win_tile_34 = win_tile >> 2

        if not valued_tiles:
            valued_tiles = ()

        if not melds:
            melds = ()

        fu_details: list[FuDetail] = []
        fu_total = 0

        is_tsumo = config.is_tsumo
        opts = config.options
        win_group_len = len(win_group)

        # detect if win_group is a chi (sequential meld)
        win_group_is_chi = False
        wg0 = wg1 = wg2 = -1
        if win_group_len == 3:
            wg0 = win_group[0]
            wg1 = win_group[1]
            wg2 = win_group[2]
            win_group_is_chi = wg0 != wg1

        # single pass over hand: find pair, collect pon/kan sets,
        # count chi groups matching win_group
        pair_tile = -1
        pon_sets: list[Sequence[int]] = []
        win_group_chi_count_in_hand = 0
        for grp in hand:
            grp_len = len(grp)
            if grp_len == 2:
                pair_tile = grp[0]
                continue

            # pon/kan: all tiles are the same
            if grp[0] == grp[1]:
                pon_sets.append(grp)
                continue

            # chi: count matches for win_group open/closed detection
            if win_group_is_chi and grp_len == 3 and grp[0] == wg0 and grp[1] == wg1 and grp[2] == wg2:
                win_group_chi_count_in_hand += 1

        # preprocess melds into a fixed-size state table (tile_34 -> bit flags)
        is_open_hand = False
        win_group_open_chi_count = 0
        meld_state = [0] * 34
        for m in melds:
            if m.opened:
                is_open_hand = True

            if m.type == Meld.CHI:
                if win_group_is_chi:
                    t0 = m.tiles[0] >> 2
                    t1 = m.tiles[1] >> 2
                    t2 = m.tiles[2] >> 2
                    if t0 == wg0 and t1 == wg1 and t2 == wg2:
                        win_group_open_chi_count += 1
            else:
                tile = m.tiles[0] >> 2
                state = 0
                if m.opened:
                    state |= _OPENED
                if m.type in (Meld.KAN, Meld.SHOUMINKAN):
                    state |= _IS_KAN
                meld_state[tile] = state

        # win_group chi is closed if hand has more of this pattern than open melds
        win_group_is_closed_chi = win_group_is_chi and win_group_chi_count_in_hand > win_group_open_chi_count

        # wait fu: penchan and kanchan (only for closed chi containing win tile)
        if win_group_is_closed_chi:
            start_rank = wg0 % 9

            # penchan: edge wait completing 1-2-3 with the 3, or 7-8-9 with the 7
            is_penchan = (start_rank == 0 and win_tile_34 == wg2) or (start_rank == 6 and win_tile_34 == wg0)
            if is_penchan:
                fu_details.append(FuDetail(fu=2, reason=FuCalculator.PENCHAN))
                fu_total += 2

            # kanchan: wait on the middle tile
            if win_tile_34 == wg1:
                fu_details.append(FuDetail(fu=2, reason=FuCalculator.KANCHAN))
                fu_total += 2

        # valued pair fu
        if pair_tile >= 0 and valued_tiles:
            valued_count = valued_tiles.count(pair_tile)
            if valued_count == 1:
                fu_details.append(FuDetail(fu=2, reason=FuCalculator.VALUED_PAIR))
                fu_total += 2
            elif valued_count >= 2:
                # e.g. east-east pair when player is east
                fu_details.append(FuDetail(fu=4, reason=FuCalculator.DOUBLE_VALUED_PAIR))
                fu_total += 4

        # pair wait fu
        if win_group_len == 2:
            fu_details.append(FuDetail(fu=2, reason=FuCalculator.PAIR_WAIT))
            fu_total += 2

        # pon/kan fu via lookup table
        for set_item in pon_sets:
            tile = set_item[0]
            state = meld_state[tile]

            set_was_open = (state & _OPENED) != 0
            is_kan_set = len(set_item) == 4 or (state & _IS_KAN) != 0

            # ron on the third pon tile counts pon as open
            if not is_tsumo and win_group_len == len(set_item) and win_group[0] == tile and win_group[1] == tile:
                set_was_open = True

            fu, reason = FuCalculator._PON_KAN_FU_TABLE[_IS_TERMINAL_OR_HONOR[tile]][is_kan_set][set_was_open]
            fu_details.append(FuDetail(fu=fu, reason=reason))
            fu_total += fu

        # tsumo fu (not for pinfu unless option is enabled)
        if is_tsumo and (fu_total > 0 or opts.fu_for_pinfu_tsumo):
            fu_details.append(FuDetail(fu=2, reason=FuCalculator.TSUMO))
            fu_total += 2

        # open pinfu: no 1-20 hands exist, add 2 fu
        if is_open_hand and fu_total == 0 and opts.fu_for_open_pinfu:
            fu_details.append(FuDetail(fu=2, reason=FuCalculator.HAND_WITHOUT_FU))
            fu_total += 2

        # base fu: 30 for closed ron, 20 for open or tsumo
        base_fu = 20 if is_open_hand or is_tsumo else 30
        fu_details.append(FuDetail(fu=base_fu, reason=FuCalculator.BASE))
        fu_total += base_fu

        # round up to the nearest 10
        return fu_details, (fu_total + 9) // 10 * 10
