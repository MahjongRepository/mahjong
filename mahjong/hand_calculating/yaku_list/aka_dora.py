from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class AkaDora(Yaku):
    """
    Red five
    """

    def set_attributes(self) -> None:
        self.yaku_id = 121

        self.name = "Aka Dora"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True

    def __str__(self) -> str:
        return "Aka Dora {}".format(self.han_closed)
