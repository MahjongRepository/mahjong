from typing import Optional

from mahjong.constants import EAST
from mahjong.hand_calculating.yaku_config import YakuConfig


class HandConstants:
    # Hands over 26+ han don't count as double yakuman
    KAZOE_LIMITED = 0
    # Hands over 13+ is a sanbaiman
    KAZOE_SANBAIMAN = 1
    # 26+ han as double yakuman, 39+ han as triple yakuman, etc.
    KAZOE_NO_LIMIT = 2


class OptionalRules:
    """
    All the supported optional rules
    """

    has_open_tanyao: bool
    has_aka_dora: bool
    has_double_yakuman: bool
    # not implemented! tenhou does not support double yakuman for a single yaku
    kazoe_limit: int
    kiriage: bool
    # if false, 1-20 hand will be possible
    fu_for_open_pinfu: bool
    # if true, pinfu tsumo will be disabled
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
    Special class to pass various settings to the hand calculator object
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
    player_wind: Optional[int]
    round_wind: Optional[int]
    # for optional yakuman paarenchan above 0 means that dealer has paarenchan possibility
    paarenchan: int

    kyoutaku_number: int  # 1000-point
    tsumi_number: int  # 100-point

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
        player_wind: Optional[int] = None,
        round_wind: Optional[int] = None,
        kyoutaku_number: int = 0,
        tsumi_number: int = 0,
        paarenchan: int = 0,
        options: Optional[OptionalRules] = None,
    ) -> None:
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
