from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Sanshoku(Yaku):
    """
    The same chi in three suits
    """

    def set_attributes(self) -> None:
        self.yaku_id = 24

        self.name = "Sanshoku Doujun"

        self.han_open = 1
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # bitmask per suit: bit i = chi starting at simplified position i
        sou_mask = 0
        pin_mask = 0
        man_mask = 0

        for item in hand:
            first = item[0]
            # check if it's a chi (consecutive tiles)
            if first + 1 != item[1]:
                continue

            simplified = first % 9
            bit = 1 << simplified

            if first >= 18:  # sou
                sou_mask |= bit
            elif first >= 9:  # pin
                pin_mask |= bit
            else:  # man
                man_mask |= bit

        # sanshoku requires same chi in all three suits
        return (sou_mask & pin_mask & man_mask) != 0
