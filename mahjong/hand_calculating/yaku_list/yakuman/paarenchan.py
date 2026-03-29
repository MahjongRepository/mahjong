from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Paarenchan(Yaku):
    """八連荘: Consecutive dealer wins, scored as yakuman when the threshold is reached (optional rule)."""

    yaku_id = 119
    name = "Paarenchan"
    han_open = 13
    han_closed = 13
    is_yakuman = True
    count = 0

    def set_paarenchan_count(self, count: int) -> None:
        """Set the consecutive win count and update han values accordingly."""
        self.han_open = 13 * count
        self.han_closed = 13 * count
        self.count = count

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True

    def __str__(self) -> str:
        """Return the yaku name with the consecutive win count."""
        return f"Paarenchan {self.count}"
