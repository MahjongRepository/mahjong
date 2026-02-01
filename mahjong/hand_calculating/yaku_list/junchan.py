from collections.abc import Collection, Sequence

from mahjong.constants import TERMINAL_INDICES
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi


class Junchan(Yaku):
    """
    Every set must have at least one terminal, and the pair must be of
    a terminal tile. Must contain at least one sequence (123 or 789).
    Honours are not allowed
    """

    yaku_id = 37
    name = "Junchan"
    han_open = 2
    han_closed = 3

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        terminal_sets = 0
        count_of_chi = 0
        for item in hand:
            if is_chi(item):
                count_of_chi += 1

            # inline set membership check - only need first or last tile
            if item[0] in TERMINAL_INDICES or item[-1] in TERMINAL_INDICES:
                terminal_sets += 1

        if count_of_chi == 0:
            return False

        return terminal_sets == 5
