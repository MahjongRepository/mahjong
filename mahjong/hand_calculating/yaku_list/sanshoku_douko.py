from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class SanshokuDoukou(Yaku):
    """
    Three pon sets consisting of the same numbers in all three suits
    """

    yaku_id = 33
    name = "Sanshoku Doukou"
    han_open = 2
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # bitmask per suit: bit i = pon at simplified position i
        sou_mask = 0
        pin_mask = 0
        man_mask = 0

        for item in hand:
            first = item[0]

            # skip honors (27-33)
            if first >= 27:
                continue

            if not is_pon_or_kan(item):
                continue

            simplified = first % 9
            bit = 1 << simplified

            if first >= 18:  # sou
                sou_mask |= bit
            elif first >= 9:  # pin
                pin_mask |= bit
            else:  # man
                man_mask |= bit

        # sanshoku douko requires same pon in all three suits
        return (sou_mask & pin_mask & man_mask) != 0
