from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.constants import HATSU
from mahjong.hand_calculating.yaku import Yaku


class Ryuuiisou(Yaku):
    """
    Hand composed entirely of green tiles. Green tiles are: green dragons and 2, 3, 4, 6 and 8 of sou.
    """

    def set_attributes(self) -> None:
        self.yaku_id = 105

        self.name = "Ryuuiisou"

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        green_indices = [19, 20, 21, 23, 25, HATSU]
        indices = chain.from_iterable(hand)
        return all(x in green_indices for x in indices)
