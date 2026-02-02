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
    RoundWindEast,
    RoundWindNorth,
    RoundWindSouth,
    RoundWindWest,
    Ryanpeikou,
    Sanankou,
    SanKantsu,
    Sanshoku,
    SanshokuDoukou,
    SeatWindEast,
    SeatWindNorth,
    SeatWindSouth,
    SeatWindWest,
    Shosangen,
    Tanyao,
    Toitoi,
    Tsumo,
    UraDora,
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

YAKU_ID_TO_TENHOU_ID: dict[int, int] = {
    Tsumo().yaku_id: 0,
    Riichi().yaku_id: 1,
    Ippatsu().yaku_id: 2,
    Chankan().yaku_id: 3,
    Rinshan().yaku_id: 4,
    Haitei().yaku_id: 5,
    Houtei().yaku_id: 6,
    Pinfu().yaku_id: 7,
    Tanyao().yaku_id: 8,
    Iipeiko().yaku_id: 9,
    SeatWindEast().yaku_id: 10,
    SeatWindSouth().yaku_id: 11,
    SeatWindWest().yaku_id: 12,
    SeatWindNorth().yaku_id: 13,
    RoundWindEast().yaku_id: 14,
    RoundWindSouth().yaku_id: 15,
    RoundWindWest().yaku_id: 16,
    RoundWindNorth().yaku_id: 17,
    Haku().yaku_id: 18,
    Hatsu().yaku_id: 19,
    Chun().yaku_id: 20,
    DaburuRiichi().yaku_id: 21,
    Chiitoitsu().yaku_id: 22,
    Chantai().yaku_id: 23,
    Ittsu().yaku_id: 24,
    Sanshoku().yaku_id: 25,
    SanshokuDoukou().yaku_id: 26,
    SanKantsu().yaku_id: 27,
    Toitoi().yaku_id: 28,
    Sanankou().yaku_id: 29,
    Shosangen().yaku_id: 30,
    Honroto().yaku_id: 31,
    Ryanpeikou().yaku_id: 32,
    Junchan().yaku_id: 33,
    Honitsu().yaku_id: 34,
    Chinitsu().yaku_id: 35,
    Renhou().yaku_id: 36,
    Tenhou().yaku_id: 37,
    Chiihou().yaku_id: 38,
    Daisangen().yaku_id: 39,
    Suuankou().yaku_id: 40,
    SuuankouTanki().yaku_id: 41,
    Tsuuiisou().yaku_id: 42,
    Ryuuiisou().yaku_id: 43,
    Chinroutou().yaku_id: 44,
    ChuurenPoutou().yaku_id: 45,
    DaburuChuurenPoutou().yaku_id: 46,
    KokushiMusou().yaku_id: 47,
    DaburuKokushiMusou().yaku_id: 48,
    DaiSuushii().yaku_id: 49,
    Shousuushii().yaku_id: 50,
    Suukantsu().yaku_id: 51,
    Dora().yaku_id: 52,
    UraDora().yaku_id: 53,
    AkaDora().yaku_id: 54,
}


class YakuConfig:
    def __init__(self) -> None:
        # Yaku situations
        self.tsumo = Tsumo()
        self.riichi = Riichi()
        self.open_riichi = OpenRiichi()
        self.ippatsu = Ippatsu()
        self.chankan = Chankan()
        self.rinshan = Rinshan()
        self.haitei = Haitei()
        self.houtei = Houtei()
        self.daburu_riichi = DaburuRiichi()
        self.daburu_open_riichi = DaburuOpenRiichi()
        self.nagashi_mangan = NagashiMangan()
        self.renhou = Renhou()

        # Yaku 1 Han
        self.pinfu = Pinfu()
        self.tanyao = Tanyao()
        self.iipeiko = Iipeiko()
        self.haku = Haku()
        self.hatsu = Hatsu()
        self.chun = Chun()

        self.yakuhai_seat_east = SeatWindEast()
        self.yakuhai_seat_south = SeatWindSouth()
        self.yakuhai_seat_west = SeatWindWest()
        self.yakuhai_seat_north = SeatWindNorth()
        self.yakuhai_round_east = RoundWindEast()
        self.yakuhai_round_south = RoundWindSouth()
        self.yakuhai_round_west = RoundWindWest()
        self.yakuhai_round_north = RoundWindNorth()

        # Yaku 2 Hans
        self.sanshoku = Sanshoku()
        self.ittsu = Ittsu()
        self.chantai = Chantai()
        self.honroto = Honroto()
        self.toitoi = Toitoi()
        self.sanankou = Sanankou()
        self.sankantsu = SanKantsu()
        self.sanshoku_douko = SanshokuDoukou()
        self.chiitoitsu = Chiitoitsu()
        self.shosangen = Shosangen()

        # Yaku 3 Hans
        self.honitsu = Honitsu()
        self.junchan = Junchan()
        self.ryanpeiko = Ryanpeikou()

        # Yaku 6 Hans
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
        self.daisharin = Daisharin()
        self.daichisei = Daichisei()

        # Double yakuman
        self.daisuushi = DaiSuushii()
        self.daburu_kokushi = DaburuKokushiMusou()
        self.suuankou_tanki = SuuankouTanki()
        self.daburu_chuuren_poutou = DaburuChuurenPoutou()

        # Yakuman situations
        self.tenhou = Tenhou()
        self.chiihou = Chiihou()
        self.renhou_yakuman = RenhouYakuman()
        self.sashikomi = Sashikomi()
        self.paarenchan = Paarenchan()

        # Other
        self.dora = Dora()
        self.aka_dora = AkaDora()
        self.ura_dora = UraDora()
