# -*- coding: utf-8 -*-
from mahjong.hand_calculating.hand_config import HandConfig


class ScoresCalculator(object):

    def calculate_scores(self, han, fu, config, is_yakuman=False):
        """
        Calculate how much scores cost a hand with given han and fu
        :param han: int
        :param fu: int
        :param config: HandConfig object
        :param is_yakuman: boolean
        :return: a dictionary with following keys:
        'main': main cost (honba number / tsumi bon not included)
        'additional': additional cost (honba number not included)
        'main_bonus': extra cost due to honba number to be added on main cost
        'additional_bonus': extra cost due to honba number to be added on additional cost
        'kyoutaku_bonus': the points taken from accumulated riichi 1000-point bons (kyoutaku)
        'total': the total points the winner is to earn

        for ron, main cost is the cost for the player who triggers the ron, and additional cost is always = 0
        for dealer tsumo, main cost is the same as additional cost, which is the cost for any other player
        for non-dealer (player) tsumo, main cost is cost for dealer and additional is cost for player

        examples:
        1. dealer tsumo 2000 ALL in 2 honba, with 3 riichi tsumi bons on desk
        {'main': 2000, 'additional': 2000,
         'main_bonus': 200, 'additional_bonus': 200,
         'kyoutaku_bonus': 3000, 'total': 9600}

         2. player tsumo 3900-2000 in 4 honba, with 1 riichi tsumi bon on desk
         {'main': 3900, 'additional': 2000,
         'main_bonus': 400, 'additional_bonus': 400,
         'kyoutaku_bonus': 1000, 'total': 10100}

         3. dealer (or player) ron 12000 in 5 honba, with no riichi tsumi bon on desk
         {'main': 12000, 'additional': 0,
         'main_bonus': 1500, 'additional_bonus': 0,
         'kyoutaku_bonus': 0, 'total': 13500}

        """

        # kazoe hand
        if han >= 13 and not is_yakuman:
            # Hands over 26+ han don't count as double yakuman
            if config.options.kazoe_limit == HandConfig.KAZOE_LIMITED:
                han = 13
            # Hands over 13+ is a sanbaiman
            elif config.options.kazoe_limit == HandConfig.KAZOE_SANBAIMAN:
                han = 12

        if han >= 5:
            if han >= 78:
                rounded = 48000
            elif han >= 65:
                rounded = 40000
            elif han >= 52:
                rounded = 32000
            elif han >= 39:
                rounded = 24000
            # double yakuman
            elif han >= 26:
                rounded = 16000
            # yakuman
            elif han >= 13:
                rounded = 8000
            # sanbaiman
            elif han >= 11:
                rounded = 6000
            # baiman
            elif han >= 8:
                rounded = 4000
            # haneman
            elif han >= 6:
                rounded = 3000
            else:
                rounded = 2000

            double_rounded = rounded * 2
            four_rounded = double_rounded * 2
            six_rounded = double_rounded * 3
        else:
            base_points = fu * pow(2, 2 + han)
            rounded = (base_points + 99) // 100 * 100
            double_rounded = (2 * base_points + 99) // 100 * 100
            four_rounded = (4 * base_points + 99) // 100 * 100
            six_rounded = (6 * base_points + 99) // 100 * 100

            is_kiriage = False
            if config.options.kiriage:
                if han == 4 and fu == 30:
                    is_kiriage = True
                if han == 3 and fu == 60:
                    is_kiriage = True

            # mangan
            if rounded > 2000 or is_kiriage:
                rounded = 2000
                double_rounded = rounded * 2
                four_rounded = double_rounded * 2
                six_rounded = double_rounded * 3

        if config.is_tsumo:
            main = double_rounded
            main_bonus = 100 * config.tsumi_number
            additional_bonus = main_bonus

            if config.is_dealer:
                additional = main
            else:   # player
                additional = rounded

        else:   # ron
            additional = 0
            additional_bonus = 0
            main_bonus = 300 * config.tsumi_number

            if config.is_dealer:
                main = six_rounded
            else:   # player
                main = four_rounded

        kyoutaku_bonus = 1000 * config.kyoutaku_number
        total = (main + main_bonus) + 2 * (additional + additional_bonus) + kyoutaku_bonus

        ret_dict = {'main': main, 'main_bonus': main_bonus,
                    'additional': additional, 'additional_bonus': additional_bonus,
                    'kyoutaku_bonus': kyoutaku_bonus, 'total': total}

        return ret_dict
