from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import classify_hand_suits, is_pin, is_sou


class Daisharin(Yaku):
    """
    Seven pairs of 2-3-4-5-6-7-8 in a single suit (optional yakuman).

    By default only the pin suit qualifies (daisharin). When other suits are allowed,
    the yaku is renamed to daisuurin (man) or daichikurin (sou).
    """

    yaku_id = 109
    name = "Daisharin"
    han_closed = 13
    is_yakuman = True

    def set_pin(self) -> None:
        """Set the yaku name to Daisharin (pin suit)."""
        self.name = "Daisharin"

    def set_man(self) -> None:
        """Set the yaku name to Daisuurin (man suit)."""
        self.name = "Daisuurin"

    def set_sou(self) -> None:
        """Set the yaku name to Daichikurin (sou suit)."""
        self.name = "Daichikurin"

    def rename(self, hand: Sequence[Sequence[int]]) -> None:
        """Set the yaku name based on the suit of the hand."""
        if is_sou(hand[0][0]):
            self.set_sou()
        elif is_pin(hand[0][0]):
            self.set_pin()
        else:
            self.set_man()

    def is_condition_met(self, hand: Collection[Sequence[int]], allow_other_sets: bool, *args) -> bool:
        """
        Check whether the hand is seven pairs of 2-3-4-5-6-7-8 in a single suit.

        :param hand: decomposed hand as a collection of tile groups in 34-format
        :param allow_other_sets: if True, allow any single suit; if False, require pin suit only
        :return: True if the hand matches the daisharin pattern
        """
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
        return all(counts[i] == 2 for i in range(1, 8))
