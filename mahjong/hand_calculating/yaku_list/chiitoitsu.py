from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Chiitoitsu(Yaku):
    """
    Hand contains only pairs
    """

    def __init__(self, yaku_id: int | None = None) -> None:
        super(Chiitoitsu, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 22

        self.name = "Chiitoitsu"

        self.han_open = None
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return len(hand) == 7
