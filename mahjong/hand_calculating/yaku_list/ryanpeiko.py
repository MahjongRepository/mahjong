from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_chi


class Ryanpeikou(Yaku):
    """
    The hand contains two different Iipeikou's
    """

    yaku_id = 38
    name = "Ryanpeikou"
    han_closed = 3

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # count occurrences of each chi set (first tile uniquely identifies a chi)
        chi_counts: dict[int, int] = {}
        for item in hand:
            if is_chi(item):
                key = item[0]
                chi_counts[key] = chi_counts.get(key, 0) + 1

        # ryanpeiko requires 4 chi that form 2 pairs
        # count pairs: each pair of identical chi contributes 1, 4 identical chi contributes 2
        total_pairs = sum(count // 2 for count in chi_counts.values())
        return total_pairs >= 2
