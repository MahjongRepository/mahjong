"""
Score calculation for winning hands.

.. rubric:: Classes

* :class:`ScoresResult` - typed dictionary holding the score breakdown
* :class:`ScoresCalculator` - standard scoring with han/fu, honba, and kyoutaku bonuses
* :class:`Aotenjou` - variant scoring with no mangan cap (aotenjou rule)
"""

from collections.abc import MutableSequence, MutableSet
from typing import TypedDict

from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.hand_calculating.yaku import Yaku


class ScoresResult(TypedDict):
    """
    Score breakdown for a winning hand.

    Each field represents a component of the final payment between players.
    The meaning of ``main`` and ``additional`` depends on the win method:

    - **Ron**: ``main`` is the full payment from the discarding player;
      ``additional`` is always 0.
    - **Dealer tsumo**: ``main`` and ``additional`` are equal — each
      non-dealer pays the same amount.
    - **Non-dealer tsumo**: ``main`` is the dealer's payment;
      ``additional`` is the payment from each non-dealer.

    :param main: base cost (before honba bonus)
    :param additional: base cost for each non-dealer (before honba bonus);
        0 for ron
    :param main_bonus: honba bonus added to ``main``
    :param additional_bonus: honba bonus added to ``additional``
    :param kyoutaku_bonus: points from accumulated riichi deposits
        (1000 per deposit)
    :param total: total points the winner earns
    :param yaku_level: scoring tier label (e.g. ``"mangan"``,
        ``"yakuman"``, ``""`` for below mangan)
    """

    main: int
    additional: int
    main_bonus: int
    additional_bonus: int
    kyoutaku_bonus: int
    total: int
    yaku_level: str


class ScoresCalculator:
    """
    Calculate scores for a winning hand using standard Japanese mahjong rules.

    Scores are determined by han and fu values, then adjusted for honba (tsumi)
    counters and kyoutaku (riichi deposit) bonuses. Hands at or above 5 han
    receive fixed-tier payouts (mangan through yakuman).
    """

    @staticmethod
    def calculate_scores(han: int, fu: int, config: HandConfig, is_yakuman: bool = False) -> ScoresResult:
        """
        Calculate score payment for a hand with the given han and fu.

        Determine the base payment from han/fu, apply scoring tier caps
        (mangan, haneman, baiman, sanbaiman, yakuman), then add honba
        and kyoutaku bonuses.

        A non-dealer ron at 3 han 30 fu:

        >>> from mahjong.hand_calculating.scores import ScoresCalculator
        >>> from mahjong.hand_calculating.hand_config import HandConfig
        >>> result = ScoresCalculator.calculate_scores(han=3, fu=30, config=HandConfig())
        >>> result["main"]
        3900
        >>> result["additional"]
        0
        >>> result["total"]
        3900

        A dealer tsumo mangan with 2 honba and 3 riichi deposits:

        >>> from mahjong.constants import EAST
        >>> config = HandConfig(is_tsumo=True, player_wind=EAST, tsumi_number=2, kyoutaku_number=3)
        >>> result = ScoresCalculator.calculate_scores(han=5, fu=30, config=config)
        >>> result["main"]
        4000
        >>> result["additional"]
        4000
        >>> result["total"]
        15600

        Mangan (5 han):

        >>> result = ScoresCalculator.calculate_scores(han=5, fu=30, config=HandConfig())
        >>> result["yaku_level"]
        'mangan'
        >>> result["main"]
        8000

        :param han: number of han (doubles)
        :param fu: fu (minipoints), rounded to nearest 10
        :param config: hand configuration with win method, dealer status, and bonuses
        :param is_yakuman: True if the hand contains yakuman yaku (bypasses kazoe limit)
        :return: :class:`ScoresResult` with the full score breakdown
        """
        yaku_level = ""

        # kazoe hand
        if han >= 13 and not is_yakuman:
            # kazoe hands capped at single yakuman
            if config.options.kazoe_limit == HandConfig.KAZOE_LIMITED:
                han = 13
                yaku_level = "kazoe yakuman"
            # kazoe hands capped at sanbaiman
            elif config.options.kazoe_limit == HandConfig.KAZOE_SANBAIMAN:
                han = 12
                yaku_level = "kazoe sanbaiman"

        if han >= 5:
            if han >= 78:
                yaku_level = "6x yakuman"
                if config.options.limit_to_sextuple_yakuman:
                    rounded = 48000
                else:
                    extra_han, _ = divmod(han - 78, 13)
                    rounded = 48000 + (extra_han * 8000)
            elif han >= 65:
                yaku_level = "5x yakuman"
                rounded = 40000
            elif han >= 52:
                yaku_level = "4x yakuman"
                rounded = 32000
            elif han >= 39:
                yaku_level = "3x yakuman"
                rounded = 24000
            # double yakuman
            elif han >= 26:
                yaku_level = "2x yakuman"
                rounded = 16000
            # yakuman
            elif han >= 13:
                yaku_level = "yakuman"
                rounded = 8000
            # sanbaiman
            elif han >= 11:
                yaku_level = "sanbaiman"
                rounded = 6000
            # baiman
            elif han >= 8:
                yaku_level = "baiman"
                rounded = 4000
            # haneman
            elif han >= 6:
                yaku_level = "haneman"
                rounded = 3000
            else:
                yaku_level = "mangan"
                rounded = 2000

            double_rounded = rounded * 2
            four_rounded = double_rounded * 2
            six_rounded = double_rounded * 3
        else:  # han < 5
            base_points = fu * pow(2, 2 + han)
            rounded = (base_points + 99) // 100 * 100
            double_rounded = (2 * base_points + 99) // 100 * 100
            four_rounded = (4 * base_points + 99) // 100 * 100
            six_rounded = (6 * base_points + 99) // 100 * 100

            is_kiriage = False
            if config.options.kiriage:
                if (han == 4 and fu == 30) or (han == 3 and fu == 60):
                    yaku_level = "kiriage mangan"
                    is_kiriage = True
            elif rounded > 2000:  # kiriage not supported
                yaku_level = "mangan"

            # mangan
            if rounded > 2000 or is_kiriage:
                rounded = 2000
                double_rounded = rounded * 2
                four_rounded = double_rounded * 2
                six_rounded = double_rounded * 3
            else:  # below mangan
                pass

        if config.is_tsumo:
            main = double_rounded
            main_bonus = 100 * config.tsumi_number
            additional_bonus = main_bonus
            additional = main if config.is_dealer else rounded

        else:  # ron
            additional = 0
            additional_bonus = 0
            main_bonus = 300 * config.tsumi_number
            main = six_rounded if config.is_dealer else four_rounded

        kyoutaku_bonus = 1000 * config.kyoutaku_number
        total = (main + main_bonus) + 2 * (additional + additional_bonus) + kyoutaku_bonus

        if config.is_nagashi_mangan:
            yaku_level = "nagashi mangan"

        return ScoresResult(
            main=main,
            additional=additional,
            main_bonus=main_bonus,
            additional_bonus=additional_bonus,
            kyoutaku_bonus=kyoutaku_bonus,
            total=total,
            yaku_level=yaku_level,
        )


class Aotenjou(ScoresCalculator):
    """
    Variant scoring calculator for the aotenjou (blue ceiling) rule.

    Under aotenjou, there is no mangan cap — the base-points formula
    ``fu * 2^(2+han)`` is applied directly regardless of han count.
    Honba and kyoutaku bonuses are not applied. Yakuman yaku are treated
    as normal yaku and contribute their han values rather than triggering
    fixed payouts.
    """

    @staticmethod
    def calculate_scores(han: int, fu: int, config: HandConfig, is_yakuman: bool = False) -> ScoresResult:  # noqa: ARG004
        """
        Calculate score payment under aotenjou rules.

        Apply the base-points formula without any mangan cap or scoring tiers.
        Honba and kyoutaku bonuses are not included.

        A non-dealer ron at 13 han 40 fu under aotenjou:

        >>> from mahjong.hand_calculating.scores import Aotenjou
        >>> from mahjong.hand_calculating.hand_config import HandConfig
        >>> result = Aotenjou.calculate_scores(han=13, fu=40, config=HandConfig())
        >>> result["main"]
        5242900
        >>> result["yaku_level"]
        ''

        :param han: number of han (doubles)
        :param fu: fu (minipoints)
        :param config: hand configuration with win method and dealer status
        :param is_yakuman: unused (aotenjou treats yakuman as normal yaku)
        :return: :class:`ScoresResult` with the score breakdown (no bonuses)
        """
        base_points: int = fu * pow(2, 2 + han)
        rounded = (base_points + 99) // 100 * 100
        double_rounded = (2 * base_points + 99) // 100 * 100
        four_rounded = (4 * base_points + 99) // 100 * 100
        six_rounded = (6 * base_points + 99) // 100 * 100

        if config.is_tsumo:
            main = double_rounded
            additional = double_rounded if config.is_dealer else rounded
        else:
            main = six_rounded if config.is_dealer else four_rounded
            additional = 0

        # aotenjou bypasses all scoring tiers and bonuses (honba/kyoutaku)
        return ScoresResult(
            main=main,
            additional=additional,
            main_bonus=0,
            additional_bonus=0,
            kyoutaku_bonus=0,
            total=main + 2 * additional,
            yaku_level="",
        )

    @staticmethod
    def aotenjou_filter_yaku(hand_yaku: MutableSequence[Yaku] | MutableSet[Yaku], config: HandConfig) -> None:
        """
        Remove lower yaku that are precursors to yakuman yaku in aotenjou mode.

        Under aotenjou, yakuman are scored as normal yaku with their han values.
        When a yakuman is present, its precursor yaku (e.g. shosangen for daisangen,
        toitoi for chinroto) must be removed to avoid double-counting.

        :param hand_yaku: mutable collection of yaku in the hand; modified in place
        :param config: hand configuration providing yaku definitions
        """
        if config.yaku.daisangen in hand_yaku:
            # for daisangen precursors are all dragons and shosangen
            hand_yaku.remove(config.yaku.chun)
            hand_yaku.remove(config.yaku.hatsu)
            hand_yaku.remove(config.yaku.haku)
            hand_yaku.remove(config.yaku.shosangen)

        if config.yaku.tsuisou in hand_yaku:
            # for tsuuiisou we need to remove toitoi and honroto
            hand_yaku.remove(config.yaku.toitoi)
            hand_yaku.remove(config.yaku.honroto)

        if config.yaku.shosuushi in hand_yaku:
            # for shosuushi we do not need to remove anything
            pass

        if config.yaku.daisuushi in hand_yaku:
            # for daisuushi we need to remove toitoi
            hand_yaku.remove(config.yaku.toitoi)

        if (
            config.yaku.suuankou in hand_yaku or config.yaku.suuankou_tanki in hand_yaku
        ) and config.yaku.toitoi in hand_yaku:
            # for suu ankou we need to remove toitoi and sanankou (sanankou is already removed by default)
            # toitoi is "optional" in closed suukantsu, maybe a bug? or toitoi is not given when it's kans?
            hand_yaku.remove(config.yaku.toitoi)

        if config.yaku.chinroto in hand_yaku:
            # for chinroto we need to remove toitoi and honroto
            hand_yaku.remove(config.yaku.toitoi)
            hand_yaku.remove(config.yaku.honroto)

        if config.yaku.suukantsu in hand_yaku and config.yaku.toitoi in hand_yaku:
            # for suukantsu we need to remove toitoi and sankantsu (sankantsu is already removed by default)
            # same as above?
            hand_yaku.remove(config.yaku.toitoi)

        if config.yaku.chuuren_poutou in hand_yaku or config.yaku.daburu_chuuren_poutou in hand_yaku:
            # for chuuren poutou we need to remove chinitsu
            hand_yaku.remove(config.yaku.chinitsu)

        if config.yaku.daisharin in hand_yaku:
            # for daisharin we need to remove chinitsu, pinfu, tanyao, ryanpeiko, chiitoitsu
            hand_yaku.remove(config.yaku.chinitsu)
            if config.yaku.pinfu in hand_yaku:
                hand_yaku.remove(config.yaku.pinfu)
            hand_yaku.remove(config.yaku.tanyao)
            if config.yaku.ryanpeiko in hand_yaku:
                hand_yaku.remove(config.yaku.ryanpeiko)
            if config.yaku.chiitoitsu in hand_yaku:
                hand_yaku.remove(config.yaku.chiitoitsu)

        if config.yaku.ryuisou in hand_yaku and config.yaku.honitsu in hand_yaku:
            # for ryuisou we need to remove honitsu, if it is there
            hand_yaku.remove(config.yaku.honitsu)
