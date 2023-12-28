from mahjong.hand_calculating.hand_config import HandConfig


class ScoresCalculator:
    def calculate_scores(self, han, fu, config, is_yakuman=False):
        """
        Calculate how much scores cost a hand with given han and fu
        :param han: int
        :param fu: int
        :param config: HandConfig object
        :param is_yakuman: boolean
        :return: a dictionary with following keys:
        'main': main cost (honba number / tsumi bou not included)
        'additional': additional cost (honba number not included)
        'main_bonus': extra cost due to honba number to be added on main cost
        'additional_bonus': extra cost due to honba number to be added on additional cost
        'kyoutaku_bonus': the points taken from accumulated riichi 1000-point bous (kyoutaku)
        'total': the total points the winner is to earn
        'yaku_level': level of yaku (e.g. yakuman, mangan, nagashi mangan, etc)

        for ron, main cost is the cost for the player who triggers the ron, and additional cost is always = 0
        for dealer tsumo, main cost is the same as additional cost, which is the cost for any other player
        for non-dealer (player) tsumo, main cost is cost for dealer and additional is cost for player

        examples:
        1. dealer tsumo 2000 ALL in 2 honba, with 3 riichi bous on desk
        {'main': 2000, 'additional': 2000,
         'main_bonus': 200, 'additional_bonus': 200,
         'kyoutaku_bonus': 3000, 'total': 9600, 'yaku_level': ''}

         2. player tsumo 3900-2000 in 4 honba, with 1 riichi bou on desk
         {'main': 3900, 'additional': 2000,
         'main_bonus': 400, 'additional_bonus': 400,
         'kyoutaku_bonus': 1000, 'total': 10100, 'yaku_level': ''}

         3. dealer (or player) ron 12000 in 5 honba, with no riichi bou on desk
         {'main': 12000, 'additional': 0,
         'main_bonus': 1500, 'additional_bonus': 0,
         'kyoutaku_bonus': 0, 'total': 13500}

        """

        yaku_level = ""

        # kazoe hand
        if han >= 13 and not is_yakuman:
            # Hands over 26+ han don't count as double yakuman
            if config.options.kazoe_limit == HandConfig.KAZOE_LIMITED:
                han = 13
                yaku_level = "kazoe yakuman"
            # Hands over 13+ is a sanbaiman
            elif config.options.kazoe_limit == HandConfig.KAZOE_SANBAIMAN:
                han = 12
                yaku_level = "kazoe sanbaiman"

        if han >= 5:
            if han >= 78:
                yaku_level = "6x yakuman"
                if config.options.limit_to_sextuple_yakuman:
                    rounded = 48000
                else:
                    extra_han, _ = divmod(han - 78, 13)
                    rounded = 48000 + (extra_han * 8000)
            elif han >= 65:
                yaku_level = "5x yakuman"
                rounded = 40000
            elif han >= 52:
                yaku_level = "4x yakuman"
                rounded = 32000
            elif han >= 39:
                yaku_level = "3x yakuman"
                rounded = 24000
            # double yakuman
            elif han >= 26:
                yaku_level = "2x yakuman"
                rounded = 16000
            # yakuman
            elif han >= 13:
                yaku_level = "yakuman"
                rounded = 8000
            # sanbaiman
            elif han >= 11:
                yaku_level = "sanbaiman"
                rounded = 6000
            # baiman
            elif han >= 8:
                yaku_level = "baiman"
                rounded = 4000
            # haneman
            elif han >= 6:
                yaku_level = "haneman"
                rounded = 3000
            else:
                yaku_level = "mangan"
                rounded = 2000

            double_rounded = rounded * 2
            four_rounded = double_rounded * 2
            six_rounded = double_rounded * 3
        else:  # han < 5
            base_points = fu * pow(2, 2 + han)
            rounded = (base_points + 99) // 100 * 100
            double_rounded = (2 * base_points + 99) // 100 * 100
            four_rounded = (4 * base_points + 99) // 100 * 100
            six_rounded = (6 * base_points + 99) // 100 * 100

            is_kiriage = False
            if config.options.kiriage:
                if (han == 4 and fu == 30) or (han == 3 and fu == 60):
                    yaku_level = "kiriage mangan"
                    is_kiriage = True
            else:  # kiriage not supported
                if rounded > 2000:
                    yaku_level = "mangan"

            # mangan
            if rounded > 2000 or is_kiriage:
                rounded = 2000
                double_rounded = rounded * 2
                four_rounded = double_rounded * 2
                six_rounded = double_rounded * 3
            else:  # below mangan
                pass

        if config.is_tsumo:
            main = double_rounded
            main_bonus = 100 * config.tsumi_number
            additional_bonus = main_bonus

            if config.is_dealer:
                additional = main
            else:  # player
                additional = rounded

        else:  # ron
            additional = 0
            additional_bonus = 0
            main_bonus = 300 * config.tsumi_number

            if config.is_dealer:
                main = six_rounded
            else:  # player
                main = four_rounded

        kyoutaku_bonus = 1000 * config.kyoutaku_number
        total = (main + main_bonus) + 2 * (additional + additional_bonus) + kyoutaku_bonus

        if config.is_nagashi_mangan:
            yaku_level = "nagashi mangan"

        ret_dict = {
            "main": main,
            "main_bonus": main_bonus,
            "additional": additional,
            "additional_bonus": additional_bonus,
            "kyoutaku_bonus": kyoutaku_bonus,
            "total": total,
            "yaku_level": yaku_level,
        }

        return ret_dict


class Aotenjou(ScoresCalculator):
    def calculate_scores(self, han, fu, config, is_yakuman=False):
        base_points = fu * pow(2, 2 + han)
        rounded = (base_points + 99) // 100 * 100
        double_rounded = (2 * base_points + 99) // 100 * 100
        four_rounded = (4 * base_points + 99) // 100 * 100
        six_rounded = (6 * base_points + 99) // 100 * 100

        if config.is_tsumo:
            return {"main": double_rounded, "additional": config.is_dealer and double_rounded or rounded}
        else:
            return {"main": config.is_dealer and six_rounded or four_rounded, "additional": 0}

    def aotenjou_filter_yaku(self, hand_yaku, config):
        # in aotenjou yakumans are normal yaku
        # but we need to filter lower yaku that are precursors to yakumans
        if config.yaku.daisangen in hand_yaku:
            # for daisangen precursors are all dragons and shosangen
            hand_yaku.remove(config.yaku.chun)
            hand_yaku.remove(config.yaku.hatsu)
            hand_yaku.remove(config.yaku.haku)
            hand_yaku.remove(config.yaku.shosangen)

        if config.yaku.tsuisou in hand_yaku:
            # for tsuuiisou we need to remove toitoi and honroto
            hand_yaku.remove(config.yaku.toitoi)
            hand_yaku.remove(config.yaku.honroto)

        if config.yaku.shosuushi in hand_yaku:
            # for shosuushi we do not need to remove anything
            pass

        if config.yaku.daisuushi in hand_yaku:
            # for daisuushi we need to remove toitoi
            hand_yaku.remove(config.yaku.toitoi)

        if config.yaku.suuankou in hand_yaku or config.yaku.suuankou_tanki in hand_yaku:
            # for suu ankou we need to remove toitoi and sanankou (sanankou is already removed by default)
            if config.yaku.toitoi in hand_yaku:
                # toitoi is "optional" in closed suukantsu, maybe a bug? or toitoi is not given when it's kans?
                hand_yaku.remove(config.yaku.toitoi)

        if config.yaku.chinroto in hand_yaku:
            # for chinroto we need to remove toitoi and honroto
            hand_yaku.remove(config.yaku.toitoi)
            hand_yaku.remove(config.yaku.honroto)

        if config.yaku.suukantsu in hand_yaku:
            # for suukantsu we need to remove toitoi and sankantsu (sankantsu is already removed by default)
            if config.yaku.toitoi in hand_yaku:
                # same as above?
                hand_yaku.remove(config.yaku.toitoi)

        if config.yaku.chuuren_poutou in hand_yaku or config.yaku.daburu_chuuren_poutou in hand_yaku:
            # for chuuren poutou we need to remove chinitsu
            hand_yaku.remove(config.yaku.chinitsu)

        if config.yaku.daisharin in hand_yaku:
            # for daisharin we need to remove chinitsu, pinfu, tanyao, ryanpeiko, chiitoitsu
            hand_yaku.remove(config.yaku.chinitsu)
            if config.yaku.pinfu in hand_yaku:
                hand_yaku.remove(config.yaku.pinfu)
            hand_yaku.remove(config.yaku.tanyao)
            if config.yaku.ryanpeiko in hand_yaku:
                hand_yaku.remove(config.yaku.ryanpeiko)
            if config.yaku.chiitoitsu in hand_yaku:
                hand_yaku.remove(config.yaku.chiitoitsu)

        if config.yaku.ryuisou in hand_yaku:
            # for ryuisou we need to remove honitsu, if it is there
            if config.yaku.honitsu in hand_yaku:
                hand_yaku.remove(config.yaku.honitsu)
