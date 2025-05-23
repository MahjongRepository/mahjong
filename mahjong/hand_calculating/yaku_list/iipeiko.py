from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi


class Iipeiko(Yaku):
    """
    Hand with two identical chi
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Iipeiko, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 9

        self.name = "Iipeiko"

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        chi_sets = [i for i in hand if is_chi(i)]

        count_of_identical_chi = 0
        for x in chi_sets:
            count = 0
            for y in chi_sets:
                if x == y:
                    count += 1
            if count > count_of_identical_chi:
                count_of_identical_chi = count

        return count_of_identical_chi >= 2
