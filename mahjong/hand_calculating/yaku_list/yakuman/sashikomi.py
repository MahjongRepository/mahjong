from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Sashikomi(Yaku):
    """差し込み: Intentional deal-in for open riichi, scored as yakuman (optional rule)."""

    yaku_id = 118
    name = "Sashikomi"
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
