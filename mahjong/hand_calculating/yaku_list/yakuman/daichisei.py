from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.constants import HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Daichisei(Yaku):
    """
    Yaku situation
    """

    def set_attributes(self) -> None:
        self.yaku_id = 110

        self.name = "Daichisei"

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        indices = chain.from_iterable(hand)
        return all(x in HONOR_INDICES for x in indices) and len(hand) == 7
