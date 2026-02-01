from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.constants import TERMINAL_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Chinroutou(Yaku):
    yaku_id = 108
    name = "Chinroutou"
    han_open = 13
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """
        Hand composed entirely of terminal tiles.
        :param hand: list of hand's sets
        :return: boolean
        """
        indices = chain.from_iterable(hand)
        return all(x in TERMINAL_INDICES for x in indices)
