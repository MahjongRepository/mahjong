# -*- coding: utf-8 -*-
import math


class ScoresCalculator(object):

    def calculate_scores(self, han, fu, is_tsumo, is_dealer):
        """
        Calculate how much scores cost a hand with given han and fu
        :param han:
        :param fu:
        :param is_tsumo:
        :param is_dealer:
        :return: a dictionary with main and additional cost
        for ron additional cost is always = 0
        for tsumo main cost is cost for dealer and additional is cost for player
        {'main': 1000, 'additional': 0}
        """
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
            rounded = math.ceil(base_points / 100.) * 100
            double_rounded = math.ceil(2 * base_points / 100.) * 100
            four_rounded = math.ceil(4 * base_points / 100.) * 100
            six_rounded = math.ceil(6 * base_points / 100.) * 100

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

        if is_tsumo:
            return {'main': double_rounded, 'additional': is_dealer and double_rounded or rounded}
        else:
            return {'main': is_dealer and six_rounded or four_rounded, 'additional': 0}
