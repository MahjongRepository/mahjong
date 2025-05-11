from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.hand_calculating.yaku import Yaku


class DaburuOpenRiichi(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id: Optional[int]) -> None:
        super(DaburuOpenRiichi, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.name = "Double Open Riichi"

        self.han_open = None
        self.han_closed = 3

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
