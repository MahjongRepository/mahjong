from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Pinfu(Yaku):
    """All sequences with a valueless pair and a two-sided wait."""

    yaku_id = 12
    name = "Pinfu"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
