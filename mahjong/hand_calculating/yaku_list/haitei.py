from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Haitei(Yaku):
    """
    Yaku situation
    """

    yaku_id = 6
    name = "Haitei Raoyue"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
