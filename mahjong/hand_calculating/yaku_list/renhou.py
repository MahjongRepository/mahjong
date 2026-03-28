from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Renhou(Yaku):
    """Non-dealer wins on the first go-around before any calls (optional rule)."""

    yaku_id = 11
    name = "Renhou"
    han_closed = 5

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
