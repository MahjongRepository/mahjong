from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.meld import Meld


class Suukantsu(Yaku):
    """The hand with four kan sets."""

    yaku_id = 106
    name = "Suu Kantsu"
    han_open = 13
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], melds: Collection[Meld], *args) -> bool:
        """
        Check whether the hand contains four kan sets.

        :param hand: decomposed hand as a collection of tile groups in 34-format
        :param melds: declared melds
        :return: True if four of the melds are kan or shouminkan
        """
        kan_sets = [x for x in melds if x.type in (Meld.KAN, Meld.SHOUMINKAN)]
        return len(kan_sets) == 4
