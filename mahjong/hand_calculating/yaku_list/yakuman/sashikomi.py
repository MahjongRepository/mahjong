from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Sashikomi(Yaku):
    """
    Yaku situation
    """

    def set_attributes(self) -> None:
        self.yaku_id = 118

        self.name = "Sashikomi"

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
