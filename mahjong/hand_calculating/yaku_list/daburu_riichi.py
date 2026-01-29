from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class DaburuRiichi(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id: int | None = None) -> None:
        super(DaburuRiichi, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 21

        self.name = "Double Riichi"

        self.han_open = None
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
