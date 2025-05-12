from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.hand_calculating.yaku import Yaku


class Haitei(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Haitei, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 5

        self.name = "Haitei Raoyue"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
