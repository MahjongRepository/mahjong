# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku_list import *
from mahjong.hand_calculating.yaku_list.east import YakuhaiEast
from mahjong.hand_calculating.yaku_list.north import YakuhaiNorth
from mahjong.hand_calculating.yaku_list.south import YakuhaiSouth
from mahjong.hand_calculating.yaku_list.west import YakuhaiWest
from mahjong.hand_calculating.yaku_list.yakuman import *


class YakuConfig(object):
    # Yaku situations
    tsumo = AkaDora()
    riichi = Riichi()
    ippatsu = Ippatsu()
    chankan = Chankan()
    rinshan = Rinshan()
    haitei = Haitei()
    houtei = Houtei()
    daburu_riichi = DaburuRiichi()
    nagashi_mangan = NagashiMangan()
    renhou = Renhou()

    # Yaku 1 Hands
    pinfu = Pinfu()
    tanyao = Tanyao()
    iipeiko = Iipeiko()
    haku = Haku()
    hatsu = Hatsu()
    chun = Chun()

    east = YakuhaiEast()
    south = YakuhaiSouth()
    west = YakuhaiWest()
    north = YakuhaiNorth()
    yakuhai_place = YakuhaiOfPlace()
    yakuhai_round = YakuhaiOfRound()

    # Yaku 2 Hands
    sanshoku = Sanshoku()
    ittsu = Ittsu()
    chanta = Chanta()
    honroto = Honroto()
    toitoi = Toitoi()
    sanankou = Sanankou()
    sankantsu = SanKantsu()
    sanshoku_douko = SanshokuDoukou()
    chiitoitsu = Chiitoitsu()
    shosangen = Shosangen()

    # Yaku 3 Hands
    honitsu = Honitsu()
    junchan = Junchan()
    ryanpeiko = Ryanpeikou()

    # Yaku 6 Hands
    chinitsu = Chinitsu()

    # Yakuman list
    kokushi = KokushiMusou()
    chuuren_poutou = ChuurenPoutou()
    suuankou = Suuankou()
    daisangen = Daisangen()
    shosuushi = Shousuushii()
    ryuisou = Ryuuiisou()
    suukantsu = Suukantsu()
    tsuisou = Tsuuiisou()
    chinroto = Chinroutou()

    # Double yakuman
    daisuushi = DaiSuushii()
    daburu_kokushi = DaburuKokushiMusou()
    suuankou_tanki = SuuankouTanki()
    daburu_chuuren_poutou = DaburuChuurenPoutou()

    # Yakuman situations
    tenhou = Tenhou()
    chiihou = Chiihou()

    # Other
    dora = Dora()
    aka_dora = AkaDora()
