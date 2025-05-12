from collections.abc import Collection, Sequence
from itertools import chain
from typing import Optional

from mahjong.constants import HONOR_INDICES, TERMINAL_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Honroto(Yaku):
    """
    All tiles are terminals or honours
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Honroto, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 31

        self.name = "Honroutou"

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        indices = chain.from_iterable(hand)
        result = HONOR_INDICES + TERMINAL_INDICES
        return all(x in result for x in indices)
