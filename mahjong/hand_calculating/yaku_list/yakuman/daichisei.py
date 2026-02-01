from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.constants import HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Daichisei(Yaku):
    """
    Yaku situation
    """

    yaku_id = 110
    name = "Daichisei"
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        indices = chain.from_iterable(hand)
        return all(x in HONOR_INDICES for x in indices) and len(hand) == 7
