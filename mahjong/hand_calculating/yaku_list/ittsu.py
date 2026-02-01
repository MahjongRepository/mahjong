from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Ittsu(Yaku):
    """
    Three sets of same suit: 1-2-3, 4-5-6, 7-8-9
    """

    yaku_id = 25
    name = "Ittsu"
    han_open = 1
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # bitmask per suit: bit 0 = chi at 0, bit 1 = chi at 3, bit 2 = chi at 6
        sou_mask = 0
        pin_mask = 0
        man_mask = 0

        for item in hand:
            first = item[0]
            # check if it's a chi (consecutive tiles)
            if first + 1 != item[1]:
                continue
            simplified = first % 9
            # only care about starting positions 0, 3, 6
            match simplified:
                case 0:
                    bit = 1
                case 3:
                    bit = 2
                case 6:
                    bit = 4
                case _:
                    continue

            if first >= 18:  # sou
                sou_mask |= bit
            elif first >= 9:  # pin
                pin_mask |= bit
            else:  # man
                man_mask |= bit

        # ittsu requires all three (mask == 7)
        return sou_mask == 7 or pin_mask == 7 or man_mask == 7
