"""
Configuration classes for the hand calculator.

.. rubric:: Classes

* :class:`HandConstants` - constants for kazoe (counted) yakuman limit modes
* :class:`OptionalRules` - toggle optional rule variants (open tanyao, aka dora, etc.)
* :class:`HandConfig` - full hand configuration combining win conditions, wind context,
  bonuses, and optional rules
"""

from mahjong.constants import EAST
from mahjong.hand_calculating.yaku_config import YakuConfig


class HandConstants:
    """Constants for kazoe (counted) yakuman limit modes."""

    KAZOE_LIMITED = 0
    """Kazoe hands (13+ han) are capped at single yakuman."""

    KAZOE_SANBAIMAN = 1
    """Kazoe hands (13+ han) are capped at sanbaiman."""

    KAZOE_NO_LIMIT = 2
    """No cap on kazoe hands; 13+ han as yakuman, 26+ as double yakuman, and so on."""


class OptionalRules:
    """
    Toggle optional rule variants for hand evaluation.

    Japanese mahjong has many rule variations across different parlors and online platforms.
    This class controls which optional rules are active during hand calculation.

    :ivar has_open_tanyao: allow tanyao on open hands (kuitan)
    :vartype has_open_tanyao: bool
    :ivar has_aka_dora: enable red five tiles as bonus dora
    :vartype has_aka_dora: bool
    :ivar has_double_yakuman: allow double yakuman scoring for applicable hands
    :vartype has_double_yakuman: bool
    :ivar kazoe_limit: kazoe yakuman limit mode; one of
        :attr:`HandConstants.KAZOE_LIMITED`, :attr:`HandConstants.KAZOE_SANBAIMAN`,
        or :attr:`HandConstants.KAZOE_NO_LIMIT`
    :vartype kazoe_limit: int
    :ivar kiriage: round up to mangan when han/fu are at the boundary (e.g. 4 han 30 fu)
    :vartype kiriage: bool
    :ivar fu_for_open_pinfu: award 2 fu for open hands with no other fu sources;
        when False, 1 han 20 fu hands become possible
    :vartype fu_for_open_pinfu: bool
    :ivar fu_for_pinfu_tsumo: award 2 fu for tsumo on pinfu hands (disabling the 0-fu
        tsumo pinfu exception)
    :vartype fu_for_pinfu_tsumo: bool
    :ivar renhou_as_yakuman: treat renhou as yakuman instead of mangan
    :vartype renhou_as_yakuman: bool
    :ivar has_daisharin: enable daisharin (seven consecutive pairs in one suit) as yakuman;
        automatically set to True when ``has_daisharin_other_suits`` is True
    :vartype has_daisharin: bool
    :ivar has_daisharin_other_suits: allow daisharin in pin and sou suits (not only man)
    :vartype has_daisharin_other_suits: bool
    :ivar has_daichisei: enable daichisei (seven pairs of honor tiles) as yakuman
    :vartype has_daichisei: bool
    :ivar has_sashikomi_yakuman: enable sashikomi (intentional deal-in for open riichi)
        as yakuman
    :vartype has_sashikomi_yakuman: bool
    :ivar limit_to_sextuple_yakuman: cap yakuman multiplier at 6x
    :vartype limit_to_sextuple_yakuman: bool
    :ivar paarenchan_needs_yaku: require at least one yaku for paarenchan to count
    :vartype paarenchan_needs_yaku: bool
    """

    has_open_tanyao: bool
    has_aka_dora: bool
    has_double_yakuman: bool
    kazoe_limit: int
    kiriage: bool
    fu_for_open_pinfu: bool
    fu_for_pinfu_tsumo: bool
    renhou_as_yakuman: bool
    has_daisharin: bool
    has_daisharin_other_suits: bool
    has_daichisei: bool
    has_sashikomi_yakuman: bool
    limit_to_sextuple_yakuman: bool
    paarenchan_needs_yaku: bool

    def __init__(
        self,
        has_open_tanyao: bool = False,
        has_aka_dora: bool = False,
        has_double_yakuman: bool = True,
        kazoe_limit: int = HandConstants.KAZOE_LIMITED,
        kiriage: bool = False,
        fu_for_open_pinfu: bool = True,
        fu_for_pinfu_tsumo: bool = False,
        renhou_as_yakuman: bool = False,
        has_daisharin: bool = False,
        has_daisharin_other_suits: bool = False,
        has_sashikomi_yakuman: bool = False,
        limit_to_sextuple_yakuman: bool = True,
        paarenchan_needs_yaku: bool = True,
        has_daichisei: bool = False,
    ) -> None:
        """
        Initialize optional rules.

        >>> from mahjong.hand_calculating.hand_config import OptionalRules
        >>> options = OptionalRules(has_open_tanyao=True, kiriage=True)
        >>> options.has_open_tanyao
        True
        >>> options.kiriage
        True

        :param has_open_tanyao: allow tanyao on open hands (kuitan)
        :param has_aka_dora: enable red five tiles as bonus dora
        :param has_double_yakuman: allow double yakuman scoring
        :param kazoe_limit: kazoe yakuman limit mode
        :param kiriage: round up to mangan at boundary han/fu combinations
        :param fu_for_open_pinfu: award 2 fu for open hands with no other fu sources
        :param fu_for_pinfu_tsumo: award tsumo fu even for pinfu hands
        :param renhou_as_yakuman: treat renhou as yakuman
        :param has_daisharin: enable daisharin yakuman
        :param has_daisharin_other_suits: allow daisharin in all suits
        :param has_sashikomi_yakuman: enable sashikomi yakuman
        :param limit_to_sextuple_yakuman: cap yakuman multiplier at 6x
        :param paarenchan_needs_yaku: require yaku for paarenchan
        :param has_daichisei: enable daichisei yakuman
        """
        self.has_open_tanyao = has_open_tanyao
        self.has_aka_dora = has_aka_dora
        self.has_double_yakuman = has_double_yakuman
        self.kazoe_limit = kazoe_limit
        self.kiriage = kiriage
        self.fu_for_open_pinfu = fu_for_open_pinfu
        self.fu_for_pinfu_tsumo = fu_for_pinfu_tsumo
        self.renhou_as_yakuman = renhou_as_yakuman
        self.has_daisharin = has_daisharin or has_daisharin_other_suits
        self.has_daisharin_other_suits = has_daisharin_other_suits
        self.has_sashikomi_yakuman = has_sashikomi_yakuman
        self.limit_to_sextuple_yakuman = limit_to_sextuple_yakuman
        self.has_daichisei = has_daichisei
        self.paarenchan_needs_yaku = paarenchan_needs_yaku


class HandConfig(HandConstants):
    """
    Configuration for the hand calculator combining win conditions, wind context, and optional rules.

    Pass a ``HandConfig`` instance to
    :meth:`~mahjong.hand_calculating.hand.HandCalculator.estimate_hand_value` to describe
    how the hand was won and which rules apply.

    A default config represents a closed ron with no special conditions:

    >>> from mahjong.hand_calculating.hand_config import HandConfig
    >>> config = HandConfig()
    >>> config.is_tsumo
    False
    >>> config.is_dealer
    False

    Configure a dealer tsumo win with riichi and ippatsu:

    >>> from mahjong.constants import EAST
    >>> config = HandConfig(is_tsumo=True, is_riichi=True, is_ippatsu=True, player_wind=EAST)
    >>> config.is_tsumo
    True
    >>> config.is_dealer
    True

    Include score bonuses and optional rules:

    >>> from mahjong.hand_calculating.hand_config import OptionalRules
    >>> options = OptionalRules(has_open_tanyao=True, has_aka_dora=True)
    >>> config = HandConfig(tsumi_number=2, kyoutaku_number=3, options=options)
    >>> config.tsumi_number
    2
    >>> config.options.has_open_tanyao
    True

    :ivar yaku: yaku definition objects used during hand evaluation
    :vartype yaku: ~mahjong.hand_calculating.yaku_config.YakuConfig
    :ivar options: optional rule settings
    :vartype options: OptionalRules
    :ivar is_tsumo: hand won by self-draw
    :vartype is_tsumo: bool
    :ivar is_riichi: player declared riichi
    :vartype is_riichi: bool
    :ivar is_ippatsu: win within one turn of declaring riichi
    :vartype is_ippatsu: bool
    :ivar is_rinshan: win on a replacement tile after calling kan
    :vartype is_rinshan: bool
    :ivar is_chankan: win by robbing another player's kan declaration
    :vartype is_chankan: bool
    :ivar is_haitei: win on the last drawable tile (tsumo) of the round
    :vartype is_haitei: bool
    :ivar is_houtei: win on the discard following the last drawable tile (ron)
    :vartype is_houtei: bool
    :ivar is_daburu_riichi: player declared double riichi (riichi on first turn)
    :vartype is_daburu_riichi: bool
    :ivar is_nagashi_mangan: all discards are terminals and honors with no calls against them
    :vartype is_nagashi_mangan: bool
    :ivar is_tenhou: dealer wins on the initial draw
    :vartype is_tenhou: bool
    :ivar is_renhou: non-dealer wins on the first go-around before any calls
    :vartype is_renhou: bool
    :ivar is_chiihou: non-dealer wins on the initial draw
    :vartype is_chiihou: bool
    :ivar is_open_riichi: player declared open riichi (revealed hand)
    :vartype is_open_riichi: bool
    :ivar is_dealer: True when ``player_wind`` is East
    :vartype is_dealer: bool
    :ivar player_wind: tile index in 34-format of the player's seat wind, or None
    :vartype player_wind: int | None
    :ivar round_wind: tile index in 34-format of the round wind, or None
    :vartype round_wind: int | None
    :ivar paarenchan: consecutive dealer wins count; above 0 enables paarenchan yakuman check
    :vartype paarenchan: int
    :ivar kyoutaku_number: number of riichi deposits on the table (1000 points each)
    :vartype kyoutaku_number: int
    :ivar tsumi_number: number of honba counters (100 points each per counter)
    :vartype tsumi_number: int
    """

    yaku: YakuConfig
    options: OptionalRules

    is_tsumo: bool
    is_riichi: bool
    is_ippatsu: bool
    is_rinshan: bool
    is_chankan: bool
    is_haitei: bool
    is_houtei: bool
    is_daburu_riichi: bool
    is_nagashi_mangan: bool
    is_tenhou: bool
    is_renhou: bool
    is_chiihou: bool
    is_open_riichi: bool

    is_dealer: bool
    player_wind: int | None
    round_wind: int | None
    paarenchan: int

    kyoutaku_number: int
    tsumi_number: int

    def __init__(
        self,
        is_tsumo: bool = False,
        is_riichi: bool = False,
        is_ippatsu: bool = False,
        is_rinshan: bool = False,
        is_chankan: bool = False,
        is_haitei: bool = False,
        is_houtei: bool = False,
        is_daburu_riichi: bool = False,
        is_nagashi_mangan: bool = False,
        is_tenhou: bool = False,
        is_renhou: bool = False,
        is_chiihou: bool = False,
        is_open_riichi: bool = False,
        player_wind: int | None = None,
        round_wind: int | None = None,
        kyoutaku_number: int = 0,
        tsumi_number: int = 0,
        paarenchan: int = 0,
        options: OptionalRules | None = None,
    ) -> None:
        """
        Initialize hand configuration.

        >>> from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
        >>> from mahjong.constants import EAST, SOUTH
        >>> config = HandConfig(
        ...     is_tsumo=True,
        ...     is_riichi=True,
        ...     player_wind=EAST,
        ...     round_wind=SOUTH,
        ...     options=OptionalRules(has_open_tanyao=True),
        ... )
        >>> config.is_dealer
        True
        >>> config.round_wind == SOUTH
        True

        :param is_tsumo: hand won by self-draw
        :param is_riichi: player declared riichi
        :param is_ippatsu: win within one turn of declaring riichi
        :param is_rinshan: win on a replacement tile after calling kan
        :param is_chankan: win by robbing another player's kan
        :param is_haitei: win on the last drawable tile
        :param is_houtei: win on the discard following the last drawable tile
        :param is_daburu_riichi: player declared double riichi
        :param is_nagashi_mangan: all discards are terminals and honors
        :param is_tenhou: dealer wins on the initial draw
        :param is_renhou: non-dealer wins on the first go-around
        :param is_chiihou: non-dealer wins on the initial draw
        :param is_open_riichi: player declared open riichi
        :param player_wind: tile index in 34-format of the player's seat wind
        :param round_wind: tile index in 34-format of the round wind
        :param kyoutaku_number: riichi deposits on the table (1000 points each)
        :param tsumi_number: honba counters (100 points each per counter)
        :param paarenchan: consecutive dealer wins count for paarenchan check
        :param options: optional rule settings; defaults to :class:`OptionalRules` with
            all defaults when None
        """
        self.yaku = YakuConfig()
        self.options = options or OptionalRules()

        self.is_tsumo = is_tsumo
        self.is_riichi = is_riichi
        self.is_ippatsu = is_ippatsu
        self.is_rinshan = is_rinshan
        self.is_chankan = is_chankan
        self.is_haitei = is_haitei
        self.is_houtei = is_houtei
        self.is_daburu_riichi = is_daburu_riichi
        self.is_nagashi_mangan = is_nagashi_mangan
        self.is_tenhou = is_tenhou
        self.is_renhou = is_renhou
        self.is_chiihou = is_chiihou
        self.is_open_riichi = is_open_riichi

        self.player_wind = player_wind
        self.round_wind = round_wind
        self.is_dealer = player_wind == EAST
        self.paarenchan = paarenchan

        self.kyoutaku_number = kyoutaku_number
        self.tsumi_number = tsumi_number
