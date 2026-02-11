from collections.abc import Collection

from mahjong.hand_calculating.fu import FuDetail
from mahjong.hand_calculating.scores import ScoresResult
from mahjong.hand_calculating.yaku import Yaku


class HandResponse:
    cost: ScoresResult | None
    han: int | None
    fu: int | None
    fu_details: list[FuDetail] | None
    yaku: list[Yaku] | None
    error: str | None
    is_open_hand: bool

    def __init__(
        self,
        cost: ScoresResult | None = None,
        han: int | None = None,
        fu: int | None = None,
        yaku: Collection[Yaku] | None = None,
        error: str | None = None,
        fu_details: list[FuDetail] | None = None,
        is_open_hand: bool = False,
    ) -> None:
        """
        :param cost: ScoresResult
        :param han: int
        :param fu: int
        :param yaku: list
        :param error: str
        :param fu_details: list[FuDetail]
        """
        self.cost = cost
        self.han = han
        self.fu = fu
        self.error = error
        self.is_open_hand = is_open_hand  # adding this field for yaku reporting

        if fu_details:
            self.fu_details = sorted(fu_details, key=lambda x: x["fu"], reverse=True)
        else:
            self.fu_details = None

        if yaku:
            self.yaku = sorted(yaku, key=lambda x: x.yaku_id)
        else:
            self.yaku = None

    def __str__(self) -> str:
        if self.error:
            return self.error
        return f"{self.han} han, {self.fu} fu"
