# -*- coding: utf-8 -*-
import unittest

from mahjong.constants import EAST, SOUTH, WEST, NORTH, FIVE_RED_SOU
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.hand_calculating.yaku_config import YakuConfig
from mahjong.meld import Meld
from mahjong.tests_mixin import TestMixin
from mahjong.tile import TilesConverter


class YakuCalculationTestCase(unittest.TestCase, TestMixin):

    def setUp(self):
        self.config = YakuConfig()

    def test_hands_calculation(self):
        """
        Group of hands that were not properly calculated on tenhou replays
        I did fixes and leave hands in tests, to be sure that bugs were fixed.
        """

        hand = HandCalculator()
        player_wind = EAST

        tiles = self._string_to_136_array(pin='112233999', honors='11177')
        win_tile = self._string_to_136_tile(pin='9')
        melds = [
            self._make_meld(Meld.PON, honors='111'),
            self._make_meld(Meld.CHI, pin='123'),
            self._make_meld(Meld.CHI, pin='123'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.fu, 30)

        # we had a bug with multiple dora indicators and honor sets
        # this test is working with this situation
        tiles = self._string_to_136_array(pin='22244456799', honors='444')
        win_tile = self._string_to_136_tile(pin='2')
        dora_indicators = [self._string_to_136_tile(sou='3'), self._string_to_136_tile(honors='3')]
        melds = [self._make_meld(Meld.KAN, honors='4444')]
        result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 6)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 2)

        # if we can't ad pinfu to the hand hand
        # we can add 2 fu to make hand more expensive
        tiles = self._string_to_136_array(sou='678', man='11', pin='123345', honors='666')
        win_tile = self._string_to_136_tile(pin='3')
        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.fu, 40)

        tiles = self._string_to_136_array(man='234789', pin='12345666')
        win_tile = self._string_to_136_tile(pin='6')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.fu, 30)

        tiles = self._string_to_136_array(sou='678', pin='34555789', honors='555')
        win_tile = self._string_to_136_tile(pin='5')
        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.fu, 40)

        tiles = self._string_to_136_array(sou='123345678', man='678', pin='88')
        win_tile = self._string_to_136_tile(sou='3')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(sou='12399', man='123456', pin='456')
        win_tile = self._string_to_136_tile(sou='1')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(sou='111123666789', honors='11')
        win_tile = self._string_to_136_tile(sou='1')
        melds = [self._make_meld(Meld.PON, sou='666')]
        dora_indicators = [self._string_to_136_tile(honors='4')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds,
                                          dora_indicators=dora_indicators,
                                          config=self._make_hand_config(player_wind=player_wind))
        self.assertEqual(result.fu, 40)
        self.assertEqual(result.han, 4)

        tiles = self._string_to_136_array(pin='12333', sou='567', honors='666777')
        win_tile = self._string_to_136_tile(pin='3')
        melds = [self._make_meld(Meld.PON, honors='666'), self._make_meld(Meld.PON, honors='777')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.fu, 30)
        self.assertEqual(result.han, 2)

        tiles = self._string_to_136_array(pin='12367778', sou='678', man='456')
        win_tile = self._string_to_136_tile(pin='7')
        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_riichi=True))
        self.assertEqual(result.fu, 40)
        self.assertEqual(result.han, 1)

        tiles = self._string_to_136_array(man='11156677899', honors='777')
        win_tile = self._string_to_136_tile(man='7')
        melds = [
            self._make_meld(Meld.KAN, honors='7777'),
            self._make_meld(Meld.PON, man='111'),
            self._make_meld(Meld.CHI, man='678'),
        ]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.fu, 40)
        self.assertEqual(result.han, 3)

        tiles = self._string_to_136_array(man='122223777888', honors='66')
        win_tile = self._string_to_136_tile(man='2')
        melds = [self._make_meld(Meld.CHI, man='123'), self._make_meld(Meld.PON, man='777')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.fu, 30)
        self.assertEqual(result.han, 2)

        tiles = self._string_to_136_array(pin='11144678888', honors='444')
        win_tile = self._string_to_136_tile(pin='8')
        melds = [
            self._make_meld(Meld.PON, honors='444'),
            self._make_meld(Meld.PON, pin='111'),
            self._make_meld(Meld.PON, pin='888'),
        ]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.fu, 30)
        self.assertEqual(result.han, 2)

        tiles = self._string_to_136_array(sou='67778', man='345', pin='999', honors='222')
        win_tile = self._string_to_136_tile(sou='7')
        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.fu, 40)
        self.assertEqual(result.han, 1)

        tiles = self._string_to_136_array(sou='33445577789', man='345')
        win_tile = self._string_to_136_tile(sou='7')
        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.fu, 30)
        self.assertEqual(result.han, 2)

        tiles = self._string_to_136_array(pin='112233667788', honors='22')
        win_tile = self._string_to_136_tile(pin='3')
        melds = [self._make_meld(Meld.CHI, pin='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.fu, 30)
        self.assertEqual(result.han, 2)

        tiles = self._string_to_136_array(sou='345', man='12333456789')
        win_tile = self._string_to_136_tile(man='3')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.fu, 40)
        self.assertEqual(result.han, 2)

        tiles = self._string_to_136_array(sou='11123456777888')
        melds = [
            self._make_meld(Meld.CHI, sou='123'),
            self._make_meld(Meld.PON, sou='777'),
            self._make_meld(Meld.PON, sou='888'),
        ]
        win_tile = self._string_to_136_tile(sou='4')
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.fu, 30)
        self.assertEqual(result.han, 5)

        tiles = self._string_to_136_array(sou='112233789', honors='55777')
        melds = [self._make_meld(Meld.CHI, sou='123')]
        win_tile = self._string_to_136_tile(sou='2')
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.fu, 40)
        self.assertEqual(result.han, 4)

        tiles = self._string_to_136_array(pin='234777888999', honors='22')
        melds = [self._make_meld(Meld.CHI, pin='234'), self._make_meld(Meld.CHI, pin='789')]
        win_tile = self._string_to_136_tile(pin='9')
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.fu, 30)
        self.assertEqual(result.han, 2)

        tiles = self._string_to_136_array(pin='77888899', honors='777', man='444')
        melds = [self._make_meld(Meld.PON, honors='777'), self._make_meld(Meld.PON, man='444')]
        win_tile = self._string_to_136_tile(pin='8')
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.fu, 30)
        self.assertEqual(result.han, 1)

        tiles = self._string_to_136_array(pin='12333345', honors='555', man='567')
        win_tile = self._string_to_136_tile(pin='3')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.fu, 40)
        self.assertEqual(result.han, 1)

        tiles = self._string_to_136_array(pin='34567777889', honors='555')
        win_tile = self._string_to_136_tile(pin='7')
        melds = [self._make_meld(Meld.CHI, pin='345')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.fu, 30)
        self.assertEqual(result.han, 3)

        tiles = self._string_to_136_array(pin='567', sou='333444555', honors='77')
        win_tile = self._string_to_136_tile(sou='3')
        melds = [self._make_meld(Meld.KAN, is_open=False, sou='4444')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=self._make_hand_config(is_riichi=True))
        self.assertEqual(result.fu, 60)
        self.assertEqual(result.han, 1)

    def test_is_riichi(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_riichi=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        melds = [self._make_meld(Meld.CHI, sou='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=self._make_hand_config(is_riichi=True))
        self.assertNotEqual(result.error, None)

    def test_is_tsumo(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

        # with open hand tsumo not giving yaku
        melds = [self._make_meld(Meld.CHI, sou='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=self._make_hand_config(is_tsumo=True))
        self.assertNotEqual(result.error, None)

    def test_is_ippatsu(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile,
                                          config=self._make_hand_config(is_riichi=True, is_ippatsu=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 2)

        # without riichi ippatsu is not possible
        result = hand.estimate_hand_value(tiles, win_tile,
                                          config=self._make_hand_config(is_riichi=False, is_ippatsu=True))
        self.assertNotEqual(result.error, None)

    def test_is_rinshan(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_rinshan=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chankan(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_chankan=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_haitei(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_haitei=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_houtei(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_houtei=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_renhou(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_renhou=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 5)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_daburu_riichi(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile,
                                          config=self._make_hand_config(is_daburu_riichi=True, is_riichi=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_nagashi_mangan(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='13579', man='234456', pin='66')

        result = hand.estimate_hand_value(tiles, None, config=self._make_hand_config(is_nagashi_mangan=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 5)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chitoitsu_hand(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='113355', man='113355', pin='11')
        self.assertTrue(self.config.chiitoitsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='2299', man='2299', pin='1199', honors='44')
        self.assertTrue(self.config.chiitoitsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='113355', man='113355', pin='11')
        win_tile = self._string_to_136_tile(pin='1')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 25)
        self.assertEqual(len(result.yaku), 1)

    def test_is_tanyao(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='234567', man='234567', pin='22')
        self.assertTrue(self.config.tanyao.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='123456', man='234567', pin='22')
        self.assertFalse(self.config.tanyao.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='234567', man='234567', honors='22')
        self.assertFalse(self.config.tanyao.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='234567', man='234567', pin='22')
        win_tile = self._string_to_136_tile(man='7')

        result = hand.estimate_hand_value(tiles, win_tile,
                                          config=self._make_hand_config(is_tsumo=False, is_riichi=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 3)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 3)

        tiles = self._string_to_136_array(sou='234567', man='234567', pin='22')
        win_tile = self._string_to_136_tile(man='7')
        melds = [self._make_meld(Meld.CHI, sou='234')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds,
                                          config=self._make_hand_config(has_open_tanyao=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(sou='234567', man='234567', pin='22')
        win_tile = self._string_to_136_tile(man='7')
        melds = [self._make_meld(Meld.CHI, sou='234')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds,
                                          config=self._make_hand_config(has_open_tanyao=False))
        self.assertNotEqual(result.error, None)

    def test_is_pinfu_hand(self):
        player_wind, round_wind = EAST, WEST
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123456', man='123456', pin='55')
        win_tile = self._string_to_136_tile(man='6')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

        # waiting in two pairs
        tiles = self._string_to_136_array(sou='123456', man='123555', pin='55')
        win_tile = self._string_to_136_tile(man='5')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertNotEqual(result.error, None)

        # contains pon or kan
        tiles = self._string_to_136_array(sou='111456', man='123456', pin='55')
        win_tile = self._string_to_136_tile(man='6')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertNotEqual(result.error, None)

        # penchan waiting
        tiles = self._string_to_136_array(sou='123456', man='123456', pin='55')
        win_tile = self._string_to_136_tile(sou='3')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertNotEqual(result.error, None)

        # kanchan waiting
        tiles = self._string_to_136_array(sou='123567', man='123456', pin='55')
        win_tile = self._string_to_136_tile(sou='6')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertNotEqual(result.error, None)

        # tanki waiting
        tiles = self._string_to_136_array(man='22456678', pin='123678')
        win_tile = self._string_to_136_tile(man='2')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertNotEqual(result.error, None)

        # valued pair
        tiles = self._string_to_136_array(sou='123678', man='123456', honors='11')
        win_tile = self._string_to_136_tile(sou='6')
        result = hand.estimate_hand_value(tiles, win_tile,
                                          config=self._make_hand_config(player_wind=player_wind, round_wind=round_wind))
        self.assertNotEqual(result.error, None)

        # not valued pair
        tiles = self._string_to_136_array(sou='123678', man='123456', honors='22')
        win_tile = self._string_to_136_tile(sou='6')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

        # open hand
        tiles = self._string_to_136_array(sou='12399', man='123456', pin='456')
        win_tile = self._string_to_136_tile(man='1')
        melds = [self._make_meld(Meld.CHI, sou='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertNotEqual(result.error, None)

    def test_is_iipeiko(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='112233', man='123', pin='23444')
        self.assertTrue(self.config.iipeiko.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='112233', man='333', pin='12344')
        win_tile = self._string_to_136_tile(man='3')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        melds = [self._make_meld(Meld.CHI, sou='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertNotEqual(result.error, None)

    def test_is_ryanpeiko(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='112233', man='22', pin='223344')
        self.assertTrue(self.config.ryanpeiko.is_condition_met(self._hand(tiles, 1)))

        tiles = self._string_to_34_array(sou='111122223333', man='22')
        self.assertTrue(self.config.ryanpeiko.is_condition_met(self._hand(tiles, 1)))

        tiles = self._string_to_34_array(sou='112233', man='123', pin='23444')
        self.assertFalse(self.config.ryanpeiko.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='112233', man='33', pin='223344')
        win_tile = self._string_to_136_tile(pin='3')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 3)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        melds = [self._make_meld(Meld.CHI, sou='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertNotEqual(result.error, None)

    def test_is_sanshoku(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='123', man='123', pin='12345677')
        self.assertTrue(self.config.sanshoku.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='123456', man='23455', pin='123')
        self.assertFalse(self.config.sanshoku.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='123456', man='12399', pin='123')
        win_tile = self._string_to_136_tile(man='2')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        melds = [self._make_meld(Meld.CHI, sou='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

    def test_is_sanshoku_douko(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='111', man='111', pin='11145677')
        self.assertTrue(self.config.sanshoku_douko.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='111', man='222', pin='33344455')
        self.assertFalse(self.config.sanshoku_douko.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='222', man='222', pin='22245699')
        melds = [self._make_meld(Meld.CHI, sou='222')]
        win_tile = self._string_to_136_tile(pin='9')

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_toitoi(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='111333', man='333', pin='44555')
        self.assertTrue(self.config.toitoi.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='777', pin='777888999', honors='44')
        self.assertTrue(self.config.toitoi.is_condition_met(self._hand(tiles, 0)))

        tiles = self._string_to_136_array(sou='111333', man='333', pin='44555')
        melds = [self._make_meld(Meld.PON, sou='111'), self._make_meld(Meld.PON, sou='333')]
        win_tile = self._string_to_136_tile(pin='5')

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(sou='777', pin='777888999', honors='44')
        melds = [self._make_meld(Meld.PON, sou='777')]
        win_tile = self._string_to_136_tile(pin='9')

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_sankantsu(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='111333', man='123', pin='44666')

        melds = [
            self._make_meld(Meld.KAN, sou='1111'),
            self._make_meld(Meld.KAN, sou='3333'),
            self._make_meld(Meld.KAN, pin='6666'),
        ]
        self.assertTrue(self.config.sankantsu.is_condition_met(hand, melds))

        melds = [
            self._make_meld(Meld.CHANKAN, sou='1111'),
            self._make_meld(Meld.KAN, sou='3333'),
            self._make_meld(Meld.KAN, pin='6666'),
        ]
        win_tile = self._string_to_136_tile(man='3')

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 60)
        self.assertEqual(len(result.yaku), 1)

    def test_is_honroto(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='111999', man='111', honors='11222')
        self.assertTrue(self.config.honroto.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(pin='11', honors='22334466', man='1199')
        self.assertTrue(self.config.honroto.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='111999', man='111', honors='11222')
        win_tile = self._string_to_136_tile(honors='2')
        melds = [self._make_meld(Meld.PON, sou='111')]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 4)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 2)

        tiles = self._string_to_136_array(pin='11', honors='22334466', man='1199')
        win_tile = self._string_to_136_tile(man='1')
        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.fu, 25)
        self.assertEqual(result.han, 4)

    def test_is_sanankou(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='111444', man='333', pin='44555')
        win_tile = self._string_to_136_tile(sou='4')

        melds = [
            self._make_meld(Meld.PON, sou='444'),
            self._make_meld(Meld.PON, sou='111')
        ]
        self.assertFalse(self.config.sanankou.is_condition_met(self._hand(tiles), win_tile, melds, False))

        melds = [
            self._make_meld(Meld.PON, sou='111')
        ]
        self.assertFalse(self.config.sanankou.is_condition_met(self._hand(tiles), win_tile, melds, False))
        self.assertTrue(self.config.sanankou.is_condition_met(self._hand(tiles), win_tile, melds, True))

        tiles = self._string_to_34_array(pin='444789999', honors='22333')
        win_tile = self._string_to_136_tile(pin='9')
        self.assertTrue(self.config.sanankou.is_condition_met(self._hand(tiles), win_tile, [], False))

        melds = [
            self._make_meld(Meld.CHI, pin='456')
        ]
        tiles = self._string_to_34_array(pin='222456666777', honors='77')
        win_tile = self._string_to_136_tile(pin='6')
        self.assertFalse(self.config.sanankou.is_condition_met(self._hand(tiles), win_tile, melds, False))

        tiles = self._string_to_136_array(sou='123444', man='333', pin='44555')
        melds = [
            self._make_meld(Meld.CHI, sou='123')
        ]
        win_tile = self._string_to_136_tile(pin='5')

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_shosangen(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='123', man='345', honors='55666777')
        self.assertTrue(self.config.shosangen.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='123', man='345', honors='55666777')
        win_tile = self._string_to_136_tile(honors='7')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 4)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 3)

    def test_is_chanta(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='123', man='123789', honors='22333')
        self.assertTrue(self.config.chanta.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='111', man='111999', honors='22333')
        self.assertFalse(self.config.chanta.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='111999', man='111999', pin='11999')
        self.assertFalse(self.config.chanta.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='123', man='123789', honors='22333')
        win_tile = self._string_to_136_tile(honors='3')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        melds = [self._make_meld(Meld.CHI, sou='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

    def test_is_junchan(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='789', man='123789', pin='12399')
        self.assertTrue(self.config.junchan.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='111', man='111999', honors='22333')
        self.assertFalse(self.config.junchan.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='111999', man='111999', pin='11999')
        self.assertFalse(self.config.junchan.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='789', man='123789', pin='12399')
        win_tile = self._string_to_136_tile(man='2')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 3)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        melds = [self._make_meld(Meld.CHI, sou='789')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

    def test_is_honitsu(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(man='123456789', honors='11122')
        self.assertTrue(self.config.honitsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(man='123456789', pin='123', honors='22')
        self.assertFalse(self.config.honitsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(man='12345666778899')
        self.assertFalse(self.config.honitsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(man='123455667', honors='11122')
        win_tile = self._string_to_136_tile(honors='2')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 3)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        melds = [self._make_meld(Meld.CHI, man='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chinitsu(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(man='12345666778899')
        self.assertTrue(self.config.chinitsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(man='123456778899', honors='22')
        self.assertFalse(self.config.chinitsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(man='11234567677889')
        win_tile = self._string_to_136_tile(man='1')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 6)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        melds = [self._make_meld(Meld.CHI, man='678')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 5)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

    def test_is_ittsu(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(man='123456789', sou='123', honors='22')
        self.assertTrue(self.config.ittsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(man='112233456789', honors='22')
        self.assertTrue(self.config.ittsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(man='122334567789', honors='11')
        self.assertFalse(self.config.ittsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(man='123456789', sou='123', honors='22')
        win_tile = self._string_to_136_tile(sou='3')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        melds = [self._make_meld(Meld.CHI, man='123')]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 1)

    def test_is_haku(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='234567', man='23422', honors='555')
        self.assertTrue(self.config.haku.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='234567', man='23422', honors='555')
        win_tile = self._string_to_136_tile(honors='5')

        result = hand.estimate_hand_value(tiles, win_tile,
                                          config=self._make_hand_config(is_tsumo=False, is_riichi=False))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_hatsu(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='234567', man='23422', honors='666')
        self.assertTrue(self.config.hatsu.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='234567', man='23422', honors='666')
        win_tile = self._string_to_136_tile(honors='6')

        result = hand.estimate_hand_value(tiles, win_tile,
                                          config=self._make_hand_config(is_tsumo=False, is_riichi=False))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chun(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='234567', man='23422', honors='777')
        self.assertTrue(self.config.chun.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='234567', man='23422', honors='777')
        win_tile = self._string_to_136_tile(honors='7')

        result = hand.estimate_hand_value(tiles, win_tile,
                                          config=self._make_hand_config(is_tsumo=False, is_riichi=False))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_east(self):
        player_wind, round_wind = EAST, WEST
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='234567', man='23422', honors='111')
        self.assertTrue(self.config.east.is_condition_met(self._hand(tiles), player_wind, round_wind))

        tiles = self._string_to_136_array(sou='234567', man='23422', honors='111')
        win_tile = self._string_to_136_tile(honors='1')

        result = hand.estimate_hand_value(tiles,
                                          win_tile,
                                          config=self._make_hand_config(
                                              is_tsumo=False,
                                              is_riichi=False,
                                              player_wind=player_wind,
                                              round_wind=round_wind
                                          ))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        round_wind = EAST
        result = hand.estimate_hand_value(tiles,
                                          win_tile,
                                          config=self._make_hand_config(
                                              is_tsumo=False,
                                              is_riichi=False,
                                              player_wind=player_wind,
                                              round_wind=round_wind
                                          ))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 2)

    def test_is_south(self):
        player_wind, round_wind = SOUTH, EAST
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='234567', man='23422', honors='222')
        self.assertTrue(self.config.south.is_condition_met(self._hand(tiles), player_wind, round_wind))

        tiles = self._string_to_136_array(sou='234567', man='23422', honors='222')
        win_tile = self._string_to_136_tile(honors='2')

        result = hand.estimate_hand_value(tiles,
                                          win_tile,
                                          config=self._make_hand_config(
                                              is_tsumo=False,
                                              is_riichi=False,
                                              player_wind=player_wind,
                                              round_wind=round_wind
                                          ))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        round_wind = SOUTH
        result = hand.estimate_hand_value(tiles,
                                          win_tile,
                                          config=self._make_hand_config(
                                              is_tsumo=False,
                                              is_riichi=False,
                                              player_wind=player_wind,
                                              round_wind=round_wind
                                          ))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 2)

    def test_is_west(self):
        player_wind, round_wind = WEST, EAST
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='234567', man='23422', honors='333')
        self.assertTrue(self.config.west.is_condition_met(self._hand(tiles), player_wind, round_wind))

        tiles = self._string_to_136_array(sou='234567', man='23422', honors='333')
        win_tile = self._string_to_136_tile(honors='3')

        result = hand.estimate_hand_value(tiles,
                                          win_tile,
                                          config=self._make_hand_config(
                                              is_tsumo=False,
                                              is_riichi=False,
                                              player_wind=player_wind,
                                              round_wind=round_wind
                                          ))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        round_wind = WEST
        result = hand.estimate_hand_value(tiles,
                                          win_tile,
                                          config=self._make_hand_config(
                                              is_tsumo=False,
                                              is_riichi=False,
                                              player_wind=player_wind,
                                              round_wind=round_wind))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 2)

    def test_is_north(self):
        player_wind, round_wind = NORTH, EAST
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='234567', man='23422', honors='444')
        self.assertTrue(self.config.north.is_condition_met(self._hand(tiles), player_wind, round_wind))

        tiles = self._string_to_136_array(sou='234567', man='23422', honors='444')
        win_tile = self._string_to_136_tile(honors='4')

        result = hand.estimate_hand_value(tiles,
                                          win_tile,
                                          config=self._make_hand_config(
                                              is_tsumo=False,
                                              is_riichi=False,
                                              player_wind=player_wind,
                                              round_wind=round_wind))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        round_wind = NORTH
        result = hand.estimate_hand_value(tiles,
                                          win_tile,
                                          config=self._make_hand_config(
                                              is_tsumo=False,
                                              is_riichi=False,
                                              player_wind=player_wind,
                                              round_wind=round_wind
                                          ))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 2)

    def test_dora_in_hand(self):
        hand = HandCalculator()

        # hand without yaku, but with dora should be consider as invalid
        tiles = self._string_to_136_array(sou='345678', man='456789', honors='55')
        win_tile = self._string_to_136_tile(sou='5')
        dora_indicators = [self._string_to_136_tile(sou='5')]
        melds = [self._make_meld(Meld.CHI, sou='678')]

        result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators, melds=melds)
        self.assertNotEqual(result.error, None)

        tiles = self._string_to_136_array(sou='123456', man='123456', pin='33')
        win_tile = self._string_to_136_tile(man='6')
        dora_indicators = [self._string_to_136_tile(pin='2')]

        result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 3)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 2)

        tiles = self._string_to_136_array(man='22456678', pin='123678')
        win_tile = self._string_to_136_tile(man='2')
        dora_indicators = [self._string_to_136_tile(man='1'), self._string_to_136_tile(pin='2')]
        result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators,
                                          config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 4)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 2)

        # double dora
        tiles = self._string_to_136_array(man='678', pin='34577', sou='123345')
        win_tile = self._string_to_136_tile(pin='7')
        dora_indicators = [self._string_to_136_tile(sou='4'), self._string_to_136_tile(sou='4')]
        result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators,
                                          config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 3)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 2)

        # double dora and honor tiles
        tiles = self._string_to_136_array(man='678', pin='345', sou='123345', honors='66')
        win_tile = self._string_to_136_tile(pin='5')
        dora_indicators = [self._string_to_136_tile(honors='5'), self._string_to_136_tile(honors='5')]
        result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators,
                                          config=self._make_hand_config(is_riichi=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 5)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 2)

        # double dora indicators and red fives
        tiles = self._string_to_136_array(sou='12346', man='123678', pin='44')
        win_tile = self._string_to_136_tile(pin='4')
        tiles.append(FIVE_RED_SOU)
        dora_indicators = [self._string_to_136_tile(pin='2'), self._string_to_136_tile(pin='2')]
        result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators,
                                          config=self._make_hand_config(is_tsumo=True, has_aka_dora=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 2)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 2)

        # dora in kan
        tiles = self._string_to_136_array(man='777', pin='34577', sou='123345')
        win_tile = self._string_to_136_tile(pin='7')
        melds = [self._make_meld(Meld.KAN, is_open=False, man='7777')]

        dora_indicators = [self._string_to_136_tile(man='6')]
        result = hand.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators, melds=melds,
                                          config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 5)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 2)

    def test_is_agari_and_closed_kan(self):
        """
        There were a bug when we don't count closed kan set for agari
        and calculator though that hand was agari (but it doesn't)
        :return:
        """
        hand = HandCalculator()

        tiles = self._string_to_136_array(man='45666777', pin='111', honors='222')
        win_tile = self._string_to_136_tile(man='4')
        melds = [
            self._make_meld(Meld.PON, pin='111'),
            self._make_meld(Meld.KAN, man='6666', is_open=False),
            self._make_meld(Meld.PON, man='777'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds)
        # error is correct answer
        self.assertNotEqual(result.error, None)

    def test_kazoe_settings(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(man='22244466677788')
        win_tile = self._string_to_136_tile(man='7')
        melds = [
            self._make_meld(Meld.KAN, man='2222', is_open=False),
        ]

        dora_indicators = [
            self._string_to_136_tile(man='1'),
            self._string_to_136_tile(man='1'),
            self._string_to_136_tile(man='1'),
            self._string_to_136_tile(man='1'),
        ]

        config = HandConfig(is_riichi=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_LIMITED))
        result = hand.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
        self.assertEqual(result.han, 28)
        self.assertEqual(result.cost['main'], 32000)

        config = HandConfig(is_riichi=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_SANBAIMAN))
        result = hand.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
        self.assertEqual(result.han, 28)
        self.assertEqual(result.cost['main'], 24000)

        config = HandConfig(is_riichi=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))
        result = hand.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
        self.assertEqual(result.han, 28)
        self.assertEqual(result.cost['main'], 64000)

    def test_open_hand_without_additional_fu(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='234678', man='234567', pin='22')
        win_tile = self._string_to_136_tile(sou='6')
        melds = [self._make_meld(Meld.CHI, sou='234')]

        config = HandConfig(options=OptionalRules(has_open_tanyao=True, fu_for_open_pinfu=False))
        result = hand.estimate_hand_value(tiles, win_tile, melds, config=config)
        self.assertEqual(result.han, 1)
        self.assertEqual(result.fu, 20)
        self.assertEqual(result.cost['main'], 700)

    def test_aka_dora(self):
        hand_calculator = HandCalculator()
        win_tile = TilesConverter.string_to_136_array(man='9')[0]

        hand_config = HandConfig(
            is_tsumo=True,
            options=OptionalRules(has_aka_dora=True)
        )

        # three red old style, but not that useful
        tiles = TilesConverter.string_to_136_array(sou='345', pin='456', man='12355599', has_aka_dora=False)
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 4)

        # zero red
        tiles = TilesConverter.string_to_136_array(sou='345', pin='456', man='12355599', has_aka_dora=True)
        win_tile = TilesConverter.string_to_136_array(man='9')[0]

        hand_config = HandConfig(
            is_tsumo=True,
            options=OptionalRules(has_aka_dora=True)
        )

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 1)

        # one red
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='456', man='12355599', has_aka_dora=True)

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 2)

        # two red
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='4r6', man='12355599', has_aka_dora=True)

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 3)

        # three red
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='4r6', man='123r5599', has_aka_dora=True)

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 4)

        # four red
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='4r6', man='123rr599', has_aka_dora=True)
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 5)

        # five+ red (technically not legal in mahjong but not the fault of evaluator, really)
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='4r6', man='123rrr99', has_aka_dora=True)

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 6)
