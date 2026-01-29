from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.constants import HONOR_INDICES, TERMINAL_INDICES
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi


class Chantai(Yaku):
    """
    Every set must have at least one terminal or honour tile, and the pair must be of
    a terminal or honour tile. Must contain at least one sequence (123 or 789)
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Chantai, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 23

        self.name = "Chantai"

        self.han_open = 1
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        honor_sets = 0
        terminal_sets = 0
        count_of_chi = 0
        for item in hand:
            if is_chi(item):
                count_of_chi += 1

            first = item[0]
            if first in TERMINAL_INDICES or item[-1] in TERMINAL_INDICES:
                terminal_sets += 1
            elif first in HONOR_INDICES:
                honor_sets += 1

        if count_of_chi == 0:
            return False

        return terminal_sets + honor_sets == 5 and terminal_sets != 0 and honor_sets != 0
