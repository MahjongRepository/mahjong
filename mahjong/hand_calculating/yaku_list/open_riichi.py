from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class OpenRiichi(Yaku):
    """Open riichi declaration where the hand is revealed (optional rule)."""

    yaku_id = 2
    name = "Open Riichi"
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
