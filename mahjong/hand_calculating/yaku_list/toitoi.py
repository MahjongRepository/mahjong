from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class Toitoi(Yaku):
    """
    The hand consists of all pon sets (and of course a pair), no sequences.
    """

    def __init__(self, yaku_id: int | None = None) -> None:
        super(Toitoi, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 28
        self.name = "Toitoi"

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        count_of_pon = sum(1 for item in hand if is_pon_or_kan(item))
        return count_of_pon == 4
