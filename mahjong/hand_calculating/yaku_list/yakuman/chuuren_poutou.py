from collections.abc import Collection, Sequence
from itertools import chain

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import classify_hand_suits, simplify


class ChuurenPoutou(Yaku):
    """
    The hand contains 1-1-1-2-3-4-5-6-7-8-9-9-9 of one suit, plus any other tile of the same suit.
    """

    yaku_id = 101
    name = "Chuuren Poutou"
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        suit_mask, honor_count = classify_hand_suits(hand)
        if honor_count > 0 or suit_mask not in (1, 2, 4):
            return False

        counts = [0] * 9
        for x in chain.from_iterable(hand):
            counts[simplify(x)] += 1

        # 1-1-1
        if counts[0] < 3:
            return False

        # 9-9-9
        if counts[8] < 3:
            return False

        has_two_tiles = False
        counts[0] -= 2
        counts[8] -= 2

        # 1-2-3-4-5-6-7-8-9 and one tile to any of them
        for c in counts:
            match c:
                case 1:
                    continue
                case 2:
                    if has_two_tiles:
                        return False
                    has_two_tiles = True
                case _:
                    return False

        return has_two_tiles
