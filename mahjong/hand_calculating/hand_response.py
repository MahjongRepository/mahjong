from collections.abc import Collection

from mahjong.hand_calculating.fu import FuDetail
from mahjong.hand_calculating.scores import ScoresResult
from mahjong.hand_calculating.yaku import Yaku


class HandResponse:
    """
    Result of a hand value estimation returned by :meth:`HandCalculator.estimate_hand_value`.

    On success, the response contains the hand's han count, fu count, scoring breakdown,
    yaku list, and fu component details. On failure, only :attr:`error` is set and all
    other fields are ``None``.

    Successful hand — access scoring information:

    >>> from mahjong.hand_calculating.hand import HandCalculator
    >>> from mahjong.tile import TilesConverter
    >>> tiles = TilesConverter.string_to_136_array(man="22444", pin="333567", sou="444")
    >>> win_tile = TilesConverter.string_to_136_array(sou="4")[0]
    >>> result = HandCalculator.estimate_hand_value(tiles, win_tile)
    >>> result.han
    1
    >>> result.fu
    40
    >>> result.cost["main"]
    1300
    >>> result.yaku
    [Tanyao]
    >>> print(result)
    1 han, 40 fu

    Invalid hand — error is set:

    >>> tiles = TilesConverter.string_to_136_array(man="12345")
    >>> win_tile = TilesConverter.string_to_136_array(man="1")[0]
    >>> result = HandCalculator.estimate_hand_value(tiles, win_tile)
    >>> result.error is not None
    True
    >>> result.cost is None
    True

    :ivar cost: scoring breakdown with main/additional payments, bonuses, and total;
        ``None`` when the hand is invalid
    :vartype cost: ScoresResult | None
    :ivar han: total han count; ``None`` when the hand is invalid
    :vartype han: int | None
    :ivar fu: total fu (minipoints) count; ``None`` when the hand is invalid
    :vartype fu: int | None
    :ivar fu_details: fu component breakdown sorted by fu value (descending);
        ``None`` when the hand is invalid
    :vartype fu_details: list[FuDetail] | None
    :ivar yaku: yaku present in the hand sorted by yaku id;
        ``None`` when the hand is invalid
    :vartype yaku: list[Yaku] | None
    :ivar error: error message describing why the hand is invalid;
        ``None`` for valid hands
    :vartype error: str | None
    :ivar is_open_hand: whether the hand contains open melds
    :vartype is_open_hand: bool
    """

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
        Initialize a hand response.

        Typically constructed by :meth:`HandCalculator.estimate_hand_value` rather than
        directly by user code.

        :param cost: scoring breakdown (payment amounts, bonuses, total)
        :param han: total han count
        :param fu: total fu (minipoints) count
        :param yaku: yaku present in the hand; stored sorted by yaku id
        :param error: error message if the hand is invalid
        :param fu_details: fu component breakdown; stored sorted by fu value (descending)
        :param is_open_hand: whether the hand contains open melds
        """
        self.cost = cost
        self.han = han
        self.fu = fu
        self.error = error
        self.is_open_hand = is_open_hand

        if fu_details:
            self.fu_details = sorted(fu_details, key=lambda x: x["fu"], reverse=True)
        else:
            self.fu_details = None

        if yaku:
            self.yaku = sorted(yaku, key=lambda x: x.yaku_id)
        else:
            self.yaku = None

    def __str__(self) -> str:
        """
        Return error message if the hand is invalid, otherwise ``"X han, Y fu"``.

        >>> from mahjong.hand_calculating.hand_response import HandResponse
        >>> str(HandResponse(error="Hand is not winning"))
        'Hand is not winning'

        >>> str(HandResponse(han=3, fu=30))
        '3 han, 30 fu'
        """
        if self.error:
            return self.error
        return f"{self.han} han, {self.fu} fu"
