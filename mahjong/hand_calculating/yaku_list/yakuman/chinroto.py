from collections.abc import Collection, Sequence
from itertools import chain
from typing import Optional

from mahjong.constants import TERMINAL_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Chinroutou(Yaku):
    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Chinroutou, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 44

        self.name = "Chinroutou"

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """
        Hand composed entirely of terminal tiles.
        :param hand: list of hand's sets
        :return: boolean
        """
        indices = chain.from_iterable(hand)
        return all(x in TERMINAL_INDICES for x in indices)
