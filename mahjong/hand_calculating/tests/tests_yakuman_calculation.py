# -*- coding: utf-8 -*-
import unittest

from mahjong.hand_calculating.hand import FinishedHand
from mahjong.meld import Meld
from mahjong.tests_mixin import TestMixin


class YakumanCalculationTestCase(unittest.TestCase, TestMixin):

    def test_is_tenhou(self):
        hand = FinishedHand()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, is_tenhou=True)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chiihou(self):
        hand = FinishedHand()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, is_chiihou=True)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_daisangen(self):
        hand = FinishedHand()

        tiles = self._string_to_34_array(sou='123', man='22', honors='555666777')
        self.assertTrue(hand.config.daisangen.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='123', man='22', honors='555666777')
        win_tile = self._string_to_136_tile(honors='7')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

    def test_is_shosuushi(self):
        hand = FinishedHand()

        tiles = self._string_to_34_array(sou='123', honors='11122233344')
        self.assertTrue(hand.config.shosuushi.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='123', honors='11122233344')
        win_tile = self._string_to_136_tile(honors='4')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 60)
        self.assertEqual(len(result.yaku), 1)

    def test_is_daisuushi(self):
        hand = FinishedHand()

        tiles = self._string_to_34_array(sou='22', honors='111222333444')
        self.assertTrue(hand.config.daisuushi.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='22', honors='111222333444')
        win_tile = self._string_to_136_tile(honors='4')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 60)
        self.assertEqual(len(result.yaku), 1)

    def test_is_tsuisou(self):
        hand = FinishedHand()

        tiles = self._string_to_34_array(honors='11122233366677')
        self.assertTrue(hand.config.tsuisou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(honors='11223344556677')
        self.assertTrue(hand.config.tsuisou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(honors='1133445577', pin='88', sou='11')
        self.assertFalse(hand.config.tsuisou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(honors='11223344556677')
        win_tile = self._string_to_136_tile(honors='7')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 25)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chinroto(self):
        hand = FinishedHand()

        tiles = self._string_to_34_array(sou='111999', man='111999', pin='99')
        self.assertTrue(hand.config.chinroto.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='111222', man='111999', pin='99')
        win_tile = self._string_to_136_tile(pin='9')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 60)
        self.assertEqual(len(result.yaku), 1)

    def test_is_kokushi(self):
        hand = FinishedHand()

        tiles = self._string_to_34_array(sou='119', man='19', pin='19', honors='1234567')
        self.assertTrue(hand.config.kokushi.is_condition_met(None, tiles))

        tiles = self._string_to_136_array(sou='119', man='19', pin='19', honors='1234567')
        win_tile = self._string_to_136_tile(sou='9')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 0)
        self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(sou='119', man='19', pin='19', honors='1234567')
        win_tile = self._string_to_136_tile(sou='1')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 0)
        self.assertEqual(len(result.yaku), 1)

    def test_is_ryuisou(self):
        hand = FinishedHand()

        tiles = self._string_to_34_array(sou='22334466888', honors='666')
        self.assertTrue(hand.config.ryuisou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='22334466888', honors='666')
        win_tile = self._string_to_136_tile(honors='6')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_suuankou(self):
        hand = FinishedHand()

        tiles = self._string_to_34_array(sou='111444', man='333', pin='44555')
        win_tile = self._string_to_136_tile(sou='4')

        self.assertTrue(hand.config.suuankou.is_condition_met(self._hand(tiles), win_tile, True))
        self.assertFalse(hand.config.suuankou.is_condition_met(self._hand(tiles), win_tile, False))

        tiles = self._string_to_136_array(sou='111444', man='333', pin='44555')
        win_tile = self._string_to_136_tile(pin='5')

        result = hand.estimate_hand_value(tiles, win_tile, is_tsumo=True)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

        result = hand.estimate_hand_value(tiles, win_tile, is_tsumo=False)
        self.assertNotEqual(result.han, 13)

        tiles = self._string_to_136_array(sou='111444', man='333', pin='44455')
        win_tile = self._string_to_136_tile(pin='5')

        result = hand.estimate_hand_value(tiles, win_tile, is_tsumo=True)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(man='33344455577799')
        win_tile = self._string_to_136_tile(man='9')

        result = hand.estimate_hand_value(tiles, win_tile, is_tsumo=False)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chuuren_poutou(self):
        hand = FinishedHand()

        tiles = self._string_to_34_array(man='11122345678999')
        self.assertTrue(hand.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(pin='11123345678999')
        self.assertTrue(hand.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123456678999')
        self.assertTrue(hand.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123456678999')
        self.assertTrue(hand.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123456678999')
        self.assertTrue(hand.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123456789999')
        self.assertTrue(hand.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(man='11123456789999')
        win_tile = self._string_to_136_tile(man='1')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(man='11122345678999')
        win_tile = self._string_to_136_tile(man='2')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

    def test_is_suukantsu(self):
        hand = FinishedHand()

        melds = [
            self._make_meld(Meld.KAN, sou='1111'),
            self._make_meld(Meld.KAN, sou='3333'),
            self._make_meld(Meld.KAN, pin='5555'),
            self._make_meld(Meld.KAN, man='2222'),
        ]
        self.assertTrue(hand.config.suukantsu.is_condition_met(None, melds))

        tiles = self._string_to_136_array(sou='111333', man='222', pin='44555')
        win_tile = self._string_to_136_tile(pin='4')
        melds = [
            self._make_meld(Meld.KAN, sou='1111'),
            self._make_meld(Meld.KAN, sou='3333'),
            self._make_meld(Meld.KAN, pin='5555'),
            self._make_meld(Meld.KAN, man='2222'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 70)
        self.assertEqual(len(result.yaku), 1)
