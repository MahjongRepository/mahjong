from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class DaburuKokushiMusou(Yaku):
    def __init__(self, yaku_id: int | None = None) -> None:
        super(DaburuKokushiMusou, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 48

        self.name = "Kokushi Musou Juusanmen Matchi"

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
