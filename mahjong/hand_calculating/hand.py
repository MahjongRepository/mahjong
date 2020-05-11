# -*- coding: utf-8 -*-
from mahjong.agari import Agari
from mahjong.constants import EAST, SOUTH, WEST, NORTH, CHUN, HATSU, HAKU
from mahjong.hand_calculating.divider import HandDivider
from mahjong.hand_calculating.fu import FuCalculator
from mahjong.hand_calculating.scores import ScoresCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.hand_calculating.hand_response import HandResponse
from mahjong.meld import Meld
from mahjong.tile import TilesConverter
from mahjong.utils import is_chi, is_pon, plus_dora, is_aka_dora


class HandCalculator(object):
    config = None

    def estimate_hand_value(self, tiles, win_tile, melds=None, dora_indicators=None, config=None):
        """
        :param tiles: array with 14 tiles in 136-tile format
        :param win_tile: 136 format tile that caused win (ron or tsumo)
        :param melds: array with Meld objects
        :param dora_indicators: array of tiles in 136-tile format
        :param config: HandConfig object
        :return: HandResponse object
        """

        if not melds:
            melds = []

        if not dora_indicators:
            dora_indicators = []

        self.config = config or HandConfig()

        agari = Agari()
        hand_yaku = []
        scores_calculator = ScoresCalculator()
        tiles_34 = TilesConverter.to_34_array(tiles)
        divider = HandDivider()
        fu_calculator = FuCalculator()

        opened_melds = [x.tiles_34 for x in melds if x.opened]
        all_melds = [x.tiles_34 for x in melds]
        is_open_hand = len(opened_melds) > 0

        # special situation
        if self.config.is_nagashi_mangan:
            hand_yaku.append(self.config.yaku.nagashi_mangan)
            fu = 30
            han = self.config.yaku.nagashi_mangan.han_closed
            cost = scores_calculator.calculate_scores(han, fu, self.config, False)
            return HandResponse(cost, han, fu, hand_yaku)

        if win_tile not in tiles:
            return HandResponse(error="Win tile not in the hand")

        if self.config.is_riichi and is_open_hand:
            return HandResponse(error="Riichi can't be declared with open hand")

        if self.config.is_daburu_riichi and is_open_hand:
            return HandResponse(error="Daburu Riichi can't be declared with open hand")

        if self.config.is_ippatsu and is_open_hand:
            return HandResponse(error="Ippatsu can't be declared with open hand")

        if self.config.is_ippatsu and not self.config.is_riichi and not self.config.is_daburu_riichi:
            return HandResponse(error="Ippatsu can't be declared without riichi")

        if not agari.is_agari(tiles_34, all_melds):
            return HandResponse(error='Hand is not winning')

        if not self.config.options.has_double_yakuman:
            self.config.yaku.daburu_kokushi.han_closed = 13
            self.config.yaku.suuankou_tanki.han_closed = 13
            self.config.yaku.daburu_chuuren_poutou.han_closed = 13
            self.config.yaku.daisuushi.han_closed = 13
            self.config.yaku.daisuushi.han_open = 13

        hand_options = divider.divide_hand(tiles_34, melds)

        calculated_hands = []
        for hand in hand_options:
            is_chiitoitsu = self.config.yaku.chiitoitsu.is_condition_met(hand)
            valued_tiles = [HAKU, HATSU, CHUN, self.config.player_wind, self.config.round_wind]

            win_groups = self._find_win_groups(win_tile, hand, opened_melds)
            for win_group in win_groups:
                cost = None
                error = None
                hand_yaku = []
                han = 0

                fu_details, fu = fu_calculator.calculate_fu(
                    hand,
                    win_tile,
                    win_group,
                    self.config,
                    valued_tiles,
                    melds
                )

                is_pinfu = len(fu_details) == 1 and not is_chiitoitsu and not is_open_hand

                pon_sets = [x for x in hand if is_pon(x)]
                chi_sets = [x for x in hand if is_chi(x)]

                if self.config.is_tsumo:
                    if not is_open_hand:
                        hand_yaku.append(self.config.yaku.tsumo)

                if is_pinfu:
                    hand_yaku.append(self.config.yaku.pinfu)

                # let's skip hand that looks like chitoitsu, but it contains open sets
                if is_chiitoitsu and is_open_hand:
                    continue

                if is_chiitoitsu:
                    hand_yaku.append(self.config.yaku.chiitoitsu)

                is_daisharin = self.config.yaku.daisharin.is_condition_met(
                    hand,
                    self.config.options.has_daisharin_other_suits
                )
                if self.config.options.has_daisharin and is_daisharin:
                    self.config.yaku.daisharin.rename(hand)
                    hand_yaku.append(self.config.yaku.daisharin)

                is_tanyao = self.config.yaku.tanyao.is_condition_met(hand)
                if is_open_hand and not self.config.options.has_open_tanyao:
                    is_tanyao = False

                if is_tanyao:
                    hand_yaku.append(self.config.yaku.tanyao)

                if self.config.is_riichi and not self.config.is_daburu_riichi:
                    hand_yaku.append(self.config.yaku.riichi)

                if self.config.is_daburu_riichi:
                    hand_yaku.append(self.config.yaku.daburu_riichi)

                if self.config.is_ippatsu:
                    hand_yaku.append(self.config.yaku.ippatsu)

                if self.config.is_rinshan:
                    hand_yaku.append(self.config.yaku.rinshan)

                if self.config.is_chankan:
                    hand_yaku.append(self.config.yaku.chankan)

                if self.config.is_haitei:
                    hand_yaku.append(self.config.yaku.haitei)

                if self.config.is_houtei:
                    hand_yaku.append(self.config.yaku.houtei)

                if self.config.is_renhou:
                    if self.config.options.renhou_as_yakuman:
                        hand_yaku.append(self.config.yaku.renhou_yakuman)
                    else:
                        hand_yaku.append(self.config.yaku.renhou)

                if self.config.is_tenhou:
                    hand_yaku.append(self.config.yaku.tenhou)

                if self.config.is_chiihou:
                    hand_yaku.append(self.config.yaku.chiihou)

                if self.config.yaku.honitsu.is_condition_met(hand):
                    hand_yaku.append(self.config.yaku.honitsu)

                if self.config.yaku.chinitsu.is_condition_met(hand):
                    hand_yaku.append(self.config.yaku.chinitsu)

                if self.config.yaku.tsuisou.is_condition_met(hand):
                    hand_yaku.append(self.config.yaku.tsuisou)

                if self.config.yaku.honroto.is_condition_met(hand):
                    hand_yaku.append(self.config.yaku.honroto)

                if self.config.yaku.chinroto.is_condition_met(hand):
                    hand_yaku.append(self.config.yaku.chinroto)

                if self.config.yaku.ryuisou.is_condition_met(hand):
                    hand_yaku.append(self.config.yaku.ryuisou)

                # small optimization, try to detect yaku with chi required sets only if we have chi sets in hand
                if len(chi_sets):
                    if self.config.yaku.chanta.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.chanta)

                    if self.config.yaku.junchan.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.junchan)

                    if self.config.yaku.ittsu.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.ittsu)

                    if not is_open_hand:
                        if self.config.yaku.ryanpeiko.is_condition_met(hand):
                            hand_yaku.append(self.config.yaku.ryanpeiko)
                        elif self.config.yaku.iipeiko.is_condition_met(hand):
                            hand_yaku.append(self.config.yaku.iipeiko)

                    if self.config.yaku.sanshoku.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.sanshoku)

                # small optimization, try to detect yaku with pon required sets only if we have pon sets in hand
                if len(pon_sets):
                    if self.config.yaku.toitoi.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.toitoi)

                    if self.config.yaku.sanankou.is_condition_met(hand, win_tile, melds, self.config.is_tsumo):
                        hand_yaku.append(self.config.yaku.sanankou)

                    if self.config.yaku.sanshoku_douko.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.sanshoku_douko)

                    if self.config.yaku.shosangen.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.shosangen)

                    if self.config.yaku.haku.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.haku)

                    if self.config.yaku.hatsu.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.hatsu)

                    if self.config.yaku.chun.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.chun)

                    if self.config.yaku.east.is_condition_met(hand, self.config.player_wind, self.config.round_wind):
                        if self.config.player_wind == EAST:
                            hand_yaku.append(self.config.yaku.yakuhai_place)

                        if self.config.round_wind == EAST:
                            hand_yaku.append(self.config.yaku.yakuhai_round)

                    if self.config.yaku.south.is_condition_met(hand, self.config.player_wind, self.config.round_wind):
                        if self.config.player_wind == SOUTH:
                            hand_yaku.append(self.config.yaku.yakuhai_place)

                        if self.config.round_wind == SOUTH:
                            hand_yaku.append(self.config.yaku.yakuhai_round)

                    if self.config.yaku.west.is_condition_met(hand, self.config.player_wind, self.config.round_wind):
                        if self.config.player_wind == WEST:
                            hand_yaku.append(self.config.yaku.yakuhai_place)

                        if self.config.round_wind == WEST:
                            hand_yaku.append(self.config.yaku.yakuhai_round)

                    if self.config.yaku.north.is_condition_met(hand, self.config.player_wind, self.config.round_wind):
                        if self.config.player_wind == NORTH:
                            hand_yaku.append(self.config.yaku.yakuhai_place)

                        if self.config.round_wind == NORTH:
                            hand_yaku.append(self.config.yaku.yakuhai_round)

                    if self.config.yaku.daisangen.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.daisangen)

                    if self.config.yaku.shosuushi.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.shosuushi)

                    if self.config.yaku.daisuushi.is_condition_met(hand):
                        hand_yaku.append(self.config.yaku.daisuushi)

                    # closed kan can't be used in chuuren_poutou
                    if not len(melds) and self.config.yaku.chuuren_poutou.is_condition_met(hand):
                        if tiles_34[win_tile // 4] == 2 or tiles_34[win_tile // 4] == 4:
                            hand_yaku.append(self.config.yaku.daburu_chuuren_poutou)
                        else:
                            hand_yaku.append(self.config.yaku.chuuren_poutou)

                    if not is_open_hand and self.config.yaku.suuankou.is_condition_met(hand, win_tile,
                                                                                       self.config.is_tsumo):
                        if tiles_34[win_tile // 4] == 2:
                            hand_yaku.append(self.config.yaku.suuankou_tanki)
                        else:
                            hand_yaku.append(self.config.yaku.suuankou)

                    if self.config.yaku.sankantsu.is_condition_met(hand, melds):
                        hand_yaku.append(self.config.yaku.sankantsu)

                    if self.config.yaku.suukantsu.is_condition_met(hand, melds):
                        hand_yaku.append(self.config.yaku.suukantsu)

                # yakuman is not connected with other yaku
                yakuman_list = [x for x in hand_yaku if x.is_yakuman]
                if yakuman_list:
                    hand_yaku = yakuman_list

                # calculate han
                for item in hand_yaku:
                    if is_open_hand and item.han_open:
                        han += item.han_open
                    else:
                        han += item.han_closed

                if han == 0:
                    error = 'There are no yaku in the hand'
                    cost = None

                # we don't need to add dora to yakuman
                if not yakuman_list:
                    tiles_for_dora = tiles[:]

                    # we had to search for dora in kan fourth tiles as well
                    for meld in melds:
                        if meld.type == Meld.KAN or meld.type == Meld.CHANKAN:
                            tiles_for_dora.append(meld.tiles[3])

                    count_of_dora = 0
                    count_of_aka_dora = 0

                    for tile in tiles_for_dora:
                        count_of_dora += plus_dora(tile, dora_indicators)

                    for tile in tiles_for_dora:
                        if is_aka_dora(tile, self.config.options.has_aka_dora):
                            count_of_aka_dora += 1

                    if count_of_dora:
                        self.config.yaku.dora.han_open = count_of_dora
                        self.config.yaku.dora.han_closed = count_of_dora
                        hand_yaku.append(self.config.yaku.dora)
                        han += count_of_dora

                    if count_of_aka_dora:
                        self.config.yaku.aka_dora.han_open = count_of_aka_dora
                        self.config.yaku.aka_dora.han_closed = count_of_aka_dora
                        hand_yaku.append(self.config.yaku.aka_dora)
                        han += count_of_aka_dora

                if not error:
                    cost = scores_calculator.calculate_scores(han, fu, self.config, len(yakuman_list) > 0)

                calculated_hand = {
                    'cost': cost,
                    'error': error,
                    'hand_yaku': hand_yaku,
                    'han': han,
                    'fu': fu,
                    'fu_details': fu_details
                }

                calculated_hands.append(calculated_hand)

        # exception hand
        if not is_open_hand and self.config.yaku.kokushi.is_condition_met(None, tiles_34):
            if tiles_34[win_tile // 4] == 2:
                hand_yaku.append(self.config.yaku.daburu_kokushi)
            else:
                hand_yaku.append(self.config.yaku.kokushi)

            if self.config.is_renhou and self.config.options.renhou_as_yakuman:
                hand_yaku.append(self.config.yaku.renhou_yakuman)

            if self.config.is_tenhou:
                hand_yaku.append(self.config.yaku.tenhou)

            if self.config.is_chiihou:
                hand_yaku.append(self.config.yaku.chiihou)

            # calculate han
            han = 0
            for item in hand_yaku:
                if is_open_hand and item.han_open:
                    han += item.han_open
                else:
                    han += item.han_closed

            fu = 0
            cost = scores_calculator.calculate_scores(han, fu, self.config, len(hand_yaku) > 0)
            calculated_hands.append({
                'cost': cost,
                'error': None,
                'hand_yaku': hand_yaku,
                'han': han,
                'fu': fu,
                'fu_details': []
            })

        # let's use cost for most expensive hand
        calculated_hands = sorted(calculated_hands, key=lambda x: (x['han'], x['fu']), reverse=True)
        calculated_hand = calculated_hands[0]

        cost = calculated_hand['cost']
        error = calculated_hand['error']
        hand_yaku = calculated_hand['hand_yaku']
        han = calculated_hand['han']
        fu = calculated_hand['fu']
        fu_details = calculated_hand['fu_details']

        return HandResponse(cost, han, fu, hand_yaku, error, fu_details)

    def _find_win_groups(self, win_tile, hand, opened_melds):
        win_tile_34 = (win_tile or 0) // 4

        # to detect win groups
        # we had to use only closed sets
        closed_set_items = []
        for x in hand:
            if x not in opened_melds:
                closed_set_items.append(x)
            else:
                opened_melds.remove(x)

        # for forms like 45666 and ron on 6
        # we can assume that ron was on 456 form and on 66 form
        # and depends on form we will have different hand cost
        # so, we had to check all possible win groups
        win_groups = [x for x in closed_set_items if win_tile_34 in x]
        unique_win_groups = [list(x) for x in set(tuple(x) for x in win_groups)]

        return unique_win_groups
