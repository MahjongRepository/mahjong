import os.path
import pkgutil
import mahjong.hand_calculating.yaku_list.non_yakuman as nym
import mahjong.hand_calculating.yaku_list.yakuman as ym

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.meld import Meld
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter
from mahjong.locale.text_reporter import TextReporter
calculator = HandCalculator()


# useful helper
def print_hand_result(hand_result, locale='Chinese'):

    reporter = TextReporter(locale=locale)
    str_dict = reporter.report(hand_result)

    if hand_result.error:
        print(str_dict['error'])
    else:
        print(str_dict['fu_details'])
        print(str_dict['yaku'])
        print(str_dict['cost'])

    print('')


####################################################################
# Tanyao hand by ron                                               #
####################################################################


# we had to use all 14 tiles in that array
tiles = TilesConverter.string_to_136_array(man='112233', pin='667788', sou='44')
win_tile = TilesConverter.string_to_136_array(sou='4')[0]
config = HandConfig()
# config.is_dealer = True
config.is_tsumo = True
result = calculator.estimate_hand_value(tiles, win_tile, config=config)
print_hand_result(result, locale='Chinese')
