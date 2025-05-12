from collections.abc import Collection, Sequence
from itertools import chain
from typing import Optional

from mahjong.constants import HATSU
from mahjong.hand_calculating.yaku import Yaku


class Ryuuiisou(Yaku):
    """
    Hand composed entirely of green tiles. Green tiles are: green dragons and 2, 3, 4, 6 and 8 of sou.
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Ryuuiisou, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 43

        self.name = "Ryuuiisou"

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        green_indices = [19, 20, 21, 23, 25, HATSU]
        indices = chain.from_iterable(hand)
        return all(x in green_indices for x in indices)
