from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class NagashiMangan(Yaku):
    """
    Yaku situation
    """

    yaku_id = 10
    name = "Nagashi Mangan"
    han_open = 5
    han_closed = 5

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
