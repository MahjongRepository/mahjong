from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Paarenchan(Yaku):
    """
    Yaku situation
    """

    yaku_id = 119
    name = "Paarenchan"
    han_open = 13
    han_closed = 13
    is_yakuman = True
    count = 0

    def set_paarenchan_count(self, count: int) -> None:
        self.han_open = 13 * count
        self.han_closed = 13 * count
        self.count = count

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True

    def __str__(self) -> str:
        return f"Paarenchan {self.count}"
