from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Chankan(Yaku):
    """Win by robbing another player's kan declaration."""

    yaku_id = 4
    name = "Chankan"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
