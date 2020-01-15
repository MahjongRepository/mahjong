# -*- coding: utf-8 -*-
from itertools import count

from mahjong.hand_calculating.yaku_list import AkaDora, Riichi, Ippatsu, Chankan, Rinshan, Haitei, Houtei, \
    DaburuRiichi, NagashiMangan, Renhou, Pinfu, Tanyao, Iipeiko, Haku, Hatsu, Chun, YakuhaiOfPlace, YakuhaiOfRound, \
    YakuhaiEast, YakuhaiSouth, YakuhaiWest, YakuhaiNorth, Sanshoku, Ittsu, Chanta, Honroto, Toitoi, Sanankou, \
    SanKantsu, SanshokuDoukou, Chiitoitsu, Shosangen, Honitsu, Junchan, Ryanpeikou, Chinitsu, Tsumo, Dora
from mahjong.hand_calculating.yaku_list.yakuman import KokushiMusou, ChuurenPoutou, Suuankou, Daisangen, Shousuushii, \
    Ryuuiisou, Suukantsu, Tsuuiisou, Chinroutou, DaiSuushii, DaburuKokushiMusou, SuuankouTanki, DaburuChuurenPoutou, \
    Tenhou, Chiihou, RenhouYakuman, Daisharin


class YakuConfig(object):

    def __init__(self):
        id = count(0)

        # Yaku situations
        self.tsumo = Tsumo(next(id))
        self.riichi = Riichi(next(id))
        self.ippatsu = Ippatsu(next(id))
        self.chankan = Chankan(next(id))
        self.rinshan = Rinshan(next(id))
        self.haitei = Haitei(next(id))
        self.houtei = Houtei(next(id))
        self.daburu_riichi = DaburuRiichi(next(id))
        self.nagashi_mangan = NagashiMangan(next(id))
        self.renhou = Renhou(next(id))

        # Yaku 1 Hands
        self.pinfu = Pinfu(next(id))
        self.tanyao = Tanyao(next(id))
        self.iipeiko = Iipeiko(next(id))
        self.haku = Haku(next(id))
        self.hatsu = Hatsu(next(id))
        self.chun = Chun(next(id))

        self.east = YakuhaiEast(next(id))
        self.south = YakuhaiSouth(next(id))
        self.west = YakuhaiWest(next(id))
        self.north = YakuhaiNorth(next(id))
        self.yakuhai_place = YakuhaiOfPlace(next(id))
        self.yakuhai_round = YakuhaiOfRound(next(id))

        # Yaku 2 Hands
        self.sanshoku = Sanshoku(next(id))
        self.ittsu = Ittsu(next(id))
        self.chanta = Chanta(next(id))
        self.honroto = Honroto(next(id))
        self.toitoi = Toitoi(next(id))
        self.sanankou = Sanankou(next(id))
        self.sankantsu = SanKantsu(next(id))
        self.sanshoku_douko = SanshokuDoukou(next(id))
        self.chiitoitsu = Chiitoitsu(next(id))
        self.shosangen = Shosangen(next(id))

        # Yaku 3 Hands
        self.honitsu = Honitsu(next(id))
        self.junchan = Junchan(next(id))
        self.ryanpeiko = Ryanpeikou(next(id))

        # Yaku 6 Hands
        self.chinitsu = Chinitsu(next(id))

        # Yakuman list
        self.kokushi = KokushiMusou(next(id))
        self.chuuren_poutou = ChuurenPoutou(next(id))
        self.suuankou = Suuankou(next(id))
        self.daisangen = Daisangen(next(id))
        self.shosuushi = Shousuushii(next(id))
        self.ryuisou = Ryuuiisou(next(id))
        self.suukantsu = Suukantsu(next(id))
        self.tsuisou = Tsuuiisou(next(id))
        self.chinroto = Chinroutou(next(id))
        self.daisharin = Daisharin(next(id))

        # Double yakuman
        self.daisuushi = DaiSuushii(next(id))
        self.daburu_kokushi = DaburuKokushiMusou(next(id))
        self.suuankou_tanki = SuuankouTanki(next(id))
        self.daburu_chuuren_poutou = DaburuChuurenPoutou(next(id))

        # Yakuman situations
        self.tenhou = Tenhou(next(id))
        self.chiihou = Chiihou(next(id))
        self.renhou_yakuman = RenhouYakuman(next(id))

        # Other
        self.dora = Dora(next(id))
        self.aka_dora = AkaDora(next(id))
