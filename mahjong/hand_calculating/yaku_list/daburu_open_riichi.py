from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class DaburuOpenRiichi(Yaku):
    """
    Yaku situation
    """

    yaku_id = 9
    name = "Double Open Riichi"
    han_closed = 3

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
