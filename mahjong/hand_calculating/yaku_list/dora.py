from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Dora(Yaku):
    def __init__(self, yaku_id: int | None = None) -> None:
        super(Dora, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 52

        self.name = "Dora"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True

    def __str__(self) -> str:
        return "Dora {}".format(self.han_closed)
