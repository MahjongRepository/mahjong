from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Renhou(Yaku):
    """
    Yaku situation
    """

    yaku_id = 11
    name = "Renhou"
    han_closed = 5

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
