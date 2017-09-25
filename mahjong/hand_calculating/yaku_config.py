# -*- coding: utf-8 -*-
from mahjong.hand_calculating.yaku_list import AkaDora, Riichi, Ippatsu, Chankan, Rinshan, Haitei, Houtei, \
    DaburuRiichi, NagashiMangan, Renhou, Pinfu, Tanyao, Iipeiko, Haku, Hatsu, Chun, YakuhaiOfPlace, YakuhaiOfRound, \
    YakuhaiEast, YakuhaiSouth, YakuhaiWest, YakuhaiNorth, Sanshoku, Ittsu, Chanta, Honroto, Toitoi, Sanankou, \
    SanKantsu, SanshokuDoukou, Chiitoitsu, Shosangen, Honitsu, Junchan, Ryanpeikou, Chinitsu, Tsumo, Dora
from mahjong.hand_calculating.yaku_list.yakuman import KokushiMusou, ChuurenPoutou, Suuankou, Daisangen, Shousuushii, \
    Ryuuiisou, Suukantsu, Tsuuiisou, Chinroutou, DaiSuushii, DaburuKokushiMusou, SuuankouTanki, DaburuChuurenPoutou, \
    Tenhou, Chiihou


class YakuConfig(object):

    def __init__(self):
        # Yaku situations
        self.tsumo = Tsumo()
        self.riichi = Riichi()
        self.ippatsu = Ippatsu()
        self.chankan = Chankan()
        self.rinshan = Rinshan()
        self.haitei = Haitei()
        self.houtei = Houtei()
        self.daburu_riichi = DaburuRiichi()
        self.nagashi_mangan = NagashiMangan()
        self.renhou = Renhou()

        # Yaku 1 Hands
        self.pinfu = Pinfu()
        self.tanyao = Tanyao()
        self.iipeiko = Iipeiko()
        self.haku = Haku()
        self.hatsu = Hatsu()
        self.chun = Chun()

        self.east = YakuhaiEast()
        self.south = YakuhaiSouth()
        self.west = YakuhaiWest()
        self.north = YakuhaiNorth()
        self.yakuhai_place = YakuhaiOfPlace()
        self.yakuhai_round = YakuhaiOfRound()

        # Yaku 2 Hands
        self.sanshoku = Sanshoku()
        self.ittsu = Ittsu()
        self.chanta = Chanta()
        self.honroto = Honroto()
        self.toitoi = Toitoi()
        self.sanankou = Sanankou()
        self.sankantsu = SanKantsu()
        self.sanshoku_douko = SanshokuDoukou()
        self.chiitoitsu = Chiitoitsu()
        self.shosangen = Shosangen()

        # Yaku 3 Hands
        self.honitsu = Honitsu()
        self.junchan = Junchan()
        self.ryanpeiko = Ryanpeikou()

        # Yaku 6 Hands
        self.chinitsu = Chinitsu()

        # Yakuman list
        self.kokushi = KokushiMusou()
        self.chuuren_poutou = ChuurenPoutou()
        self.suuankou = Suuankou()
        self.daisangen = Daisangen()
        self.shosuushi = Shousuushii()
        self.ryuisou = Ryuuiisou()
        self.suukantsu = Suukantsu()
        self.tsuisou = Tsuuiisou()
        self.chinroto = Chinroutou()

        # Double yakuman
        self.daisuushi = DaiSuushii()
        self.daburu_kokushi = DaburuKokushiMusou()
        self.suuankou_tanki = SuuankouTanki()
        self.daburu_chuuren_poutou = DaburuChuurenPoutou()

        # Yakuman situations
        self.tenhou = Tenhou()
        self.chiihou = Chiihou()

        # Other
        self.dora = Dora()
        self.aka_dora = AkaDora()
