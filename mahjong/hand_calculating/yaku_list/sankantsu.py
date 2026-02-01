from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.meld import Meld


class SanKantsu(Yaku):
    """
    The hand with three kan sets
    """

    def set_attributes(self) -> None:
        self.yaku_id = 30

        self.name = "San Kantsu"

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], melds: Collection[Meld], *args) -> bool:
        kan_sets = [x for x in melds if x.type == Meld.KAN or x.type == Meld.SHOUMINKAN]
        return len(kan_sets) == 3
