from collections.abc import Collection

from mahjong.agari import Agari
from mahjong.constants import CHUN, EAST, HAKU, HATSU, NORTH, SOUTH, WEST
from mahjong.hand_calculating.divider import HandDivider
from mahjong.hand_calculating.fu import FuCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.hand_calculating.hand_response import HandResponse
from mahjong.hand_calculating.scores import Aotenjou, ScoresCalculator
from mahjong.meld import Meld
from mahjong.tile import TilesConverter
from mahjong.utils import is_aka_dora, is_chi, is_kan, is_pon, plus_dora

_DEFAULT_CONFIG = HandConfig()


class HandCalculator:
    ERR_NO_WINNING_TILE = "winning_tile_not_in_hand"
    ERR_OPEN_HAND_RIICHI = "open_hand_riichi_not_allowed"
    ERR_OPEN_HAND_DABURI = "open_hand_daburi_not_allowed"
    ERR_IPPATSU_WITHOUT_RIICHI = "ippatsu_without_riichi_not_allowed"
    ERR_HAND_NOT_WINNING = "hand_not_winning"
    ERR_HAND_NOT_CORRECT = "hand_not_correct"
    ERR_NO_YAKU = "no_yaku"
    ERR_CHANKAN_WITH_TSUMO = "chankan_with_tsumo_not_allowed"
    ERR_RINSHAN_WITHOUT_TSUMO = "rinshan_without_tsumo_not_allowed"
    ERR_HAITEI_WITHOUT_TSUMO = "haitei_without_tsumo_not_allowed"
    ERR_HOUTEI_WITH_TSUMO = "houtei_with_tsumo_not_allowed"
    ERR_HAITEI_WITH_RINSHAN = "haitei_with_rinshan_not_allowed"
    ERR_HOUTEI_WITH_CHANKAN = "houtei_with_chankan_not_allowed"
    ERR_TENHOU_NOT_AS_DEALER = "tenhou_not_as_dealer_not_allowed"
    ERR_TENHOU_WITHOUT_TSUMO = "tenhou_without_tsumo_not_allowed"
    ERR_TENHOU_WITH_MELD = "tenhou_with_meld_not_allowed"
    ERR_CHIIHOU_AS_DEALER = "chiihou_as_dealer_not_allowed"
    ERR_CHIIHOU_WITHOUT_TSUMO = "chiihou_without_tsumo_not_allowed"
    ERR_CHIIHOU_WITH_MELD = "chiihou_with_meld_not_allowed"
    ERR_RENHOU_AS_DEALER = "renhou_as_dealer_not_allowed"
    ERR_RENHOU_WITH_TSUMO = "renhou_with_tsumo_not_allowed"
    ERR_RENHOU_WITH_MELD = "renhou_with_meld_not_allowed"

    # more possible errors, like tenhou and haitei can't be together (so complicated :<)

    @staticmethod
    def estimate_hand_value(
        tiles: Collection[int],
        win_tile: int,
        melds: Collection[Meld] | None = None,
        dora_indicators: Collection[int] | None = None,
        config: HandConfig | None = None,
        scores_calculator_factory: type[ScoresCalculator] = ScoresCalculator,
    ) -> HandResponse:
        """
        :param tiles: array with 14 tiles in 136-tile format
        :param win_tile: 136 format tile that caused win (ron or tsumo)
        :param melds: array with Meld objects
        :param dora_indicators: array of tiles in 136-tile format
        :param config: HandConfig object
        :param use_hand_divider_cache: could be useful if you are calculating a lot of menchin hands
        :return: HandResponse object
        """

        if not melds:
            melds = []

        if not dora_indicators:
            dora_indicators = []

        config = config or _DEFAULT_CONFIG

        hand_yaku = []
        scores_calculator = scores_calculator_factory()
        tiles_34 = TilesConverter.to_34_array(tiles)

        is_aotenjou = isinstance(scores_calculator, Aotenjou)

        opened_melds = [x.tiles_34 for x in melds if x.opened]
        all_melds = [x.tiles_34 for x in melds]
        is_open_hand = len(opened_melds) > 0

        # special situation
        if config.is_nagashi_mangan:
            hand_yaku.append(config.yaku.nagashi_mangan)
            fu = 30
            han = config.yaku.nagashi_mangan.han_closed
            cost = scores_calculator.calculate_scores(han, fu, config, False)
            return HandResponse(cost, han, fu, hand_yaku)

        if win_tile not in tiles:
            return HandResponse(error=HandCalculator.ERR_NO_WINNING_TILE)

        if config.is_riichi and not config.is_daburu_riichi and is_open_hand:
            return HandResponse(error=HandCalculator.ERR_OPEN_HAND_RIICHI)

        if config.is_daburu_riichi and is_open_hand:
            return HandResponse(error=HandCalculator.ERR_OPEN_HAND_DABURI)

        if config.is_ippatsu and not config.is_riichi and not config.is_daburu_riichi:
            return HandResponse(error=HandCalculator.ERR_IPPATSU_WITHOUT_RIICHI)

        if config.is_chankan and config.is_tsumo:
            return HandResponse(error=HandCalculator.ERR_CHANKAN_WITH_TSUMO)

        if config.is_rinshan and not config.is_tsumo:
            return HandResponse(error=HandCalculator.ERR_RINSHAN_WITHOUT_TSUMO)

        if config.is_haitei and not config.is_tsumo:
            return HandResponse(error=HandCalculator.ERR_HAITEI_WITHOUT_TSUMO)

        if config.is_houtei and config.is_tsumo:
            return HandResponse(error=HandCalculator.ERR_HOUTEI_WITH_TSUMO)

        if config.is_haitei and config.is_rinshan:
            return HandResponse(error=HandCalculator.ERR_HAITEI_WITH_RINSHAN)

        if config.is_houtei and config.is_chankan:
            return HandResponse(error=HandCalculator.ERR_HOUTEI_WITH_CHANKAN)

        # raise error only when player wind is defined (and is *not* EAST)
        if config.is_tenhou and config.player_wind and not config.is_dealer:
            return HandResponse(error=HandCalculator.ERR_TENHOU_NOT_AS_DEALER)

        if config.is_tenhou and not config.is_tsumo:
            return HandResponse(error=HandCalculator.ERR_TENHOU_WITHOUT_TSUMO)

        if config.is_tenhou and melds:
            return HandResponse(error=HandCalculator.ERR_TENHOU_WITH_MELD)

        # raise error only when player wind is defined (and is EAST)
        if config.is_chiihou and config.player_wind and config.is_dealer:
            return HandResponse(error=HandCalculator.ERR_CHIIHOU_AS_DEALER)

        if config.is_chiihou and not config.is_tsumo:
            return HandResponse(error=HandCalculator.ERR_CHIIHOU_WITHOUT_TSUMO)

        if config.is_chiihou and melds:
            return HandResponse(error=HandCalculator.ERR_CHIIHOU_WITH_MELD)

        # raise error only when player wind is defined (and is EAST)
        if config.is_renhou and config.player_wind and config.is_dealer:
            return HandResponse(error=HandCalculator.ERR_RENHOU_AS_DEALER)

        if config.is_renhou and config.is_tsumo:
            return HandResponse(error=HandCalculator.ERR_RENHOU_WITH_TSUMO)

        if config.is_renhou and melds:
            return HandResponse(error=HandCalculator.ERR_RENHOU_WITH_MELD)

        if not Agari.is_agari(tiles_34, all_melds):
            return HandResponse(error=HandCalculator.ERR_HAND_NOT_WINNING)

        if not config.options.has_double_yakuman:
            config.yaku.daburu_kokushi.han_closed = 13
            config.yaku.suuankou_tanki.han_closed = 13
            config.yaku.daburu_chuuren_poutou.han_closed = 13
            config.yaku.daisuushi.han_closed = 13
            config.yaku.daisuushi.han_open = 13

        hand_options = HandDivider.divide_hand(tiles_34, melds)

        calculated_hands = []
        for hand in hand_options:
            is_chiitoitsu = config.yaku.chiitoitsu.is_condition_met(hand)
            valued_tiles = [HAKU, HATSU, CHUN, config.player_wind, config.round_wind]

            win_groups = HandCalculator._find_win_groups(win_tile, hand, opened_melds)
            for win_group in win_groups:
                cost = None
                error = None
                hand_yaku = []
                han = 0

                fu_details, fu = FuCalculator.calculate_fu(hand, win_tile, win_group, config, valued_tiles, melds)

                is_pinfu = len(fu_details) == 1 and not is_chiitoitsu and not is_open_hand

                pon_sets = [x for x in hand if is_pon(x)]
                kan_sets = [x for x in hand if is_kan(x)]
                chi_sets = [x for x in hand if is_chi(x)]

                if config.is_tsumo:
                    if not is_open_hand:
                        hand_yaku.append(config.yaku.tsumo)

                if is_pinfu:
                    hand_yaku.append(config.yaku.pinfu)

                if is_chiitoitsu:
                    hand_yaku.append(config.yaku.chiitoitsu)

                if config.options.has_daisharin:
                    is_daisharin = config.yaku.daisharin.is_condition_met(
                        hand, config.options.has_daisharin_other_suits
                    )
                    if is_daisharin:
                        config.yaku.daisharin.rename(hand)
                        hand_yaku.append(config.yaku.daisharin)

                if config.options.has_daichisei and config.yaku.daichisei.is_condition_met(hand):
                    hand_yaku.append(config.yaku.daichisei)

                if (not is_open_hand or config.options.has_open_tanyao) and config.yaku.tanyao.is_condition_met(hand):
                    hand_yaku.append(config.yaku.tanyao)

                if config.is_riichi and not config.is_daburu_riichi:
                    if config.is_open_riichi:
                        hand_yaku.append(config.yaku.open_riichi)
                    else:
                        hand_yaku.append(config.yaku.riichi)

                if config.is_daburu_riichi:
                    if config.is_open_riichi:
                        hand_yaku.append(config.yaku.daburu_open_riichi)
                    else:
                        hand_yaku.append(config.yaku.daburu_riichi)

                if (
                    not config.is_tsumo
                    and config.options.has_sashikomi_yakuman
                    and ((config.yaku.daburu_open_riichi in hand_yaku) or (config.yaku.open_riichi in hand_yaku))
                ):
                    hand_yaku.append(config.yaku.sashikomi)

                if config.is_ippatsu:
                    hand_yaku.append(config.yaku.ippatsu)

                if config.is_rinshan:
                    hand_yaku.append(config.yaku.rinshan)

                if config.is_chankan:
                    hand_yaku.append(config.yaku.chankan)

                if config.is_haitei:
                    hand_yaku.append(config.yaku.haitei)

                if config.is_houtei:
                    hand_yaku.append(config.yaku.houtei)

                if config.is_renhou:
                    if config.options.renhou_as_yakuman:
                        hand_yaku.append(config.yaku.renhou_yakuman)
                    else:
                        hand_yaku.append(config.yaku.renhou)

                if config.is_tenhou:
                    hand_yaku.append(config.yaku.tenhou)

                if config.is_chiihou:
                    hand_yaku.append(config.yaku.chiihou)

                # chinitsu and honitsu are mutually exclusive
                if config.yaku.chinitsu.is_condition_met(hand):
                    hand_yaku.append(config.yaku.chinitsu)
                elif config.yaku.honitsu.is_condition_met(hand):
                    hand_yaku.append(config.yaku.honitsu)

                # tsuisou, honroto, chinroto require no chi sets (chi involves suited middle tiles)
                if not chi_sets:
                    if config.yaku.tsuisou.is_condition_met(hand):
                        hand_yaku.append(config.yaku.tsuisou)

                    if config.yaku.honroto.is_condition_met(hand):
                        hand_yaku.append(config.yaku.honroto)

                    if config.yaku.chinroto.is_condition_met(hand):
                        hand_yaku.append(config.yaku.chinroto)

                if config.yaku.ryuisou.is_condition_met(hand):
                    hand_yaku.append(config.yaku.ryuisou)

                if config.paarenchan > 0 and not config.options.paarenchan_needs_yaku:
                    # if no yaku is even needed to win on paarenchan and it is paarenchan condition, just add paarenchan
                    config.yaku.paarenchan.set_paarenchan_count(config.paarenchan)
                    hand_yaku.append(config.yaku.paarenchan)

                # small optimization, try to detect yaku with chi required sets only if we have chi sets in hand
                if chi_sets:
                    if config.yaku.chantai.is_condition_met(hand):
                        hand_yaku.append(config.yaku.chantai)

                    if config.yaku.junchan.is_condition_met(hand):
                        hand_yaku.append(config.yaku.junchan)

                    if config.yaku.ittsu.is_condition_met(hand):
                        hand_yaku.append(config.yaku.ittsu)

                    if not is_open_hand:
                        if config.yaku.ryanpeiko.is_condition_met(hand):
                            hand_yaku.append(config.yaku.ryanpeiko)
                        elif config.yaku.iipeiko.is_condition_met(hand):
                            hand_yaku.append(config.yaku.iipeiko)

                    if config.yaku.sanshoku.is_condition_met(hand):
                        hand_yaku.append(config.yaku.sanshoku)

                # small optimization, try to detect yaku with pon required sets only if we have pon sets in hand
                if pon_sets or kan_sets:
                    if config.yaku.toitoi.is_condition_met(hand):
                        hand_yaku.append(config.yaku.toitoi)

                    if config.yaku.sanankou.is_condition_met(hand, win_tile, melds, config.is_tsumo):
                        hand_yaku.append(config.yaku.sanankou)

                    if config.yaku.sanshoku_douko.is_condition_met(hand):
                        hand_yaku.append(config.yaku.sanshoku_douko)

                    if config.yaku.shosangen.is_condition_met(hand):
                        hand_yaku.append(config.yaku.shosangen)

                    if config.yaku.haku.is_condition_met(hand):
                        hand_yaku.append(config.yaku.haku)

                    if config.yaku.hatsu.is_condition_met(hand):
                        hand_yaku.append(config.yaku.hatsu)

                    if config.yaku.chun.is_condition_met(hand):
                        hand_yaku.append(config.yaku.chun)

                    if config.yaku.east.is_condition_met(hand, config.player_wind, config.round_wind):
                        if config.player_wind == EAST:
                            hand_yaku.append(config.yaku.yakuhai_place)

                        if config.round_wind == EAST:
                            hand_yaku.append(config.yaku.yakuhai_round)

                    if config.yaku.south.is_condition_met(hand, config.player_wind, config.round_wind):
                        if config.player_wind == SOUTH:
                            hand_yaku.append(config.yaku.yakuhai_place)

                        if config.round_wind == SOUTH:
                            hand_yaku.append(config.yaku.yakuhai_round)

                    if config.yaku.west.is_condition_met(hand, config.player_wind, config.round_wind):
                        if config.player_wind == WEST:
                            hand_yaku.append(config.yaku.yakuhai_place)

                        if config.round_wind == WEST:
                            hand_yaku.append(config.yaku.yakuhai_round)

                    if config.yaku.north.is_condition_met(hand, config.player_wind, config.round_wind):
                        if config.player_wind == NORTH:
                            hand_yaku.append(config.yaku.yakuhai_place)

                        if config.round_wind == NORTH:
                            hand_yaku.append(config.yaku.yakuhai_round)

                    if config.yaku.daisangen.is_condition_met(hand):
                        hand_yaku.append(config.yaku.daisangen)

                    if config.yaku.shosuushi.is_condition_met(hand):
                        hand_yaku.append(config.yaku.shosuushi)

                    if config.yaku.daisuushi.is_condition_met(hand):
                        hand_yaku.append(config.yaku.daisuushi)

                    # closed kan can't be used in chuuren_poutou
                    if not melds and config.yaku.chuuren_poutou.is_condition_met(hand):
                        if tiles_34[win_tile // 4] == 2 or tiles_34[win_tile // 4] == 4:
                            hand_yaku.append(config.yaku.daburu_chuuren_poutou)
                        else:
                            hand_yaku.append(config.yaku.chuuren_poutou)

                    if not is_open_hand and config.yaku.suuankou.is_condition_met(hand, win_tile, config.is_tsumo):
                        if tiles_34[win_tile // 4] == 2:
                            hand_yaku.append(config.yaku.suuankou_tanki)
                        else:
                            hand_yaku.append(config.yaku.suuankou)

                    if config.yaku.sankantsu.is_condition_met(hand, melds):
                        hand_yaku.append(config.yaku.sankantsu)

                    if config.yaku.suukantsu.is_condition_met(hand, melds):
                        hand_yaku.append(config.yaku.suukantsu)

                if config.paarenchan > 0 and config.options.paarenchan_needs_yaku and len(hand_yaku) > 0:
                    # we waited until here to add paarenchan yakuman only if there is any other yaku
                    config.yaku.paarenchan.set_paarenchan_count(config.paarenchan)
                    hand_yaku.append(config.yaku.paarenchan)

                # yakuman is not connected with other yaku
                yakuman_list = [x for x in hand_yaku if x.is_yakuman]
                if yakuman_list:
                    if not is_aotenjou:
                        hand_yaku = yakuman_list
                    else:
                        scores_calculator.aotenjou_filter_yaku(hand_yaku, config)
                        yakuman_list = []

                # calculate han
                for item in hand_yaku:
                    if is_open_hand and item.han_open:
                        han += item.han_open
                    else:
                        han += item.han_closed

                if han == 0:
                    error = HandCalculator.ERR_NO_YAKU
                    cost = None

                # we don't need to add dora to yakuman
                if not yakuman_list:
                    tiles_for_dora = list(tiles)

                    count_of_dora = 0
                    count_of_aka_dora = 0

                    for tile in tiles_for_dora:
                        count_of_dora += plus_dora(tile, dora_indicators)

                    for tile in tiles_for_dora:
                        if is_aka_dora(tile, config.options.has_aka_dora):
                            count_of_aka_dora += 1

                    if count_of_dora:
                        config.yaku.dora.han_open = count_of_dora
                        config.yaku.dora.han_closed = count_of_dora
                        hand_yaku.append(config.yaku.dora)
                        han += count_of_dora

                    if count_of_aka_dora:
                        config.yaku.aka_dora.han_open = count_of_aka_dora
                        config.yaku.aka_dora.han_closed = count_of_aka_dora
                        hand_yaku.append(config.yaku.aka_dora)
                        han += count_of_aka_dora

                if not is_aotenjou and (config.options.limit_to_sextuple_yakuman and han > 78):
                    han = 78

                if not error:
                    cost = scores_calculator.calculate_scores(han, fu, config, len(yakuman_list) > 0)

                calculated_hand = {
                    "cost": cost,
                    "error": error,
                    "hand_yaku": hand_yaku,
                    "han": han,
                    "fu": fu,
                    "fu_details": fu_details,
                }

                calculated_hands.append(calculated_hand)

        # exception hand
        if not is_open_hand and config.yaku.kokushi.is_condition_met(None, tiles_34):
            if tiles_34[win_tile // 4] == 2:
                hand_yaku.append(config.yaku.daburu_kokushi)
            else:
                hand_yaku.append(config.yaku.kokushi)

            if not config.is_tsumo and config.options.has_sashikomi_yakuman:
                if config.is_riichi and not config.is_daburu_riichi:
                    if config.is_open_riichi:
                        hand_yaku.append(config.yaku.sashikomi)

                if config.is_daburu_riichi:
                    if config.is_open_riichi:
                        hand_yaku.append(config.yaku.sashikomi)

            if config.is_renhou and config.options.renhou_as_yakuman:
                hand_yaku.append(config.yaku.renhou_yakuman)

            if config.is_tenhou:
                hand_yaku.append(config.yaku.tenhou)

            if config.is_chiihou:
                hand_yaku.append(config.yaku.chiihou)

            if config.paarenchan > 0:
                config.yaku.paarenchan.set_paarenchan_count(config.paarenchan)
                hand_yaku.append(config.yaku.paarenchan)

            # calculate han
            han = 0
            for item in hand_yaku:
                han += item.han_closed

            fu = 0
            if is_aotenjou:
                if config.is_tsumo:
                    fu = 30
                else:
                    fu = 40

                tiles_for_dora = list(tiles)

                count_of_dora = 0
                for tile in tiles_for_dora:
                    count_of_dora += plus_dora(tile, dora_indicators)

                if count_of_dora:
                    config.yaku.dora.han_open = count_of_dora
                    config.yaku.dora.han_closed = count_of_dora
                    hand_yaku.append(config.yaku.dora)
                    han += count_of_dora

            cost = scores_calculator.calculate_scores(han, fu, config, len(hand_yaku) > 0)
            calculated_hands.append(
                {"cost": cost, "error": None, "hand_yaku": hand_yaku, "han": han, "fu": fu, "fu_details": []}
            )

        if not calculated_hands:
            return HandResponse(error=HandCalculator.ERR_HAND_NOT_CORRECT)

        # find most expensive hand
        calculated_hands = sorted(calculated_hands, key=lambda x: (x["han"], x["fu"]), reverse=True)
        # correctly sort expensive hands by fu details
        calculated_hands = [
            x
            for x in calculated_hands
            if x["han"] == calculated_hands[0]["han"] and x["fu"] == calculated_hands[0]["fu"]
        ]
        calculated_hands = sorted(calculated_hands, key=lambda x: sum([y["fu"] for y in x["fu_details"]]), reverse=True)
        calculated_hand = calculated_hands[0]

        cost = calculated_hand["cost"]
        error = calculated_hand["error"]
        hand_yaku = calculated_hand["hand_yaku"]
        han = calculated_hand["han"]
        fu = calculated_hand["fu"]
        fu_details = calculated_hand["fu_details"]

        return HandResponse(cost, han, fu, hand_yaku, error, fu_details, is_open_hand)

    @staticmethod
    def _find_win_groups(win_tile: int, hand: list[list[int]], opened_melds: list[list[int]]) -> list[list[int]]:
        win_tile_34 = (win_tile or 0) // 4
        _opened_melds = opened_melds[:]

        # to detect win groups
        # we had to use only closed sets
        closed_set_items = []
        for x in hand:
            if x not in _opened_melds:
                closed_set_items.append(x)
            else:
                _opened_melds.remove(x)

        # for forms like 45666 and ron on 6
        # we can assume that ron was on 456 form and on 66 form
        # and depends on form we will have different hand cost
        # so, we had to check all possible win groups
        win_groups = [x for x in closed_set_items if win_tile_34 in x]
        unique_win_groups = [list(x) for x in {tuple(x) for x in win_groups}]

        return unique_win_groups
