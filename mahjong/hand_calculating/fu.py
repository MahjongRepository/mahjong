from collections.abc import Collection, Sequence
from typing import TypedDict

from mahjong.constants import TERMINAL_AND_HONOR_INDICES
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld


class FuDetail(TypedDict):
    """
    A single fu component with its point value and reason.

    Each entry in the fu breakdown returned by :meth:`FuCalculator.calculate_fu`
    describes one source of fu (e.g., base fu, a closed pon, or a wait type).

    :param fu: fu points awarded for this component
    :param reason: identifier string matching one of the :class:`FuCalculator` reason constants
    """

    fu: int
    reason: str


# terminal/honor membership lookup for tile_34 indices 0..33
_IS_TERMINAL_OR_HONOR = [i in TERMINAL_AND_HONOR_INDICES for i in range(34)]

# meld state bit flags
_OPENED = 1
_IS_KAN = 2


class FuCalculator:
    """
    Calculate fu (minipoints) for a winning hand decomposition.

    Fu are computed from the hand's meld structure, wait type, pair, and winning method.
    The result is a detailed breakdown of fu components and the total fu rounded up to
    the nearest 10.
    """

    BASE = "base"
    """Base fu: 20 for open/tsumo, 30 for closed ron, 25 for chiitoitsu."""

    PENCHAN = "penchan"
    """Penchan (edge wait): 2 fu for completing 1-2-3 with the 3, or 7-8-9 with the 7."""

    KANCHAN = "kanchan"
    """Kanchan (closed wait): 2 fu for waiting on the middle tile of a sequence."""

    VALUED_PAIR = "valued_pair"
    """Valued pair: 2 fu for a pair of dragon, seat wind, or round wind tiles."""

    DOUBLE_VALUED_PAIR = "double_valued_pair"
    """Double valued pair: 4 fu when the pair tile is both seat wind and round wind."""

    PAIR_WAIT = "pair_wait"
    """Pair wait: 2 fu for winning on the pair tile."""

    TSUMO = "tsumo"
    """Tsumo: 2 fu for winning by self-draw."""

    HAND_WITHOUT_FU = "hand_without_fu"
    """Open pinfu: 2 fu for an open hand with no other fu sources."""

    CLOSED_PON = "closed_pon"
    """Closed pon of simple tiles: 4 fu."""

    OPEN_PON = "open_pon"
    """Open pon of simple tiles: 2 fu."""

    CLOSED_TERMINAL_PON = "closed_terminal_pon"
    """Closed pon of terminal or honor tiles: 8 fu."""

    OPEN_TERMINAL_PON = "open_terminal_pon"
    """Open pon of terminal or honor tiles: 4 fu."""

    CLOSED_KAN = "closed_kan"
    """Closed kan of simple tiles: 16 fu."""

    OPEN_KAN = "open_kan"
    """Open kan of simple tiles: 8 fu."""

    CLOSED_TERMINAL_KAN = "closed_terminal_kan"
    """Closed kan of terminal or honor tiles: 32 fu."""

    OPEN_TERMINAL_KAN = "open_terminal_kan"
    """Open kan of terminal or honor tiles: 16 fu."""

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
        Calculate fu for a winning hand decomposition.

        Analyze the hand's meld structure, wait type, pair, and winning method to produce
        a detailed breakdown of fu components and the total fu rounded up to the nearest 10.

        Chiitoitsu (seven pairs) always receives 25 fu:

        >>> from mahjong.hand_calculating.fu import FuCalculator
        >>> from mahjong.hand_calculating.hand_config import HandConfig
        >>> hand = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
        >>> win_tile = 24
        >>> win_group = [6, 6]
        >>> fu_details, fu = FuCalculator.calculate_fu(hand, win_tile, win_group, HandConfig())
        >>> fu
        25

        A closed ron hand with only chi melds and a non-valued pair (pinfu) receives 30 fu:

        >>> hand = [[0, 1, 2], [3, 4, 5], [9, 10, 11], [18, 19, 20], [27, 27]]
        >>> win_tile = 20
        >>> win_group = [3, 4, 5]
        >>> fu_details, fu = FuCalculator.calculate_fu(hand, win_tile, win_group, HandConfig())
        >>> fu
        30

        A closed pon of simple tiles adds 4 fu:

        >>> hand = [[2, 2, 2], [3, 4, 5], [9, 10, 11], [18, 19, 20], [27, 27]]
        >>> win_tile = 20
        >>> win_group = [3, 4, 5]
        >>> fu_details, fu = FuCalculator.calculate_fu(hand, win_tile, win_group, HandConfig())
        >>> fu
        40
        >>> {"fu": 4, "reason": FuCalculator.CLOSED_PON} in fu_details
        True

        :param hand: decomposed hand as a collection of tile sets, each a sequence of tile
            indices in 34-format: a pair (length 2), chi (length 3 with consecutive tiles),
            pon (length 3 with identical tiles), or kan (length 4);
            chiitoitsu hands have 7 pairs
        :param win_tile: the winning tile index in 136-format
        :param win_group: the tile set (from ``hand``) that contains the winning tile,
            as tile indices in 34-format
        :param config: hand configuration with win method and optional rule settings
        :param valued_tiles: tile indices in 34-format for tiles that grant pair fu
            (dragons, player wind, round wind); pass the same index twice for double-valued
        :param melds: declared melds (open chi, open/closed pon, open/closed kan)
        :return: tuple of (fu component list, total fu rounded up to nearest 10)
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
