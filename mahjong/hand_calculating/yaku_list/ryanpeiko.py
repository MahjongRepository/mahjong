from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi


class Ryanpeikou(Yaku):
    """
    The hand contains two different Iipeikou’s
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Ryanpeikou, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 32

        self.name = "Ryanpeikou"

        self.han_open = None
        self.han_closed = 3

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        chi_sets = [i for i in hand if is_chi(i)]
        count_of_identical_chi = []
        for x in chi_sets:
            count = 0
            for y in chi_sets:
                if x == y:
                    count += 1
            count_of_identical_chi.append(count)

        return len([x for x in count_of_identical_chi if x >= 2]) == 4
