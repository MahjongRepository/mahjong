from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class DaburuKokushiMusou(Yaku):
    def set_attributes(self) -> None:
        self.yaku_id = 112

        self.name = "Kokushi Musou Juusanmen Matchi"

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
