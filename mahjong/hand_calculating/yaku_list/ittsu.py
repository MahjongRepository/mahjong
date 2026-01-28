from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.hand_calculating.yaku import Yaku


class Ittsu(Yaku):
    """
    Three sets of same suit: 1-2-3, 4-5-6, 7-8-9
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Ittsu, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 24

        self.name = "Ittsu"

        self.han_open = 1
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # bitmask per suit: bit 0 = chi at 0, bit 1 = chi at 3, bit 2 = chi at 6
        sou_mask = 0
        pin_mask = 0
        man_mask = 0
        chi_count = 0

        for item in hand:
            if len(item) != 3:
                continue
            first = item[0]
            # check if it's a chi (consecutive tiles)
            if first + 1 != item[1] or first + 2 != item[2]:
                continue

            chi_count += 1
            simplified = first % 9
            # only care about starting positions 0, 3, 6
            if simplified == 0:
                bit = 1
            elif simplified == 3:
                bit = 2
            elif simplified == 6:
                bit = 4
            else:
                continue

            if first >= 18:  # sou
                sou_mask |= bit
            elif first >= 9:  # pin
                pin_mask |= bit
            else:  # man
                man_mask |= bit

        if chi_count < 3:
            return False

        # ittsu requires all three (mask == 7)
        return sou_mask == 7 or pin_mask == 7 or man_mask == 7
