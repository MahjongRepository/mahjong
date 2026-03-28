from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class UraDora(Yaku):
    """Bonus han from ura dora indicators revealed after a riichi win."""

    yaku_id = 122
    name = "Ura Dora"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True

    def __str__(self) -> str:
        """Return the yaku name with the current han count."""
        return f"Ura Dora {self.han_closed}"
