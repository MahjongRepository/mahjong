from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Dora(Yaku):
    """ドラ: Bonus han from dora indicator tiles."""

    yaku_id = 120
    name = "Dora"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True

    def __str__(self) -> str:
        """Return the yaku name with the current han count."""
        return f"Dora {self.han_closed}"
