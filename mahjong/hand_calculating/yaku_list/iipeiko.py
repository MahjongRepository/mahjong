from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi


class Iipeiko(Yaku):
    """
    Hand with two identical chi
    """

    yaku_id = 14
    name = "Iipeiko"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # count occurrences of each chi set (first tile uniquely identifies a chi)
        chi_counts: dict[int, int] = {}
        for item in hand:
            if is_chi(item):
                key = item[0]
                chi_counts[key] = chi_counts.get(key, 0) + 1

        # iipeiko requires at least one pair of identical chi
        return any(count >= 2 for count in chi_counts.values())
