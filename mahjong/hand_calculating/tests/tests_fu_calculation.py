# -*- coding: utf-8 -*-
import unittest

from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.constants import EAST
from mahjong.hand_calculating.fu import FuCalculator
from mahjong.meld import Meld
from mahjong.tests_mixin import TestMixin


class FuCalculationTestCase(unittest.TestCase, TestMixin):

    def _get_win_group(self, hand, win_tile):
        return [x for x in hand if win_tile // 4 in x][0]

    def test_chitoitsu_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='112244', man='115599', pin='6')
        win_tile = self._string_to_136_tile(pin='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(1, len(fu_details))
        self.assertTrue({'fu': 25, 'reason': FuCalculator.BASE} in fu_details)
        self.assertEqual(fu, 25)

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(1, len(fu_details))
        self.assertTrue({'fu': 25, 'reason': FuCalculator.BASE} in fu_details)
        self.assertEqual(fu, 25)

    def test_open_hand_base(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='22278', man='123456', pin='11')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))
        melds = [self._make_meld(Meld.PON, sou='222')]

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config,
                                                    melds=melds)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.OPEN_PON} in fu_details)
        self.assertEqual(fu, 30)

    def test_fu_based_on_win_group(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(man='234789', pin='1234566')
        win_tile = self._string_to_136_tile(pin='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        win_groups = [x for x in hand if win_tile // 4 in x]

        # pinfu wait 4-5-6
        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, win_groups[0], config)
        self.assertEqual(fu, 30)

        # pair wait 66
        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, win_groups[1], config)
        self.assertEqual(fu, 40)

    def test_open_hand_without_additional_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='23478', man='234567', pin='22')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))
        melds = [self._make_meld(Meld.CHI, sou='234')]

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config,
                                                    melds=melds)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.HAND_WITHOUT_FU} in fu_details)
        self.assertEqual(fu, 30)

    def test_open_hand_withou_additional_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='23478', man='234567', pin='22')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))
        melds = [self._make_meld(Meld.CHI, sou='234')]

        config = HandConfig(options=OptionalRules(fu_for_open_pinfu=False))
        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config,
                                                    melds=melds)
        self.assertEqual(1, len(fu_details))
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertEqual(fu, 20)

    def test_tsumo_hand_base(self):
        fu_calculator = FuCalculator()
        config = HandConfig(is_tsumo=True)

        tiles = self._string_to_136_array(sou='22278', man='123456', pin='11')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, _ = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)

    def test_tsumo_hand_and_pinfu(self):
        fu_calculator = FuCalculator()
        config = HandConfig(is_tsumo=True)

        tiles = self._string_to_136_array(sou='2278', man='123456', pin='123')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(1, len(fu_details))
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertEqual(fu, 20)

    def test_tsumo_hand_and_disabled_pinfu(self):
        fu_calculator = FuCalculator()
        config = HandConfig(is_tsumo=True, options=OptionalRules(fu_for_pinfu_tsumo=True))

        tiles = self._string_to_136_array(sou='2278', man='123456', pin='123')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.TSUMO} in fu_details)
        self.assertEqual(fu, 30)

    def test_tsumo_hand_and_not_pinfu(self):
        fu_calculator = FuCalculator()
        config = HandConfig(is_tsumo=True)

        tiles = self._string_to_136_array(sou='2278', man='123456', pin='111')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.TSUMO} in fu_details)
        self.assertEqual(fu, 30)

    def test_penchan_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        # 1-2-... wait
        tiles = self._string_to_136_array(sou='12456', man='123456', pin='55')
        win_tile = self._string_to_136_tile(sou='3')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.PENCHAN} in fu_details)
        self.assertEqual(fu, 40)

        # ...-8-9 wait
        tiles = self._string_to_136_array(sou='34589', man='123456', pin='55')
        win_tile = self._string_to_136_tile(sou='7')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.PENCHAN} in fu_details)
        self.assertEqual(fu, 40)

    def test_kanchan_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='12357', man='123456', pin='55')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.KANCHAN} in fu_details)
        self.assertEqual(fu, 40)

    def test_valued_pair_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='12378', man='123456', honors='11')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        valued_tiles = [EAST]
        fu_details, fu = fu_calculator.calculate_fu(hand,
                                                    win_tile,
                                                    self._get_win_group(hand, win_tile),
                                                    config,
                                                    valued_tiles=valued_tiles,)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.VALUED_PAIR} in fu_details)
        self.assertEqual(fu, 40)

        # double valued pair
        valued_tiles = [EAST, EAST]
        fu_details, fu = fu_calculator.calculate_fu(hand,
                                                    win_tile,
                                                    self._get_win_group(hand, win_tile),
                                                    config,
                                                    valued_tiles=valued_tiles)
        self.assertEqual(3, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.VALUED_PAIR} in fu_details)
        self.assertEqual(fu, 40)

    def test_pair_wait_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='123678', man='123456', pin='1')
        win_tile = self._string_to_136_tile(pin='1')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.PAIR_WAIT} in fu_details)
        self.assertEqual(fu, 40)

    def test_closed_pon_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='22278', man='123456', pin='11')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 4, 'reason': FuCalculator.CLOSED_PON} in fu_details)
        self.assertEqual(fu, 40)

        # when we ron on the third pon tile we consider pon as open
        tiles = self._string_to_136_array(sou='22678', man='123456', pin='11')
        win_tile = self._string_to_136_tile(sou='2')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.OPEN_PON} in fu_details)
        self.assertEqual(fu, 40)

    def test_closed_terminal_pon_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='11178', man='123456', pin='11')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 8, 'reason': FuCalculator.CLOSED_TERMINAL_PON} in fu_details)
        self.assertEqual(fu, 40)

        # when we ron on the third pon tile we consider pon as open
        tiles = self._string_to_136_array(sou='11678', man='123456', pin='11')
        win_tile = self._string_to_136_tile(sou='1')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 4, 'reason': FuCalculator.OPEN_TERMINAL_PON} in fu_details)
        self.assertEqual(fu, 40)

    def test_closed_honor_pon_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='1178', man='123456', honors='111')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 8, 'reason': FuCalculator.CLOSED_TERMINAL_PON} in fu_details)
        self.assertEqual(fu, 40)

        # when we ron on the third pon tile we consider pon as open
        tiles = self._string_to_136_array(sou='11678', man='123456', honors='11')
        win_tile = self._string_to_136_tile(honors='1')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 4, 'reason': FuCalculator.OPEN_TERMINAL_PON} in fu_details)
        self.assertEqual(fu, 40)

    def test_open_pon_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='22278', man='123456', pin='11')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))
        melds = [self._make_meld(Meld.PON, sou='222')]

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config,
                                                    melds=melds)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 2, 'reason': FuCalculator.OPEN_PON} in fu_details)
        self.assertEqual(fu, 30)

    def test_open_terminal_pon_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='2278', man='123456', honors='111')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))
        melds = [self._make_meld(Meld.PON, honors='111')]

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config,
                                                    melds=melds)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 4, 'reason': FuCalculator.OPEN_TERMINAL_PON} in fu_details)
        self.assertEqual(fu, 30)

    def test_closed_kan_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='22278', man='123456', pin='11')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))
        melds = [self._make_meld(Meld.KAN, sou='222', is_open=False)]

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config,
                                                    melds=melds)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 16, 'reason': FuCalculator.CLOSED_KAN} in fu_details)
        self.assertEqual(fu, 50)

    def test_open_kan_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='22278', man='123456', pin='11')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))
        melds = [self._make_meld(Meld.KAN, sou='222', is_open=True)]

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config,
                                                    melds=melds)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 8, 'reason': FuCalculator.OPEN_KAN} in fu_details)
        self.assertEqual(fu, 30)

    def test_closed_terminal_kan_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='2278', man='123456', pin='111')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))
        melds = [self._make_meld(Meld.KAN, pin='111', is_open=False)]

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config,
                                                    melds=melds)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 30, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 32, 'reason': FuCalculator.CLOSED_TERMINAL_KAN} in fu_details)
        self.assertEqual(fu, 70)

    def test_open_terminal_kan_fu(self):
        fu_calculator = FuCalculator()
        config = HandConfig()

        tiles = self._string_to_136_array(sou='2278', man='123456', pin='111')
        win_tile = self._string_to_136_tile(sou='6')
        hand = self._hand(self._to_34_array(tiles + [win_tile]))
        melds = [self._make_meld(Meld.KAN, pin='111', is_open=True)]

        fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, self._get_win_group(hand, win_tile), config,
                                                    melds=melds)
        self.assertEqual(2, len(fu_details))
        self.assertTrue({'fu': 20, 'reason': FuCalculator.BASE} in fu_details)
        self.assertTrue({'fu': 16, 'reason': FuCalculator.OPEN_TERMINAL_KAN} in fu_details)
        self.assertEqual(fu, 40)
