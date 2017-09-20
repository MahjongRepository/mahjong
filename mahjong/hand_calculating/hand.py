# -*- coding: utf-8 -*-
from mahjong.agari import Agari
from mahjong.constants import EAST, SOUTH, WEST, NORTH, CHUN, HATSU, HAKU
from mahjong.hand_calculating.divider import HandDivider
from mahjong.hand_calculating.fu import HandFuCalculator
from mahjong.hand_calculating.scores import ScoresCalculator
from mahjong.hand_calculating.yaku_config import YakuConfig
from mahjong.meld import Meld
from mahjong.tile import TilesConverter
from mahjong.utils import is_chi, is_pon, plus_dora


class HandResponse(object):
    cost = None
    han = None
    fu = None
    fu_details = None
    yaku = None
    error = None

    def __init__(self, cost=None, han=None, fu=None, yaku=None, error=None, fu_details=None):
        self.cost = cost
        self.han = han
        self.fu = fu
        self.fu_details = fu_details
        self.yaku = yaku
        self.error = error


class FinishedHand(object):
    config = YakuConfig()

    def estimate_hand_value(self,
                            tiles,
                            win_tile,
                            is_tsumo=False,
                            is_riichi=False,
                            is_dealer=False,
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
                            melds=None,
                            dora_indicators=None,
                            player_wind=None,
                            round_wind=None,
                            has_open_tanyao=False,
                            has_aka_dora=False):
        """
        :param tiles: array with 14 tiles in 136-tile format
        :param win_tile: tile that caused win (ron or tsumo)
        :param is_tsumo:
        :param is_riichi:
        :param is_dealer:
        :param is_ippatsu:
        :param is_rinshan:
        :param is_chankan:
        :param is_haitei:
        :param is_houtei:
        :param is_tenhou:
        :param is_renhou:
        :param is_chiihou:
        :param is_daburu_riichi:
        :param is_nagashi_mangan:
        :param has_open_tanyao:
        :param has_aka_dora:
        :param melds: array with Meld objects
        :param dora_indicators: array of tiles in 136-tile format
        :param player_wind: index of player wind
        :param round_wind: index of round wind
        :return: HandResponse object
        """

        if not melds:
            melds = []

        opened_melds = [x.tiles_34 for x in melds if x.opened]
        is_open_hand = len(opened_melds) > 0
        win_tile_34 = (win_tile or 0) // 4

        # TODO Deprecated. Change it to melds in all places
        called_kan_indices = []
        kan_indices_136 = []
        for meld in melds:
            if meld.type == Meld.KAN or meld.type == Meld.CHANKAN:
                called_kan_indices.append(meld.tiles[0] // 4)
                kan_indices_136 = [meld.tiles[0]]

        if not dora_indicators:
            dora_indicators = []

        agari = Agari()
        hand_yaku = []
        scores_calculator = ScoresCalculator()

        # special situation
        if is_nagashi_mangan:
            hand_yaku.append(self.config.nagashi_mangan)
            fu = 30
            han = self.config.nagashi_mangan.han_closed
            cost = scores_calculator.calculate_scores(han, fu, is_tsumo, is_dealer)
            return HandResponse(cost, han, fu, hand_yaku)

        if win_tile not in tiles:
            return HandResponse(error="Win tile not in the hand")

        if is_riichi and is_open_hand:
            return HandResponse(error="Riichi can't be declared with open hand")

        if is_ippatsu and is_open_hand:
            return HandResponse(error="Ippatsu can't be declared with open hand")

        if is_ippatsu and not is_riichi and not is_daburu_riichi:
            return HandResponse(error="Ippatsu can't be declared without riichi")

        tiles_34 = TilesConverter.to_34_array(tiles)
        divider = HandDivider()
        fu_calculator = HandFuCalculator()

        if not agari.is_agari(tiles_34, opened_melds):
            return HandResponse(error='Hand is not winning')

        hand_options = divider.divide_hand(tiles_34, opened_melds, called_kan_indices)

        calculated_hands = []
        for hand in hand_options:
            is_chitoitsu = self.config.chiitoitsu.is_condition_met(hand)
            valued_tiles = [HAKU, HATSU, CHUN, player_wind, round_wind]

            # to detect win groups
            # we had to use only closed sets
            # and we had to filter sets that in open hand
            copied_opened_melds = opened_melds[:]
            closed_set_items = []
            for x in hand:
                if x not in copied_opened_melds:
                    closed_set_items.append(x)
                else:
                    copied_opened_melds.remove(x)

            # for forms like 45666 and ron on 6
            # we can assume that ron was on 456 form and on 66 form
            # and depends on form we will have different hand cost
            win_groups = [x for x in closed_set_items if win_tile_34 in x]
            for win_group in win_groups:
                cost = None
                error = None
                hand_yaku = []
                han = 0

                fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, win_group, is_tsumo, valued_tiles, melds)
                is_pinfu = len(fu_details) == 1 and not is_chitoitsu

                pon_sets = [x for x in hand if is_pon(x)]
                chi_sets = [x for x in hand if is_chi(x)]

                if is_tsumo:
                    if not is_open_hand:
                        hand_yaku.append(self.config.tsumo)

                if is_pinfu:
                    hand_yaku.append(self.config.pinfu)

                # let's skip hand that looks like chitoitsu, but it contains open sets
                if is_chitoitsu and is_open_hand:
                    continue

                if is_chitoitsu:
                    hand_yaku.append(self.config.chiitoitsu)

                is_tanyao = self.config.tanyao.is_condition_met(hand)
                if is_open_hand and not has_open_tanyao:
                    is_tanyao = False

                if is_tanyao:
                    hand_yaku.append(self.config.tanyao)

                if is_riichi and not is_daburu_riichi:
                    hand_yaku.append(self.config.riichi)

                if is_daburu_riichi:
                    hand_yaku.append(self.config.daburu_riichi)

                if is_ippatsu:
                    hand_yaku.append(self.config.ippatsu)

                if is_rinshan:
                    hand_yaku.append(self.config.rinshan)

                if is_chankan:
                    hand_yaku.append(self.config.chankan)

                if is_haitei:
                    hand_yaku.append(self.config.haitei)

                if is_houtei:
                    hand_yaku.append(self.config.houtei)

                if is_renhou:
                    hand_yaku.append(self.config.renhou)

                if is_tenhou:
                    hand_yaku.append(self.config.tenhou)

                if is_chiihou:
                    hand_yaku.append(self.config.chiihou)

                if self.config.honitsu.is_condition_met(hand):
                    hand_yaku.append(self.config.honitsu)

                if self.config.chinitsu.is_condition_met(hand):
                    hand_yaku.append(self.config.chinitsu)

                if self.config.tsuisou.is_condition_met(hand):
                    hand_yaku.append(self.config.tsuisou)

                if self.config.honroto.is_condition_met(hand):
                    hand_yaku.append(self.config.honroto)

                if self.config.chinroto.is_condition_met(hand):
                    hand_yaku.append(self.config.chinroto)

                # small optimization, try to detect yaku with chi required sets only if we have chi sets in hand
                if len(chi_sets):
                    if self.config.chanta.is_condition_met(hand):
                        hand_yaku.append(self.config.chanta)

                    if self.config.junchan.is_condition_met(hand):
                        hand_yaku.append(self.config.junchan)

                    if self.config.ittsu.is_condition_met(hand):
                        hand_yaku.append(self.config.ittsu)

                    if not is_open_hand:
                        if self.config.ryanpeiko.is_condition_met(hand):
                            hand_yaku.append(self.config.ryanpeiko)
                        elif self.config.iipeiko.is_condition_met(hand):
                            hand_yaku.append(self.config.iipeiko)

                    if self.config.sanshoku.is_condition_met(hand):
                        hand_yaku.append(self.config.sanshoku)

                # small optimization, try to detect yaku with pon required sets only if we have pon sets in hand
                if len(pon_sets):
                    if self.config.toitoi.is_condition_met(hand):
                        hand_yaku.append(self.config.toitoi)

                    if self.config.sanankou.is_condition_met(hand, win_tile, opened_melds, is_tsumo):
                        hand_yaku.append(self.config.sanankou)

                    if self.config.sanshoku_douko.is_condition_met(hand):
                        hand_yaku.append(self.config.sanshoku_douko)

                    if self.config.shosangen.is_condition_met(hand):
                        hand_yaku.append(self.config.shosangen)

                    if self.config.haku.is_condition_met(hand):
                        hand_yaku.append(self.config.haku)

                    if self.config.hatsu.is_condition_met(hand):
                        hand_yaku.append(self.config.hatsu)

                    if self.config.chun.is_condition_met(hand):
                        hand_yaku.append(self.config.hatsu)

                    if self.config.east.is_condition_met(hand, player_wind, round_wind):
                        if player_wind == EAST:
                            hand_yaku.append(self.config.yakuhai_place)

                        if round_wind == EAST:
                            hand_yaku.append(self.config.yakuhai_round)

                    if self.config.south.is_condition_met(hand, player_wind, round_wind):
                        if player_wind == SOUTH:
                            hand_yaku.append(self.config.yakuhai_place)

                        if round_wind == SOUTH:
                            hand_yaku.append(self.config.yakuhai_round)

                    if self.config.west.is_condition_met(hand, player_wind, round_wind):
                        if player_wind == WEST:
                            hand_yaku.append(self.config.yakuhai_place)

                        if round_wind == WEST:
                            hand_yaku.append(self.config.yakuhai_round)

                    if self.config.north.is_condition_met(hand, player_wind, round_wind):
                        if player_wind == NORTH:
                            hand_yaku.append(self.config.yakuhai_place)

                        if round_wind == NORTH:
                            hand_yaku.append(self.config.yakuhai_round)

                    if self.config.daisangen.is_condition_met(hand):
                        hand_yaku.append(self.config.daisangen)

                    if self.config.shosuushi.is_condition_met(hand):
                        hand_yaku.append(self.config.shosuushi)

                    if self.config.daisuushi.is_condition_met(hand):
                        hand_yaku.append(self.config.daisuushi)

                    if self.config.ryuisou.is_condition_met(hand):
                        hand_yaku.append(self.config.ryuisou)

                    if not is_open_hand and self.config.chuuren_poutou.is_condition_met(hand):
                        if tiles_34[win_tile // 4] == 2:
                            hand_yaku.append(self.config.daburu_chuuren_poutou)
                        else:
                            hand_yaku.append(self.config.chuuren_poutou)

                    if not is_open_hand and self.config.suuankou.is_condition_met(hand, win_tile, is_tsumo):
                        if tiles_34[win_tile // 4] == 2:
                            hand_yaku.append(self.config.suuankou_tanki)
                        else:
                            hand_yaku.append(self.config.suuankou)

                    if self.config.sankantsu.is_condition_met(hand, melds):
                        hand_yaku.append(self.config.sankantsu)

                    if self.config.suukantsu.is_condition_met(hand, melds):
                        hand_yaku.append(self.config.suukantsu)

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

                if han == 0 or (han == 1 and fu < 30):
                    error = 'Not valid han ({0}) and fu ({1})'.format(han, fu)
                    cost = None

                # we can add dora han only if we have other yaku in hand
                # and if we don't have yakuman
                if not yakuman_list:
                    tiles_for_dora = tiles + kan_indices_136
                    count_of_dora = 0
                    count_of_aka_dora = 0
                    for tile in tiles_for_dora:
                        count_of_dora += plus_dora(tile, dora_indicators, has_aka_dora)

                    if count_of_dora:
                        yaku_item = self.config.dora
                        yaku_item.han_open = count_of_dora
                        yaku_item.han_closed = count_of_dora
                        hand_yaku.append(yaku_item)
                        han += count_of_dora

                    if count_of_aka_dora:
                        yaku_item = self.config.aka_dora
                        yaku_item.han_open = count_of_aka_dora
                        yaku_item.han_closed = count_of_aka_dora
                        hand_yaku.append(yaku_item)
                        han += count_of_aka_dora

                if not error:
                    cost = scores_calculator.calculate_scores(han, fu, is_tsumo, is_dealer)

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
        if not is_open_hand and self.config.kokushi.is_condition_met(None, tiles_34):
            if tiles_34[win_tile // 4] == 2:
                han = self.config.daburu_kokushi.han_closed
            else:
                han = self.config.kokushi.han_closed

            fu = 0
            cost = scores_calculator.calculate_scores(han, fu, is_tsumo, is_dealer)
            calculated_hands.append({
                'cost': cost,
                'error': None,
                'hand_yaku': [self.config.kokushi],
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
