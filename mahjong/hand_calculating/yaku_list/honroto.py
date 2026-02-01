from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.constants import TERMINAL_AND_HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Honroto(Yaku):
    """
    All tiles are terminals or honours
    """

    yaku_id = 27
    name = "Honroutou"
    han_open = 2
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        indices = chain.from_iterable(hand)
        return all(x in TERMINAL_AND_HONOR_INDICES for x in indices)
