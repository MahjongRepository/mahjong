from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.constants import TERMINAL_AND_HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Tanyao(Yaku):
    """
    Hand without 1, 9, dragons and winds
    """

    def set_attributes(self) -> None:
        self.yaku_id = 13

        self.name = "Tanyao"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        indices = chain.from_iterable(hand)
        return not any(x in TERMINAL_AND_HONOR_INDICES for x in indices)
