from typing import Optional

from mahjong.hand_calculating.divider import HandDivider
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld
from mahjong.tile import TilesConverter


def _string_to_34_tiles(
    sou: Optional[str] = "",
    pin: Optional[str] = "",
    man: Optional[str] = "",
    honors: Optional[str] = "",
) -> list[int]:
    tiles = TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)
    return [t // 4 for t in tiles]


def _string_to_open_34_set(
    sou: Optional[str] = "",
    pin: Optional[str] = "",
    man: Optional[str] = "",
    honors: Optional[str] = "",
) -> list[int]:
    open_set = TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)
    open_set[0] //= 4
    open_set[1] //= 4
    open_set[2] //= 4
    return open_set


def _string_to_34_tile(
    sou: Optional[str] = "",
    pin: Optional[str] = "",
    man: Optional[str] = "",
    honors: Optional[str] = "",
) -> int:
    item = TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)
    item[0] //= 4
    return item[0]


def _string_to_136_tile(
    sou: Optional[str] = "",
    pin: Optional[str] = "",
    man: Optional[str] = "",
    honors: Optional[str] = "",
) -> int:
    return TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)[0]


def _hand(tiles: list[int], hand_index: int = 0) -> list[list[int]]:
    hand_divider = HandDivider()
    return hand_divider.divide_hand(tiles)[hand_index]


def _make_meld(
    meld_type: str,
    is_open: bool = True,
    man: Optional[str] = "",
    pin: Optional[str] = "",
    sou: Optional[str] = "",
    honors: Optional[str] = "",
) -> Meld:
    tiles = TilesConverter.string_to_136_array(man=man, pin=pin, sou=sou, honors=honors)
    meld = Meld(meld_type=meld_type, tiles=tiles, opened=is_open, called_tile=tiles[0], who=0)
    return meld


def _make_hand_config(
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
    player_wind: Optional[int] = None,
    round_wind: Optional[int] = None,
    has_open_tanyao: bool = False,
    has_aka_dora: bool = False,
    disable_double_yakuman: bool = False,
    renhou_as_yakuman: bool = False,
    allow_daisharin: bool = False,
    allow_daisharin_other_suits: bool = False,
    is_open_riichi: bool = False,
    has_sashikomi_yakuman: bool = False,
    limit_to_sextuple_yakuman: bool = True,
    paarenchan_needs_yaku: bool = True,
    has_daichisei: bool = False,
    paarenchan: int = 0,
) -> HandConfig:
    options = OptionalRules(
        has_open_tanyao=has_open_tanyao,
        has_aka_dora=has_aka_dora,
        has_double_yakuman=not disable_double_yakuman,
        renhou_as_yakuman=renhou_as_yakuman,
        has_daisharin=allow_daisharin,
        has_daisharin_other_suits=allow_daisharin_other_suits,
        has_daichisei=has_daichisei,
        has_sashikomi_yakuman=has_sashikomi_yakuman,
        limit_to_sextuple_yakuman=limit_to_sextuple_yakuman,
        paarenchan_needs_yaku=paarenchan_needs_yaku,
    )
    return HandConfig(
        is_tsumo=is_tsumo,
        is_riichi=is_riichi,
        is_ippatsu=is_ippatsu,
        is_rinshan=is_rinshan,
        is_chankan=is_chankan,
        is_haitei=is_haitei,
        is_houtei=is_houtei,
        is_daburu_riichi=is_daburu_riichi,
        is_nagashi_mangan=is_nagashi_mangan,
        is_tenhou=is_tenhou,
        is_renhou=is_renhou,
        is_chiihou=is_chiihou,
        player_wind=player_wind,
        round_wind=round_wind,
        is_open_riichi=is_open_riichi,
        paarenchan=paarenchan,
        options=options,
    )
