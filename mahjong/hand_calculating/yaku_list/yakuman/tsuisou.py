from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.constants import HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Tsuuiisou(Yaku):
    """
    Hand composed entirely of honour tiles
    """

    yaku_id = 107
    name = "Tsuu Iisou"
    han_open = 13
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """
        Hand composed entirely of honour tiles.
        :param hand: list of hand's sets
        :return: boolean
        """
        indices = chain.from_iterable(hand)
        return all(x in HONOR_INDICES for x in indices)
