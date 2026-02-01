from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.constants import TERMINAL_AND_HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Tanyao(Yaku):
    """
    Hand without 1, 9, dragons and winds
    """

    yaku_id = 13
    name = "Tanyao"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        indices = chain.from_iterable(hand)
        return not any(x in TERMINAL_AND_HONOR_INDICES for x in indices)
