from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Rinshan(Yaku):
    """嶺上開花: Win on a replacement tile after calling kan."""

    yaku_id = 5
    name = "Rinshan Kaihou"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
