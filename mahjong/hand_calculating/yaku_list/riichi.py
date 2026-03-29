from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Riichi(Yaku):
    """立直: Declared ready hand."""

    yaku_id = 1
    name = "Riichi"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
