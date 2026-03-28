from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.meld import Meld


class SanKantsu(Yaku):
    """The hand with three kan sets."""

    yaku_id = 32
    name = "San Kantsu"
    han_open = 2
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], melds: Collection[Meld], *args) -> bool:
        """
        Check whether the hand contains three kan sets.

        :param hand: decomposed hand as a collection of tile groups in 34-format
        :param melds: declared melds
        :return: True if three of the melds are kan or shouminkan
        """
        kan_sets = [x for x in melds if x.type in (Meld.KAN, Meld.SHOUMINKAN)]
        return len(kan_sets) == 3
