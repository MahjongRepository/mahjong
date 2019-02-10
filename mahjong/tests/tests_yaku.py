# -*- coding: utf-8 -*-
import unittest

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.tile import TilesConverter


class YakuTestCase(unittest.TestCase):
    
    def test_kokushi_musou_multiple_yakuman(self):
        hand_calculator = HandCalculator()
        
        # kokushi test
        
        tiles = TilesConverter.string_to_136_array(sou='19', pin='19', man='19', honors='12345677')
        win_tile = TilesConverter.string_to_136_array(honors='1')[0]
        
        hand_config = HandConfig(
                    is_tsumo=True,
                    is_tenhou=False,
                    is_chiihou=False)
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 1)
        self.assertTrue(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 13)
                
        hand_config = HandConfig(
                    is_tsumo=True,
                    is_tenhou=True,
                    is_chiihou=False)
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 2)
        self.assertTrue(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 26)
        
        hand_config = HandConfig(
                    is_tsumo=True,
                    is_tenhou=False,
                    is_chiihou=True)
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 2)
        self.assertTrue(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 26)
        
        # double kokushi test
        
        tiles = TilesConverter.string_to_136_array(sou='19', pin='19', man='19', honors='12345677')
        win_tile = TilesConverter.string_to_136_array(honors='7')[0]
        
        hand_config = HandConfig(
                    is_tsumo=True,
                    is_tenhou=False,
                    is_chiihou=False)
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 1)
        self.assertFalse(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 26)
                
        hand_config = HandConfig(
                    is_tsumo=True,
                    is_tenhou=True,
                    is_chiihou=False)
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 2)
        self.assertFalse(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 39)
        
        hand_config = HandConfig(
                    is_tsumo=True,
                    is_tenhou=False,
                    is_chiihou=True)
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 2)
        self.assertFalse(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 39)
        
    def test_aka_dora(self):
        hand_calculator = HandCalculator()
        tiles = TilesConverter.string_to_136_array(sou='345', pin='456', man='12355599')
        win_tile = TilesConverter.string_to_136_array(man='9')[0]
        
        hand_config = HandConfig(
                    is_tsumo=True,
                    has_aka_dora=True
                    )
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 1)
        
        # one red
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='456', man='12355599')
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 2)
        
        # two red
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='4r6', man='12355599')
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 3)
        
        # three red
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='4r6', man='123r5599')
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 4)
        
        # four red
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='4r6', man='123rr599')
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 5)
        
        # five+ red (technically not legal in mahjong but not the fault of evaluator, really)
        tiles = TilesConverter.string_to_136_array(sou='34r', pin='4r6', man='123rrr99')
        
        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)
        self.assertIsNone(hand_calculation.error)
        self.assertEqual(hand_calculation.han, 6)
        
