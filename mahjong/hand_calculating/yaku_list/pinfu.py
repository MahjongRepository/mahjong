from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Pinfu(Yaku):
    """
    Yaku situation
    """

    def set_attributes(self) -> None:
        self.yaku_id = 12

        self.name = "Pinfu"

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
