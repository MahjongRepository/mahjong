from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.meld import Meld


class Suukantsu(Yaku):
    """
    The hand with four kan sets
    """

    def set_attributes(self) -> None:
        self.yaku_id = 106

        self.name = "Suu Kantsu"

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], melds: Collection[Meld], *args) -> bool:
        kan_sets = [x for x in melds if x.type == Meld.KAN or x.type == Meld.SHOUMINKAN]
        return len(kan_sets) == 4
