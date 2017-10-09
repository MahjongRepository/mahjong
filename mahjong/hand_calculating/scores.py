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
        :return: a dictionary with main and additional cost
        for ron additional cost is always = 0
        for tsumo main cost is cost for dealer and additional is cost for player
        {'main': 1000, 'additional': 0}
        """

        # kazoe hand
        if han >= 13 and not is_yakuman:
            # Hands over 26+ han don't count as double yakuman
            if config.kazoe == HandConfig.KAZOE_LIMITED:
                han = 13
            # Hands over 13+ is a sanbaiman
            elif config.kazoe == HandConfig.KAZOE_SANBAIMAN:
                han = 12

        if han >= 5:
            # double yakuman
            if han >= 26:
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

            # mangan
            if rounded > 2000:
                rounded = 2000
                double_rounded = rounded * 2
                four_rounded = double_rounded * 2
                six_rounded = double_rounded * 3

            # kiriage mangan
            if han == 4 and fu == 30:
                rounded = 2000
                double_rounded = 3900
                four_rounded = 7700
                six_rounded = 11600

        if config.is_tsumo:
            return {'main': double_rounded, 'additional': config.is_dealer and double_rounded or rounded}
        else:
            return {'main': config.is_dealer and six_rounded or four_rounded, 'additional': 0}
