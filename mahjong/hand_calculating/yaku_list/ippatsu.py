from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Ippatsu(Yaku):
    """
    Yaku situation
    """

    yaku_id = 3
    name = "Ippatsu"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
