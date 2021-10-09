from mahjong.hand_calculating.yaku import Yaku


class Tenhou(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id=None):
        super(Tenhou, self).__init__(yaku_id)

    def set_attributes(self):
        self.tenhou_id = 37

        self.name = "Tenhou"

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand, *args):
        # was it here or not is controlling by superior code
        return True
