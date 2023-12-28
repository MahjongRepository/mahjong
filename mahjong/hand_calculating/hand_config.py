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

    has_open_tanyao = False
    has_aka_dora = False
    has_double_yakuman = True
    # not implemented! tenhou does not support double yakuman for a single yaku
    kazoe_limit = HandConstants.KAZOE_LIMITED
    kiriage = False
    # if false, 1-20 hand will be possible
    fu_for_open_pinfu = True
    # if true, pinfu tsumo will be disabled
    fu_for_pinfu_tsumo = False
    renhou_as_yakuman = False
    has_daisharin = False
    has_daisharin_other_suits = False
    has_daichisei = False
    has_sashikomi_yakuman = False
    limit_to_sextuple_yakuman = True
    paarenchan_needs_yaku = True

    def __init__(
        self,
        has_open_tanyao=False,
        has_aka_dora=False,
        has_double_yakuman=True,
        kazoe_limit=HandConstants.KAZOE_LIMITED,
        kiriage=False,
        fu_for_open_pinfu=True,
        fu_for_pinfu_tsumo=False,
        renhou_as_yakuman=False,
        has_daisharin=False,
        has_daisharin_other_suits=False,
        has_sashikomi_yakuman=False,
        limit_to_sextuple_yakuman=True,
        paarenchan_needs_yaku=True,
        has_daichisei=False,
    ):
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

    yaku = None
    options = None

    is_tsumo = False
    is_riichi = False
    is_ippatsu = False
    is_rinshan = False
    is_chankan = False
    is_haitei = False
    is_houtei = False
    is_daburu_riichi = False
    is_nagashi_mangan = False
    is_tenhou = False
    is_renhou = False
    is_chiihou = False
    is_open_riichi = False

    is_dealer = False
    player_wind = None
    round_wind = None
    # for optional yakuman paarenchan above 0 means that dealer has paarenchan possibility
    paarenchan = 0

    kyoutaku_number = 0  # 1000-point
    tsumi_number = 0  # 100-point

    def __init__(
        self,
        is_tsumo=False,
        is_riichi=False,
        is_ippatsu=False,
        is_rinshan=False,
        is_chankan=False,
        is_haitei=False,
        is_houtei=False,
        is_daburu_riichi=False,
        is_nagashi_mangan=False,
        is_tenhou=False,
        is_renhou=False,
        is_chiihou=False,
        is_open_riichi=False,
        player_wind=None,
        round_wind=None,
        kyoutaku_number=0,
        tsumi_number=0,
        paarenchan=0,
        options=None,
    ):
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
