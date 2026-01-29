from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.constants import TERMINAL_AND_HONOR_INDICES
from mahjong.hand_calculating.yaku import Yaku


class Honroto(Yaku):
    """
    All tiles are terminals or honours
    """

    def __init__(self, yaku_id: int | None = None) -> None:
        super(Honroto, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 31

        self.name = "Honroutou"

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        indices = chain.from_iterable(hand)
        return all(x in TERMINAL_AND_HONOR_INDICES for x in indices)
