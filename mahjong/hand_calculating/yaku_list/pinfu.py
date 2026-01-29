from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Pinfu(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id: int | None = None) -> None:
        super(Pinfu, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 7

        self.name = "Pinfu"

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
