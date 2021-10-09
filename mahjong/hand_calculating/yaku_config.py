from itertools import count

from mahjong.hand_calculating.yaku_list import (
    AkaDora,
    Chankan,
    Chantai,
    Chiitoitsu,
    Chinitsu,
    Chun,
    DaburuOpenRiichi,
    DaburuRiichi,
    Dora,
    Haitei,
    Haku,
    Hatsu,
    Honitsu,
    Honroto,
    Houtei,
    Iipeiko,
    Ippatsu,
    Ittsu,
    Junchan,
    NagashiMangan,
    OpenRiichi,
    Pinfu,
    Renhou,
    Riichi,
    Rinshan,
    Ryanpeikou,
    Sanankou,
    SanKantsu,
    Sanshoku,
    SanshokuDoukou,
    Shosangen,
    Tanyao,
    Toitoi,
    Tsumo,
    YakuhaiEast,
    YakuhaiNorth,
    YakuhaiOfPlace,
    YakuhaiOfRound,
    YakuhaiSouth,
    YakuhaiWest,
)
from mahjong.hand_calculating.yaku_list.yakuman import (
    Chiihou,
    Chinroutou,
    ChuurenPoutou,
    DaburuChuurenPoutou,
    DaburuKokushiMusou,
    Daichisei,
    Daisangen,
    Daisharin,
    DaiSuushii,
    KokushiMusou,
    Paarenchan,
    RenhouYakuman,
    Ryuuiisou,
    Sashikomi,
    Shousuushii,
    Suuankou,
    SuuankouTanki,
    Suukantsu,
    Tenhou,
    Tsuuiisou,
)


class YakuConfig:
    def __init__(self):
        id = count(0)

        # Yaku situations
        self.tsumo = Tsumo(next(id))
        self.riichi = Riichi(next(id))
        self.open_riichi = OpenRiichi(next(id))
        self.ippatsu = Ippatsu(next(id))
        self.chankan = Chankan(next(id))
        self.rinshan = Rinshan(next(id))
        self.haitei = Haitei(next(id))
        self.houtei = Houtei(next(id))
        self.daburu_riichi = DaburuRiichi(next(id))
        self.daburu_open_riichi = DaburuOpenRiichi(next(id))
        self.nagashi_mangan = NagashiMangan(next(id))
        self.renhou = Renhou(next(id))

        # Yaku 1 Han
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

        # Yaku 2 Hans
        self.sanshoku = Sanshoku(next(id))
        self.ittsu = Ittsu(next(id))
        self.chantai = Chantai(next(id))
        self.honroto = Honroto(next(id))
        self.toitoi = Toitoi(next(id))
        self.sanankou = Sanankou(next(id))
        self.sankantsu = SanKantsu(next(id))
        self.sanshoku_douko = SanshokuDoukou(next(id))
        self.chiitoitsu = Chiitoitsu(next(id))
        self.shosangen = Shosangen(next(id))

        # Yaku 3 Hans
        self.honitsu = Honitsu(next(id))
        self.junchan = Junchan(next(id))
        self.ryanpeiko = Ryanpeikou(next(id))

        # Yaku 6 Hans
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
        self.daichisei = Daichisei(next(id))

        # Double yakuman
        self.daisuushi = DaiSuushii(next(id))
        self.daburu_kokushi = DaburuKokushiMusou(next(id))
        self.suuankou_tanki = SuuankouTanki(next(id))
        self.daburu_chuuren_poutou = DaburuChuurenPoutou(next(id))

        # Yakuman situations
        self.tenhou = Tenhou(next(id))
        self.chiihou = Chiihou(next(id))
        self.renhou_yakuman = RenhouYakuman(next(id))
        self.sashikomi = Sashikomi(next(id))
        self.paarenchan = Paarenchan(next(id))

        # Other
        self.dora = Dora(next(id))
        self.aka_dora = AkaDora(next(id))
