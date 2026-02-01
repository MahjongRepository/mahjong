from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.meld import Meld


class SanKantsu(Yaku):
    """
    The hand with three kan sets
    """

    yaku_id = 30
    name = "San Kantsu"
    han_open = 2
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], melds: Collection[Meld], *args) -> bool:
        kan_sets = [x for x in melds if x.type == Meld.KAN or x.type == Meld.SHOUMINKAN]
        return len(kan_sets) == 3
