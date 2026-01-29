from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import classify_hand_suits, is_pin, is_sou


class Daisharin(Yaku):
    """
    Optional yakuman

    The hand contains 2-2 3-3 4-4 5-5 6-6 7-7 8-8 of one pin suit

    Optionally can be of any suit
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Daisharin, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.set_pin()

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def set_pin(self) -> None:
        self.name = "Daisharin"

    def set_man(self) -> None:
        self.name = "Daisuurin"

    def set_sou(self) -> None:
        self.name = "Daichikurin"

    def rename(self, hand: Sequence[Sequence[int]]) -> None:
        if is_sou(hand[0][0]):
            self.set_sou()
        elif is_pin(hand[0][0]):
            self.set_pin()
        else:
            self.set_man()

    def is_condition_met(self, hand: Collection[Sequence[int]], allow_other_sets: bool, *args) -> bool:
        suit_mask, honor_count = classify_hand_suits(hand)

        if honor_count > 0 or suit_mask not in (1, 2, 4):
            return False

        # if not allowing other suits, must be pin (suit_mask == 2)
        if not allow_other_sets and suit_mask != 2:
            return False

        # count simplified tile values - daisharin needs pairs of 2-3-4-5-6-7-8
        counts = [0] * 9
        for item in hand:
            for tile in item:
                counts[tile % 9] += 1

        # each of 2-8 (indices 1-7) must appear exactly twice
        for i in range(1, 8):
            if counts[i] != 2:
                return False

        return True
